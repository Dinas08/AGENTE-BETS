# Agente Bets — instruções para o agente (Claude)

Projeto de previsões de futebol (Liga Portugal, Premier League, Bundesliga, Serie A, taças nacionais e
provas europeias). A parte estatística é Python; **tu és a parte qualitativa**: notícias, lesões,
instabilidade dos clubes e a análise pós-jornada. Escreve sempre em português de Portugal.

Python: `.venv\Scripts\python.exe` (Windows). Define `$env:PYTHONIOENCODING="utf-8"` antes de correr.

## Comandos
- `run.py tudo` — resultados + previsões novas (usa football-data.co.uk e API-Football se houver chave em `.env`)
- `run.py prever` — só previsões (volta a aplicar `dados/ajustes.json`)
- `run.py resultados` — resultados + gera/atualiza `dados/recaps/AAAA-Sxx.md`
- `run.py lista [dias]` — resumo dos próximos jogos (probabilidades, forma, lesões, ajustes ativos)
- `run.py estado` — quota da API e contagens
- `run.py aprendizagem` — correções automáticas por equipa (aprendidas com os erros) e calibração por mercado

## Na nuvem (rotinas do Claude na nuvem)
O sistema corre sem o PC: o GitHub Actions trata dos dados (`resultados.yml` de 30 em 30 min, `previsoes.yml`
às 10h30 e 17h30 corre `run.py tudo`) e a dashboard está no Streamlit Cloud. Os dados (`agente.db`, `ajustes.json`,
`licoes.md`, `equipas/`, `recaps/`) **não estão no ramo principal**: estão no ramo `claude/dados`.
Se estiveres numa sessão na nuvem (não existe a pasta `.venv`), antes de tudo:
```bash
git fetch origin claude/dados && git worktree add --detach dados FETCH_HEAD
pip install -q -r requirements-core.txt
```
- Usa `python` em vez de `.venv\Scripts\python.exe`. **Não corras `tudo`, `prever` nem `resultados`** (a rede da
  nuvem pode bloquear as fontes e quem escreve a base de dados é o GitHub Actions). Podes correr `run.py lista 4`
  e `run.py aprendizagem` (só leem). Os teus ajustes entram nas previsões às 10h30/17h30.
- Edita só ficheiros de texto em `dados/` (ajustes.json, licoes.md, equipas/*.md, a secção de análise dos recaps).
- No fim, guarda e envia: `bash scripts/guardar_dados.sh "rotina 1" theirs` (ou "rotina 2"). Não faças commits
  no ramo principal nem abras PRs.

## Memória (aprender com os erros)
- `dados/licoes.md` — padrões gerais aprendidos. **Lê sempre antes de ajustar** e atualiza depois de cada recap.
- `dados/equipas/<Equipa>.md` — uma ficha por equipa (nome igual ao do `run.py lista`): estado atual, estilo e
  tendências (casa/fora, golos, cantos, cartões), e "Erros do modelo com esta equipa". **Lê a ficha de cada
  equipa que joga** antes de a ajustar; cria a ficha se não existir.
- O Python já corrige sozinho o ataque/defesa de cada equipa com base nos erros anteriores (`run.py aprendizagem`,
  máx. ±12%, só com 2+ jogos). Não dupliques essas correções em `ajustes.json`: os teus ajustes são para o que
  os números não sabem (lesões, crise, rotação, motivação, padrões qualitativos das fichas e lições).

Jogos, odds e resultados de taças e provas europeias vêm do ESPN (grátis). A API-Football grátis não dá
acesso à época atual, por isso as **lesões não vêm automaticamente: tens de as pesquisar tu** (passo 2).
A API-Football grátis tem 100 pedidos/dia. **Nunca** corras `prever`/`tudo` em ciclo; no máximo 2-3 vezes por dia.

## Rotina 1 — Pré-jornada (notícias e ajustes)
1. `run.py tudo`, depois `run.py lista 4` e `run.py aprendizagem`. Lê `dados/licoes.md` e as fichas
   `dados/equipas/*.md` das equipas que jogam nos próximos 4 dias.
2. Para cada equipa com jogo nos próximos 4 dias, pesquisa na web notícias recentes (últimos 7 dias):
   lesões e castigos de titulares, onze provável, rotação (jogo europeu/taça perto), troca de treinador,
   crise interna (salários em atraso, conflitos, direção, adeptos), motivação (já qualificado/despromovido).
   Prioriza jogos das ligas principais e jogos europeus. Fontes por liga:
   - Liga Portugal: Record, A Bola, O Jogo, Maisfutebol (pesquisa "boletim clínico <clube>", "convocados <clube>",
     "castigados jornada"); conferências de imprensa de lançamento do jogo.
   - Premier League: BBC Sport, Sky Sports ("team news"), The Guardian, Premier Injuries.
   - Bundesliga: Kicker, Sport1, Bundesliga.com ("Verletzte", "Ausfälle").
   - Serie A: Gazzetta dello Sport, Corriere dello Sport, Sky Sport Italia ("infortunati", "probabili formazioni").
   - Provas europeias: as mesmas, mais UEFA.com.
   Para poupar pesquisas, procura primeiro resumos por jornada ("lesionados e castigados jornada X Liga Portugal",
   "Premier League injury news gameweek X") e depois só os clubes que faltarem.
   Regista **todos** os ausentes relevantes em `ausentes` (mesmo sem efeito nos golos), com a fonte.
3. Atualiza `dados/ajustes.json` (formato abaixo). Regras para quantificar (percentagens sobre os golos):
   - Ponta de lança/goleador titular fora: `golos_marcados` −5 a −10
   - 3+ titulares fora: `golos_marcados` −8 a −15 e/ou `golos_sofridos` +5 a +10
   - Guarda-redes ou central titular fora: `golos_sofridos` +4 a +8
   - Crise interna forte / treinador em risco: −3 a −8 marcados, +3 a +8 sofridos
   - Treinador novo (1.º-3.º jogo): efeito incerto, no máximo ±4
   - Rotação provável (jogo grande 3 dias depois, taça contra equipa inferior): −5 a −15 marcados
   - Limite: ±20 por equipa. As odds das casas já incluem a informação pública conhecida
     (os golos esperados são 30% modelo + 70% mercado quando há odds), por isso ajusta com moderação;
     o teu valor está nas notícias de última hora e na instabilidade que o mercado ainda não refletiu.
     Em taças e jogos europeus sem odds o modelo está sozinho: aí os teus ajustes pesam mais.
   - Remove entradas cujo `valido_ate` já passou.
4. Corre `run.py prever` para aplicar os ajustes e confirma com `run.py lista 4`.
5. Termina com um resumo curto: jogos com ajustes, e as 3-5 previsões mais fortes da jornada.

### Formato de `dados/ajustes.json`
```json
{
  "atualizado_em": "2026-10-30",
  "equipas": {
    "Benfica": {"golos_marcados": -8, "golos_sofridos": 0, "motivo": "Pavlidis lesionado (3 semanas)",
                "ausentes": [{"jogador": "Pavlidis", "motivo": "lesão muscular", "importancia": "titular"},
                             {"jogador": "Otamendi", "motivo": "castigo (5 amarelos)", "importancia": "titular"}],
                "fontes": ["https://..."], "valido_ate": "2026-11-15"}
  },
  "jogos": {
    "20261101-P1-porto-sporting": {"golos_casa": 0, "golos_fora": -5, "nota": "Clássico: jogo tático"}
  }
}
```
`importancia`: "titular", "rotação" ou "suplente". Os ausentes aparecem na dashboard em cada jogo.
Os nomes das equipas devem ser os do football-data.co.uk (os que aparecem em `run.py lista`, por exemplo
"Sp Lisbon", "Sp Braga", "Man United", "Bayern Munich", "Ein Frankfurt"). As chaves de `jogos` são os ids entre `[...]` no `lista`.

## Rotina 2 — Recap e aprendizagem (todas as noites)
1. `run.py resultados` (gera `dados/recaps/AAAA-Sxx.md` com acertos, falhas e explicações automáticas
   baseadas no xG, nas expulsões e nas probabilidades). Depois `run.py aprendizagem`.
2. Abre o recap da semana atual (e o da anterior, se ainda tiver jogos sem análise). Na secção
   `## Análise do agente`, substitui o comentário `<!-- AGENTE: ... -->` — ou **acrescenta** aos jogos novos
   desde a última análise, sem apagar o que já lá está — uma análise com:
   - **Balanço**: taxa de acerto por mercado e se o modelo esteve bem calibrado.
   - **O que acertámos**: 3-5 destaques e porquê (o modelo leu bem o quê?).
   - **O que falhámos e porquê**: para cada falha importante, pesquisa o resumo do jogo (expulsões,
     penáltis, lesões durante o jogo, onze inesperado, golos tardios) e diz se foi azar (o xG dava
     razão ao modelo) ou erro de leitura (o modelo ou os ajustes estavam errados).
   - **Lições**: padrões (ex.: "sobrestimamos equipas da casa na Liga Portugal", "ajustes de crise
     exagerados") e o que mudas nos ajustes da próxima jornada.
3. **Aprende com cada jogo falhado** (sobretudo os que falharam 3+ mercados):
   - Atualiza a ficha `dados/equipas/<Equipa>.md` das duas equipas: o que aconteceu, porquê (azar vs erro de
     leitura) e a tendência que isso revela (ex.: "em casa contra equipas de baixo fecha-se: poucos golos").
   - Se o mesmo tipo de erro aparecer em 2+ jogos, escreve/atualiza uma lição em `dados/licoes.md`
     ("Em observação" com 1 ocorrência; "Ativas" a partir de 2, com o que fazer de diferente).
   - Se uma lição deixou de se confirmar em 3+ jogos, apaga-a. Mantém o ficheiro curto e útil.
4. Se encontrares um padrão do próprio modelo (não de uma equipa) que se repete há 3+ semanas, regista-o em
   `dados/notas_modelo.md` e propõe a mudança ao utilizador (não alteres o código sozinho).

## Regras
- Isto é análise estatística, não aconselhamento financeiro. Nunca prometas lucros.
- Não alteres o código do modelo sem o utilizador pedir; propõe primeiro.
- Não reveles nem escrevas a chave da API fora do `.env`.
