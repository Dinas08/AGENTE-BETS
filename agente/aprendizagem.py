"""Aprendizagem com os erros: compara, equipa a equipa, os golos que prevíamos com os que aconteceram nos jogos
que já previmos, e corrige as previsões seguintes. As correções são pequenas, encolhidas para zero quando há
poucos jogos e limitadas a ±12%, para não reagir a um resultado isolado."""
import pandas as pd

from agente import db

LAST_GAMES = 10       # só os últimos jogos previstos de cada equipa contam (forma atual)
MIN_GAMES = 2         # um jogo isolado nunca mexe nas previsões
PRIOR_GAMES = 10      # "jogos imaginários" sem erro: com 5 jogos a correção é 1/3 do erro visto
XG_WEIGHT = 0.5       # mistura golos reais com xG (o xG separa azar de erro de leitura)
LIMIT = 0.12


def _actual(goals, xg):
    return goals if pd.isna(xg) else (1 - XG_WEIGHT) * goals + XG_WEIGHT * xg


def team_corrections(preds: pd.DataFrame | None = None) -> pd.DataFrame:
    """Uma linha por equipa: multiplicadores de ataque (golos marcados) e defesa (golos sofridos)."""
    preds = db.load_predictions() if preds is None else preds
    done = preds.dropna(subset=["hg"]) if not preds.empty else preds
    rows = []
    for _, r in done.iterrows():
        e = r["expected"]
        if "golos_casa" not in e:
            continue
        # golos esperados finais (já com ajustes do agente e correções anteriores)
        eh, ea = e["golos_casa"], e["golos_fora"]
        ah, aa = _actual(r["hg"], r.get("hxg")), _actual(r["ag"], r.get("axg"))
        rows += [{"equipa": r["home"], "kickoff": r["kickoff"], "exp_for": eh, "act_for": ah, "exp_ag": ea, "act_ag": aa},
                 {"equipa": r["away"], "kickoff": r["kickoff"], "exp_for": ea, "act_for": aa, "exp_ag": eh, "act_ag": ah}]
    if not rows:
        return pd.DataFrame(columns=["equipa", "jogos", "ataque", "defesa"])
    df = pd.DataFrame(rows).sort_values("kickoff").groupby("equipa").tail(LAST_GAMES)
    out = []
    for team, g in df.groupby("equipa"):
        n = len(g)
        prior_f = PRIOR_GAMES * g["exp_for"].mean()
        prior_a = PRIOR_GAMES * g["exp_ag"].mean()
        att = (g["act_for"].sum() + prior_f) / (g["exp_for"].sum() + prior_f) if n >= MIN_GAMES else 1.0
        dfn = (g["act_ag"].sum() + prior_a) / (g["exp_ag"].sum() + prior_a) if n >= MIN_GAMES else 1.0
        out.append({"equipa": team, "jogos": n,
                    "ataque": round(min(max(att, 1 - LIMIT), 1 + LIMIT), 3),
                    "defesa": round(min(max(dfn, 1 - LIMIT), 1 + LIMIT), 3),
                    "golos_previstos": round(g["exp_for"].sum(), 1), "golos_reais": round(g["act_for"].sum(), 1),
                    "sofridos_previstos": round(g["exp_ag"].sum(), 1), "sofridos_reais": round(g["act_ag"].sum(), 1)})
    return pd.DataFrame(out).sort_values("jogos", ascending=False)


def describe(team: str, att: float, dfn: float) -> str | None:
    parts = []
    if abs(att - 1) >= 0.03:
        parts.append(f"temos {'subestimado' if att > 1 else 'sobrestimado'} o ataque ({att - 1:+.0%})")
    if abs(dfn - 1) >= 0.03:
        parts.append(f"sofre {'mais' if dfn > 1 else 'menos'} do que previmos ({dfn - 1:+.0%})")
    return f"Aprendizagem — {team}: " + " e ".join(parts) if parts else None


def market_calibration(preds: pd.DataFrame | None = None) -> pd.DataFrame:
    """Por mercado: quanto esperávamos acertar vs quanto acertámos (confiança a mais / a menos)."""
    from agente.recap import PICK_NAMES, evaluate
    preds = db.load_predictions() if preds is None else preds
    done = preds.dropna(subset=["hg"]) if not preds.empty else preds
    if done.empty:
        return pd.DataFrame()
    ev = evaluate(done)
    s = ev.groupby("tipo").agg(previsoes=("acertou", "size"), acerto=("acertou", "mean"),
                               esperado=("prob", "mean")).reset_index()
    s["diferenca"] = s["acerto"] - s["esperado"]
    s["leitura"] = s.apply(lambda x: "poucos dados" if x["previsoes"] < 15 else
                           ("confiança a mais" if x["diferenca"] < -0.06 else
                            "confiança a menos" if x["diferenca"] > 0.06 else "bem calibrado"), axis=1)
    s["mercado"] = s["tipo"].map(lambda t: PICK_NAMES.get(t, t))
    return s
