"""Modelo estatístico: forças de ataque/defesa por equipa (Poisson com decaimento temporal, estilo Dixon-Coles)
para golos, cantos e cartões, e cálculo de todos os mercados e combinadas a partir da matriz de resultados."""
from dataclasses import dataclass, field

import numpy as np
import pandas as pd
from scipy.optimize import minimize
from scipy.stats import nbinom, poisson

from agente import config


@dataclass
class Strengths:
    mu: float
    home: float
    att: dict
    dfn: dict
    games: dict
    phi: float = 1.0  # sobre-dispersão (var/média), 1 = Poisson

    def has(self, team):
        return team in self.att


def fit_strengths(df: pd.DataFrame, yh: np.ndarray, ya: np.ndarray, ref_date, prior: dict | None = None,
                  ridge: float | None = None) -> Strengths:
    """Ajusta log(λ_casa) = mu + casa + att[c] - def[f]; log(λ_fora) = mu + att[f] - def[c]."""
    prior = prior or {}
    teams = sorted(set(df["home"]) | set(df["away"]))
    ix = {t: i for i, t in enumerate(teams)}
    n = len(teams)
    h = df["home"].map(ix).to_numpy()
    a = df["away"].map(ix).to_numpy()
    age = (pd.Timestamp(ref_date) - df["date"]).dt.days.clip(lower=0).to_numpy()
    w = np.exp(-config.MODEL["decay_per_day"] * age)
    p0 = np.array([prior.get(t, 0.0) for t in teams])
    lam = config.MODEL["ridge"] if ridge is None else ridge

    def nll(x):
        mu, ha, att, dfn = x[0], x[1], x[2:2 + n], x[2 + n:]
        eh = mu + ha + att[h] - dfn[a]
        ea = mu + att[a] - dfn[h]
        lh, la = np.exp(eh), np.exp(ea)
        f = np.sum(w * (lh - yh * eh)) + np.sum(w * (la - ya * ea))
        f += lam / 2 * (np.sum((att - p0) ** 2) + np.sum((dfn - p0) ** 2))
        gh, ga = w * (lh - yh), w * (la - ya)
        g = np.zeros_like(x)
        g[0] = gh.sum() + ga.sum()
        g[1] = gh.sum()
        g[2:2 + n] = np.bincount(h, gh, n) + np.bincount(a, ga, n) + lam * (att - p0)
        g[2 + n:] = -np.bincount(a, gh, n) - np.bincount(h, ga, n) + lam * (dfn - p0)
        return f, g

    x0 = np.zeros(2 + 2 * n)
    x0[0] = np.log(max(np.average(np.r_[yh, ya], weights=np.r_[w, w]), 0.1))
    res = minimize(nll, x0, jac=True, method="L-BFGS-B")
    x = res.x
    mu, ha, att, dfn = x[0], x[1], x[2:2 + n], x[2 + n:]
    lh = np.exp(mu + ha + att[h] - dfn[a])
    la = np.exp(mu + att[a] - dfn[h])
    phi = float(np.sum(w * ((yh - lh) ** 2 / lh + (ya - la) ** 2 / la)) / (2 * w.sum()))
    games = pd.Series(np.r_[w, w], index=np.r_[df["home"].to_numpy(), df["away"].to_numpy()]).groupby(level=0).sum()
    return Strengths(mu, ha, dict(zip(teams, att)), dict(zip(teams, dfn)), games.to_dict(), max(phi, 1.0))


@dataclass
class LeagueModel:
    div: str
    goals: Strengths
    corners: Strengths | None
    cards: Strengths | None
    strength: float
    teams: set = field(default_factory=set)


def fit_league(hist: pd.DataFrame, div: str, ref_date) -> LeagueModel | None:
    d = hist[(hist["div"] == div) & (hist["date"] < pd.Timestamp(ref_date))].copy()
    if len(d) < 30:
        return None
    # Equipas promovidas (não jogaram na liga na época anterior) começam abaixo da média
    cur = d["season"].max()
    prev_teams = set(d.loc[d["season"] == cur - 1, "home"])
    cur_teams = set(d.loc[d["season"] == cur, "home"]) | set(d.loc[d["season"] == cur, "away"])
    prior = {t: -0.12 for t in cur_teams - prev_teams} if prev_teams else {}

    xw = config.MODEL["xg_weight"]
    yh, ya = d["hg"].to_numpy(float), d["ag"].to_numpy(float)
    if "hxg" in d and d["hxg"].notna().mean() > 0.5:
        hx = d["hxg"].fillna(d["hg"]).to_numpy(float)
        ax = d["axg"].fillna(d["ag"]).to_numpy(float)
        yh, ya = (1 - xw) * yh + xw * hx, (1 - xw) * ya + xw * ax
    goals = fit_strengths(d, yh, ya, ref_date, prior)

    def opt(hc, ac):
        if hc not in d or d[hc].notna().mean() < 0.8:
            return None
        dd = d.dropna(subset=[hc, ac])
        return fit_strengths(dd, dd[hc].to_numpy(float), dd[ac].to_numpy(float), ref_date,
                             ridge=config.MODEL["ridge_other"])

    teams = set(d.loc[d["season"] == cur, "home"]) | set(d.loc[d["season"] == cur, "away"])
    return LeagueModel(div, goals, opt("hc", "ac"), opt("hy", "ay"), config.ALL_LEAGUES[div]["strength"], teams)


class Predictor:
    """Reúne os modelos de todas as ligas e prevê qualquer jogo (liga, taça ou europeu)."""

    def __init__(self, hist: pd.DataFrame, ref_date, divs=None):
        self.models: dict[str, LeagueModel] = {}
        for div in divs or config.ALL_LEAGUES:
            m = fit_league(hist, div, ref_date)
            if m:
                self.models[div] = m
        self.team_div = {}
        for div, m in self.models.items():
            for t in m.teams:
                self.team_div[t] = div
        self.mu_ref = float(np.mean([m.goals.mu for m in self.models.values()]))

    def known_teams(self):
        return list(self.team_div)

    def _global(self, s_attr: str, team: str, comp_type: str, comp_league: str | None):
        div = self.team_div.get(team)
        if div is None:
            base = config.ALL_LEAGUES.get(comp_league, {}).get("strength", -0.2) if comp_league else -0.2
            off = base + config.UNKNOWN_TEAM_STRENGTH["europe" if comp_type == "europe" else "domestic_cup"]
            return off, off, True
        m = self.models[div]
        s: Strengths = getattr(m, s_attr)
        if s is None or team not in s.att:
            return m.strength, m.strength, True
        off = m.strength if s_attr == "goals" else 0.0
        return s.att[team] + off, s.dfn[team] + off, False

    def expected(self, home: str, away: str, comp_type: str = "league", comp_league: str | None = None,
                 neutral: bool = False):
        """Devolve (λ golos casa, λ golos fora, cantos c/f, cartões c/f, dispersões, dados_limitados)."""
        out = {}
        limited = False
        same = self.team_div.get(home) is not None and self.team_div.get(home) == self.team_div.get(away)
        for kind in ("goals", "corners", "cards"):
            if same:
                s: Strengths = getattr(self.models[self.team_div[home]], kind)
                if s is not None and s.has(home) and s.has(away):
                    ha = 0.0 if neutral else s.home
                    out[kind] = (np.exp(s.mu + ha + s.att[home] - s.dfn[away]),
                                 np.exp(s.mu + s.att[away] - s.dfn[home]), s.phi)
                    continue
            ah, dh, l1 = self._global(kind, home, comp_type, comp_league)
            aa, da, l2 = self._global(kind, away, comp_type, comp_league)
            limited |= (l1 or l2) and kind == "goals"
            ss = [getattr(m, kind) for m in self.models.values() if getattr(m, kind) is not None]
            if not ss:
                out[kind] = None
                continue
            mu = self.mu_ref if kind == "goals" else float(np.mean([s.mu for s in ss]))
            ha = 0.0 if neutral else (config.MODEL["home_adv_neutral_europe"] if kind == "goals"
                                      else float(np.mean([s.home for s in ss])))
            phi = float(np.mean([s.phi for s in ss]))
            out[kind] = (np.exp(mu + ha + ah - da), np.exp(mu + aa - dh), phi)
        out["limited"] = limited
        return out


# ---------------------------------------------------------------- mercados

def score_matrix(lh: float, la: float) -> np.ndarray:
    k = np.arange(config.MODEL["max_goals"] + 1)
    m = np.outer(poisson.pmf(k, lh), poisson.pmf(k, la))
    rho = config.MODEL["dc_rho"]
    m[0, 0] *= 1 - lh * la * rho
    m[0, 1] *= 1 + lh * rho
    m[1, 0] *= 1 + la * rho
    m[1, 1] *= 1 - rho
    return m / m.sum()


def market_lambdas(odds: dict) -> tuple[float, float] | None:
    """Golos esperados implícitos nas odds das casas (1X2 e, se houver, +/-2.5), sem a margem da casa."""
    if not all(odds.get(k) for k in ("1", "X", "2")):
        return None
    inv = np.array([1 / odds[k] for k in ("1", "X", "2")])
    target = inv / inv.sum()
    ou = None
    if odds.get("over_2.5") and odds.get("under_2.5"):
        o, u = 1 / odds["over_2.5"], 1 / odds["under_2.5"]
        ou = o / (o + u)
    n = config.MODEL["max_goals"] + 1
    i, j = np.meshgrid(np.arange(n), np.arange(n), indexing="ij")

    def err(x):
        m = score_matrix(*np.exp(x))
        e = np.sum((np.array([m[i > j].sum(), m[i == j].sum(), m[i < j].sum()]) - target) ** 2)
        if ou is not None:
            e += (m[i + j > 2.5].sum() - ou) ** 2
        return e

    r = minimize(err, np.log([1.4, 1.1]), method="Nelder-Mead", options={"xatol": 1e-4, "fatol": 1e-9})
    return tuple(np.exp(r.x)) if r.success or r.fun < 1e-3 else None


def blend_with_market(exp: dict, odds: dict) -> dict:
    """Mistura os golos esperados do modelo com os do mercado (média geométrica pesada)."""
    mk = market_lambdas(odds or {})
    w = config.MODEL["model_weight"]
    if exp.get("limited"):  # equipa sem histórico: o modelo só tem um palpite genérico
        w = min(w, 0.1)
    if mk is None or w >= 1:
        return {**exp, "blended": False}
    lh, la, phi = exp["goals"]
    return {**exp, "goals": (lh ** w * mk[0] ** (1 - w), la ** w * mk[1] ** (1 - w), phi),
            "goals_model": (lh, la), "goals_market": mk, "blended": True}


def _nb(mean: float, phi: float, kmax: int = 40):
    k = np.arange(kmax)
    if phi <= 1.02:
        return poisson.pmf(k, mean)
    n = mean / (phi - 1)
    return nbinom.pmf(k, n, n / (n + mean))


def label(key: str, home: str = "Casa", away: str = "Fora") -> str:
    fixed = {"1": f"Vitória {home}", "X": "Empate", "2": f"Vitória {away}", "1X": f"{home} ou empate",
             "X2": f"{away} ou empate", "12": "Não há empate", "btts_sim": "Ambas marcam",
             "btts_nao": "Ambas não marcam"}
    if key in fixed:
        return fixed[key]
    if key.startswith("over_") or key.startswith("under_"):
        side, line = key.split("_")
        return f"{'Mais' if side == 'over' else 'Menos'} de {line} golos"
    if key == "cantos_mais_casa":
        return f"Mais cantos: {home}"
    if key == "cantos_mais_fora":
        return f"Mais cantos: {away}"
    if key.startswith("cantos_") or key.startswith("cartoes_"):
        kind, side, line = key.split("_")
        noun = "cantos" if kind == "cantos" else "cartões amarelos"
        return f"{'Mais' if side == 'over' else 'Menos'} de {line} {noun}"
    if key.startswith("combo:"):
        return " + ".join(label(p, home, away) for p in key[6:].split("&"))
    if key.startswith("placar_"):
        return f"Resultado exato {key[7:]}"
    if key == "casa_marca":
        return f"{home} marca"
    if key == "fora_marca":
        return f"{away} marca"
    if key == "casa_sem_sofrer":
        return f"{home} não sofre"
    if key == "fora_sem_sofrer":
        return f"{away} não sofre"
    return key


COMBOS_GOALS = [
    ("1", "btts_sim"), ("2", "btts_sim"), ("X", "btts_sim"), ("1", "over_2.5"), ("2", "over_2.5"),
    ("1", "under_3.5"), ("2", "under_3.5"), ("1X", "under_3.5"), ("X2", "under_3.5"), ("1X", "over_1.5"),
    ("X2", "over_1.5"), ("btts_sim", "over_2.5"), ("1", "casa_sem_sofrer"), ("2", "fora_sem_sofrer"),
    ("1", "btts_nao"), ("2", "btts_nao"), ("12", "over_2.5"), ("1X", "btts_sim"), ("X2", "btts_sim"),
]
COMBOS_CORNERS = [("1", "cantos_over_8.5"), ("over_2.5", "cantos_over_9.5"), ("2", "cantos_over_8.5"),
                  ("1X", "cantos_over_7.5")]


def _goal_masks(n: int):
    i, j = np.meshgrid(np.arange(n), np.arange(n), indexing="ij")
    t = i + j
    masks = {"1": i > j, "X": i == j, "2": i < j}
    masks["1X"], masks["X2"], masks["12"] = i >= j, i <= j, i != j
    masks["btts_sim"], masks["btts_nao"] = (i > 0) & (j > 0), (i == 0) | (j == 0)
    masks["casa_marca"], masks["fora_marca"] = i > 0, j > 0
    masks["casa_sem_sofrer"], masks["fora_sem_sofrer"] = j == 0, i == 0
    for line in (0.5, 1.5, 2.5, 3.5, 4.5):
        masks[f"over_{line}"], masks[f"under_{line}"] = t > line, t < line
    return masks


def markets(exp: dict, adj: dict | None = None) -> dict:
    """Probabilidades de todos os mercados. `adj` multiplica os golos esperados (ajustes do agente)."""
    adj = adj or {}
    lh, la, _ = exp["goals"]
    lh *= adj.get("home_goals", 1.0)
    la *= adj.get("away_goals", 1.0)
    m = score_matrix(lh, la)
    masks = _goal_masks(m.shape[0])
    p = {k: float(m[v].sum()) for k, v in masks.items()}
    for a, b in COMBOS_GOALS:
        p[f"combo:{a}&{b}"] = float(m[masks[a] & masks[b]].sum())

    flat = [(m[i, j], f"{i}-{j}") for i in range(6) for j in range(6)]
    top = sorted(flat, reverse=True)[:6]
    p.update({f"placar_{s}": float(v) for v, s in top})

    xc = {"golos_casa": lh, "golos_fora": la}
    if exp.get("corners"):
        ch, ca, phi = exp["corners"]
        dh, da = _nb(ch, phi), _nb(ca, phi)
        tot = np.convolve(dh, da)[:60]
        for line in (7.5, 8.5, 9.5, 10.5, 11.5, 12.5):
            over = float(tot[int(line) + 1:].sum())
            p[f"cantos_over_{line}"], p[f"cantos_under_{line}"] = over, 1 - over
        joint = np.outer(dh, da)
        i, j = np.meshgrid(np.arange(len(dh)), np.arange(len(da)), indexing="ij")
        p["cantos_mais_casa"], p["cantos_mais_fora"] = float(joint[i > j].sum()), float(joint[i < j].sum())
        for a, b in COMBOS_CORNERS:  # aproximação: golos e cantos tratados como independentes
            p[f"combo:{a}&{b}"] = p[a] * p[b]
        xc.update({"cantos_casa": ch, "cantos_fora": ca})
    if exp.get("cards"):
        yh, ya, phi = exp["cards"]
        tot = np.convolve(_nb(yh, phi), _nb(ya, phi))[:60]
        for line in (2.5, 3.5, 4.5, 5.5):
            over = float(tot[int(line) + 1:].sum())
            p[f"cartoes_over_{line}"], p[f"cartoes_under_{line}"] = over, 1 - over
        xc.update({"cartoes_casa": yh, "cartoes_fora": ya})
    return {"probs": p, "expected": {k: round(float(v), 2) for k, v in xc.items()}}


def main_picks(probs: dict) -> dict:
    """A previsão principal em cada mercado (o que é avaliado no recap)."""
    res = max(("1", "X", "2"), key=lambda k: probs[k])
    picks = {"resultado": res,
             "golos": "over_2.5" if probs["over_2.5"] >= 0.5 else "under_2.5",
             "ambas": "btts_sim" if probs["btts_sim"] >= 0.5 else "btts_nao"}
    if "cantos_over_9.5" in probs:
        picks["cantos"] = "cantos_over_9.5" if probs["cantos_over_9.5"] >= 0.5 else "cantos_under_9.5"
    if "cartoes_over_4.5" in probs:
        picks["cartoes"] = "cartoes_over_4.5" if probs["cartoes_over_4.5"] >= 0.5 else "cartoes_under_4.5"
    # combinada: a mais provável entre as que pagam pelo menos ~1.60 (as outras são quase certas e pouco úteis)
    combos = {k: v for k, v in probs.items() if k.startswith("combo:") and v <= 0.625}
    combos = combos or {k: v for k, v in probs.items() if k.startswith("combo:")}
    picks["combinada"] = max(combos, key=combos.get)
    picks["dupla"] = max(("1X", "X2", "12"), key=lambda k: probs[k])
    return picks


def value_bets(probs: dict, odds: dict) -> list[dict]:
    out = []
    for k, odd in (odds or {}).items():
        if k in probs and odd and odd > 1:
            ev = probs[k] * odd - 1
            if ev >= config.MODEL["value_threshold"] and probs[k] >= 0.2:
                out.append({"mercado": k, "prob": round(probs[k], 3), "odd_casa": odd,
                            "odd_justa": round(1 / probs[k], 2), "valor": round(ev, 3)})
    return sorted(out, key=lambda x: -x["valor"])


def team_form(hist: pd.DataFrame, team: str, n: int = 6) -> dict:
    d = hist[(hist["home"] == team) | (hist["away"] == team)].sort_values("date").tail(n)
    seq, gf, ga, xgf, xga = [], 0, 0, 0.0, 0.0
    for _, r in d.iterrows():
        home = r["home"] == team
        f, a = (r["hg"], r["ag"]) if home else (r["ag"], r["hg"])
        gf, ga = gf + f, ga + a
        if pd.notna(r.get("hxg")):
            xgf += r["hxg"] if home else r["axg"]
            xga += r["axg"] if home else r["hxg"]
        seq.append("V" if f > a else "E" if f == a else "D")
    pts = sum(3 if s == "V" else 1 if s == "E" else 0 for s in seq)
    return {"seq": "".join(seq), "pontos": pts, "gm": int(gf), "gs": int(ga),
            "xg": round(xgf, 1), "xga": round(xga, 1), "jogos": len(seq)}
