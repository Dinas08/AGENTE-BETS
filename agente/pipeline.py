"""Pipeline: recolhe dados -> treina modelo -> gera previsões -> recolhe resultados."""
import datetime as dt
import json
import re

import pandas as pd

from agente import aprendizagem, config, db
from agente.model import Predictor, blend_with_market, main_picks, markets, team_form, value_bets
from agente.sources import api_football as apif
from agente.sources import espn
from agente.sources import football_data_uk as fd
from agente.teams import TeamMatcher

FINISHED = {"FT", "AET", "PEN"}
MAX_ODDS_REQUESTS = 30       # por execução
MAX_STATS_REQUESTS = 15      # cantos de jogos de taça/europeus terminados


def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", s.lower())


def match_id(kickoff: dt.datetime, comp: str, home: str, away: str) -> str:
    return f"{kickoff:%Y%m%d}-{comp}-{slug(home)}-{slug(away)}"


def load_adjustments() -> dict:
    if not config.ADJUSTMENTS_PATH.exists():
        return {"equipas": {}, "jogos": {}}
    try:
        return json.loads(config.ADJUSTMENTS_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"  [ajustes] ficheiro inválido, ignorado: {e}")
        return {"equipas": {}, "jogos": {}}


def adjustment_for(adj: dict, matcher: TeamMatcher, mid: str, home: str, away: str, day: dt.date) -> dict:
    """Converte ajustes do agente (percentagens por equipa / por jogo) em multiplicadores de golos."""
    teams = {}
    for name, a in adj.get("equipas", {}).items():
        until = a.get("valido_ate")
        if until and dt.date.fromisoformat(until) < day:
            continue
        teams[matcher.match(name) or name] = a
    h, a = teams.get(home, {}), teams.get(away, {})
    hg = (1 + h.get("golos_marcados", 0) / 100) * (1 + a.get("golos_sofridos", 0) / 100)
    ag = (1 + a.get("golos_marcados", 0) / 100) * (1 + h.get("golos_sofridos", 0) / 100)
    j = adj.get("jogos", {}).get(mid, {})
    hg *= 1 + j.get("golos_casa", 0) / 100
    ag *= 1 + j.get("golos_fora", 0) / 100
    notes = [f"{t}: {x['motivo']}" for t, x in ((home, h), (away, a)) if x.get("motivo")]
    if j.get("nota"):
        notes.append(j["nota"])
    # jogadores ausentes registados pelo agente (lesões/castigos lidos nas notícias)
    missing = [{"equipa": t, "jogador": p.get("jogador"), "motivo": p.get("motivo"),
                "importancia": p.get("importancia"), "fonte": (x.get("fontes") or [""])[0]}
               for t, x in ((home, h), (away, a)) for p in x.get("ausentes", [])]
    return {"home_goals": round(hg, 3), "away_goals": round(ag, 3), "notas": notes, "ausentes": missing}


def _fd_odds(r) -> dict:
    m = {"odd_h": "1", "odd_d": "X", "odd_a": "2", "odd_o25": "over_2.5", "odd_u25": "under_2.5"}
    return {v: float(r[k]) for k, v in m.items() if k in r and pd.notna(r[k])}


def collect_fixtures(matcher: TeamMatcher, today: dt.date) -> tuple[list[dict], list[dict]]:
    """Devolve (jogos futuros, jogos terminados recentes da API)."""
    horizon = today + dt.timedelta(days=config.PREDICTION_DAYS_AHEAD)
    games: dict[str, dict] = {}

    up = fd.upcoming_fixtures()
    for _, r in up.iterrows():
        t = str(r.get("time")) if pd.notna(r.get("time")) else "15:00"
        ko = dt.datetime.combine(r["date"].date(), dt.time.fromisoformat(t[:5]))
        if not (today <= ko.date() <= horizon):
            continue
        mid = match_id(ko, r["div"], r["home"], r["away"])
        games[mid] = {"match_id": mid, "kickoff": ko, "comp": r["div"], "home": r["home"], "away": r["away"],
                      "round": "", "apif_id": None, "odds": _fd_odds(r)}

    def find_existing(comp, home, away, day):
        # mesmo jogo vindo de outra fonte: mesma prova, mesmo dia e pelo menos uma equipa igual
        return next((g for g in games.values() if g["comp"] == comp and g["kickoff"].date() == day
                     and (g["home"] == home or g["away"] == away)), None)

    finished = []
    unmatched = set()
    for comp, c in config.COMPETITIONS.items():
        if not c.get("espn"):
            continue
        day = today - dt.timedelta(days=4)
        while day <= horizon:
            # jogos de hoje/ontem mudam (resultados): cache curta
            fresh = 0.2 if day >= today - dt.timedelta(days=1) and day <= today else None
            for ev in espn.events(c["espn"], day, ttl_hours=fresh):
                home, away = matcher.match(ev["home"]), matcher.match(ev["away"])
                unmatched |= {n for n, m in ((ev["home"], home), (ev["away"], away)) if m is None}
                home, away = home or ev["home"], away or ev["away"]
                ko = ev["kickoff"]
                existing = find_existing(comp, home, away, ko.date())
                mid = existing["match_id"] if existing else match_id(ko, comp, home, away)
                db.set_espn_ref(mid, f"{ev['slug']}|{ev['espn_id']}")
                if ev["finished"]:
                    finished.append({"match_id": mid, "hg": ev["hg"], "ag": ev["ag"], "comp": comp,
                                     "espn": (ev["slug"], ev["espn_id"])})
                    continue
                if ko.date() < today:
                    continue
                ref = f"{ev['slug']}|{ev['espn_id']}"
                if existing:
                    existing["odds"] = {**ev["odds"], **existing["odds"]}
                    existing["round"] = existing["round"] or ev["round"]
                    existing["espn_ref"] = ref
                else:
                    games[mid] = {"match_id": mid, "kickoff": ko, "comp": comp, "home": home, "away": away,
                                  "round": ev["round"], "apif_id": None, "odds": ev["odds"],
                                  "neutral": ev["neutral"], "espn_ref": ref}
            day += dt.timedelta(days=1)
    if unmatched:
        print(f"  equipas sem histórico (tratadas como desconhecidas): {', '.join(sorted(unmatched))}")

    if apif.enabled():
        for comp, c in config.COMPETITIONS.items():
            try:
                resp = apif.fixtures(c["apif"], config.CURRENT_SEASON, today - dt.timedelta(days=4), horizon)
            except apif.QuotaExhausted as e:
                print(f"  [API-Football] {e}")
                break
            for f in resp:
                ko = dt.datetime.fromisoformat(f["fixture"]["date"]).replace(tzinfo=None)
                hn, an = f["teams"]["home"]["name"], f["teams"]["away"]["name"]
                home, away = matcher.match(hn) or hn, matcher.match(an) or an
                mid = match_id(ko, comp, home, away)
                status = f["fixture"]["status"]["short"]
                if status in FINISHED:
                    finished.append({"match_id": mid, "apif_id": f["fixture"]["id"],
                                     "hg": f["goals"]["home"], "ag": f["goals"]["away"], "comp": comp})
                    continue
                if ko.date() < today or status in {"CANC", "PST", "ABD", "AWD", "WO"}:
                    continue
                # junta com o jogo do football-data se já existir (mesma data e equipas)
                existing = next((g for g in games.values() if g["comp"] == comp and g["home"] == home
                                 and g["away"] == away and g["kickoff"].date() == ko.date()), None)
                if existing:
                    existing.update({"apif_id": f["fixture"]["id"], "round": f["league"].get("round", ""),
                                     "kickoff": ko})
                else:
                    games[mid] = {"match_id": mid, "kickoff": ko, "comp": comp, "home": home, "away": away,
                                  "round": f["league"].get("round", ""), "apif_id": f["fixture"]["id"], "odds": {}}
    return sorted(games.values(), key=lambda g: g["kickoff"]), finished


def enrich_from_api(games: list[dict]):
    """Lesões e odds (BTTS, cantos, taças/europeus) via API-Football, dentro da quota."""
    ids = [g["apif_id"] for g in games if g.get("apif_id")]
    if not ids:
        return
    try:
        inj = apif.injuries_for_fixtures(ids)
    except apif.QuotaExhausted as e:
        print(f"  [API-Football] {e}")
        return
    by_fx: dict[int, list] = {}
    for i in inj:
        by_fx.setdefault(i["fixture"]["id"], []).append({
            "equipa": i["team"]["name"], "jogador": i["player"]["name"],
            "tipo": i["player"].get("type"), "motivo": i["player"].get("reason")})
    for g in games:
        g["injuries"] = by_fx.get(g.get("apif_id"), [])

    # odds: primeiro jogos sem odds nenhumas (taças/europa), depois os mais próximos
    order = sorted([g for g in games if g.get("apif_id")], key=lambda g: (bool(g["odds"]), g["kickoff"]))
    for g in order[:MAX_ODDS_REQUESTS]:
        try:
            o = apif.parse_odds(apif.odds_for_fixture(g["apif_id"]))
        except apif.QuotaExhausted as e:
            print(f"  [API-Football] {e}")
            break
        g["odds"] = {**o, **g["odds"]}  # odds do football-data têm prioridade no 1X2/2.5


def predict(today: dt.date | None = None) -> int:
    today = today or dt.date.today()
    print("1/4 A descarregar histórico (football-data.co.uk)...")
    hist = fd.history()
    print(f"    {len(hist)} jogos históricos")
    print("2/4 A treinar o modelo...")
    pred = Predictor(hist, today)
    matcher = TeamMatcher(set(hist["home"]) | set(hist["away"]))
    print("3/4 A recolher próximos jogos (football-data + ESPN" + (" + API-Football)..." if apif.enabled() else ")..."))
    games, finished = collect_fixtures(matcher, today)
    if apif.enabled():
        enrich_from_api(games)
    store_results(finished)
    adj = load_adjustments()
    corr = aprendizagem.team_corrections().set_index("equipa")
    n_corr = 0 if corr.empty else int((((corr["ataque"] - 1).abs() >= .03) | ((corr["defesa"] - 1).abs() >= .03)).sum())
    print(f"    aprendizagem: {n_corr} equipa(s) com correção pelos erros anteriores")
    print(f"4/4 A prever {len(games)} jogos...")
    n = 0
    for g in games:
        comp = config.COMPETITIONS[g["comp"]]
        exp = pred.expected(g["home"], g["away"], comp["type"], comp.get("league"),
                            neutral=bool(g.get("neutral")) or "final" == str(g.get("round", "")).lower())
        exp = blend_with_market(exp, g.get("odds", {}))
        a = adjustment_for(adj, matcher, g["match_id"], g["home"], g["away"], g["kickoff"].date())
        # correções aprendidas com os erros anteriores (ataque de uma equipa x defesa da outra)
        ch = corr.loc[g["home"]] if g["home"] in corr.index else None
        ca = corr.loc[g["away"]] if g["away"] in corr.index else None
        fh = (ch["ataque"] if ch is not None else 1) * (ca["defesa"] if ca is not None else 1)
        fa = (ca["ataque"] if ca is not None else 1) * (ch["defesa"] if ch is not None else 1)
        a["home_goals"] = round(a["home_goals"] * fh, 3)
        a["away_goals"] = round(a["away_goals"] * fa, 3)
        a["aprendizagem"] = {"casa": round(fh, 3), "fora": round(fa, 3)}
        for team, c in ((g["home"], ch), (g["away"], ca)):
            note = aprendizagem.describe(team, c["ataque"], c["defesa"]) if c is not None else None
            if note:
                a["notas"].append(note)
        mk = markets(exp, a)
        if exp["blended"]:
            mk["expected"]["golos_modelo"] = [round(float(x), 2) for x in exp["goals_model"]]
            mk["expected"]["golos_mercado"] = [round(float(x), 2) for x in exp["goals_market"]]
        row = {
            "match_id": g["match_id"], "kickoff": g["kickoff"].isoformat(), "comp": g["comp"],
            "comp_name": comp["name"], "round": g.get("round", ""), "home": g["home"], "away": g["away"],
            "apif_id": g.get("apif_id"), "espn_ref": g.get("espn_ref"), "expected": mk["expected"],
            "probs": {k: round(v, 4) for k, v in mk["probs"].items()}, "picks": main_picks(mk["probs"]),
            "odds": g.get("odds", {}), "value_bets": value_bets(mk["probs"], g.get("odds", {})),
            "adjustments": a, "injuries": g.get("injuries") or a["ausentes"],
            "form": {"casa": team_form(hist, g["home"]), "fora": team_form(hist, g["away"])},
            "limited": int(exp["limited"]),
        }
        n += db.upsert_prediction(row)
    print(f"    {n} previsões gravadas/atualizadas. Quota API hoje: {apif.quota_status()}")
    return n


def store_results(finished: list[dict]):
    """Grava resultados dos jogos que previmos e vai buscar cantos/cartões (ESPN ou API-Football)."""
    preds = db.load_predictions(with_results=True)
    if preds.empty:
        return
    known = preds.set_index("match_id")
    need = [f for f in finished if f["match_id"] in known.index and f["hg"] is not None]
    for f in need:
        db.upsert_result({"match_id": f["match_id"], "hg": f["hg"], "ag": f["ag"],
                          "source": "espn" if f.get("espn") else "api-football"})
    need = [f for f in need if pd.isna(known.loc[f["match_id"], "hc"])]
    for f in [f for f in need if f.get("espn")]:
        s = espn.match_stats(*f["espn"])
        if s:
            db.upsert_result({"match_id": f["match_id"], "hg": f["hg"], "ag": f["ag"], "hc": s.get("hc"),
                              "ac": s.get("ac"), "hy": s.get("hy"), "ay": s.get("ay"), "hr": s.get("hr"),
                              "ar": s.get("ar"), "source": "espn"})
    for f in [f for f in need if f.get("apif_id")][:MAX_STATS_REQUESTS]:
        try:
            stats = apif.fixture_statistics(f["apif_id"])
        except apif.QuotaExhausted:
            break
        vals = {}
        for side, team in zip(("h", "a"), stats):
            s = {x["type"]: x["value"] for x in team.get("statistics", [])}
            vals[f"{side}c"] = s.get("Corner Kicks")
            vals[f"{side}y"] = s.get("Yellow Cards")
            vals[f"{side}r"] = s.get("Red Cards")
            xg = s.get("expected_goals")
            vals[f"{side}xg"] = float(xg) if xg not in (None, "") else None
        if vals:
            db.upsert_result({"match_id": f["match_id"], "hg": f["hg"], "ag": f["ag"], "hc": vals.get("hc"),
                              "ac": vals.get("ac"), "hy": vals.get("hy"), "ay": vals.get("ay"),
                              "hr": vals.get("hr"), "ar": vals.get("ar"), "hxg": vals.get("hxg"),
                              "axg": vals.get("axg"), "source": "api-football"})


def quick_results() -> list[str]:
    """Resultado (e cantos/cartões) dos jogos previstos que já acabaram, direto do ESPN — rápido, sem treinar
    o modelo. Atualiza os recaps das semanas afetadas. Devolve os ids dos jogos com resultado novo."""
    preds = db.load_predictions(with_results=True)
    if preds.empty or "espn_ref" not in preds:
        return []
    now = pd.Timestamp.now()
    # um jogo dura ~1h55 com intervalo; damos margem para descontos
    pending = preds[preds["hg"].isna() & preds["espn_ref"].notna() & (preds["kickoff"] < now - pd.Timedelta(minutes=110))]
    if pending.empty:
        return []
    wanted = {p["espn_ref"].split("|")[1]: p for _, p in pending.iterrows()}
    new = []
    lookups = {(p["espn_ref"].split("|")[0], p["kickoff"].date()) for _, p in pending.iterrows()}
    for slug, day in lookups:
        for d in (day, day - dt.timedelta(days=1)):  # o ESPN agrupa por dia na hora dos EUA
            for ev in espn.events(slug, d, ttl_hours=0.05):
                p = wanted.get(ev["espn_id"])
                if p is None or not ev["finished"] or ev["hg"] is None or p["match_id"] in new:
                    continue
                s = espn.match_stats(slug, ev["espn_id"])
                db.upsert_result({"match_id": p["match_id"], "hg": ev["hg"], "ag": ev["ag"], "hc": s.get("hc"),
                                  "ac": s.get("ac"), "hy": s.get("hy"), "ay": s.get("ay"), "hr": s.get("hr"),
                                  "ar": s.get("ar"), "source": "espn"})
                new.append(p["match_id"])
    if new:
        from agente import recap
        for day in {preds.set_index("match_id").loc[m, "kickoff"].date() for m in new}:
            recap.build_recap(day)
    return new


def update_results() -> int:
    """Resultados das ligas (com cantos, cartões e xG) a partir do football-data.co.uk."""
    preds = db.load_predictions(with_results=True)
    if preds.empty:
        return 0
    pending = preds[(preds["kickoff"] < pd.Timestamp.now()) & preds["comp"].isin(config.MAIN_LEAGUES)]
    if pending.empty:
        return 0
    hist = pd.concat([fd.season_results(d, config.CURRENT_SEASON) for d in config.MAIN_LEAGUES])
    n = 0
    for _, p in pending.iterrows():
        r = hist[(hist["div"] == p["comp"]) & (hist["home"] == p["home"]) & (hist["away"] == p["away"])
                 & (hist["date"].dt.date == p["kickoff"].date())]
        if r.empty:
            continue
        r = r.iloc[0]
        val = lambda k: float(r[k]) if k in r and pd.notna(r[k]) else None
        db.upsert_result({"match_id": p["match_id"], "hg": int(r["hg"]), "ag": int(r["ag"]),
                          "hc": val("hc"), "ac": val("ac"), "hy": val("hy"), "ay": val("ay"), "hr": val("hr"),
                          "ar": val("ar"), "hxg": val("hxg"), "axg": val("axg"), "source": "football-data"})
        n += 1
    return n
