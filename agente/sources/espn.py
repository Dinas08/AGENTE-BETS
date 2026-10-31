"""ESPN (endpoints públicos, sem chave): jogos, resultados, cantos/cartões e odds (DraftKings)
das ligas, taças nacionais e provas europeias."""
import datetime as dt
import hashlib
import json
import time
from zoneinfo import ZoneInfo

import requests

from agente import config

BASE = "https://site.api.espn.com/apis/site/v2/sports/soccer"
LISBON = ZoneInfo("Europe/Lisbon")
FINISHED = {"STATUS_FULL_TIME", "STATUS_FINAL", "STATUS_FINAL_AET", "STATUS_FINAL_PEN", "STATUS_END_OF_EXTRATIME"}
SKIP = {"STATUS_POSTPONED", "STATUS_CANCELED", "STATUS_ABANDONED", "STATUS_SUSPENDED", "STATUS_FORFEIT"}


def _get(path: str, params: dict, ttl_hours: float) -> dict | None:
    key = hashlib.md5(f"{path}?{sorted(params.items())}".encode()).hexdigest()[:16]
    cache = config.CACHE_DIR / f"espn_{key}.json"
    if cache.exists() and time.time() - cache.stat().st_mtime < ttl_hours * 3600:
        return json.loads(cache.read_text(encoding="utf-8"))
    try:
        r = requests.get(f"{BASE}/{path}", params=params, timeout=20)
        r.raise_for_status()
        data = r.json()
    except (requests.RequestException, ValueError) as e:
        print(f"  [ESPN] falhou {path} {params}: {e}")
        return None
    cache.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    return data


def american_to_decimal(v) -> float | None:
    try:
        a = float(str(v).replace("+", ""))
    except (TypeError, ValueError):
        return None
    if a == 0:
        return None
    return round(1 + (a / 100 if a > 0 else 100 / -a), 2)


def _dig(d, *keys):
    for k in keys:
        if not isinstance(d, dict):
            return None
        d = d.get(k)
    return d


def _odds(comp: dict) -> dict:
    out = {}
    for o in comp.get("odds") or []:
        for side, k in (("home", "1"), ("draw", "X"), ("away", "2")):
            v = american_to_decimal(_dig(o, "moneyline", side, "close", "odds"))
            if v:
                out.setdefault(k, v)
        for side in ("over", "under"):
            line = str(_dig(o, "total", side, "close", "line") or "")[1:]
            v = american_to_decimal(_dig(o, "total", side, "close", "odds"))
            if line and v:
                out.setdefault(f"{side}_{line}", v)
    return out


def _team(comp: dict, side: str) -> dict:
    return next(c for c in comp["competitors"] if c.get("homeAway") == side)


def events(slug: str, day: dt.date, ttl_hours: float | None = None) -> list[dict]:
    """Jogos de uma competição num dia (hora de Lisboa)."""
    ttl = ttl_hours if ttl_hours is not None else (24 * 30 if day < dt.date.today() - dt.timedelta(days=3) else 3)
    data = _get(f"{slug}/scoreboard", {"dates": day.strftime("%Y%m%d")}, ttl)
    out = []
    for e in (data or {}).get("events", []):
        c = e["competitions"][0]
        status = e["status"]["type"]["name"]
        if status in SKIP:
            continue
        h, a = _team(c, "home"), _team(c, "away")
        ko = dt.datetime.fromisoformat(e["date"].replace("Z", "+00:00")).astimezone(LISBON).replace(tzinfo=None)
        finished = status in FINISHED
        out.append({
            "espn_id": e["id"], "slug": slug, "kickoff": ko, "status": status, "finished": finished,
            "home": h["team"]["displayName"], "away": a["team"]["displayName"],
            "hg": int(h["score"]) if finished and h.get("score") not in (None, "") else None,
            "ag": int(a["score"]) if finished and a.get("score") not in (None, "") else None,
            "round": (c.get("notes") or [{}])[0].get("headline", ""),
            "neutral": bool(c.get("neutralSite")), "odds": _odds(c),
        })
    return out


def match_stats(slug: str, espn_id: str) -> dict:
    """Cantos, cartões e remates de um jogo terminado."""
    data = _get(f"{slug}/summary", {"event": espn_id}, 24 * 30)
    teams = ((data or {}).get("boxscore") or {}).get("teams") or []
    comp = (((data or {}).get("header") or {}).get("competitions") or [{}])[0]
    sides = {c["team"]["id"]: c.get("homeAway") for c in comp.get("competitors", [])}
    out = {}
    for t in teams:
        side = "h" if sides.get(t["team"]["id"], t.get("homeAway")) == "home" else "a"
        s = {x["name"]: x.get("displayValue") for x in t.get("statistics", [])}
        for name, k in (("wonCorners", "c"), ("yellowCards", "y"), ("redCards", "r")):
            try:
                out[f"{side}{k}"] = float(s[name])
            except (KeyError, TypeError, ValueError):
                pass
    return out
