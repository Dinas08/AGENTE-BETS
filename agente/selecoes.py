"""Seleções nacionais (Liga das Nações e outras provas de seleções).

Golos: força de ataque/defesa de cada seleção ajustada a todos os jogos internacionais desde 2020
(github.com/martj42/international_results, atualizado poucos dias depois de cada janela), com os amigáveis a
pesar metade e sem vantagem de casa nos jogos em campo neutro.
Cantos e cartões: estatísticas do ESPN dos jogos oficiais das seleções europeias desde 2024, guardadas em
dados/selecoes_stats.json (só se vão buscar os jogos que faltam, no máximo MAX_NOVOS por execução).
Os nomes ficam em português (são os que aparecem no Telegram, na dashboard e em ajustes.json)."""
import io
import json
import time

import numpy as np
import pandas as pd
import requests

from agente import config
from agente.model import Strengths, fit_strengths

RESULTS_URL = "https://raw.githubusercontent.com/martj42/international_results/master/results.csv"
ESPN = "https://site.api.espn.com/apis/site/v2/sports/soccer"
STATS_PATH = config.DATA_DIR / "selecoes_stats.json"
DESDE = "2020-01-01"          # jogos usados para a força das seleções
DESDE_STATS = "2024-06-01"    # jogos com cantos/cartões (ESPN)
MAX_NOVOS = 350               # resumos do ESPN por execução (o resto fica para a seguinte)
PESO = {"Friendly": 0.5}      # amigáveis valem metade (rotação, sem nada em jogo)
MIN_JOGOS = 6                 # menos jogos (pesados) do que isto = dados limitados

# provas do ficheiro de resultados -> competição no ESPN (para ir buscar cantos e cartões)
ESPN_PROVA = {"UEFA Nations League": "uefa.nations", "FIFA World Cup qualification": "fifa.worldq.uefa",
              "FIFA World Cup": "fifa.world", "UEFA Euro": "uefa.euro"}

PT = {
    "Portugal": "Portugal", "Spain": "Espanha", "France": "França", "Germany": "Alemanha", "Italy": "Itália",
    "England": "Inglaterra", "Netherlands": "Países Baixos", "Belgium": "Bélgica", "Croatia": "Croácia",
    "Switzerland": "Suíça", "Denmark": "Dinamarca", "Austria": "Áustria", "Turkey": "Turquia", "Türkiye": "Turquia",
    "Poland": "Polónia", "Czech Republic": "Chéquia", "Czechia": "Chéquia", "Serbia": "Sérvia", "Ukraine": "Ucrânia",
    "Scotland": "Escócia", "Wales": "País de Gales", "Northern Ireland": "Irlanda do Norte",
    "Republic of Ireland": "Irlanda", "Ireland": "Irlanda", "Sweden": "Suécia", "Norway": "Noruega",
    "Finland": "Finlândia", "Iceland": "Islândia", "Hungary": "Hungria", "Romania": "Roménia", "Greece": "Grécia",
    "Slovakia": "Eslováquia", "Slovenia": "Eslovénia", "Bosnia and Herzegovina": "Bósnia",
    "Bosnia-Herzegovina": "Bósnia", "Albania": "Albânia", "North Macedonia": "Macedónia do Norte",
    "Montenegro": "Montenegro", "Kosovo": "Kosovo", "Bulgaria": "Bulgária", "Georgia": "Geórgia",
    "Armenia": "Arménia", "Azerbaijan": "Azerbaijão", "Kazakhstan": "Cazaquistão", "Israel": "Israel",
    "Cyprus": "Chipre", "Malta": "Malta", "Luxembourg": "Luxemburgo", "Liechtenstein": "Liechtenstein",
    "Andorra": "Andorra", "San Marino": "São Marino", "Gibraltar": "Gibraltar", "Faroe Islands": "Ilhas Faroé",
    "Estonia": "Estónia", "Latvia": "Letónia", "Lithuania": "Lituânia", "Belarus": "Bielorrússia",
    "Moldova": "Moldávia", "Russia": "Rússia",
    # variantes de nomes (API-Football, ESPN)
    "Rep. Of Ireland": "Irlanda", "Bosnia & Herzegovina": "Bósnia", "FYR Macedonia": "Macedónia do Norte",
    "Macedonia": "Macedónia do Norte", "Faroe Isl.": "Ilhas Faroé",
    # fora da Europa (amigáveis e Mundial)
    "Brazil": "Brasil", "Argentina": "Argentina", "Uruguay": "Uruguai", "Colombia": "Colômbia", "Chile": "Chile",
    "Mexico": "México", "United States": "EUA", "USA": "EUA", "Canada": "Canadá", "Japan": "Japão",
    "South Korea": "Coreia do Sul", "Korea Republic": "Coreia do Sul", "Morocco": "Marrocos", "Senegal": "Senegal",
    "Egypt": "Egito", "Saudi Arabia": "Arábia Saudita", "Australia": "Austrália", "Cape Verde": "Cabo Verde",
    "Ivory Coast": "Costa do Marfim", "Côte d'Ivoire": "Costa do Marfim", "Nigeria": "Nigéria", "Ghana": "Gana",
    "Ecuador": "Equador", "Paraguay": "Paraguai", "Peru": "Peru", "Iran": "Irão", "Tunisia": "Tunísia",
    "Algeria": "Argélia", "Angola": "Angola", "Mozambique": "Moçambique", "Qatar": "Catar",
}
UEFA = {v for k, v in PT.items() if k in list(PT)[:list(PT).index("Russia") + 1]}


def nome(n: str) -> str:
    """Nome da seleção em português (o do ESPN ou do ficheiro de resultados)."""
    return PT.get(n, PT.get(n.replace(" FC", ""), n))


def historico() -> pd.DataFrame:
    """Todos os jogos internacionais desde DESDE, com nomes em português e peso por tipo de jogo."""
    cache = config.CACHE_DIR / "selecoes_resultados.csv"
    if not cache.exists() or time.time() - cache.stat().st_mtime > 12 * 3600:
        try:
            r = requests.get(RESULTS_URL, timeout=60)
            r.raise_for_status()
            cache.write_text(r.text, encoding="utf-8")
        except requests.RequestException as e:
            print(f"  [seleções] não consegui atualizar os resultados internacionais: {e}")
    if not cache.exists():
        return pd.DataFrame()
    d = pd.read_csv(io.StringIO(cache.read_text(encoding="utf-8")))
    d = d[(d["date"] >= DESDE) & d["home_score"].notna()].copy()
    d["date"] = pd.to_datetime(d["date"])
    d["home"], d["away"] = d["home_team"].map(nome), d["away_team"].map(nome)
    d["hg"], d["ag"] = d["home_score"].astype(int), d["away_score"].astype(int)
    d["neutral"] = d["neutral"].astype(str).str.upper().eq("TRUE")
    d["peso"] = d["tournament"].map(PESO).fillna(1.0)
    return d[["date", "home", "away", "hg", "ag", "neutral", "tournament", "peso"]].reset_index(drop=True)


def _chave(date, home, away) -> str:
    return f"{pd.Timestamp(date):%Y-%m-%d}|{home}|{away}"


def estatisticas(hist: pd.DataFrame) -> dict:
    """Cantos e cartões dos jogos oficiais das seleções europeias (ESPN), guardados em STATS_PATH."""
    stats = json.loads(STATS_PATH.read_text(encoding="utf-8")) if STATS_PATH.exists() else {}
    falta = hist[(hist["date"] >= DESDE_STATS) & hist["tournament"].isin(ESPN_PROVA)
                 & (hist["home"].isin(UEFA) | hist["away"].isin(UEFA))]
    falta = falta[[_chave(r.date, r.home, r.away) not in stats for r in falta.itertuples()]]
    novos = 0
    for (date, prova), grupo in falta.groupby(["date", "tournament"]):
        if novos >= MAX_NOVOS:
            print(f"  [seleções] faltam cantos/cartões de {len(falta) - novos} jogos: ficam para a próxima execução")
            break
        slug = ESPN_PROVA[prova]
        try:
            evs = requests.get(f"{ESPN}/{slug}/scoreboard", params={"dates": f"{date:%Y%m%d}"}, timeout=20).json()
        except (requests.RequestException, ValueError):
            continue
        quer = {(r.home, r.away) for r in grupo.itertuples()}
        for e in evs.get("events", []):
            comp = e["competitions"][0]
            lado = {c.get("homeAway"): nome(c["team"]["displayName"]) for c in comp.get("competitors", [])}
            if (lado.get("home"), lado.get("away")) not in quer:
                continue
            try:
                s = requests.get(f"{ESPN}/{slug}/summary", params={"event": e["id"]}, timeout=20).json()
            except (requests.RequestException, ValueError):
                continue
            novos += 1
            out = {}
            ids = {c["team"]["id"]: c.get("homeAway") for c in comp.get("competitors", [])}
            for t in (s.get("boxscore") or {}).get("teams") or []:
                side = "h" if ids.get(t["team"]["id"]) == "home" else "a"
                v = {x["name"]: x.get("displayValue") for x in t.get("statistics", [])}
                for nm, k in (("wonCorners", "c"), ("yellowCards", "y")):
                    try:
                        out[f"{side}{k}"] = float(v[nm])
                    except (KeyError, TypeError, ValueError):
                        pass
            stats[_chave(date, lado["home"], lado["away"])] = out
        # jogos que o ESPN não tem: marca como vistos para não voltar a procurar
        for r in grupo.itertuples():
            stats.setdefault(_chave(date, r.home, r.away), {})
    if novos or not STATS_PATH.exists():
        STATS_PATH.write_text(json.dumps(stats, ensure_ascii=False, indent=0, sort_keys=True), encoding="utf-8")
    return stats


class ModeloSelecoes:
    """Mesma ideia do modelo das ligas (ataque/defesa com decaimento no tempo), para seleções."""

    def __init__(self, ref_date):
        self.hist = historico()
        d = self.hist[self.hist["date"] < pd.Timestamp(ref_date)]
        self.goals = self.corners = self.cards = None
        if len(d) < 100:
            return
        neu = d["neutral"].to_numpy(float)
        self.goals = fit_strengths(d, d["hg"].to_numpy(float), d["ag"].to_numpy(float), ref_date,
                                   neutral=neu, peso=d["peso"].to_numpy(float))
        try:
            st = estatisticas(d)
        except Exception as e:  # sem rede: fica só com os golos
            print(f"  [seleções] cantos/cartões indisponíveis: {e}")
            st = {}
        for kind, (kh, ka) in (("corners", ("hc", "ac")), ("cards", ("hy", "ay"))):
            rows = [(r, st.get(_chave(r.date, r.home, r.away), {})) for r in d.itertuples()]
            rows = [(r, s) for r, s in rows if kh in s and ka in s]
            if len(rows) < 80:
                continue
            dd = pd.DataFrame([{"date": r.date, "home": r.home, "away": r.away, "neutral": r.neutral} for r, _ in rows])
            setattr(self, kind, fit_strengths(dd, np.array([s[kh] for _, s in rows]), np.array([s[ka] for _, s in rows]),
                                              ref_date, ridge=config.MODEL["ridge_other"],
                                              neutral=dd["neutral"].to_numpy(float)))

    def expected(self, home: str, away: str, neutral: bool = False) -> dict:
        out = {"limited": True}
        for kind in ("goals", "corners", "cards"):
            s: Strengths | None = getattr(self, kind)
            if s is None or not (s.has(home) and s.has(away)):
                out[kind] = None
                continue
            ha = 0.0 if neutral else s.home
            out[kind] = (float(np.exp(s.mu + ha + s.att[home] - s.dfn[away])),
                         float(np.exp(s.mu + s.att[away] - s.dfn[home])), s.phi)
            if kind == "goals":
                out["limited"] = min(s.games.get(home, 0), s.games.get(away, 0)) < MIN_JOGOS
        if out["goals"] is None:  # seleção sem histórico: média, sem vantagem
            mu = self.goals.mu if self.goals else np.log(1.3)
            out["goals"] = (float(np.exp(mu)), float(np.exp(mu)), 1.0)
        return out

    def forma(self, team: str, n: int = 6) -> dict:
        """Últimos n jogos (V/E/D, golos), no formato da forma das equipas dos clubes (sem xG)."""
        from agente.model import team_form
        return team_form(self.hist, team, n)


def e_selecoes(comp: str) -> bool:
    return config.COMPETITIONS.get(comp, {}).get("type") == "selecoes"
