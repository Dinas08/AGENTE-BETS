---
name: pre-jornada
description: Corre a Rotina 1 do Agente Bets — atualiza dados, pesquisa notícias (lesões, castigos, rotação, crise) de todos os jogos dos próximos dias, atualiza dados/ajustes.json e refaz as previsões. Usar quando o utilizador pede "prepara a jornada", "rotina 1", "atualiza os ajustes", "vê as lesões para este fim de semana", ou escreve /pre-jornada.
---

# Pré-jornada (Rotina 1)

O procedimento completo está no `CLAUDE.md`, secção **"Rotina 1 — Pré-jornada"**. Lê-a e segue-a à letra; esta
skill só acrescenta a forma de controlar o progresso e o resumo final.

## Antes de começar
- Na nuvem (sem `.venv`): faz primeiro a preparação da secção "Na nuvem" e **não** corras `tudo`/`prever`.
- Localmente: `run.py tudo` no máximo 2-3 vezes por dia (quota de 100 pedidos da API).

## Controlo do progresso
Depois do `run.py lista 4`, faz uma lista de tarefas com **um item por jogo dos próximos 2 dias** das ligas
principais e europeus (os de dia 3-4 e das Américas ficam opcionais). Marca cada jogo como feito só depois de:
- ≥1 pesquisa com a data por extenso e ≥2 tentativas se a primeira trouxe artigos antigos;
- artigos confirmados com menos de 7 dias;
- ausentes registados em `ausentes` com fonte (mesmo os que não mudam os golos).

Não termines com jogos dos próximos 2 dias por tentar.

## Antes de escrever `ajustes.json`
- Remove entradas com `valido_ate` passado.
- Não dupliques as correções automáticas (`run.py aprendizagem`) nem a calibração por mercado.
- Aplica as lições ativas de `dados/licoes.md` que se encaixem (diz quais no resumo).
- Valida o JSON antes de correr `run.py prever` (ex.: `python -c "import json;json.load(open('dados/ajustes.json',encoding='utf-8'))"`).

## Resumo final
```
**Pré-jornada <data>** · <n> jogos vistos · <n> ajustes

**Ajustes**
- <Equipa>: marcados ±x / sofridos ±y — <motivo> (fonte)

**Lições aplicadas**: ...

**Previsões mais fortes** (3-5)
- <Casa> vs <Fora> — <mercado> <prob>% — porquê

**Ficou por ver**: jogos sem notícias encontradas
```
Na nuvem, termina com `bash scripts/guardar_dados.sh "rotina 1" theirs`.
