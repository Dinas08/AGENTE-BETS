---
name: analisar-jogo
description: Análise rápida de um ou mais jogos de futebol do Agente Bets — junta as probabilidades do modelo, a ficha das equipas, as lições e as notícias de última hora (lesões, castigos, rotação, crise) numa leitura curta, e propõe um ajuste para dados/ajustes.json. Usar quando o utilizador pergunta por um jogo concreto ("o que achas do Benfica–Porto?", "analisa o jogo do Arsenal", "vale a pena o over no Sporting?"), por uma equipa que joga em breve, ou escreve /analisar-jogo.
---

# Analisar jogo

Análise de um jogo à escolha, fora das rotinas. Escreve em português de Portugal. As regras gerais, os nomes das
equipas e o formato de `ajustes.json` estão no `CLAUDE.md` do projeto — segue-os.

Python: `.venv\Scripts\python.exe` com `$env:PYTHONIOENCODING="utf-8"` (na nuvem, `python3.13`).

## Passos

1. **Encontrar o jogo.** Corre `run.py lista 7` e procura o jogo pelos nomes (o utilizador pode escrever
   "Sporting" e no `lista` aparecer "Sp Lisbon"). Se não estiver na lista, diz isso e pergunta a data ou a prova —
   não inventes probabilidades. Guarda o id entre `[...]`.
2. **Ler a memória.** `dados/licoes.md` (que lições se aplicam a este jogo?) e as fichas
   `dados/equipas/<Equipa>.md` das duas equipas, se existirem. Vê em `dados/ajustes.json` se já há ajustes ativos.
3. **Notícias.** Faz as pesquisas como manda a Rotina 1 do `CLAUDE.md`: as duas equipas e a data por extenso,
   `mode: "extended"`, fontes da liga, confirma a data de cada artigo e descarta o que tiver mais de 7 dias.
   No mínimo 2 tentativas antes de concluir que não há novidades. Procura: ausentes (lesão/castigo) e se são
   titulares, onze provável, rotação, treinador, crise, motivação.
4. **Ler o jogo.** Cruza números e notícias:
   - O que o modelo diz (1X2, golos esperados, forma) e se as odds já incluem as notícias conhecidas.
   - O que os números não sabem: notícias de última hora, padrões da ficha, lições ativas.
   - Mercados onde o modelo e a leitura qualitativa concordam (mais fortes) e onde discordam (evitar).
5. **Propor o ajuste** com as regras de quantificação do `CLAUDE.md` (limite ±20, moderação quando há odds).
   **Não escrevas em `ajustes.json` sem o utilizador dizer que sim** — mostra a entrada JSON proposta. Se
   aceitar, escreve, corre `run.py prever` e confirma com `run.py lista 7`.

## Resposta

Curta e fácil de ler no telemóvel:

```
**<Casa> vs <Fora>** · <prova> · <dia hora>
Modelo: 1 xx% · X xx% · 2 xx% · golos x.x–x.x

**Notícias** (fonte, data)
- ...

**Leitura**
- 2-4 pontos: o que pesa e porquê

**Mercados**
- Mais fortes: ...
- A evitar: ...

**Ajuste proposto** (ou "nenhum: as odds já refletem isto")
```json
...
```
```

Fecha sempre com: análise estatística, não aconselhamento financeiro. Nunca prometas lucros nem "certezas".
