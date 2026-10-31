"""football-data.co.uk: histórico (golos, xG, remates, cantos, cartões, odds) e próximos jogos com odds. Grátis."""
import io
import time

import pandas as pd
import requests

from agente import config

BASE = "https://www.football-data.co.uk"
UA = {"User-Agent": "Mozilla/5.0 (AgenteBets)"}

COLS = {
    "Div": "div", "Date": "date", "Time": "time", "HomeTeam": "home", "AwayTeam": "away",
    "FTHG": "hg", "FTAG": "ag", "HTHG": "hthg", "HTAG": "htag", "HxG": "hxg", "AxG": "axg",
    "HS": "hs", "AS": "as_", "HST": "hst", "AST": "ast", "HC": "hc", "AC": "ac",
    "HY": "hy", "AY": "ay", "HR": "hr", "AR": "ar", "Referee": "referee",
    "AvgH": "odd_h", "AvgD": "odd_d", "AvgA": "odd_a",
    "Avg>2.5": "odd_o25", "Avg<2.5": "odd_u25",
    "AvgCH": "codd_h", "AvgCD": "codd_d", "AvgCA": "codd_a",
}


def _get(url: str, cache_name: str, max_age_hours: float | None) -> str | None:
    path = config.CACHE_DIR / cache_name
    if path.exists() and (max_age_hours is None or time.time() - path.stat().st_mtime < max_age_hours * 3600):
        return path.read_text(encoding="utf-8")
    try:
        r = requests.get(url, headers=UA, timeout=30)
        r.raise_for_status()
        text = r.content.decode("utf-8-sig", errors="replace")
        path.write_text(text, encoding="utf-8")
        return text
    except requests.RequestException as e:
        print(f"  [football-data] falhou {url}: {e}")
        return path.read_text(encoding="utf-8") if path.exists() else None


def _parse(text: str) -> pd.DataFrame:
    df = pd.read_csv(io.StringIO(text), on_bad_lines="skip")
    df = df.rename(columns=COLS)
    keep = [c for c in COLS.values() if c in df.columns]
    df = df[keep].dropna(subset=["home", "away", "date"])
    df["date"] = pd.to_datetime(df["date"], dayfirst=True, errors="coerce", format="mixed")
    return df.dropna(subset=["date"])


def season_results(div: str, season: int) -> pd.DataFrame:
    code = config.fd_season_code(season)
    max_age = 6 if season == config.CURRENT_SEASON else None
    text = _get(f"{BASE}/mmz4281/{code}/{div}.csv", f"fd_{div}_{code}.csv", max_age)
    if not text:
        return pd.DataFrame()
    df = _parse(text)
    df = df.dropna(subset=["hg", "ag"])
    df["season"] = season
    df["div"] = div
    return df


def history(divs=None, seasons=None) -> pd.DataFrame:
    divs = divs or list(config.ALL_LEAGUES)
    seasons = seasons or config.TRAIN_SEASONS
    frames = [season_results(d, s) for d in divs for s in seasons]
    frames = [f for f in frames if not f.empty]
    return pd.concat(frames, ignore_index=True).sort_values("date") if frames else pd.DataFrame()


def upcoming_fixtures() -> pd.DataFrame:
    """Próximos jogos (publicados ~2x por semana) com odds médias das casas."""
    text = _get(f"{BASE}/fixtures.csv", "fd_fixtures.csv", 3)
    if not text:
        return pd.DataFrame()
    df = _parse(text)
    return df[df["div"].isin(config.MAIN_LEAGUES)].reset_index(drop=True)
