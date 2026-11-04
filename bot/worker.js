// Bot público do canal (@Claudiotips_bot) no Cloudflare Workers: responde às pessoas na hora, 24h por dia.
//
// O Telegram manda cada mensagem para aqui (webhook). Os textos e botões vêm de bot_publico.json no ramo de
// dados, que o GitHub Actions reescreve de 10 em 10 min (boas-vindas, /resultados, /comofunciona). Assim os
// textos continuam a ser feitos em Python (agente/telegram.py) e este ficheiro quase nunca muda.
// Nada é guardado sobre as pessoas.
//
// Variáveis (Cloudflare → Worker → Settings → Variables and Secrets, todas como "Secret"):
//   BOT_TOKEN       token do @Claudiotips_bot (o mesmo do Secret TELEGRAM_BOT_TOKEN do GitHub)
//   WEBHOOK_SECRET  uma palavra-passe inventada (só letras e números, 20+ caracteres)
// Ligar: abre https://<o-teu-worker>.workers.dev/ligar?chave=<WEBHOOK_SECRET> uma vez.

const DADOS = "https://raw.githubusercontent.com/Dinas08/AGENTE-BETS/claude/dados/bot_publico.json";
const COMANDOS = { "/start": "ola", "/resultados": "res", "/comofunciona": "como" };
const RESERVA = {  // se o GitHub falhar: boas-vindas mínimas
  ola: { text: "👋 Olá! Bem-vindo ao <b>CLAUDIO BET TIPS FREE</b> ⚽🤖\n\n🔞 Só para maiores de 18.\n\n" +
             "🔞 +18 | Joga com responsabilidade" },
};

let cache = { em: 0, dados: null };

async function textos() {
  if (cache.dados && Date.now() - cache.em < 60_000) return cache.dados;
  try {
    const r = await fetch(DADOS, { cf: { cacheTtl: 60 } });
    if (r.ok) cache = { em: Date.now(), dados: await r.json() };
  } catch (e) { /* fica com a última versão */ }
  return cache.dados || { textos: RESERVA };
}

async function tg(env, metodo, corpo) {
  const r = await fetch(`https://api.telegram.org/bot${env.BOT_TOKEN}/${metodo}`, {
    method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify(corpo),
  });
  return r.json().catch(() => ({}));
}

async function responder(env, chat, acao, editar) {
  const d = await textos();
  const t = d.textos[acao] || d.textos.ola || RESERVA.ola;
  const corpo = { chat_id: chat, text: t.text, parse_mode: "HTML", disable_web_page_preview: true };
  if (t.reply_markup) corpo.reply_markup = t.reply_markup;
  if (editar && (acao === "18" || acao === "menor")) {  // substitui a pergunta da idade
    const r = await tg(env, "editMessageText", { ...corpo, message_id: editar });
    if (r.ok) return;
  }
  await tg(env, "sendMessage", corpo);
}

async function update(env, u) {
  const cb = u.callback_query;
  if (cb) {
    const [acao, alvo] = (cb.data || "").split(":");
    if (acao === "pb") {  // botões das boas-vindas antigas
      await tg(env, "answerCallbackQuery", { callback_query_id: cb.id });
      const m = cb.message || {};
      return responder(env, (m.chat || {}).id || cb.from.id, alvo, m.message_id);
    }
    // botões de rascunhos antigos: a aprovação passou para o bot de admin
    return tg(env, "answerCallbackQuery", { callback_query_id: cb.id, show_alert: true,
      text: "As aprovações passaram para o bot de admin. Usa os rascunhos que ele te mandar." });
  }
  const m = u.message;
  if (!m || (m.chat || {}).type !== "private") return;
  const cmd = ((m.text || "").trim().split(/\s+/)[0] || "").split("@")[0].toLowerCase();
  if (cmd === "/id") return tg(env, "sendMessage", { chat_id: m.chat.id, text: `O teu id do Telegram: ${m.chat.id}` });
  return responder(env, m.chat.id, COMANDOS[cmd] || "ola");
}

export default {
  async fetch(req, env, ctx) {
    const url = new URL(req.url);
    if (url.pathname === "/ligar") {  // regista este Worker como webhook do bot (uma vez)
      if (url.searchParams.get("chave") !== env.WEBHOOK_SECRET) return new Response("chave errada", { status: 403 });
      const r = await tg(env, "setWebhook", {
        url: `${url.origin}/telegram`, secret_token: env.WEBHOOK_SECRET,
        allowed_updates: ["message", "callback_query"], drop_pending_updates: false,
      });
      return new Response(r.ok ? "✅ Bot ligado: já responde na hora." : `❌ ${r.description}`,
                          { headers: { "content-type": "text/plain; charset=utf-8" } });
    }
    if (url.pathname === "/desligar") {  // volta ao modo antigo (GitHub Actions lê a fila)
      if (url.searchParams.get("chave") !== env.WEBHOOK_SECRET) return new Response("chave errada", { status: 403 });
      const r = await tg(env, "deleteWebhook", {});
      return new Response(r.ok ? "Webhook desligado." : `❌ ${r.description}`,
                          { headers: { "content-type": "text/plain; charset=utf-8" } });
    }
    if (url.pathname === "/telegram" && req.method === "POST") {
      if (req.headers.get("X-Telegram-Bot-Api-Secret-Token") !== env.WEBHOOK_SECRET)
        return new Response("", { status: 403 });
      const u = await req.json().catch(() => null);
      if (u) ctx.waitUntil(update(env, u).catch((e) => console.log("erro", e)));
      return new Response("ok");  // o Telegram quer resposta rápida; o envio acaba em segundo plano
    }
    return new Response("Agente Claudio 🤖", { headers: { "content-type": "text/plain; charset=utf-8" } });
  },
};
