# ⚽ Agente Bets

Previsões para a Liga Portugal, Premier League, Bundesliga e Serie A, taças nacionais e provas europeias:
1X2, dupla hipótese, golos (+/-), ambas marcam, resultado exato, cantos, cartões e combinadas, com
odds justas e odds das casas. Um agente (Claude) junta notícias, lesões e instabilidade dos clubes e
escreve um recap depois de cada jornada.

## Como usar
| Ação | Como |
|---|---|
| Abrir a dashboard | duplo clique em **Abrir dashboard.bat** (abre em http://127.0.0.1:8501). Enquanto estiver aberta, verifica de 5 em 5 minutos se algum jogo previsto acabou e atualiza o Desempenho e o Recap sozinha |
| Atualizar previsões e resultados | duplo clique em **Atualizar previsoes.bat** |
| Resultados em segundo plano | tarefa do Windows **"Agente Bets - resultados"** (Agendador de Tarefas), de 30 em 30 min, mesmo com a dashboard fechada; registo em `dados/auto.log`. Para desligar: Agendador de Tarefas → clicar com o botão direito → Desativar |
| Notícias, ajustes e recap com o agente | numa sessão do Claude nesta pasta: "faz a rotina 1" / "faz a rotina 2" (ver `CLAUDE.md`) |

## Abrir no telemóvel / tablet / outro PC
1. **Na mesma rede Wi-Fi de casa:** com a dashboard aberta no PC, abre no outro dispositivo
   `http://192.168.1.202:8501` (ou `http://192.168.1.220:8501`). Na primeira vez, o Windows tem de deixar
   passar a ligação: em Definições → Rede e Internet, marca a rede como **Privada**, e, se aparecer o aviso
   da Firewall para o Python, escolhe **Permitir** (só em redes privadas).
2. **Fora de casa:** instala o **Tailscale** (grátis) no PC e no telemóvel, com a mesma conta; depois abre
   `http://<nome-do-pc>:8501` no telemóvel. Funciona em qualquer rede, sem abrir portas na internet.
3. Recomendado: define `DASHBOARD_PASSWORD=` no ficheiro `.env` para a dashboard pedir palavra-passe.
O PC tem de estar ligado e a dashboard aberta (janela preta).

## Aprendizagem
- Todas as noites o agente analisa os jogos falhados, atualiza o recap, as fichas das equipas
  (`dados/equipas/`) e as lições (`dados/licoes.md`), que lê antes de cada ronda de previsões.
- O Python corrige sozinho o ataque/defesa das equipas em que errou sistematicamente (2+ jogos, máx. ±12%).
- Tudo visível na página **Lições** da dashboard.

## Fontes de dados (todas grátis)
- **football-data.co.uk**: histórico das ligas (golos, xG, remates, cantos, cartões, odds) para treinar o modelo.
- **ESPN**: jogos, resultados, cantos, cartões e odds de todas as provas: 4 ligas, Taça de Portugal, FA Cup,
  Carabao Cup, DFB-Pokal, Coppa Italia, Champions, Liga Europa e Conferência. Não tem a Taça da Liga.
- **Lesões e instabilidade**: o agente pesquisa-as nas notícias.
- **API-Football**: a chave está no `.env`, mas o plano grátis só dá acesso às épocas 2022–2024. O programa
  deteta isso e gasta só 1 pedido por dia. Num plano pago, as lesões e as odds extra passam a ser usadas
  automaticamente.

## Como funciona
1. **Dados**: football-data.co.uk (histórico desde 2024/25 com golos, xG, remates, cantos, cartões e odds) +
   API-Football (jogos de taças/Europa, lesões, odds extra).
2. **Modelo** (`agente/model.py`): força de ataque/defesa de cada equipa (Poisson Dixon-Coles, jogos recentes
   pesam mais), um modelo igual para cantos e outro para cartões, e uma força relativa entre ligas para os
   jogos europeus. Daí sai a matriz de resultados e, a partir dela, todos os mercados e combinadas.
3. **Mistura com o mercado**: quando há odds, os golos esperados são 30% modelo + 70% casas de apostas
   (foi o que melhor previu no backtest).
4. **Agente**: ajusta os golos esperados por equipa com base nas notícias (`dados/ajustes.json`).
5. **Recap**: `run.py resultados` avalia cada previsão. Explica as falhas com o xG, as expulsões e as
   surpresas, e o agente acrescenta a análise.

## Backtest 2025/26 (1270 jogos, sem olhar para o futuro)
| Mercado | Acerto | Prob. média prevista |
|---|---|---|
| Dupla hipótese | 80.6% | 78.6% |
| Cartões +/-4.5 | 63.7% | 63.7% |
| Golos +/-2.5 | 57.5% | 57.5% |
| Combinada (odd justa ≥ 1.60) | 56.4% | 56.7% |
| Cantos +/-9.5 | 56.2% | 58.6% |
| Ambas marcam | 55.6% | 55.8% |
| Resultado 1X2 | 53.5% | 51.8% |

As probabilidades estão bem calibradas: quando o agente diz 57%, acontece cerca de 57% das vezes. No
1X2 o agente iguala o mercado; as "apostas de valor" puramente estatísticas deram ROI −5%. A vantagem
real, se existir, tem de vir das notícias de última hora e de mercados menos eficientes. Por isso
acompanha o separador 📈 Desempenho antes de pagar pela API ou de apostar dinheiro.

> Isto é uma ferramenta de análise estatística, não aconselhamento financeiro. Aposta só o que podes perder.
