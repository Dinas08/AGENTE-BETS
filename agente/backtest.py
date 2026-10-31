"""Backtest walk-forward: prevê cada semana de uma época passada só com dados anteriores e mede o acerto."""
import datetime as dt

import pandas as pd

from agente import config
from agente.model import Predictor, blend_with_market, main_picks, markets, value_bets
from agente.recap import outcome
from agente.sources import football_data_uk as fd


def run(season: int = config.CURRENT_SEASON - 1) -> pd.DataFrame:
    hist = fd.history(seasons=[season - 2, season - 1, season])
    test = hist[(hist["season"] == season) & hist["div"].isin(config.MAIN_LEAGUES)]
    weeks = sorted(test["date"].dt.to_period("W-SUN").unique())
    rows = []
    for i, wk in enumerate(weeks):
        start = wk.start_time
        games = test[test["date"].dt.to_period("W-SUN") == wk]
        if start < test["date"].min() + pd.Timedelta(days=21):
            continue  # primeiras jornadas: pouca informação da época
        pred = Predictor(hist, start.date(), divs=list(config.MAIN_LEAGUES))
        for _, r in games.iterrows():
            odds = {k: float(r[c]) for c, k in (("odd_h", "1"), ("odd_d", "X"), ("odd_a", "2"),
                                                 ("odd_o25", "over_2.5"), ("odd_u25", "under_2.5"))
                    if c in r and pd.notna(r[c])}
            exp = blend_with_market(pred.expected(r["home"], r["away"]), odds)
            probs = markets(exp)["probs"]
            res = {"hg": r["hg"], "ag": r["ag"], "hc": r.get("hc"), "ac": r.get("ac"),
                   "hy": r.get("hy"), "ay": r.get("ay")}
            for kind, key in main_picks(probs).items():
                hit = outcome(key, res)
                if hit is not None:
                    rows.append({"date": r["date"], "div": r["div"], "tipo": kind, "mercado": key,
                                 "prob": probs[key], "acertou": hit, "valor": False, "lucro": None})
            if all(k in odds for k in ("1", "X", "2")):
                inv = {k: 1 / odds[k] for k in ("1", "X", "2")}
                s = sum(inv.values())
                res1x2 = "1" if r["hg"] > r["ag"] else "X" if r["hg"] == r["ag"] else "2"
                for src, pr in (("agente", probs), ("mercado", {k: v / s for k, v in inv.items()})):
                    rows.append({"date": r["date"], "div": r["div"], "tipo": f"brier_{src}", "mercado": "1X2",
                                 "prob": sum((pr[k] - (k == res1x2)) ** 2 for k in ("1", "X", "2")),
                                 "acertou": max(("1", "X", "2"), key=pr.get) == res1x2, "valor": False,
                                 "lucro": None})
            for vb in value_bets(probs, odds):
                hit = outcome(vb["mercado"], res)
                rows.append({"date": r["date"], "div": r["div"], "tipo": "valor", "mercado": vb["mercado"],
                             "prob": vb["prob"], "acertou": hit, "valor": True,
                             "lucro": vb["odd_casa"] - 1 if hit else -1.0})
        print(f"  semana {i + 1}/{len(weeks)}", end="\r")
    out = pd.DataFrame(rows)
    out.to_csv(config.DATA_DIR / f"backtest_{season}.csv", index=False)
    return out


def summary(bt: pd.DataFrame) -> pd.DataFrame:
    picks = bt[~bt["valor"]]
    s = picks.groupby("tipo").agg(jogos=("acertou", "size"), taxa=("acertou", "mean"),
                                  prob_media=("prob", "mean"))
    v = bt[bt["valor"]]
    if not v.empty:
        s.loc["apostas de valor"] = [len(v), v["acertou"].mean(), v["prob"].mean()]
    return s


if __name__ == "__main__":
    b = run()
    print(summary(b).round(3))
    v = b[b["valor"]]
    if not v.empty:
        print(f"Apostas de valor: {len(v)} | lucro {v['lucro'].sum():+.1f} u | ROI {v['lucro'].mean():+.1%}")
