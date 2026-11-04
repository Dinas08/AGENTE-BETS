"""Calibração por mercado: corrige as probabilidades do modelo com o que ele acertou de facto no passado.

O modelo é honesto no geral, mas não em todos os mercados (ex.: sobrestima cantos e 'ambas marcam', subestima
o resultado). Para cada família de mercado ajusta-se uma regressão logística logit(p_real) = a + b·logit(p_modelo)
com os jogos do backtest e os jogos reais já com resultado. Os coeficientes ficam em `calibracao.json` (no código,
não nos dados) e são aplicados a cada previsão nova. Refazer com `run.py calibrar`.
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.optimize import minimize

FICHEIRO = Path(__file__).with_name("calibracao.json")
# família -> (chave "positiva", chave complementar) nos mercados binários
BINARIOS = {"golos": ("over_2.5", "under_2.5"), "ambas": ("btts_sim", "btts_nao"),
            "cantos": ("cantos_over_9.5", "cantos_under_9.5"), "cartoes": ("cartoes_over_4.5", "cartoes_under_4.5")}
LAMBDA = 3.0       # puxa os coeficientes para "sem correção" (a=0, b=1) quando há poucos dados
MIN_JOGOS = 60     # abaixo disto a família não é corrigida
EPS = 1e-4


def _logit(p):
    p = np.clip(np.asarray(p, float), EPS, 1 - EPS)
    return np.log(p / (1 - p))


def _sig(x):
    return 1 / (1 + np.exp(-x))


def ajustar(p: np.ndarray, y: np.ndarray) -> tuple[float, float]:
    """(a, b) da regressão logística com penalização para (0, 1)."""
    x, y = _logit(p), np.asarray(y, float)

    def perda(t):
        q = np.clip(_sig(t[0] + t[1] * x), EPS, 1 - EPS)
        return -np.sum(y * np.log(q) + (1 - y) * np.log(1 - q)) + LAMBDA * (t[0] ** 2 + (t[1] - 1) ** 2)

    a, b = minimize(perda, [0.0, 1.0], method="L-BFGS-B", bounds=[(-1.5, 1.5), (0.3, 2.0)]).x
    return float(a), float(b)


def _amostras(linhas: pd.DataFrame) -> dict:
    """linhas: colunas familia, chave, prob, acertou (a previsão principal de cada mercado em cada jogo).
    Os binários passam para o lado 'positivo' (over/sim) para usar toda a informação."""
    out = {}
    for fam, (pos, neg) in BINARIOS.items():
        x = linhas[linhas["chave"].isin([pos, neg])]
        if len(x):
            neg_ = x["chave"] == neg
            out[fam] = (np.where(neg_, 1 - x["prob"], x["prob"]), np.where(neg_, ~x["acertou"].astype(bool),
                                                                          x["acertou"].astype(bool)))
    x = linhas[linhas["chave"].isin(["1", "X", "2"])]
    if len(x):
        out["resultado"] = (x["prob"].to_numpy(), x["acertou"].astype(bool).to_numpy())
    return out


def treinar(linhas: pd.DataFrame) -> dict:
    coef = {}
    for fam, (p, y) in _amostras(linhas).items():
        if len(p) >= MIN_JOGOS:
            a, b = ajustar(p, y)
            coef[fam] = {"a": round(a, 4), "b": round(b, 4), "jogos": int(len(p))}
    return coef


def linhas_backtest(path) -> pd.DataFrame:
    """As previsões principais de um backtest (`backtest_AAAA.csv`), com probabilidades ainda por calibrar."""
    b = pd.read_csv(path)
    b = b[b["tipo"].isin(["resultado", "golos", "ambas", "cantos", "cartoes"])].rename(columns={"mercado": "chave"})
    return b.assign(acertou=b["acertou"].astype(str).eq("True"))


def recalcular() -> dict:
    """Refaz os coeficientes com todos os backtests em dados/ (só backtests: as previsões guardadas desde a
    calibração já vêm corrigidas e não servem para a voltar a treinar)."""
    from agente import config
    fs = sorted(config.DATA_DIR.glob("backtest_*.csv"))
    if not fs:
        raise SystemExit("Sem backtest em dados/: corre primeiro `run.py backtest`.")
    coef = treinar(pd.concat([linhas_backtest(f) for f in fs]))
    FICHEIRO.write_text(json.dumps({"fonte": [f.name for f in fs], "familias": coef}, indent=1), encoding="utf-8")
    global _cache
    _cache = coef
    return coef


_cache: dict | None = None


def coeficientes() -> dict:
    global _cache
    if _cache is None:
        _cache = json.loads(FICHEIRO.read_text(encoding="utf-8"))["familias"] if FICHEIRO.exists() else {}
    return _cache


def aplicar(probs: dict, coef: dict | None = None) -> dict:
    """Devolve uma cópia das probabilidades com as famílias calibradas (o resto fica igual)."""
    coef = coeficientes() if coef is None else coef
    p = dict(probs)
    for fam, (pos, neg) in BINARIOS.items():
        c = coef.get(fam)
        if c and pos in p:
            p[pos] = float(_sig(c["a"] + c["b"] * _logit(p[pos])))
            p[neg] = 1 - p[pos]
    c = coef.get("resultado")
    if c and all(k in p for k in ("1", "X", "2")):
        r = {k: float(_sig(c["a"] + c["b"] * _logit(p[k]))) for k in ("1", "X", "2")}
        s = sum(r.values())
        p.update({k: v / s for k, v in r.items()})
        p["1X"], p["X2"], p["12"] = p["1"] + p["X"], p["X"] + p["2"], p["1"] + p["2"]
    return p
