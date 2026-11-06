# ⚽ Agente Bets

Previsões para a Liga Portugal, Premier League, Bundesliga e Serie A, taças nacionais, provas europeias e
ligas das Américas (Brasileirão, Liga Argentina, Liga MX e MLS; aqui só golos e resultado, sem cantos nem cartões):
1X2, dupla hipótese, golos (+/-), ambas marcam, resultado exato, cantos, cartões e combinadas, com
odds justas e odds das casas. Um agente (Claude) junta notícias, lesões e instabilidade dos clubes e
escreve um recap depois de cada jornada.

## Como usar
| Ação | Como |
|---|---|
| Abrir a dashboard | **https://agente-bets-dinis.streamlit.app** (em qualquer dispositivo; vai buscar os dados novos de 5 em 5 min) |
| Atualizar à mão | GitHub → AGENTE-BETS → Actions → "Previsões" ou "Resultados" → Run workflow |
| Notícias, ajustes e recap | rotinas na nuvem (ver abaixo), ou numa sessão do Claude: "faz a rotina 1" / "faz a rotina 2" |

## Na nuvem (funciona com o PC desligado)
- **Dashboard:** https://agente-bets-dinis.streamlit.app (palavra-passe nos Secrets do Streamlit). Abre em
  qualquer dispositivo. Se ninguém a abrir durante uns dias adormece; ao abrir demora ~30 s a acordar.
- **Código:** repositório `Dinas08/AGENTE-BETS` (ramo `main`). **Dados:** ramo `claude/dados`.
- **GitHub Actions** (separador Actions do repositório): `Resultados` de 30 em 30 min (11h–24h),
  `Previsões` às 10h30 e 17h30, `Manutenção dos dados` à terça (compacta o histórico). Todos têm "Run workflow"
  para correr à mão.
- **Rotinas do agente** (claude.ai/code/routines): notícias e ajustes às 9h, recap e aprendizagem às 23h50.
- As tarefas do PC (Agendador do Windows e tarefas do Claude desktop) estão **desativadas**; a dashboard local
  (`Abrir dashboard.bat`) mostra dados antigos — usa o link da nuvem.
- Alterações ao código: faz-se no PC e `git push` para o `main`; o Streamlit atualiza sozinho.

## Canal de Telegram
- O bot publica no canal grátis: dicas do dia + múltipla (10h30), 2 dicas tardias ~30-45 min antes dos jogos
  da noite (a partir das 17h) com os onzes confirmados (se faltarem jogos fortes, completa com ≥55%) (não dá dica se uma equipa rodar 5+ jogadores), 2 dicas de madrugada às 22h
  (jogos das 00h às 3h), GREEN/RED quando cada jogo acaba, o resumo do dia seguinte e o balanço à segunda-feira.
  Quem escreve ao bot em privado recebe as boas-vindas do Agente Claudio com o aviso +18 e botões de link (abrem
  logo, sem esperar pelo bot): "✅ Tenho 18+ · Entrar no canal" e "📊 Últimos resultados" (último resumo/balanço,
  só com canal público). Nada é guardado. Comandos: `/resultados` (últimos 7 dias) e `/comofunciona`.
  Respostas na hora: o bot público corre no Cloudflare Workers (`bot/worker.js`, webhook, grátis) com os textos de
  `dados/bot_publico.json`, que o workflow Resultados reescreve de 10 em 10 min. Sem o Worker, o bot só lê as
  mensagens quando o workflow corre (até 10 min de espera). Estado das dicas em `dados/telegram.json`.
- Secrets do GitHub: `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_GRATIS` (id do canal), e opcionais `AFILIADO_LINK`,
  `AFILIADO_CASA` (só casas com licença SRIJ).
- Aprovação: com o Secret `TELEGRAM_ADMIN` (o teu id; manda `/id` ao bot para o saber) as dicas, múltiplas,
  tardias e madrugada chegam-te primeiro em privado como rascunho (pelo bot de admin, Secret
  `TELEGRAM_ADMIN_BOT_TOKEN`, obrigatório quando o bot público está no Worker), com ✅ Publicar / ❌ Descartar. Para editar,
  responde ao rascunho com o texto novo. Além das recomendadas (⭐), chegam também todas as outras
  apostas do dia (📎 extra, ≥50%), que só saem se as publicares. 🔄 Trocar (nas dicas e em cada perna das múltiplas)
  pede-te a aposta por escrito (ex.: "mais de 2.5 golos", "Porto ou empate", "ambas marcam e mais de 2.5");
  ❌ Tirar tira uma perna. Rascunhos não aprovados expiram quando o jogo começa. Nada vai para o
  canal sem aprovação: os GREEN/RED, resumos e balanços também chegam como rascunho 📣 (expiram em 24 h). A múltipla turbo nunca repete apostas da múltipla do dia.
- Por dia: 2 a 4 dicas (≥62%; num dia fraco completa até 2 com ≥55%), 1 dica 💎 de odd alta (1.80-2.60,
  a mais provável dessa faixa, de preferência com valor) e a múltipla turbo com o fundamento de cada perna.
- Testar: Actions → "Testar Telegram". Local: `run.py telegram dicas AAAA-MM-DD` (sem token = só mostra).

## Aprendizagem
- Todas as noites o agente analisa os jogos falhados, atualiza o recap, as fichas das equipas
  (`dados/equipas/`) e as lições (`dados/licoes.md`), que lê antes de cada ronda de previsões.
- O Python corrige sozinho o ataque/defesa das equipas em que errou sistematicamente (2+ jogos, máx. ±12%).
- Calibração por mercado (`agente/calibracao.json`): as probabilidades de resultado, golos, ambas marcam, cantos e
  cartões são corrigidas com o que o modelo acertou no backtest (cantos e cartões descem, o resultado sobe).
  Refazer com `run.py backtest` e `run.py calibrar`.
- Tudo visível na página **Lições** da dashboard.

## Fontes de dados (todas grátis)
- **football-data.co.uk**: histórico das ligas (golos, xG, remates, cantos, cartões, odds) para treinar o modelo.
- **ESPN**: jogos, resultados, cantos, cartões e odds de todas as provas: 4 ligas, Taça de Portugal, FA Cup,
  Carabao Cup, DFB-Pokal, Coppa Italia, Champions, Liga Europa e Conferência. Não tem a Taça da Liga.
- **Lesões e instabilidade**: o agente pesquisa-as nas notícias.
- **API-Football**: a chave está no `.env`, mas o plano grátis só dá acesso às épocas 2022–2024. O programa
  deteta isso e gasta só 1 pedido por dia. Num plano pago, as lesões e as odds extra passam a ser usadas
  automaticamente.

## Como funciona
1. **Dados**: football-data.co.uk (histórico desde 2024/25 com golos, xG, remates, cantos, cartões e odds) +
   API-Football (jogos de taças/Europa, lesões, odds extra).
2. **Modelo** (`agente/model.py`): força de ataque/defesa de cada equipa (Poisson Dixon-Coles, jogos recentes
   pesam mais), um modelo igual para cantos e outro para cartões, e uma força relativa entre ligas para os
   jogos europeus. Daí sai a matriz de resultados e, a partir dela, todos os mercados e combinadas.
3. **Mistura com o mercado**: quando há odds, os golos esperados são 30% modelo + 70% casas de apostas
   (foi o que melhor previu no backtest).
4. **Agente**: ajusta os golos esperados por equipa com base nas notícias (`dados/ajustes.json`).
5. **Recap**: `run.py resultados` avalia cada previsão. Explica as falhas com o xG, as expulsões e as
   surpresas, e o agente acrescenta a análise.

## Backtest 2025/26 (1270 jogos, sem olhar para o futuro)
| Mercado | Acerto | Prob. média prevista |
|---|---|---|
| Dupla hipótese | 80.6% | 78.6% |
| Cartões +/-4.5 | 63.7% | 63.7% |
| Golos +/-2.5 | 57.5% | 57.5% |
| Combinada (odd justa ≥ 1.60) | 56.4% | 56.7% |
| Cantos +/-9.5 | 56.2% | 58.6% |
| Ambas marcam | 55.6% | 55.8% |
| Resultado 1X2 | 53.5% | 51.8% |

As probabilidades estão bem calibradas: quando o agente diz 57%, acontece cerca de 57% das vezes. No
1X2 o agente iguala o mercado; as "apostas de valor" puramente estatísticas deram ROI −5%. A vantagem
real, se existir, tem de vir das notícias de última hora e de mercados menos eficientes. Por isso
acompanha o separador 📈 Desempenho antes de pagar pela API ou de apostar dinheiro.

> Isto é uma ferramenta de análise estatística, não aconselhamento financeiro. Aposta só o que podes perder.
