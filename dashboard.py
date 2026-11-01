"""Dashboard do Agente Bets — abrir com «Abrir dashboard.bat» (ou: streamlit run dashboard.py)."""
import contextlib
import datetime as dt
import html
import io
import json

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from agente import config, db
from agente.model import label
from agente.recap import PICK_NAMES, evaluate, outcome, value_pnl, week_bounds
from agente.sources import api_football as apif

st.set_page_config(page_title="Agente Bets", page_icon="⚽", layout="wide")

# Tema preto + dourado. Paleta validada (incl. daltonismo) sobre fundo preto:
# casa = dourado, empate = grafite, fora = marfim; estados verde/vermelho (sempre com ✅/❌)
HOME, DRAW, AWAY = "#d4af37", "#5f5e5a", "#e9e6df"
INK = {HOME: "#0b0b0b", DRAW: "#ffffff", AWAY: "#0b0b0b"}  # texto legível dentro de cada cor
GOLD_SOFT = "rgba(212,175,55,.14)"
GOOD, BAD = "#0ca30c", "#d03b3b"

st.markdown(f"""
<style>
.block-container {{padding-top: 3.2rem; max-width: 1250px;}}
.muted {{opacity:.62; font-size:.82rem;}}
.teams {{font-weight:650; font-size:1.02rem; line-height:1.35;}}
.teams .vs {{opacity:.45; font-weight:400; padding:0 .25rem;}}
.time {{font-weight:650; font-size:1.05rem;}}
.pbar {{display:flex; gap:2px; height:22px; border-radius:6px; overflow:hidden; font-size:.74rem;
        font-weight:700;}}
.pbar div {{display:flex; align-items:center; justify-content:center; white-space:nowrap; overflow:hidden;}}
.pbar.big {{height:34px; font-size:.9rem;}}
.plegend {{display:flex; justify-content:space-between; font-size:.72rem; opacity:.7; margin-top:2px;}}
.form span {{display:inline-block; width:16px; height:16px; line-height:16px; text-align:center; border-radius:4px;
        margin-right:2px; font-size:.65rem; font-weight:700; color:#fff;}}
.form .V {{background:{GOOD};}} .form .E {{background:#898781;}} .form .D {{background:{BAD};}}
h1 {{color:{HOME} !important; letter-spacing:-.01em;}}
h1::after {{content:""; display:block; width:56px; height:3px; background:{HOME}; border-radius:2px; margin-top:6px;}}
[data-testid="stVerticalBlockBorderWrapper"]:hover {{border-color:rgba(212,175,55,.45);}}
[data-testid="stMetricValue"] {{color:#f0ece2;}}
.chip {{display:inline-block; padding:2px 9px; border-radius:999px; font-size:.78rem; margin:2px 4px 2px 0;
        background:{GOLD_SOFT}; border:1px solid rgba(212,175,55,.35);}}
.chip.warn {{background:rgba(250,178,25,.16); border-color:rgba(250,178,25,.35);}}
.chip.good {{background:rgba(12,163,12,.13); border-color:rgba(12,163,12,.3);}}
.pick {{font-weight:600; font-size:.9rem;}}
.pick small {{display:block; font-weight:400; opacity:.65;}}
table.mk {{width:100%; border-collapse:collapse; font-size:.84rem; margin:.2rem 0 1rem;}}
table.mk th, table.mk td {{padding:5px 8px; border-bottom:1px solid rgba(128,128,128,.18); text-align:left;}}
table.mk th {{opacity:.65; font-weight:600; font-size:.76rem; text-transform:uppercase; letter-spacing:.02em;}}
table.mk td.num, table.mk th.num {{text-align:right; font-variant-numeric:tabular-nums;}}
.pos {{color:{GOOD}; font-weight:600;}} .neg {{opacity:.55;}}
.mini {{display:inline-block; height:7px; border-radius:4px; background:{HOME}; vertical-align:middle; margin-right:6px;}}
.leg {{padding:8px 0; border-bottom:1px solid rgba(128,128,128,.18);}}
.hero {{font-size:2rem; font-weight:700; line-height:1.1;}}
</style>""", unsafe_allow_html=True)

DAYS = ["seg", "ter", "qua", "qui", "sex", "sáb", "dom"]
# (o Windows não desenha emojis de bandeiras, por isso as ligas usam a bola)
COMP_ICON = {"P1": "⚽", "E0": "⚽", "D1": "⚽", "I1": "⚽", "UCL": "⭐", "UEL": "🟠", "UECL": "🟢",
             "TP": "🏆", "TL": "🏆", "FAC": "🏆", "EFL": "🏆", "DFB": "🏆", "CI": "🏆"}
COMP_ORDER = ["UCL", "UEL", "UECL", "P1", "E0", "D1", "I1", "TP", "TL", "FAC", "EFL", "DFB", "CI"]
MARKET_TYPES = {
    "Resultado": ["1", "X", "2"],
    "Dupla hipótese": ["1X", "X2", "12"],
    "Golos": [f"{s}_{l}" for l in (1.5, 2.5, 3.5) for s in ("over", "under")],
    "Ambas marcam": ["btts_sim", "btts_nao"],
    "Cantos": [f"cantos_{s}_{l}" for l in (8.5, 9.5, 10.5) for s in ("over", "under")],
    "Cartões": [f"cartoes_{s}_{l}" for l in (3.5, 4.5) for s in ("over", "under")],
    "Combinadas do jogo": None,
}
E = html.escape


# ------------------------------------------------------------------ dados e utilitários

@st.cache_data(ttl=60)
def _load_db() -> pd.DataFrame:
    return db.load_predictions()


def load() -> pd.DataFrame:
    df = _load_db().copy()
    if not df.empty:
        df["day"] = df["kickoff"].dt.date
        df["icon"] = df["comp"].map(COMP_ICON).fillna("⚽")
    return df


def upcoming(df):
    if df.empty:
        return df
    return df[df["kickoff"] >= pd.Timestamp.now() - pd.Timedelta(hours=2)].sort_values("kickoff")


def day_label(d: dt.date) -> str:
    today = dt.date.today()
    if d == today:
        return "Hoje"
    if d == today + dt.timedelta(days=1):
        return "Amanhã"
    if d == today - dt.timedelta(days=1):
        return "Ontem"
    return f"{DAYS[d.weekday()]} {d:%d/%m}"


def fair(p) -> str:
    return f"{1 / p:.2f}" if p and p > 0 else "—"


def prob_bar(p: dict, big=False) -> str:
    segs = []
    for k, color in (("1", HOME), ("X", DRAW), ("2", AWAY)):
        w = p.get(k, 0) * 100
        txt = f"{w:.0f}%" if w >= 13 else ""
        segs.append(f"<div style='width:{w:.1f}%;background:{color};color:{INK[color]}' "
                    f"title='{k}: {w:.0f}%'>{txt}</div>")
    return f"<div class='pbar{' big' if big else ''}'>{''.join(segs)}</div>"


def form_html(f: dict) -> str:
    seq = (f or {}).get("seq", "")
    return "<span class='form'>" + "".join(f"<span class='{c}'>{c}</span>" for c in seq[-5:]) + "</span>"


def html_table(rows: list[dict], num_cols=()) -> str:
    if not rows:
        return ""
    head = "".join(f"<th class='{'num' if c in num_cols else ''}'>{c}</th>" for c in rows[0])
    body = "".join("<tr>" + "".join(f"<td class='{'num' if c in num_cols else ''}'>{v}</td>" for c, v in r.items())
                   + "</tr>" for r in rows)
    return f"<table class='mk'><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>"


def market_rows(r, keys) -> list[dict]:
    rows = []
    for k in keys:
        if k not in r["probs"]:
            continue
        p, odd = r["probs"][k], r["odds"].get(k)
        val = p * odd - 1 if odd else None
        rows.append({
            "Mercado": E(label(k, r["home"], r["away"])),
            "Prob.": f"<span class='mini' style='width:{p * 60:.0f}px'></span>{p:.0%}",
            "Odd justa": fair(p),
            "Odd casas": f"{odd:.2f}" if odd else "—",
            "Valor": "" if val is None else f"<span class='{'pos' if val > 0 else 'neg'}'>{val:+.0%}</span>",
        })
    return rows


def show_table(r, keys, title=None):
    rows = market_rows(r, keys)
    if rows:
        st.markdown((f"**{title}**\n\n" if title else "") + html_table(rows, ("Odd justa", "Odd casas", "Valor")),
                    unsafe_allow_html=True)


def best_pick(r):
    """A previsão mais segura do jogo (entre resultado, golos, ambas, cantos e dupla)."""
    p, picks = r["probs"], r["picks"]
    cands = [picks[k] for k in ("resultado", "golos", "ambas", "cantos") if k in picks]
    return max(cands, key=lambda k: p.get(k, 0))


def add_to_slip(r, key):
    slip = st.session_state.setdefault("slip", [])
    if any(s["match_id"] == r["match_id"] and s["mercado"] == key for s in slip):
        return
    slip.append({"match_id": r["match_id"], "mercado": key, "jogo": f"{r['home']} vs {r['away']}",
                 "selecao": label(key, r["home"], r["away"]), "prob": r["probs"][key],
                 "odd": r["odds"].get(key), "kickoff": r["kickoff"], "icon": r["icon"]})


def empty_state(text, icon="ℹ️"):
    with st.container(border=True):
        st.markdown(f"<div style='text-align:center;padding:1.5rem;opacity:.75'>{icon}<br>{text}</div>",
                    unsafe_allow_html=True)


# ------------------------------------------------------------------ janela de detalhe do jogo

@st.dialog("Análise do jogo", width="large")
def match_dialog(mid: str):
    df = load()
    r = df[df["match_id"] == mid].iloc[0]
    p, e = r["probs"], r["expected"]
    st.markdown(f"<span class='muted'>{r['icon']} {E(r['comp_name'])}"
                f"{' · ' + E(r['round']) if r['round'] else ''} · {day_label(r['day'])} {r['kickoff']:%H:%M}</span>",
                unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    c1.markdown(f"<div class='teams'>{E(r['home'])}</div>{form_html(r['form'].get('casa'))}", unsafe_allow_html=True)
    c2.markdown(f"<div class='teams' style='text-align:right'>{E(r['away'])}</div>"
                f"<div style='text-align:right'>{form_html(r['form'].get('fora'))}</div>", unsafe_allow_html=True)
    st.markdown(prob_bar(p, big=True) +
                f"<div class='plegend'><span>Vitória {E(r['home'])}</span><span>Empate</span>"
                f"<span>Vitória {E(r['away'])}</span></div>", unsafe_allow_html=True)
    if r["limited"]:
        st.caption("⚠️ Dados limitados: uma das equipas não tem histórico; a previsão segue sobretudo as odds.")

    tabs = st.tabs(["Resumo", "Golos", "Cantos e cartões", "Combinadas", f"Lesões e notas ({len(r['injuries'])})"])
    with tabs[0]:
        m = st.columns(4)
        m[0].metric("Golos esperados", f"{e.get('golos_casa', 0):.1f} – {e.get('golos_fora', 0):.1f}")
        if "cantos_casa" in e:
            m[1].metric("Cantos esperados", f"{e['cantos_casa']:.1f} – {e['cantos_fora']:.1f}")
        if "cartoes_casa" in e:
            m[2].metric("Amarelos esperados", f"{e['cartoes_casa']:.1f} – {e['cartoes_fora']:.1f}")
        top = max((k for k in p if k.startswith("placar_")), key=p.get)
        m[3].metric("Resultado mais provável", top[7:], f"{p[top]:.0%}", delta_color="off")
        if "golos_modelo" in e:
            st.caption(f"Golos esperados = 30% modelo ({e['golos_modelo'][0]:.1f}–{e['golos_modelo'][1]:.1f}) "
                       f"+ 70% casas de apostas ({e['golos_mercado'][0]:.1f}–{e['golos_mercado'][1]:.1f}).")
        st.markdown("**Previsões principais**")
        keys = [r["picks"][k] for k in ("resultado", "dupla", "golos", "ambas", "cantos", "cartoes", "combinada")
                if k in r["picks"]]
        show_table(r, keys)
        fc, ff = r["form"].get("casa", {}), r["form"].get("fora", {})
        st.markdown(html_table([
            {"Últimos jogos": E(r["home"]), "Pontos": fc.get("pontos", 0), "Golos": f"{fc.get('gm', 0)}-{fc.get('gs', 0)}",
             "xG": f"{fc.get('xg', 0)}-{fc.get('xga', 0)}"},
            {"Últimos jogos": E(r["away"]), "Pontos": ff.get("pontos", 0), "Golos": f"{ff.get('gm', 0)}-{ff.get('gs', 0)}",
             "xG": f"{ff.get('xg', 0)}-{ff.get('xga', 0)}"}], ("Pontos",)), unsafe_allow_html=True)
    with tabs[1]:
        a, b = st.columns(2)
        with a:
            show_table(r, [f"{s}_{l}" for l in (0.5, 1.5, 2.5, 3.5, 4.5) for s in ("over", "under")], "Total de golos")
        with b:
            show_table(r, ["btts_sim", "btts_nao", "casa_marca", "fora_marca", "casa_sem_sofrer", "fora_sem_sofrer"],
                       "Marcar / sofrer")
            scores = sorted((k for k in p if k.startswith("placar_")), key=lambda k: -p[k])
            fig = go.Figure(go.Bar(x=[p[k] for k in scores], y=[k[7:] for k in scores], orientation="h",
                                   marker_color=HOME, hovertemplate="%{y}: %{x:.1%}<extra></extra>"))
            fig.update_layout(height=230, margin=dict(l=0, r=0, t=30, b=0), title="Resultados exatos mais prováveis",
                              xaxis_tickformat=".0%", yaxis_autorange="reversed", bargap=0.35)
            st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})
    with tabs[2]:
        a, b = st.columns(2)
        with a:
            show_table(r, [f"cantos_{s}_{l}" for l in (7.5, 8.5, 9.5, 10.5, 11.5, 12.5) for s in ("over", "under")]
                       + ["cantos_mais_casa", "cantos_mais_fora"], "Cantos")
        with b:
            show_table(r, [f"cartoes_{s}_{l}" for l in (2.5, 3.5, 4.5, 5.5) for s in ("over", "under")],
                       "Cartões amarelos")
    with tabs[3]:
        combos = sorted((k for k in p if k.startswith("combo:")), key=lambda k: -p[k])
        show_table(r, combos)
        st.caption("Combinadas com cantos assumem golos e cantos independentes (aproximação).")
    with tabs[4]:
        if r["injuries"]:
            rows = [{"Equipa": E(i.get("equipa", "")), "Jogador": E(i.get("jogador") or ""),
                     "Motivo": E(i.get("motivo") or ""), "Importância": E(i.get("importancia") or ""),
                     "Fonte": f"<a href='{E(i['fonte'])}' target='_blank'>notícia ↗</a>" if i.get("fonte") else ""}
                    for i in r["injuries"]]
            st.markdown(html_table(rows), unsafe_allow_html=True)
        else:
            st.caption("Sem ausências registadas. O agente pesquisa lesões e castigos todos os dias às 10h.")
        for n in r["adjustments"].get("notas", []):
            st.info(n, icon="📰")
        if r["adjustments"].get("notas"):
            st.caption(f"Efeito nos golos esperados: casa ×{r['adjustments']['home_goals']}, "
                       f"fora ×{r['adjustments']['away_goals']}")

    st.divider()
    opts = {label(k, r["home"], r["away"]) + f"  ·  {p[k]:.0%}": k
            for k in sorted((k for k in p if not k.startswith("placar_")), key=lambda k: -p[k])}
    c1, c2 = st.columns([4, 1.3], vertical_alignment="bottom")
    chosen = c1.multiselect("Adicionar ao bilhete", list(opts), placeholder="Escolhe uma ou mais seleções")
    if c2.button("➕ Adicionar", width="stretch", disabled=not chosen):
        for c in chosen:
            add_to_slip(r, opts[c])
        st.toast(f"{len(chosen)} seleção(ões) adicionada(s) ao bilhete", icon="🎟️")


# ------------------------------------------------------------------ página: jogos

def page_jogos():
    df = upcoming(load())
    st.title("Jogos")
    if df.empty:
        from agente import nuvem
        if not nuvem.ativo():
            empty_state("Ainda não há previsões. Vai a <b>Estado</b> e carrega em <b>Atualizar previsões</b>.", "📭")
        elif st.session_state.get("sync_erro"):
            empty_state(f"Não consegui ir buscar os dados ao GitHub.<br>{E(st.session_state['sync_erro'])}", "⚠️")
        else:
            empty_state("A ir buscar os dados ao GitHub… recarrega a página daqui a uns segundos.", "⏳")
        return

    days = sorted(df["day"].unique())
    day = st.segmented_control("Dia", days, format_func=day_label, default=days[0], key="day")
    sel = df[df["day"] == (day or days[0])]
    comps = [c for c in COMP_ORDER if c in set(sel["comp"])]
    names = {c: f"{COMP_ICON.get(c, '')} {config.COMPETITIONS[c]['name']}" for c in comps}
    c1, c2 = st.columns([3, 1.4], vertical_alignment="bottom")
    with c1:
        chosen = st.pills("Provas", comps, format_func=names.get, selection_mode="multi", default=comps,
                          key=f"comps_{day}")
    with c2:
        search = st.text_input("Procurar equipa", placeholder="ex.: Benfica, Arsenal…")
    sel = sel[sel["comp"].isin(chosen or comps)]
    if search:
        s = search.lower()
        sel = sel[sel["home"].str.lower().str.contains(s) | sel["away"].str.lower().str.contains(s)]

    # destaques do dia
    if not sel.empty:
        best = max(((r, best_pick(r)) for _, r in sel.iterrows()), key=lambda x: x[0]["probs"][x[1]])
        k = st.columns(4)
        with k[0].container(border=True):
            st.metric("Jogos", len(sel))
        with k[1].container(border=True):
            st.metric("Previsão mais segura", f"{best[0]['probs'][best[1]]:.0%}")
            st.caption(f"{label(best[1], best[0]['home'], best[0]['away'])} · "
                       f"{best[0]['home']}–{best[0]['away']}")
        with k[2].container(border=True):
            st.metric("Jogos com ausências", int((sel["injuries"].map(len) > 0).sum()))
        with k[3].container(border=True):
            st.metric("Apostas de valor", int(sel["value_bets"].map(len).sum()))

    if sel.empty:
        empty_state("Nenhum jogo com estes filtros.", "🔎")
        return

    st.markdown(f"<div class='plegend' style='justify-content:flex-start;gap:14px'>"
                f"<span><b style='color:{HOME}'>■</b> vitória casa</span><span><b style='color:{DRAW}'>■</b> empate</span>"
                f"<span><b style='color:{AWAY}'>■</b> vitória fora</span><span>⭐ previsão mais segura do jogo</span>"
                f"</div>", unsafe_allow_html=True)
    for comp in [c for c in COMP_ORDER if c in set(sel["comp"])]:
        g = sel[sel["comp"] == comp]
        st.subheader(f"{COMP_ICON.get(comp, '')} {config.COMPETITIONS[comp]['name']}", divider="gray")
        for _, r in g.iterrows():
            with st.container(border=True):
                c = st.columns([0.8, 3.2, 3, 2.6, 1.2], vertical_alignment="center")
                c[0].markdown(f"<div class='time'>{r['kickoff']:%H:%M}</div>", unsafe_allow_html=True)
                c[1].markdown(f"<div class='teams'>{E(r['home'])}<span class='vs'>vs</span>{E(r['away'])}</div>"
                              f"{form_html(r['form'].get('casa'))}&nbsp;&nbsp;{form_html(r['form'].get('fora'))}",
                              unsafe_allow_html=True)
                c[2].markdown(prob_bar(r["probs"]), unsafe_allow_html=True)
                bp = best_pick(r)
                chips = ""
                if r["injuries"]:
                    chips += f"<span class='chip warn'>🩹 {len(r['injuries'])} ausente(s)</span>"
                if r["value_bets"]:
                    chips += "<span class='chip good'>💰 valor</span>"
                if r["limited"]:
                    chips += "<span class='chip warn'>dados limitados</span>"
                c[3].markdown(f"<div class='pick'>⭐ {E(label(bp, r['home'], r['away']))}"
                              f"<small>{r['probs'][bp]:.0%} · odd justa {fair(r['probs'][bp])}</small></div>{chips}",
                              unsafe_allow_html=True)
                if c[4].button("Análise", key=f"open_{r['match_id']}", width="stretch", icon=":material/insights:"):
                    match_dialog(r["match_id"])


# ------------------------------------------------------------------ página: construtor de apostas

def candidates(df, types, min_p, only_odds) -> pd.DataFrame:
    rows = []
    for _, r in df.iterrows():
        keys = []
        for t in types:
            ks = MARKET_TYPES[t]
            keys += [k for k in r["probs"] if k.startswith("combo:")] if ks is None else ks
        for k in keys:
            pr = r["probs"].get(k)
            if pr is None or pr < min_p:
                continue
            odd = r["odds"].get(k)
            if only_odds and not odd:
                continue
            rows.append({"match_id": r["match_id"], "mercado": k,
                         "Quando": f"{DAYS[r['day'].weekday()]} {r['kickoff']:%H:%M}",
                         "Jogo": f"{r['icon']} {r['home']} vs {r['away']}",
                         "Seleção": label(k, r["home"], r["away"]), "Prob.": round(pr * 100, 1),
                         "Odd justa": round(1 / pr, 2), "Odd casas": f"{odd:.2f}" if odd else "—",
                         "Valor": f"{(pr * odd - 1) * 100:+.0f}%" if odd else ""})
    return pd.DataFrame(rows)


def page_bilhete():
    df = upcoming(load())
    df = df[df["kickoff"] > pd.Timestamp.now()] if not df.empty else df
    st.title("Construtor de apostas")
    st.caption("Escolhe seleções de vários jogos: o bilhete calcula a probabilidade de acertar tudo e a odd justa.")
    if df.empty:
        empty_state("Sem jogos futuros.", "📭")
        return
    slip = st.session_state.setdefault("slip", [])

    left, right = st.columns([2.3, 1], gap="large")
    with left:
        days = sorted(df["day"].unique())
        f1, f2 = st.columns([3, 2])
        sel_days = f1.pills("Dias", days, format_func=day_label, selection_mode="multi", default=days[:2])
        min_p = f2.slider("Probabilidade mínima", 0.3, 0.95, 0.6, 0.05, format="%.2f")
        types = st.pills("Mercados", list(MARKET_TYPES), selection_mode="multi",
                         default=["Resultado", "Dupla hipótese", "Golos", "Ambas marcam"])
        comps = [c for c in COMP_ORDER if c in set(df["comp"])]
        sel_comps = st.pills("Provas", comps, selection_mode="multi", default=comps,
                             format_func=lambda c: f"{COMP_ICON.get(c, '')} {config.COMPETITIONS[c]['name']}")
        only_odds = st.toggle("Só seleções com odds das casas", value=False)
        sub = df[df["day"].isin(sel_days or days) & df["comp"].isin(sel_comps or comps)]
        cand = candidates(sub, types or ["Resultado"], min_p, only_odds)
        if cand.empty:
            empty_state("Nenhuma seleção com estes filtros. Baixa a probabilidade mínima.", "🔎")
        else:
            cand = cand.sort_values("Prob.", ascending=False).reset_index(drop=True)
            st.caption(f"{len(cand)} seleções · marca as linhas que queres e carrega em «Adicionar ao bilhete»")
            ev = st.dataframe(
                cand.drop(columns=["match_id", "mercado"]), hide_index=True, width="stretch", height=420,
                on_select="rerun", selection_mode="multi-row", key="cand_table",
                column_config={
                    "Quando": st.column_config.TextColumn(width="small"),
                    "Jogo": st.column_config.TextColumn(width="medium"),
                    "Seleção": st.column_config.TextColumn(width="medium"),
                    "Prob.": st.column_config.ProgressColumn("Prob.", min_value=0, max_value=100, format="%.0f%%",
                                                             width="small"),
                    "Odd justa": st.column_config.NumberColumn(format="%.2f", width="small"),
                    "Odd casas": st.column_config.TextColumn(width="small"),
                    "Valor": st.column_config.TextColumn(width="small",
                                                         help="Prob. × odd das casas − 1 (positivo = valor)"),
                })
            rows = ev.selection.rows if ev and ev.selection else []
            if st.button(f"➕ Adicionar ao bilhete ({len(rows)})", disabled=not rows, type="primary"):
                for i in rows:
                    c = cand.iloc[i]
                    add_to_slip(df[df["match_id"] == c["match_id"]].iloc[0], c["mercado"])
                st.rerun()

            with st.expander("✨ Gerar sugestão automática", expanded=not slip):
                s1, s2 = st.columns([2, 1], vertical_alignment="bottom")
                target = s1.segmented_control("Odd alvo", [1.5, 2.0, 3.0, 5.0, 10.0], default=2.0,
                                              format_func=lambda x: f"@{x:.1f}")
                if s2.button("Gerar", width="stretch"):
                    picks, odd, used = [], 1.0, set()
                    for _, c in cand.iterrows():  # mais prováveis primeiro, um jogo de cada vez
                        if c["match_id"] in used:
                            continue
                        picks.append(c)
                        used.add(c["match_id"])
                        odd *= c["Odd justa"]
                        if odd >= (target or 2.0):
                            break
                    st.session_state["suggestion"] = [(c["match_id"], c["mercado"]) for c in picks]
                sug = st.session_state.get("suggestion")
                if sug:
                    prob = 1.0
                    for mid, k in sug:
                        r = df[df["match_id"] == mid].iloc[0]
                        prob *= r["probs"][k]
                        st.markdown(f"- {r['icon']} **{E(r['home'])} vs {E(r['away'])}** — "
                                    f"{E(label(k, r['home'], r['away']))} ({r['probs'][k]:.0%})")
                    st.markdown(f"Probabilidade de acertar tudo: **{prob:.0%}** · odd justa **{1 / prob:.2f}**")
                    if st.button("Usar esta sugestão"):
                        for mid, k in sug:
                            add_to_slip(df[df["match_id"] == mid].iloc[0], k)
                        st.session_state["suggestion"] = None
                        st.rerun()

    with right:
        with st.container(border=True):
            st.markdown(f"#### 🎟️ Bilhete ({len(slip)})")
            if not slip:
                st.caption("Vazio. Adiciona seleções da tabela, da sugestão automática ou da análise de cada jogo.")
            prob, odd_c, all_odds = 1.0, 1.0, True
            for i, s in enumerate(slip):
                a, b = st.columns([5, 1], vertical_alignment="center")
                odd_txt = f" · @{s['odd']:.2f}" if s["odd"] else ""
                a.markdown(f"<div class='leg'><b>{E(s['selecao'])}</b><br><span class='muted'>{s['icon']} "
                           f"{E(s['jogo'])} · {s['prob']:.0%}{odd_txt}</span></div>", unsafe_allow_html=True)
                if b.button("✕", key=f"rm_{i}", help="Remover"):
                    slip.pop(i)
                    st.rerun()
                prob *= s["prob"]
                if s["odd"]:
                    odd_c *= s["odd"]
                else:
                    all_odds = False
            if slip:
                st.markdown(f"<div class='muted'>Probabilidade de acertar tudo</div><div class='hero'>{prob:.0%}</div>",
                            unsafe_allow_html=True)
                m1, m2 = st.columns(2)
                m1.metric("Odd justa", f"{1 / prob:.2f}")
                if all_odds:
                    m2.metric("Odd das casas", f"{odd_c:.2f}", f"valor {prob * odd_c - 1:+.0%}",
                              delta_color="normal" if prob * odd_c > 1 else "off")
                else:
                    m2.metric("Odd das casas", "—", help="Falta a odd das casas em alguma seleção")
                ids = [s["match_id"] for s in slip]
                if len(ids) != len(set(ids)):
                    st.warning("Há duas seleções do mesmo jogo: não são independentes e a probabilidade fica errada. "
                               "Usa antes uma «Combinada do jogo».", icon="⚠️")
                if st.button("Limpar bilhete", width="stretch"):
                    st.session_state["slip"] = []
                    st.rerun()

        vb = [(r, v) for _, r in df.iterrows() for v in r["value_bets"]]
        with st.container(border=True):
            st.markdown("#### 💰 Apostas de valor")
            st.caption("Onde a nossa probabilidade × odd das casas > 1. Diferenças grandes costumam ser "
                       "informação que o modelo não tem — confirma as notícias.")
            if not vb:
                st.caption("Nenhuma neste momento.")
            for r, v in sorted(vb, key=lambda x: -x[1]["valor"])[:8]:
                st.markdown(f"<div class='leg'><b>{E(label(v['mercado'], r['home'], r['away']))}</b> "
                            f"<span class='pos'>{v['valor']:+.0%}</span><br><span class='muted'>{r['icon']} "
                            f"{E(r['home'])} vs {E(r['away'])} · {v['prob']:.0%} · @{v['odd_casa']:.2f}</span></div>",
                            unsafe_allow_html=True)


# ------------------------------------------------------------------ página: recaps

def page_recaps():
    st.title("Recaps")
    df = load()
    done = df.dropna(subset=["hg"]) if not df.empty else df
    if done.empty:
        empty_state("Os recaps aparecem quando os primeiros jogos previstos terminarem.<br>"
                    "O agente escreve a análise às terças e sextas às 12h.", "🗓️")
        return
    done = done.assign(week=done["day"].map(lambda d: week_bounds(d)[0]))
    weeks = sorted(done["week"].unique(), reverse=True)
    wk = st.selectbox("Semana", weeks, format_func=lambda w: f"Semana {w.isocalendar().week} · "
                      f"{w:%d/%m} a {w + dt.timedelta(days=6):%d/%m}")
    g = done[done["week"] == wk]
    ev = evaluate(g)

    k = st.columns(5)
    for col, kind in zip(k, ("resultado", "golos", "ambas", "cantos", "combinada")):
        e = ev[ev["tipo"] == kind]
        with col.container(border=True):
            if e.empty:
                st.metric(PICK_NAMES[kind], "—")
            else:
                diff = (e["acertou"].mean() - e["prob"].mean()) * 100
                st.metric(PICK_NAMES[kind], f"{e['acertou'].mean():.0%}", f"{diff:+.0f} pp vs esperado",
                          help=f"{int(e['acertou'].sum())}/{len(e)} acertos; o modelo esperava {e['prob'].mean():.0%}")

    path = config.RECAP_DIR / f"{wk.isocalendar().year}-S{wk.isocalendar().week:02d}.md"
    txt = path.read_text(encoding="utf-8") if path.exists() else ""
    analysis = txt.split("## Análise do agente", 1)[1].strip() if "## Análise do agente" in txt else ""
    with st.container(border=True):
        st.markdown("#### 🧠 Análise do agente")
        if not analysis or analysis.startswith("<!-- AGENTE"):
            st.caption("Ainda não escrita — o agente faz a análise às terças e sextas às 12h.")
        else:
            st.markdown(analysis)

    a, b = st.columns([1.2, 1], gap="large")
    with a:
        st.markdown("#### Jogo a jogo")
        only_miss = st.toggle("Só jogos com falhas no resultado")
        rows = []
        for _, r in g.sort_values("kickoff").iterrows():
            e = ev[ev["match_id"] == r["match_id"]]
            res_hit = outcome(r["picks"]["resultado"], r)
            if only_miss and res_hit:
                continue
            rows.append({"Jogo": f"{r['icon']} {r['home']} {int(r['hg'])}-{int(r['ag'])} {r['away']}",
                         "Resultado previsto": f"{'✅' if res_hit else '❌'} {label(r['picks']['resultado'], r['home'], r['away'])}",
                         "Acertos": f"{int(e['acertou'].sum())}/{len(e)}",
                         "xG": f"{r['hxg']:.1f}-{r['axg']:.1f}" if pd.notna(r.get("hxg")) else "",
                         "Cantos": f"{int(r['hc'])}-{int(r['ac'])}" if pd.notna(r.get("hc")) else ""})
        st.dataframe(pd.DataFrame(rows), hide_index=True, width="stretch")
    with b:
        st.markdown("#### Acerto por mercado")
        s = ev.groupby("tipo").agg(acerto=("acertou", "mean"), esperado=("prob", "mean"), n=("acertou", "size"))
        s.index = s.index.map(lambda t: PICK_NAMES.get(t, t))
        fig = go.Figure()
        fig.add_bar(y=s.index, x=s["acerto"], orientation="h", name="Acerto real", marker_color=HOME,
                    customdata=s["n"], hovertemplate="%{y}: %{x:.0%} (%{customdata} jogos)<extra></extra>")
        fig.add_scatter(y=s.index, x=s["esperado"], mode="markers", name="Esperado pelo modelo",
                        marker=dict(symbol="line-ns", size=18, line=dict(width=3, color=AWAY)),
                        hovertemplate="%{y}: esperado %{x:.0%}<extra></extra>")
        fig.update_layout(height=320, margin=dict(l=0, r=0, t=10, b=0), xaxis=dict(tickformat=".0%", range=[0, 1]),
                          legend=dict(orientation="h", y=-0.15), bargap=0.4)
        st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})
    if txt:
        with st.expander("Relatório completo (com explicações de cada falha)"):
            st.markdown(txt.split("## Análise do agente")[0])


# ------------------------------------------------------------------ página: desempenho

KIND_ORDER = ("resultado", "dupla", "golos", "ambas", "cantos", "cartoes", "combinada")


def page_desempenho():
    st.title("Desempenho")
    df = load()
    done = df.dropna(subset=["hg"]) if not df.empty else df
    if done.empty:
        empty_state("Ainda não há jogos terminados. Quando um jogo com previsão acabar, aparece aqui sozinho "
                    "em poucos minutos com o que acertámos e falhámos.", "⏳")
        backtest_expander(True)
        return

    ev = evaluate(done).merge(done[["match_id", "kickoff", "day", "home", "away", "hg", "ag", "comp_name", "icon"]],
                              on="match_id")
    stars = {r["match_id"]: best_pick(r) for _, r in done.iterrows()}
    ev["estrela"] = ev["mercado"] == ev["match_id"].map(stars)
    hits, n = int(ev["acertou"].sum()), len(ev)
    es = ev[ev["estrela"]]
    if not es.empty:
        eh = int(es["acertou"].sum())
        st.markdown(
            f"<div style='background:{GOLD_SOFT};border:1px solid {HOME};border-radius:12px;padding:14px 18px;"
            f"margin-bottom:12px'><span style='font-size:1.05rem'>⭐ <b>Apostas com estrela</b> "
            f"(a previsão mais segura de cada jogo)</span><br><span style='font-size:1.9rem;font-weight:700;"
            f"color:{HOME}'>{eh}/{len(es)} · {eh / len(es):.0%}</span> "
            f"<span class='muted'>· o modelo esperava {es['prob'].mean():.0%}</span></div>",
            unsafe_allow_html=True)
    k = st.columns(3)
    with k[0].container(border=True):
        st.metric("✅ Acertámos", hits)
    with k[1].container(border=True):
        st.metric("❌ Falhámos", n - hits)
    with k[2].container(border=True):
        st.metric("Taxa de acerto", f"{hits / n:.0%}")
    kinds = [k for k in KIND_ORDER if k in set(ev["tipo"])]
    st.markdown(" ".join(
        f"<span class='chip'>{PICK_NAMES[t]}: <b>{int(ev[ev['tipo'] == t]['acertou'].sum())}/"
        f"{int((ev['tipo'] == t).sum())}</b></span>" for t in kinds)
        + f"<span class='muted'> · {done.shape[0]} jogos terminados · atualiza sozinho quando um jogo acaba</span>",
        unsafe_allow_html=True)

    f1, f2 = st.columns([2, 3], vertical_alignment="bottom")
    show = f1.segmented_control("Mostrar", ["Todas", "⭐ Estrelas", "✅ Certas", "❌ Erradas"], default="Todas")
    chosen = f2.pills("Mercados", kinds, format_func=PICK_NAMES.get, selection_mode="multi", default=kinds)
    sel = ev[ev["tipo"].isin(chosen or kinds)]
    if show == "⭐ Estrelas":
        sel = sel[sel["estrela"]]
    elif show == "✅ Certas":
        sel = sel[sel["acertou"]]
    elif show == "❌ Erradas":
        sel = sel[~sel["acertou"]]
    if sel.empty:
        empty_state("Nada para mostrar com estes filtros.", "🔎")

    order = sel.sort_values("kickoff", ascending=False)["match_id"].drop_duplicates().tolist()
    cols = st.columns(2)
    for i, mid in enumerate(order):
        g = sel[sel["match_id"] == mid]
        g = g.assign(o=g["tipo"].map(KIND_ORDER.index) - 100 * g["estrela"]).sort_values("o")  # estrela primeiro
        r = g.iloc[0]
        lines = "".join(
            (f"<div style='padding:4px 8px;margin:2px -8px;background:{GOLD_SOFT};border-left:3px solid {HOME};"
             f"border-radius:6px;font-weight:600'>" if x.estrela else "<div style='padding:3px 0'>")
            + f"{'✅' if x.acertou else '❌'} {'⭐ ' if x.estrela else ''}{E(label(x.mercado, r['home'], r['away']))}"
            f" <span class='muted' style='font-weight:400'>· {PICK_NAMES[x.tipo]} · {x.prob:.0%}</span></div>"
            for x in g.itertuples())
        with cols[i % 2].container(border=True):
            st.markdown(f"<span class='muted'>{r['icon']} {E(r['comp_name'])} · {day_label(r['day'])}</span>"
                        f"<div class='teams' style='margin:2px 0 6px'>{E(r['home'])} {int(r['hg'])}-{int(r['ag'])} "
                        f"{E(r['away'])}</div>{lines}", unsafe_allow_html=True)

    with st.expander("📊 Gráficos (evolução, calibração, apostas de valor)"):
        perf_charts(ev.sort_values("kickoff"), done)
    backtest_expander(False)


def perf_charts(ev, done):
        kinds = [k for k in KIND_ORDER if k in set(ev["tipo"])]
        a, b = st.columns(2, gap="large")
        with a:
            focus = st.segmented_control("Evolução do acerto", kinds, format_func=PICK_NAMES.get,
                                         default=kinds[0], key="perf_kind")
            e = ev[ev["tipo"] == (focus or kinds[0])].reset_index(drop=True)
            fig = go.Figure()
            fig.add_scatter(x=e["kickoff"], y=e["acertou"].expanding().mean(), mode="lines", name="Acerto real",
                            line=dict(color=HOME, width=2), hovertemplate="%{x|%d/%m}: %{y:.0%}<extra>acerto</extra>")
            fig.add_scatter(x=e["kickoff"], y=e["prob"].expanding().mean(), mode="lines", name="Esperado",
                            line=dict(color=AWAY, width=2, dash="dot"),
                            hovertemplate="%{x|%d/%m}: %{y:.0%}<extra>esperado</extra>")
            fig.update_layout(height=300, margin=dict(l=0, r=0, t=10, b=0), yaxis_tickformat=".0%",
                              hovermode="x unified", legend=dict(orientation="h", y=-0.2))
            st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})
        with b:
            st.markdown("**Calibração** — quando o agente diz X%, acontece X%?")
            bins = pd.cut(ev["prob"], [0, .5, .6, .7, .8, .9, 1], labels=["<50%", "50-60%", "60-70%", "70-80%",
                                                                          "80-90%", "90%+"])
            cal = ev.groupby(bins, observed=True).agg(real=("acertou", "mean"), prev=("prob", "mean"),
                                                       n=("acertou", "size")).reset_index()
            fig = go.Figure()
            fig.add_bar(x=cal["prob"].astype(str), y=cal["real"], name="Aconteceu", marker_color=HOME,
                        customdata=cal["n"], hovertemplate="%{x}: %{y:.0%} (%{customdata} previsões)<extra></extra>")
            fig.add_scatter(x=cal["prob"].astype(str), y=cal["prev"], mode="markers", name="Previsto",
                            marker=dict(symbol="line-ew", size=26, line=dict(width=3, color=AWAY)),
                            hovertemplate="%{x}: previsto %{y:.0%}<extra></extra>")
            fig.update_layout(height=300, margin=dict(l=0, r=0, t=10, b=0), yaxis=dict(tickformat=".0%", range=[0, 1]),
                              legend=dict(orientation="h", y=-0.2), bargap=0.4)
            st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})

        pnl = value_pnl(done)
        if not pnl.empty:
            pnl = pnl.sort_values("kickoff")
            fig = go.Figure(go.Scatter(x=pnl["kickoff"], y=pnl["lucro"].cumsum(), mode="lines",
                                       line=dict(color=HOME, width=2), fill="tozeroy",
                                       hovertemplate="%{x|%d/%m}: %{y:+.1f} u<extra></extra>"))
            fig.update_layout(height=260, margin=dict(l=0, r=0, t=40, b=0),
                              title=f"Apostas de valor simuladas (1 unidade cada): {pnl['lucro'].sum():+.1f} u "
                                    f"em {len(pnl)} apostas")
            st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})


def backtest_expander(expanded: bool):
    bts = sorted(config.DATA_DIR.glob("backtest_*.csv"))
    if bts:
        with st.expander("📚 Backtest da época passada (1270 jogos, sem olhar para o futuro)", expanded=expanded):
            bt = pd.read_csv(bts[-1])
            picks = bt[~bt["valor"] & ~bt["tipo"].str.startswith("brier")]
            s = picks.groupby("tipo").agg(Jogos=("acertou", "size"), Acerto=("acertou", "mean"),
                                          Esperado=("prob", "mean")).reset_index()
            s["tipo"] = s["tipo"].map(lambda k: PICK_NAMES.get(k, k))
            st.dataframe(s.rename(columns={"tipo": "Mercado"}).sort_values("Acerto", ascending=False),
                         hide_index=True, width="stretch",
                         column_config={"Acerto": st.column_config.ProgressColumn(min_value=0, max_value=1,
                                                                                   format="percent"),
                                        "Esperado": st.column_config.NumberColumn(format="percent")})
            v = bt[bt["valor"]]
            if not v.empty:
                st.caption(f"Apostas de valor no backtest: {len(v)}, ROI {v['lucro'].mean():+.1%}. "
                           "No 1X2 o agente iguala as casas de apostas; a vantagem tem de vir das notícias.")


# ------------------------------------------------------------------ página: lições

def page_licoes():
    from agente import aprendizagem
    from agente.recap import explain
    st.title("Lições")
    st.caption("O que o agente aprende com os erros — e como isso muda as previsões seguintes.")
    df = load()
    done = df.dropna(subset=["hg"]) if not df.empty else df

    a, b = st.columns([1.4, 1], gap="large")
    with a:
        with st.container(border=True):
            st.markdown("#### 🧠 O que aprendemos")
            p = config.DATA_DIR / "licoes.md"
            txt = p.read_text(encoding="utf-8") if p.exists() else ""
            body = txt.split("## Ativas", 1)[1] if "## Ativas" in txt else txt
            body = body.replace("\n## ", "\n##### ")  # subtítulos do ficheiro em tamanho pequeno
            st.markdown("##### Ativas" + body if body.strip() else "Ainda sem lições.")
    with b:
        with st.container(border=True):
            st.markdown("#### 🔧 Correções automáticas")
            st.caption("Equipas em que errámos sistematicamente os golos (2+ jogos). Já entram nas próximas previsões.")
            c = aprendizagem.team_corrections(df)
            c = c[(c["ataque"] - 1).abs().ge(.03) | (c["defesa"] - 1).abs().ge(.03)] if not c.empty else c
            if c.empty:
                st.caption("Nenhuma ainda — cada equipa precisa de pelo menos 2 jogos previstos terminados.")
            else:
                st.markdown(html_table([{"Equipa": E(r.equipa), "Jogos": r.jogos,
                                         "Ataque": f"{r.ataque - 1:+.0%}", "Defesa (sofre)": f"{r.defesa - 1:+.0%}"}
                                        for r in c.itertuples()], ("Jogos", "Ataque", "Defesa (sofre)")),
                            unsafe_allow_html=True)
        with st.container(border=True):
            st.markdown("#### 🎯 Confiança por mercado")
            m = aprendizagem.market_calibration(df)
            if m.empty:
                st.caption("Sem jogos terminados.")
            else:
                icon = {"bem calibrado": "✅", "confiança a mais": "⬇️", "confiança a menos": "⬆️", "poucos dados": "⏳"}
                st.markdown(html_table([{"Mercado": r.mercado, "Acerto": f"{r.acerto:.0%}",
                                         "Esperado": f"{r.esperado:.0%}", "Leitura": f"{icon[r.leitura]} {r.leitura}"}
                                        for r in m.itertuples()], ("Acerto", "Esperado")), unsafe_allow_html=True)

    st.markdown("#### ❌ Jogos em que falhámos mais")
    if done.empty:
        st.caption("Sem jogos terminados.")
    else:
        ev = evaluate(done)
        miss = ev.groupby("match_id")["acertou"].agg(falhas=lambda s: int((~s).sum()), total="size")
        worst = miss[miss["falhas"] >= 3].sort_values("falhas", ascending=False).head(8)
        if worst.empty:
            st.caption("Nenhum jogo com 3 ou mais mercados falhados. 👌")
        cols = st.columns(2)
        for i, (mid, w) in enumerate(worst.iterrows()):
            r = done[done["match_id"] == mid].iloc[0]
            why = "".join(f"<li>{E(x)}</li>" for x in explain(r)) or "<li>Sem explicação automática.</li>"
            with cols[i % 2].container(border=True):
                st.markdown(f"<span class='muted'>{r['icon']} {E(r['comp_name'])} · {day_label(r['day'])} · "
                            f"falhámos {w['falhas']}/{w['total']}</span><div class='teams'>{E(r['home'])} "
                            f"{int(r['hg'])}-{int(r['ag'])} {E(r['away'])}</div><ul style='margin:.3rem 0 0 1rem;"
                            f"font-size:.85rem'>{why}</ul>", unsafe_allow_html=True)

    files = sorted((config.DATA_DIR / "equipas").glob("*.md"))
    st.markdown("#### 📒 Fichas das equipas")
    if not files:
        st.caption("O agente cria uma ficha por equipa à medida que analisa os jogos.")
    else:
        f = st.selectbox("Equipa", files, format_func=lambda p: p.stem)
        with st.container(border=True):
            st.markdown(f.read_text(encoding="utf-8"))


# ------------------------------------------------------------------ página: estado

def run_and_log(fn):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        fn()
    return buf.getvalue()


def page_estado():
    st.title("Estado")
    df = load()
    q = apif.quota_status()
    k = st.columns(4)
    with k[0].container(border=True):
        st.metric("Previsões guardadas", len(df))
    with k[1].container(border=True):
        st.metric("Com resultado", int(df["hg"].notna().sum()) if not df.empty else 0)
    with k[2].container(border=True):
        last = pd.to_datetime(df["updated_at"]).max() if not df.empty else None
        st.metric("Última atualização", f"{last:%d/%m %H:%M}" if last is not None else "—")
    with k[3].container(border=True):
        st.metric("API-Football", "Em pausa" if q.get("plan_blocked") else ("Ativa" if apif.enabled() else "Sem chave"),
                  help="O plano grátis não dá acesso à época atual; o ESPN e as notícias substituem-na.")

    from agente import nuvem
    if nuvem.ativo():
        st.markdown("#### Atualizações automáticas (nuvem)")
        st.caption("Resultados de 30 em 30 min e previsões às 10h30 e 17h30 (GitHub Actions); notícias e ajustes "
                   "às 9h e recap às 23h50 (rotinas do agente). A dashboard vai buscar os dados novos sozinha. "
                   f"Versão dos dados: {nuvem.SHA_FILE.read_text()[:7] if nuvem.SHA_FILE.exists() else '—'}")
        if st.session_state.get("sync_erro"):
            st.error(f"Última sincronização falhou: {st.session_state['sync_erro']}")
    b1 = b2 = None
    if not nuvem.ativo():
        st.markdown("#### Atualizar agora")
        st.caption("O agente já faz isto sozinho às 10h. Usa estes botões só se quiseres dados mais recentes.")
        b1, b2 = st.columns(2)
    if b1 and b1.button("🔄 Atualizar previsões", width="stretch", type="primary"):
        from agente import pipeline
        with st.status("A atualizar previsões (cerca de 1 minuto)…", expanded=True) as s:
            log = run_and_log(pipeline.predict)
            st.code(log[-2500:])
            s.update(label="Previsões atualizadas", state="complete")
        _load_db.clear()
    if b2 and b2.button("📥 Atualizar resultados e recaps", width="stretch"):
        from agente import pipeline, recap
        with st.status("A recolher resultados…", expanded=True) as s:
            n = pipeline.update_results()
            for d in (dt.date.today() - dt.timedelta(days=7), dt.date.today()):
                recap.build_recap(d)
            s.update(label=f"{n} resultados atualizados", state="complete")
        _load_db.clear()

    st.markdown("#### Fontes de dados")
    st.markdown(html_table([
        {"Fonte": "football-data.co.uk", "Para quê": "histórico das ligas, xG, odds", "Estado": "✅ ativa (grátis)"},
        {"Fonte": "ESPN", "Para quê": "jogos, resultados, cantos e odds de todas as provas", "Estado": "✅ ativa (grátis)"},
        {"Fonte": "Notícias (Record, A Bola, BBC, Kicker…)", "Para quê": "lesões, castigos, instabilidade",
         "Estado": "✅ pesquisadas pelo agente às 10h"},
        {"Fonte": "API-Football", "Para quê": "lesões e odds automáticas",
         "Estado": "⏸️ plano grátis sem época atual" if q.get("plan_blocked") else ("✅" if apif.enabled() else "—")},
    ]), unsafe_allow_html=True)

    st.markdown("#### Ajustes ativos do agente")
    if config.ADJUSTMENTS_PATH.exists():
        adj = json.loads(config.ADJUSTMENTS_PATH.read_text(encoding="utf-8"))
        rows = [{"Equipa": t, "Golos marcados": f"{a.get('golos_marcados', 0):+d}%",
                 "Golos sofridos": f"{a.get('golos_sofridos', 0):+d}%", "Ausentes": len(a.get("ausentes", [])),
                 "Motivo": a.get("motivo", ""), "Válido até": a.get("valido_ate", "")}
                for t, a in adj.get("equipas", {}).items()]
        if rows:
            st.dataframe(pd.DataFrame(rows), hide_index=True, width="stretch")
            st.caption(f"Atualizado em {adj.get('atualizado_em', '—')}")
        else:
            st.caption("Sem ajustes.")
    else:
        st.caption("Sem ajustes.")


# ------------------------------------------------------------------ palavra-passe (opcional)

def require_password():
    """Se DASHBOARD_PASSWORD estiver definida no .env, pede-a a quem abre a dashboard (útil no telemóvel/rede)."""
    import hmac
    import os
    pwd = os.getenv("DASHBOARD_PASSWORD", "").strip()
    if not pwd and config.AGENTE_REPO and not config.ROOT.drive:  # na internet (Linux) é obrigatória
        st.error("Falta definir DASHBOARD_PASSWORD nos Secrets da app.")
        st.stop()
    if not pwd or st.session_state.get("auth_ok"):
        return
    st.markdown("<div style='max-width:360px;margin:12vh auto 0'>", unsafe_allow_html=True)
    st.title("Agente Bets")
    typed = st.text_input("Palavra-passe", type="password")
    if typed and hmac.compare_digest(typed, pwd):
        st.session_state["auth_ok"] = True
        st.rerun()
    elif typed:
        st.error("Palavra-passe errada.")
    st.stop()


require_password()

# ------------------------------------------------------------------ resultados automáticos

@st.fragment(run_every="5m")
def auto_results():
    """De 5 em 5 minutos (com a dashboard aberta) vai buscar o resultado dos jogos previstos que acabaram;
    atualiza o Desempenho e o recap da semana. Em modo nuvem só descarrega os dados que o GitHub Actions
    e o agente já atualizaram."""
    from agente import nuvem, pipeline
    try:
        new = nuvem.sincronizar() if nuvem.ativo() else pipeline.quick_results()
    except Exception as e:  # sem internet, ESPN/GitHub em baixo… tenta outra vez daqui a 5 minutos
        print(f"[auto_results] {e}")
        st.session_state["sync_erro"] = nuvem.explicar(e) if nuvem.ativo() else str(e)
        return
    st.session_state.pop("sync_erro", None)
    if new:
        _load_db.clear()
        st.toast("Dados atualizados" if new is True else
                 f"{len(new)} jogo(s) terminado(s) — Desempenho e Recap atualizados", icon="✅")
        if not st.session_state.get("_full_run"):  # só no temporizador; numa execução normal a página já lê os dados novos
            st.rerun(scope="app")

# ------------------------------------------------------------------ navegação

pg = st.navigation([
    st.Page(page_jogos, title="Jogos", icon=":material/sports_soccer:", url_path="jogos", default=True),
    st.Page(page_bilhete, title="Construtor de apostas", icon=":material/receipt_long:", url_path="bilhete"),
    st.Page(page_recaps, title="Recaps", icon=":material/fact_check:", url_path="recaps"),
    st.Page(page_desempenho, title="Desempenho", icon=":material/monitoring:", url_path="desempenho"),
    st.Page(page_licoes, title="Lições", icon=":material/school:", url_path="licoes"),
    st.Page(page_estado, title="Estado", icon=":material/settings:", url_path="estado"),
], position="top")
st.session_state["_full_run"] = True
auto_results()
pg.run()
st.session_state["_full_run"] = False
