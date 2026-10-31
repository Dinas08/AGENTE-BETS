"""Configuração central: competições, fontes e parâmetros do modelo."""
import os
import time
from pathlib import Path

from dotenv import load_dotenv

# Na nuvem (GitHub Actions, Streamlit Cloud) os servidores estão em UTC; as horas dos jogos são de Lisboa
if os.name != "nt":
    os.environ.setdefault("TZ", "Europe/Lisbon")
    time.tzset()

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "dados"
CACHE_DIR = DATA_DIR / "cache"
RECAP_DIR = DATA_DIR / "recaps"
DB_PATH = Path(os.getenv("AGENTE_DB", DATA_DIR / "agente.db"))
ADJUSTMENTS_PATH = DATA_DIR / "ajustes.json"
for _d in (DATA_DIR, CACHE_DIR, RECAP_DIR):
    _d.mkdir(parents=True, exist_ok=True)

load_dotenv(ROOT / ".env")
API_FOOTBALL_KEY = os.getenv("API_FOOTBALL_KEY", "").strip()
# Pedidos que ficam sempre por gastar no plano grátis (100/dia)
API_FOOTBALL_RESERVE = int(os.getenv("API_FOOTBALL_RESERVE", "5"))

# Modo nuvem: os dados vivem no ramo DADOS_BRANCH do repositório GitHub (escritos pelo GitHub Actions e pelas
# rotinas do agente); a dashboard só os lê. Sem AGENTE_REPO, tudo corre localmente como antes.
AGENTE_REPO = os.getenv("AGENTE_REPO", "").strip()          # ex.: "utilizador/agente-bets"
DADOS_BRANCH = os.getenv("DADOS_BRANCH", "claude/dados").strip()
GH_TOKEN = os.getenv("GH_TOKEN", "").strip()                # token só de leitura (repositório privado)

# Época atual (ano de início) e épocas usadas para treinar o modelo
CURRENT_SEASON = 2026
TRAIN_SEASONS = [2024, 2025, 2026]


def fd_season_code(start_year: int) -> str:
    """2026 -> '2627' (formato do football-data.co.uk)."""
    return f"{start_year % 100:02d}{(start_year + 1) % 100:02d}"


# Ligas principais (previsões) — football-data.co.uk div, id API-Football, força relativa (escala log-golos)
MAIN_LEAGUES = {
    "P1": {"name": "Liga Portugal", "country": "Portugal", "apif": 94, "strength": -0.22},
    "E0": {"name": "Premier League", "country": "Inglaterra", "apif": 39, "strength": 0.0},
    "D1": {"name": "Bundesliga", "country": "Alemanha", "apif": 78, "strength": -0.07},
    "I1": {"name": "Serie A", "country": "Itália", "apif": 135, "strength": -0.06},
}

# Ligas usadas só para dar rating aos adversários nas provas europeias
RATING_LEAGUES = {
    "SP1": {"name": "La Liga", "strength": -0.03},
    "F1": {"name": "Ligue 1", "strength": -0.13},
    "N1": {"name": "Eredivisie", "strength": -0.27},
    "B1": {"name": "Jupiler Pro League", "strength": -0.32},
    "T1": {"name": "Süper Lig", "strength": -0.33},
    "G1": {"name": "Super League Grécia", "strength": -0.40},
    "SC0": {"name": "Scottish Premiership", "strength": -0.45},
    # 2.as divisões (adversários frequentes nas taças)
    "E1": {"name": "Championship", "strength": -0.42},
    "D2": {"name": "2. Bundesliga", "strength": -0.50},
    "I2": {"name": "Serie B", "strength": -0.55},
}

ALL_LEAGUES = {**MAIN_LEAGUES, **RATING_LEAGUES}

# Força assumida para equipas sem dados (divisões inferiores, ligas pequenas)
UNKNOWN_TEAM_STRENGTH = {"domestic_cup": -0.65, "europe": -0.50}

# Taças e provas europeias (só via API-Football)
CUPS = {
    "TP": {"name": "Taça de Portugal", "apif": 96, "country": "Portugal", "type": "domestic_cup", "league": "P1"},
    "TL": {"name": "Taça da Liga", "apif": 97, "country": "Portugal", "type": "domestic_cup", "league": "P1"},
    "FAC": {"name": "FA Cup", "apif": 45, "country": "Inglaterra", "type": "domestic_cup", "league": "E0"},
    "EFL": {"name": "Carabao Cup", "apif": 48, "country": "Inglaterra", "type": "domestic_cup", "league": "E0"},
    "DFB": {"name": "DFB-Pokal", "apif": 81, "country": "Alemanha", "type": "domestic_cup", "league": "D1"},
    "CI": {"name": "Coppa Italia", "apif": 137, "country": "Itália", "type": "domestic_cup", "league": "I1"},
    "UCL": {"name": "Liga dos Campeões", "apif": 2, "country": "Europa", "type": "europe"},
    "UEL": {"name": "Liga Europa", "apif": 3, "country": "Europa", "type": "europe"},
    "UECL": {"name": "Liga Conferência", "apif": 848, "country": "Europa", "type": "europe"},
}

COMPETITIONS = {**{k: {**v, "type": "league", "league": k} for k, v in MAIN_LEAGUES.items()}, **CUPS}

# Identificadores das competições no ESPN (fonte grátis de jogos, resultados, cantos e odds)
ESPN_SLUGS = {
    "P1": "por.1", "E0": "eng.1", "D1": "ger.1", "I1": "ita.1",
    "TP": "por.taca.portugal", "FAC": "eng.fa", "EFL": "eng.league_cup", "DFB": "ger.dfb_pokal",
    "CI": "ita.coppa_italia", "UCL": "uefa.champions", "UEL": "uefa.europa", "UECL": "uefa.europa.conf",
}
for _k, _s in ESPN_SLUGS.items():
    COMPETITIONS[_k]["espn"] = _s

# Parâmetros do modelo
MODEL = {
    # valores afinados no backtest 2025/26 (ver agente/backtest.py)
    "decay_per_day": 0.0012,   # peso dos jogos cai para metade a cada ~1.5 anos; a forma recente pesa mais
    "xg_weight": 0.4,          # mistura golos reais (60%) com xG (40%) quando há xG
    "ridge": 3.0,              # encolhe equipas com poucos jogos para a média (golos)
    "ridge_other": 15.0,       # idem para cantos e cartões (mais ruído)
    "dc_rho": -0.10,           # correção Dixon-Coles para 0-0, 1-0, 0-1, 1-1
    "max_goals": 10,
    "home_adv_neutral_europe": 0.18,  # vantagem casa (log) usada em jogos europeus
    "value_threshold": 0.05,   # valor esperado mínimo para assinalar uma aposta de valor
    # peso do modelo vs odds das casas nos golos esperados (1 = só modelo). No backtest 2025/26 o mercado
    # sozinho foi o mais preciso no 1X2 (Brier 0.577 vs 0.587); 0.3 fica quase igual e mantém a opinião do modelo.
    # Jogos sem odds (taças/europeus sem chave API) usam só o modelo.
    "model_weight": 0.3,
}

PREDICTION_DAYS_AHEAD = 8   # quantos dias à frente se procuram jogos
