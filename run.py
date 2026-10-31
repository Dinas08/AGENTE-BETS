"""Agente Bets — comandos:
    python run.py prever      recolhe dados, treina o modelo e gera previsões dos próximos dias
    python run.py resultados  recolhe resultados e gera o recap da semana passada (e da atual)
    python run.py tudo        resultados + previsões
    python run.py backtest    testa o modelo na época anterior
    python run.py estado      mostra quota da API e nº de previsões
"""
import datetime as dt
import sys

from agente import db, pipeline, recap
from agente.sources import api_football as apif


def cmd_resultados():
    print(f"Resultados novos (ESPN): {len(pipeline.quick_results())}")
    n = pipeline.update_results()
    print(f"Resultados de liga atualizados: {n}")
    for day in (dt.date.today() - dt.timedelta(days=7), dt.date.today()):
        out = recap.build_recap(day)
        if out:
            print(f"Recap {out[0]} -> {out[1]}")


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "tudo"
    if cmd == "prever":
        pipeline.predict()
    elif cmd == "resultados":
        cmd_resultados()
    elif cmd == "tudo":
        cmd_resultados()
        pipeline.predict()
        cmd_resultados()
    elif cmd == "backtest":
        from agente import backtest
        b = backtest.run()
        print(backtest.summary(b).round(3))
        v = b[b["valor"]]
        if not v.empty:
            print(f"Apostas de valor: {len(v)} | lucro {v['lucro'].sum():+.1f} u | ROI {v['lucro'].mean():+.1%}")
    elif cmd == "auto":
        # corrido pela tarefa do Windows de 30 em 30 min (sem janela): só resultados dos jogos acabados
        from agente import config
        try:
            new = pipeline.quick_results()
            msg = f"{len(new)} resultado(s) novo(s): {', '.join(new)}" if new else "nada novo"
        except Exception as e:  # sem internet, etc. — tenta na próxima execução
            msg = f"erro: {e}"
        log = config.DATA_DIR / "auto.log"
        lines = log.read_text(encoding="utf-8").splitlines()[-300:] if log.exists() else []
        lines.append(f"{dt.datetime.now():%Y-%m-%d %H:%M} {msg}")
        log.write_text("\n".join(lines) + "\n", encoding="utf-8")
    elif cmd == "aprendizagem":
        from agente import aprendizagem
        c = aprendizagem.team_corrections()
        c = c[(c["ataque"] - 1).abs().ge(.03) | (c["defesa"] - 1).abs().ge(.03)]
        print("Correções automáticas por equipa (ataque/defesa ×):")
        print(c.to_string(index=False) if not c.empty else "  nenhuma ainda (precisa de 2+ jogos por equipa)")
        m = aprendizagem.market_calibration()
        if not m.empty:
            print("\nCalibração por mercado:")
            print(m[["mercado", "previsoes", "acerto", "esperado", "leitura"]].round(2).to_string(index=False))
    elif cmd == "telegram":
        # telegram dicas [AAAA-MM-DD] | resultados | balanco [forcar]  (sem token = ensaio, só mostra)
        from agente import telegram
        sub = sys.argv[2] if len(sys.argv) > 2 else "dicas"
        if sub == "dicas":
            day = dt.date.fromisoformat(sys.argv[3]) if len(sys.argv) > 3 else None
            print(f"Dicas publicadas: {telegram.dicas(day)}")
        elif sub == "resultados":
            print(f"Resultados publicados: {telegram.resultados()}")
        elif sub == "teste":
            telegram.send("👋 Olá! O bot está ligado. As dicas do dia aparecem aqui todas as manhãs.\n\n"
                          + telegram.RODAPE)
            print("Mensagem de teste enviada.")
        elif sub == "descobrir":
            # canais/grupos onde o bot recebeu mensagens recentemente (para encontrar o id do canal)
            import requests
            r = requests.get(f"https://api.telegram.org/bot{telegram.TOKEN}/getUpdates", timeout=30).json()
            vistos = {}
            for u in r.get("result", []):
                for k in ("channel_post", "my_chat_member", "message", "edited_channel_post"):
                    c = (u.get(k) or {}).get("chat")
                    if c and c.get("type") != "private":
                        vistos[c["id"]] = c
            print("Canais/grupos que o bot vê (usa o 'id' em TELEGRAM_CHAT_GRATIS):" if vistos else
                  "O bot ainda não vê nenhum canal: adiciona-o como administrador e publica uma mensagem no canal.")
            for c in vistos.values():
                print(f"  id={c['id']}  nome={c.get('title')}  @{c.get('username') or '(privado, sem @)'}")
        elif sub == "balanco":
            print(f"Balanço publicado: {telegram.balanco(len(sys.argv) > 3)}")
    elif cmd == "lista":
        days = int(sys.argv[2]) if len(sys.argv) > 2 else 4
        p = db.load_predictions(with_results=False)
        now = dt.datetime.now()
        p = p[(p["kickoff"] >= now) & (p["kickoff"] <= now + dt.timedelta(days=days))].sort_values("kickoff")
        for _, r in p.iterrows():
            pr, e = r["probs"], r["expected"]
            print(f"[{r['match_id']}] {r['comp_name']} {r['kickoff']:%d/%m %H:%M} | {r['home']} vs {r['away']} | "
                  f"1 {pr['1']:.0%} X {pr['X']:.0%} 2 {pr['2']:.0%} | golos {e['golos_casa']}-{e['golos_fora']} | "
                  f"forma {r['form']['casa'].get('seq', '')} / {r['form']['fora'].get('seq', '')}"
                  + (" | DADOS LIMITADOS" if r["limited"] else ""))
            for i in r["injuries"]:
                print(f"    lesão/castigo: {i['equipa']} - {i['jogador']} ({i.get('motivo')})")
            for n in r["adjustments"].get("notas", []):
                print(f"    ajuste ativo: {n}")
    elif cmd == "estado":
        p = db.load_predictions()
        print(f"Previsões: {len(p)} | com resultado: {p['hg'].notna().sum() if not p.empty else 0}")
        print(f"API-Football ativa: {apif.enabled()} | quota: {apif.quota_status()}")
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
