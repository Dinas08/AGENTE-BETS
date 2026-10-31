"""Cliente API-Football (v3) com cache e controlo da quota diária (plano grátis: 100 pedidos/dia)."""
import datetime as dt
import hashlib
import json
import time

import requests

from agente import config

BASE = "https://v3.football.api-sports.io"
QUOTA_FILE = config.CACHE_DIR / "apif_quota.json"


class QuotaExhausted(Exception):
    pass


class PlanRestricted(QuotaExhausted):
    """O plano (ex.: grátis) não dá acesso à época atual."""


def _quota() -> dict:
    today = dt.datetime.now(dt.UTC).strftime("%Y-%m-%d")
    q = json.loads(QUOTA_FILE.read_text()) if QUOTA_FILE.exists() else {}
    if q.get("day") != today:
        q = {"day": today, "used": 0, "remaining": None, "errors": []}
    return q


def _save_quota(q: dict):
    QUOTA_FILE.write_text(json.dumps(q, indent=1, ensure_ascii=False))


def quota_status() -> dict:
    return _quota()


def enabled() -> bool:
    return bool(config.API_FOOTBALL_KEY)


def get(endpoint: str, params: dict, ttl_hours: float = 6) -> list:
    """Devolve `response` da API. Usa cache para não gastar pedidos repetidos."""
    if not enabled():
        return []
    key = hashlib.md5(f"{endpoint}?{sorted(params.items())}".encode()).hexdigest()[:16]
    cache = config.CACHE_DIR / f"apif_{endpoint.replace('/', '_')}_{key}.json"
    if cache.exists() and time.time() - cache.stat().st_mtime < ttl_hours * 3600:
        return json.loads(cache.read_text(encoding="utf-8"))

    q = _quota()
    if q.get("plan_blocked"):
        raise PlanRestricted(q["plan_blocked"])
    if q["remaining"] is not None and q["remaining"] <= config.API_FOOTBALL_RESERVE:
        raise QuotaExhausted(f"Quota diária quase esgotada ({q['remaining']} restantes)")

    r = requests.get(f"{BASE}/{endpoint}", params=params,
                     headers={"x-apisports-key": config.API_FOOTBALL_KEY}, timeout=30)
    q["used"] += 1
    rem = r.headers.get("x-ratelimit-requests-remaining")
    if rem is not None and rem.isdigit():
        q["remaining"] = int(rem)
    data = r.json() if r.ok else {}
    errors = data.get("errors")
    if errors:
        msg = json.dumps(errors, ensure_ascii=False)
        q["errors"] = (q.get("errors", []) + [f"{endpoint} {params}: {msg}"])[-20:]
        if isinstance(errors, dict) and "plan" in errors:
            q["plan_blocked"] = f"Plano sem acesso à época {config.CURRENT_SEASON} (usa-se o ESPN)"
            _save_quota(q)
            raise PlanRestricted(q["plan_blocked"])
        _save_quota(q)
        print(f"  [API-Football] {endpoint} {params}: {msg}")
        if "requests" in msg.lower() or "limit" in msg.lower():
            raise QuotaExhausted(msg)
        return []
    _save_quota(q)
    resp = data.get("response", [])
    cache.write_text(json.dumps(resp, ensure_ascii=False), encoding="utf-8")
    time.sleep(6.5)  # plano grátis: ~10 pedidos/minuto
    return resp


def fixtures(league_id: int, season: int, date_from: dt.date, date_to: dt.date) -> list:
    return get("fixtures", {"league": league_id, "season": season, "from": date_from.isoformat(),
                            "to": date_to.isoformat(), "timezone": "Europe/Lisbon"}, ttl_hours=6)


def injuries_for_fixtures(fixture_ids: list[int]) -> list:
    out = []
    for i in range(0, len(fixture_ids), 20):
        chunk = fixture_ids[i:i + 20]
        out += get("injuries", {"ids": "-".join(map(str, chunk))}, ttl_hours=8)
    return out


def odds_for_fixture(fixture_id: int) -> list:
    return get("odds", {"fixture": fixture_id}, ttl_hours=8)


def fixture_statistics(fixture_id: int) -> list:
    return get("fixtures/statistics", {"fixture": fixture_id}, ttl_hours=24 * 30)


def parse_odds(resp: list) -> dict:
    """Média das casas para os mercados principais -> {'1': 2.1, 'X': 3.3, 'over_2.5': 1.9, 'btts_sim': 1.8, ...}."""
    acc: dict[str, list[float]] = {}
    for item in resp:
        for bm in item.get("bookmakers", []):
            for bet in bm.get("bets", []):
                name = bet.get("name", "")
                for v in bet.get("values", []):
                    val, odd = str(v.get("value")), v.get("odd")
                    try:
                        odd = float(odd)
                    except (TypeError, ValueError):
                        continue
                    k = None
                    if name == "Match Winner":
                        k = {"Home": "1", "Draw": "X", "Away": "2"}.get(val)
                    elif name == "Goals Over/Under":
                        k = val.lower().replace(" ", "_")  # over_2.5
                    elif name == "Both Teams Score":
                        k = {"Yes": "btts_sim", "No": "btts_nao"}.get(val)
                    elif name in ("Corners Over Under", "Corners Over/Under"):
                        k = "cantos_" + val.lower().replace(" ", "_")
                    elif name == "Double Chance":
                        k = {"Home/Draw": "1X", "Home/Away": "12", "Draw/Away": "X2"}.get(val)
                    if k:
                        acc.setdefault(k, []).append(odd)
    return {k: round(sum(v) / len(v), 2) for k, v in acc.items()}
