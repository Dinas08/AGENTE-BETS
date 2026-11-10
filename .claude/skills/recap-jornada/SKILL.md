---
name: recap-jornada
description: Corre a Rotina 2 do Agente Bets — recolhe resultados, escreve a análise do agente no recap da semana (acertos, falhas, azar vs erro de leitura), atualiza as fichas das equipas e as lições. Usar quando o utilizador pede "faz o recap", "rotina 2", "como correram as previsões", "aprende com os erros de ontem", ou escreve /recap-jornada.
---

# Recap e aprendizagem (Rotina 2)

O procedimento completo está no `CLAUDE.md`, secção **"Rotina 2 — Recap e aprendizagem"**. Lê-a e segue-a à
letra; esta skill acrescenta o controlo do progresso e critérios para não perder aprendizagem.

## Antes de começar
- Na nuvem (sem `.venv`): faz a preparação da secção "Na nuvem" e **não** corras `run.py resultados`.
- Lê também `dados/relatorio_falhas.md` e `dados/licoes.md` antes de escrever.

## Controlo do progresso
Faz uma lista de tarefas com **um item por jogo falhado** desde a última análise (primeiro os que falharam 3+
mercados). Para cada um, só marca como feito depois de:
1. pesquisar o resumo do jogo (expulsões e minuto, penáltis, lesões durante o jogo, onze inesperado, golos tardios);
2. classificar: **azar** (o xG dava razão ao modelo) ou **erro de leitura** (modelo ou ajustes errados);
3. atualizar as fichas `dados/equipas/<Equipa>.md` das duas equipas (cria-as se não existirem, com as secções
   "Estado atual", "Tendências observadas" e "Erros do modelo com esta equipa").

## Lições
- Mesmo tipo de erro em 2+ jogos → lição em "Ativas" com evidência e o que fazer.
- 1 ocorrência → "Em observação".
- Lição desmentida em 3+ jogos → apaga. Máximo ~25 lições.
- Padrão do próprio modelo há 3+ semanas → `dados/notas_modelo.md` e propõe a mudança ao utilizador
  (nunca alteres o código sozinho).

## No recap
Acrescenta na secção `## Análise do agente`, sem apagar análises anteriores: Balanço, O que acertámos, O que
falhámos e porquê, Lições (e se algum grupo de dicas do Telegram está abaixo do esperado).

## Resumo final ao utilizador
```
**Recap <semana>** · acerto <x>% (<mercado>: x%, ...)
- Melhor leitura: ...
- Falhas: <n> azar / <n> erro de leitura
- Fichas atualizadas: ...
- Lições novas/alteradas/apagadas: ...
```
Na nuvem, termina com `bash scripts/guardar_dados.sh "rotina 2" theirs`.
