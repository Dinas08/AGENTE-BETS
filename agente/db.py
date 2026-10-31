"""Base de dados SQLite com previsões e resultados."""
import datetime as dt
import json
import sqlite3

import pandas as pd

from agente import config

SCHEMA = """
CREATE TABLE IF NOT EXISTS predictions (
    match_id TEXT PRIMARY KEY, kickoff TEXT, comp TEXT, comp_name TEXT, round TEXT,
    home TEXT, away TEXT, apif_id INTEGER, expected TEXT, probs TEXT, picks TEXT, odds TEXT,
    value_bets TEXT, adjustments TEXT, injuries TEXT, form TEXT, limited INTEGER,
    created_at TEXT, updated_at TEXT
);
CREATE TABLE IF NOT EXISTS results (
    match_id TEXT PRIMARY KEY, hg INTEGER, ag INTEGER, hc REAL, ac REAL, hy REAL, ay REAL,
    hr REAL, ar REAL, hxg REAL, axg REAL, source TEXT, updated_at TEXT
);
"""
JSON_COLS = ("expected", "probs", "picks", "odds", "value_bets", "adjustments", "injuries", "form")


def conn():
    c = sqlite3.connect(config.DB_PATH)
    c.executescript(SCHEMA)
    cols = {r[1] for r in c.execute("PRAGMA table_info(predictions)")}
    if "espn_ref" not in cols:  # migração: referência do jogo no ESPN ("slug|id") para buscar o resultado
        c.execute("ALTER TABLE predictions ADD COLUMN espn_ref TEXT")
    return c


def now():
    return dt.datetime.now().isoformat(timespec="seconds")


def upsert_prediction(row: dict):
    """Grava/atualiza a previsão. Depois do início do jogo a previsão fica congelada."""
    with conn() as c:
        cur = c.execute("SELECT kickoff, created_at FROM predictions WHERE match_id=?", (row["match_id"],)).fetchone()
        if cur and cur[0] and dt.datetime.fromisoformat(cur[0]) <= dt.datetime.now():
            return False
        data = {k: (json.dumps(v, ensure_ascii=False) if k in JSON_COLS else v) for k, v in row.items()}
        data["created_at"] = cur[1] if cur else now()
        data["updated_at"] = now()
        cols = ",".join(data)
        c.execute(f"INSERT OR REPLACE INTO predictions ({cols}) VALUES ({','.join('?' * len(data))})",
                  list(data.values()))
        return True


def set_espn_ref(match_id: str, ref: str):
    """Grava a referência ESPN mesmo em previsões já congeladas (para ir buscar o resultado)."""
    with conn() as c:
        c.execute("UPDATE predictions SET espn_ref=? WHERE match_id=? AND espn_ref IS NULL", (ref, match_id))


def upsert_result(row: dict):
    row = {**row, "updated_at": now()}
    with conn() as c:
        old = c.execute("SELECT * FROM results WHERE match_id=?", (row["match_id"],)).fetchone()
        if old:  # não apagar estatísticas já conhecidas (cantos, xG…) quando a nova fonte só traz o resultado
            names = [d[0] for d in c.execute("SELECT * FROM results LIMIT 0").description]
            merged = dict(zip(names, old))
            for k, v in row.items():
                if v is not None and not (isinstance(v, float) and pd.isna(v)):
                    merged[k] = v
            row = merged
        cols = ",".join(row)
        c.execute(f"INSERT OR REPLACE INTO results ({cols}) VALUES ({','.join('?' * len(row))})", list(row.values()))


def load_predictions(with_results=True) -> pd.DataFrame:
    with conn() as c:
        q = "SELECT p.*, r.hg, r.ag, r.hc, r.ac, r.hy, r.ay, r.hr, r.ar, r.hxg, r.axg FROM predictions p " \
            "LEFT JOIN results r USING(match_id)" if with_results else "SELECT * FROM predictions"
        df = pd.read_sql_query(q, c)
    for col in JSON_COLS:
        if col in df:
            df[col] = df[col].apply(lambda s: json.loads(s) if isinstance(s, str) and s else {})
    if not df.empty:
        df["kickoff"] = pd.to_datetime(df["kickoff"])
    return df
