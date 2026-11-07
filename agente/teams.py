"""Converte nomes de equipas (API-Football, notícias) para os nomes usados no football-data.co.uk."""
import difflib
import re
import unicodedata

# nome API-Football / comum -> nome football-data.co.uk
ALIASES = {
    "sporting cp": "Sp Lisbon", "sporting": "Sp Lisbon", "sporting lisbon": "Sp Lisbon",
    "sc braga": "Sp Braga", "braga": "Sp Braga", "fc porto": "Porto", "vitoria guimaraes": "Guimaraes",
    "vitoria sc": "Guimaraes", "estrela amadora": "Estrela", "estrela da amadora": "Estrela", "avs": "AVS",
    "manchester united": "Man United", "manchester city": "Man City", "nottingham forest": "Nott'm Forest",
    "wolverhampton wanderers": "Wolves", "tottenham hotspur": "Tottenham", "brighton & hove albion": "Brighton",
    "west ham united": "West Ham", "newcastle united": "Newcastle", "leeds united": "Leeds",
    "sheffield utd": "Sheffield United", "afc bournemouth": "Bournemouth",
    "bayern munchen": "Bayern Munich", "bayern munich": "Bayern Munich", "borussia dortmund": "Dortmund",
    "bayer leverkusen": "Leverkusen", "borussia monchengladbach": "M'gladbach", "eintracht frankfurt": "Ein Frankfurt",
    "1. fc koln": "FC Koln", "fc koln": "FC Koln", "fsv mainz 05": "Mainz", "1899 hoffenheim": "Hoffenheim",
    "tsg hoffenheim": "Hoffenheim", "fc st. pauli": "St Pauli", "1. fc heidenheim": "Heidenheim",
    "hamburger sv": "Hamburg", "vfl bochum": "Bochum", "1. fc union berlin": "Union Berlin",
    "ac milan": "Milan", "inter milan": "Inter", "internazionale": "Inter", "as roma": "Roma", "hellas verona": "Verona",
    "paris saint germain": "Paris SG", "psg": "Paris SG", "atletico madrid": "Ath Madrid", "athletic club": "Ath Bilbao",
    "athletic bilbao": "Ath Bilbao", "real sociedad": "Sociedad", "real betis": "Betis", "celta vigo": "Celta",
    "rayo vallecano": "Vallecano", "espanyol": "Espanol", "club brugge kv": "Club Brugge", "club brugge": "Club Brugge",
    "union st. gilloise": "St. Gilloise", "union saint-gilloise": "St. Gilloise", "olympiakos piraeus": "Olympiakos",
    "olympiacos": "Olympiakos", "olympique marseille": "Marseille", "olympique lyonnais": "Lyon",
    "stade brestois 29": "Brest", "stade rennais": "Rennes", "losc lille": "Lille", "as monaco": "Monaco",
    "ogc nice": "Nice", "rc lens": "Lens", "psv eindhoven": "PSV Eindhoven", "az alkmaar": "AZ Alkmaar",
    "fc twente": "Twente", "fc utrecht": "Utrecht", "paok": "PAOK", "aek athens": "AEK", "panathinaikos": "Panathinaikos",
    "fenerbahce": "Fenerbahce", "galatasaray": "Galatasaray", "besiktas": "Besiktas", "celtic": "Celtic", "rangers": "Rangers",
    # nomes do ESPN
    "c.d. nacional": "Nacional", "fc cologne": "FC Koln", "vitoria de guimaraes": "Guimaraes", "ajax amsterdam": "Ajax",
    "feyenoord rotterdam": "Feyenoord", "kaa gent": "Gent", "nec nijmegen": "Nijmegen", "paris saint-germain": "Paris SG",
    "union st.-gilloise": "St. Gilloise", "heart of midlothian": "Hearts", "hamburg sv": "Hamburg",
    "sporting braga": "Sp Braga", "atletico de madrid": "Ath Madrid", "internazionale milano": "Inter",
    # Américas (ESPN / API-Football -> football-data)
    "red bull bragantino": "Bragantino", "rb bragantino": "Bragantino", "vasco da gama": "Vasco",
    "flamengo": "Flamengo RJ", "botafogo": "Botafogo RJ", "atletico mineiro": "Atletico-MG",
    "atletico-mg": "Atletico-MG", "athletico paranaense": "Athletico-PR", "athletico-pr": "Athletico-PR",
    "chapecoense": "Chapecoense-SC", "vitoria": "Vitoria", "sao paulo": "Sao Paulo",
    "atletico tucuman": "Atl. Tucuman", "belgrano (cordoba)": "Belgrano", "instituto (cordoba)": "Instituto",
    "central cordoba (santiago del estero)": "Central Cordoba", "central cordoba de santiago": "Central Cordoba",
    "deportivo riestra": "Dep. Riestra", "estudiantes de la plata": "Estudiantes L.P.", "estudiantes l.p.": "Estudiantes L.P.",
    "gimnasia la plata": "Gimnasia L.P.", "gimnasia l.p.": "Gimnasia L.P.", "independiente rivadavia": "Ind. Rivadavia",
    "newell's old boys": "Newells Old Boys", "talleres": "Talleres Cordoba", "union santa fe": "Union de Santa Fe",
    "sarmiento": "Sarmiento Junin", "estudiantes de rio cuarto": "Estudiantes Rio Cuarto",
    "gimnasia mendoza": "Gimnasia Mendoza", "gimnasia y esgrima de mendoza": "Gimnasia Mendoza",
    "america": "Club America", "club america": "Club America", "atletico de san luis": "Atl. San Luis",
    "atletico san luis": "Atl. San Luis", "guadalajara": "Guadalajara Chivas", "chivas": "Guadalajara Chivas",
    "leon": "Club Leon", "pumas unam": "UNAM Pumas", "u.n.a.m. - pumas": "UNAM Pumas", "tijuana": "Club Tijuana",
    "club queretaro": "Queretaro", "fc juarez": "Juarez", "tigres": "Tigres UANL",
    "la galaxy": "Los Angeles Galaxy", "lafc": "Los Angeles FC", "red bull new york": "New York Red Bulls",
    "new york city fc": "New York City", "atlanta united": "Atlanta Utd", "atlanta united fc": "Atlanta Utd",
    "atletico paranaense": "Athletico-PR", "belgrano cordoba": "Belgrano", "instituto cordoba": "Instituto",
    "d.c. united": "DC United", "st. louis city sc": "St. Louis City", "montreal impact": "CF Montreal",
    # Bélgica, Espanha e Países Baixos (ESPN -> football-data)
    "kvc westerlo": "Westerlo", "oh leuven": "Oud-Heverlee Leuven", "racing genk": "Genk", "krc genk": "Genk",
    "royal charleroi sc": "Charleroi", "sporting charleroi": "Charleroi", "standard liege": "Standard",
    "waasland-beveren": "Beveren", "zulte-waregem": "Waregem", "kv mechelen": "Mechelen", "kv kortrijk": "Kortrijk",
    "royal antwerp": "Antwerp", "sint-truiden": "St Truiden", "stvv": "St Truiden", "cercle brugge ksv": "Cercle Brugge",
    "deportivo": "La Coruna", "deportivo la coruna": "La Coruna", "racing santander": "Santander",
    "ado den haag": "Den Haag", "pec zwolle": "Zwolle",
}

# nomes que dependem da liga (o mesmo nome é outra equipa noutra liga)
LEAGUE_ALIASES = {}

# clubes diferentes que partilham a cidade com uma equipa conhecida
NO_MATCH = {"bristol rovers", "oxford city", "sheffield wednesday", "notts county", "nottingham",
            "manchester", "inter d'escaldes", "red star belgrade", "cardiff metropolitan"}

STOPWORDS = {"fc", "cf", "ac", "sc", "afc", "sv", "fk", "sk", "cd", "ud", "rc", "ss", "ssc", "us", "as", "1.", "vfl", "vfb", "tsg"}
# sufixos que o football-data costuma omitir ("Hull City" -> "Hull", "Hertha Berlin" -> "Hertha")
SUFFIXES = {"city", "town", "united", "utd", "rovers", "county", "athletic", "wanderers", "albion", "hotspur",
            "berlin", "96", "98", "05", "04", "calcio", "1846", "1907", "1913"}


def norm(name: str) -> str:
    s = unicodedata.normalize("NFKD", str(name)).encode("ascii", "ignore").decode().lower().strip()
    return re.sub(r"\s+", " ", s)


def _core(name: str) -> str:
    return " ".join(t for t in norm(name).replace("-", " ").split() if t not in STOPWORDS)


def _short(name: str) -> str:
    return " ".join(t for t in _core(name).split() if t not in SUFFIXES)


class TeamMatcher:
    def __init__(self, known_teams):
        self.known = sorted(set(known_teams))
        self._by_norm = {norm(t): t for t in self.known}
        self._by_core = {_core(t): t for t in self.known}
        shorts: dict[str, list] = {}
        for t in self.known:
            shorts.setdefault(_short(t), []).append(t)
        self._by_short = {s: ts[0] for s, ts in shorts.items() if len(ts) == 1 and len(s) >= 4}

    def match(self, name: str, comp: str | None = None) -> str | None:
        n = norm(name)
        la = LEAGUE_ALIASES.get(comp, {})
        if n in la and la[n] in self.known:
            return la[n]
        if n in NO_MATCH:
            return None
        if n in ALIASES and ALIASES[n] in self.known:
            return ALIASES[n]
        if n in self._by_norm:
            return self._by_norm[n]
        c = _core(name)
        if c in self._by_core:
            return self._by_core[c]
        s = _short(name)
        if s in self._by_short:
            return self._by_short[s]
        hit = difflib.get_close_matches(c, list(self._by_core), n=1, cutoff=0.82)
        if hit:
            return self._by_core[hit[0]]
        hit = difflib.get_close_matches(s, list(self._by_short), n=1, cutoff=0.86)
        return self._by_short[hit[0]] if hit else None
