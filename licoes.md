# Lições do agente

Padrões aprendidos com os erros. O agente lê este ficheiro **antes** de cada ronda de ajustes (Rotina 1)
e atualiza-o depois de cada recap (Rotina 2). Mantém no máximo ~25 lições: junta as repetidas, apaga as que
deixaram de se confirmar. Cada lição: data, o padrão, a evidência (jogos), e o que fazer.

## Ativas

- **2026-10-31 · Equipas em zona de descida sobrevalorizadas.** Evidência (18/11: Grémio, 18.º, 0-0 em casa com Bahia a 42%, 5 mercados falhados): Gladbach (último, 47% em casa, 0-0 e 7/7 falhados) e Sunderland
  (último, 41% fora, perdeu 1-3). Confirmado a 06/11: Hamburg 3-1 Gladbach (Gladbach sem vitórias, vermelho). O que fazer: rever sempre a tabela. Se uma equipa dos 3 últimos aparecer como favorita, aplicar o ajuste de crise
  (−3 a −8 nos golos marcados e +3 a +5 nos sofridos), salvo notícias que o contrariem.
- **2026-10-31 · "Mais de 2.5" sobrestimado quando o favorito tem uma defesa sólida.** Evidência (reforçada a 05/11: quinta europeia 15/36; e a 07/11: Sporting 1-0 Moreirense a 64%, Stuttgart 1-0 Bremen a 69%): Benfica 1-0 Alverca (S45, 68% e falhou); 7 das 9 falhas de golos da S44 foram "Mais 2.5"
  que não aconteceu (e depois Como–Venezia, Frosinone–Torino e Arouca–Nacional). Quatro delas foram 2-0 do favorito (Casa Pia–Sporting, Schalke–Leipzig, Chelsea–Man United, Brentford–Forest) e as outras foram jogos táticos
  na Bundesliga (Werder–Hoffenheim, com xG total de 1.8). O que fazer: nos jogos com favorito claro e a outra equipa fraca no ataque, aplicar −3 a −5
  aos golos do outsider. Mas "Menos de 2.5" também falhou 3 vezes (Lazio, Lecce–Genoa, Braga) por vermelhos ou favoritos que marcaram 2+: não compensar demais. Não escolher "Ambas marcam" ou "Mais 2.5" como mercado principal sem confiança acima de 60%.
- **2026-11-03 · "Ambas marcam" sobrestimado na Champions/provas europeias com favorito claro.** Evidência: S45, 8 de 13 jogos europeus falharam o BTTS "Sim" a 59-70% (Galatasaray–Stuttgart, Shakhtar–Sporting, Atlético–Bayern, Barcelona–Villa, Feyenoord–Inter, LASK–Slovan, Villarreal–PSG, Atalanta–Parma); mercado total 43% contra 60% previsto. O que fazer: com favorito acima de 60%, descontar −3 a −5 nos golos do outsider e não usar "Ambas marcam" como mercado principal nem em combinadas.
- **2026-10-30 · "Não há empate" demasiado confiante em jogos equilibrados.** Evidência (12/11: Arménia 1-1 Chipre a 71%; 09/11 León–Chivas 73%): Fiorentina–Atalanta (74%) e Hull–Ipswich (72%), ambos
  empatados. O que fazer: com o favorito abaixo de 50%, evitar a dupla "12" nas combinadas.

- **2026-11-07 · Quebra de forma de grandes equipas não captada pelo modelo.** Evidência: Man City (2 derrotas seguidas, perdeu 3-1 em Forest como favorito a 53%, sem Semenyo). O que fazer: com grande equipa em 2+ derrotas seguidas ou com baixa de peso, aplicar −3 a −5 nos golos marcados e não dar mais de 50% de vitória fora.

- **2026-11-08 · MLS/Liga MX sem odds: "Mais 2.5" e BTTS demasiado generosos.** Evidência (18/11 Brasileirão: Grémio 0-0 Bahia, Coritiba 0-1 Santos, Remo 2-0 Chape com Mais 2.5 a 56-57% falhados, BTTS 2/6; 15/11: Queretaro 0-1 Monterrey 58%/60%, Chapecoense 0-2 Vasco Mais 2.5 a 62% falharam): sábado ~8/15 falhados; domingo San Diego 0-1 Sporting KC (75%/68%), Houston 0-1 St. Louis, Austin 0-2 Portland; 09/11 Liga MX: Queretaro 0-2 Puebla (Mais 2.5 e BTTS a 55%), León 1-1 Chivas (Mais 2.5 a 56%). O que fazer: sem odds nas Américas, −5 a −8 nos golos esperados dos dois lados e não usar "Mais 2.5"/BTTS como mercado principal acima de 60%.
- **2026-11-08 · Ajuste de "crise" a equipas em descida não funciona em casa.** Evidência: Sunderland 1-0 Chelsea (Chelsea 57%, desfecho a 19%), embora Sunderland perdesse 0-2 em Zagreb. O que fazer: aplicar o ajuste de crise sobretudo fora de casa; em casa contra adversário também desfalcado, ajuste ≤ metade.

- **2026-11-12 · Favoritos com 4+ baixas titulares fora de casa/na estrada sobrevalorizados.** Evidência: Fenerbahce 3-2 Liverpool (58%), Atalanta 0-3 Parma, Itália 3-1 França (França favorita a 44% com várias baixas, derrota em San Siro). O que fazer: −6 a −10 nos golos marcados e baixar o favorito para ≤45%; em seleções com jogo decisivo para o adversário, rever a motivação.
- **2026-11-12 · Seleções com favorito claro: "Mais 2.5" a 65-70% falha com 2-0.** Evidência: Chéquia 0-2 Espanha (67%), São Marino 0-2 Bielorrússia (67%). O que fazer: com favorito ≥75% e outsider fraco, não usar "Mais 2.5" como mercado principal acima de 60%; preferir 1X2/dupla.

- **2026-11-14 · Favorito já apurado/sem nada em jogo (ou em novo ciclo, com baixas) gere o jogo e perde pontos.** Evidência (3 casos na semana): Suíça 0-0 Eslovénia, Chéquia 0-2 Espanha (Mais 2.5 falhou), Portugal 1-4 Dinamarca (61%, apurada, sem 4 titulares e sem Ronaldo; xG 1.26-2.33). O que fazer: favorito já qualificado com 3+ baixas → ≤50% de vitória e −8 a −12 nos golos marcados; não usar vitória seca nem "Mais 2.5" como principal.

- **2026-11-21 · Favoritos ≥90% com 3+ baixas titulares ou rotação (taças) falham o 1X2/Mais 2.5.** Evidência: Bayern 1-1 Köln (91%, sem Neuer/Díaz/Gnabry/Davies, Kane e Olise saíram lesionados), Porto 1-1 Paredes (91%, 98% "1X", equipa B, passou nos penáltis); antes Bayern 2-2 Dortmund (65%). O que fazer: com baixas pesadas ou rotação, limitar a probabilidade do favorito a ~80% e −8 a −12 nos golos marcados; não usar 1X2 seco nem Mais 2.5 acima de 75% como dica.

## Em observação (1 ocorrência — confirmar antes de agir)

- 2026-11-21 · Treinador novo em equipa em crise (Eder Sarabia, Espanyol 1-0 Ath Bilbao a 15%): efeito treinador novo não está no modelo; dar +3 a +4 golos marcados à equipa visitante com treinador novo no 1.º jogo. 1 caso.

- 2026-11-16 · Seleções com favorito muito acima e adversário com 5+ baixas (Alemanha 5-0, Suíça 4-0): BTTS Sim (57-67%) falhou nos dois; descontar BTTS nesses casos. Em casa, o favorito desfalcado do outro lado gere bem (nuance da lição de favoritos sem nada em jogo). 2 casos.
- 2026-11-16 · Eslováquia (e Malta) fora de casa: empate 2-2 e 1-1 com outsiders (Faroé, Cazaquistão, Gibraltar); descontar ~5 pts na vitória visitante de favoritos modestos em seleções.
- 2026-11-15 · Cantos nas seleções: semana 46% contra 56% (calibração geral 49% contra 56%): descontar confiança acima de 65%; propor revisão da calibração a Dinis.
- 2026-11-15 · Seleções de topo em jogos decisivos pelo 1.º lugar superam o modelo (Inglaterra 3-2 Espanha a 24%): 1 caso. Albânia subestimada (2-0 Finlândia, 2-0 Bielorrússia).

- 2026-11-05 · Previsões "com dados limitados" (equipas sem histórico) dão 77-89% ao favorito e falharam várias vezes (Milan–Ferencvaros 77%, Hajduk 89%, Atalanta–Kairat 86%, Sunderland–Zagreb 70%, Sturm Graz 63%). Sem odds, tratar favoritos acima de 75% como ≤70% e evitar "X ou 2" como mercado principal nesses jogos. "Mais 2.5" na Liga Europa/Conferência: 15/36 (42%) na quinta da S45.

- 2026-11-04 · Cantos europeus na S45: 46% contra 58% previsto (ruído nos dois sentidos, jogos 7-10 cantos). Descontar confiança acima de 70%.
- 2026-11-03 · Cantos "Mais de 9.5" a 80%+ demasiado confiante (Shakhtar–Sporting 83%, caiu com 9 cantos). Observar.

- 2026-11-13 · Seleções: favorito que só precisa do empate/já apurado (Suíça 0-0 Eslovénia, Espanha 2-0 Chéquia) gere o jogo: baixar Mais 2.5 e vitória seca; e outsiders fracos marcam de penálti (Faroé 2-2 Eslováquia, 21%). 2 casos na semana, a confirmar.
- Favoritos fora de casa entre 40% e 50%: parecia falhar muito (2/7), mas com a semana completa foi 5/10, em linha com as probabilidades. Sem ajuste. Se nas próximas semanas ficar abaixo de 40%, reativar (procurar sinais de força da casa; preferir "X2" à vitória seca).
- Jogos com muitas baixas dos dois lados (Union–Köln 1-1): o "Mais 2.5" fica generoso; observar mais um caso.

- Jogos com expulsão cedo (Elversberg 4-1 Mainz, Chelsea 2-0 Man United) estragam as previsões de golos e
  cantos; não é erro de leitura. Não corrigir equipas por isto. Confirmar sempre o minuto do vermelho: em Coventry–Sunderland foi aos 90+9'
  e não mudou nada.
- Favoritos muito altos com 3+ baixas titulares (Bayern 65% empatou 2-2 com Dortmund, sem Díaz, Musiala e outros). Confirmar com mais um caso antes de agir.
- Liga Portugal: "Mais de 4.5 cartões" falhou em Casa Pia–Sporting e Moreirense–Estrela (a 55%). Observar.
- Enfermaria cheia (8+ ausentes, incluindo GR): Atalanta 0-3 Parma (1.8-0.9 previsto, dava 18% ao desfecho). O ajuste de sofridos pode ser curto; se houver mais um caso, usar +8 a +10 em sofridos.
- 2026-11-06 · Taças nacionais com dados limitados (Bristol Rovers 2-0 Cambridge, 5 mercados falhados a ~40-50%): sem viés claro, 1 ocorrência.
- Gil Vicente 0-0 Guimarães e Newcastle 0-1 Everton: azar/vermelho, sem lição.
- 2026-11-08 · domingo: "Não há empate" falhou 6 vezes (Napoli–Lazio, Twente–Ajax, United–Villa, Fiorentina–Juve; 09/11 León 1-1 Chivas a 73%): já coberto pela lição ativa. Domínio de cantos sem golos (Brugge 9-1, Brest–Lyon 1-8) é variância.
- 2026-11-07 · FA Cup (e 08/11: Oldham 2-1 Sheff. Wed.): favoritos de divisão acima falharam (Huddersfield 69% perdeu com Exeter; Fleetwood 56%) além de Bristol Rovers–Cambridge. Observar; descontar 5-8 pts nos favoritos de taças inglesas com dados limitados.

- 2026-11-14 · Outsider da casa em risco de despromoção bate favorito fora (Roménia 2-1 Polónia a 56%, Moldávia 2-1 Cazaquistão a 36% de visitante). 2 casos: motivação não está no modelo; com 3.º caso passa a Ativa (dar +3 a +5 golos marcados ao outsider da casa em jogo decisivo).
- 2026-11-14 · Brasileirão/Liga MX sem odds: 0-0 a mais (Mirassol–Atlético-MG, Queretaro/León), já coberto pela lição das Américas.

- 2026-11-17 · Seleções: favorito a 47-50% com 2+ defesas fora ou já promovido empata (Israel 1-1 Áustria, Hungria 1-1 NI, Polónia 1-1 Suécia a 40%). 3 casos na semana: preferir "X ou 1/2" ao 1X2 seco e rotação do promovido ≤ −10. A confirmar com mais casos.
