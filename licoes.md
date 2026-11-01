# Lições do agente

Padrões aprendidos com os erros. O agente lê este ficheiro **antes** de cada ronda de ajustes (Rotina 1)
e atualiza-o depois de cada recap (Rotina 2). Mantém no máximo ~25 lições: junta as repetidas, apaga as que
deixaram de se confirmar. Cada lição: data, o padrão, a evidência (jogos), e o que fazer.

## Ativas

- **2026-10-31 · Equipas em zona de descida sobrevalorizadas.** Evidência: Gladbach (último, 47% em casa, 0-0 e 7/7 falhados) e Sunderland
  (último, 41% fora, perdeu 1-3). O que fazer: rever sempre a tabela. Se uma equipa dos 3 últimos aparecer como favorita, aplicar o ajuste de crise
  (−3 a −8 nos golos marcados e +3 a +5 nos sofridos), salvo notícias que o contrariem.
- **2026-10-31 · "Mais de 2.5" sobrestimado quando o favorito tem uma defesa sólida.** Evidência: 7 das 9 falhas de golos da S44 foram "Mais 2.5"
  que não aconteceu (e depois Como–Venezia, Frosinone–Torino e Arouca–Nacional). Quatro delas foram 2-0 do favorito (Casa Pia–Sporting, Schalke–Leipzig, Chelsea–Man United, Brentford–Forest) e as outras foram jogos táticos
  na Bundesliga (Werder–Hoffenheim, com xG total de 1.8). O que fazer: nos jogos com favorito claro e a outra equipa fraca no ataque, aplicar −3 a −5
  aos golos do outsider. Mas "Menos de 2.5" também falhou 3 vezes (Lazio, Lecce–Genoa, Braga) por vermelhos ou favoritos que marcaram 2+: não compensar demais. Não escolher "Ambas marcam" ou "Mais 2.5" como mercado principal sem confiança acima de 60%.
- **2026-10-30 · "Não há empate" demasiado confiante em jogos equilibrados.** Evidência: Fiorentina–Atalanta (74%) e Hull–Ipswich (72%), ambos
  empatados. O que fazer: com o favorito abaixo de 50%, evitar a dupla "12" nas combinadas.

## Em observação (1 ocorrência — confirmar antes de agir)

- Favoritos fora de casa entre 40% e 50%: parecia falhar muito (2/7), mas com a semana completa foi 5/10, em linha com as probabilidades. Sem ajuste. Se nas próximas semanas ficar abaixo de 40%, reativar (procurar sinais de força da casa; preferir "X2" à vitória seca).
- Jogos com muitas baixas dos dois lados (Union–Köln 1-1): o "Mais 2.5" fica generoso; observar mais um caso.

- Jogos com expulsão cedo (Elversberg 4-1 Mainz, Chelsea 2-0 Man United) estragam as previsões de golos e
  cantos; não é erro de leitura. Não corrigir equipas por isto. Confirmar sempre o minuto do vermelho: em Coventry–Sunderland foi aos 90+9'
  e não mudou nada.
- Cartões: "Menos de 4.5" falhou em 6 jogos da S44 mas a semana acabou calibrada (66% real contra 66%); desconfirmado, apagar se se mantiver na S45. Se se repetir mais 2 semanas, passa para
  `notas_modelo.md` como padrão do modelo.
- Quebra de forma de grandes equipas (Man City, 2 derrotas seguidas) não é captada pelo modelo. Se houver mais casos, ajustar −3 a −5 nos golos marcados.
- Favoritos muito altos com 3+ baixas titulares (Bayern 65% empatou 2-2 com Dortmund, sem Díaz, Musiala e outros). Confirmar com mais um caso antes de agir.
- Liga Portugal: "Mais de 4.5 cartões" falhou em Casa Pia–Sporting e Moreirense–Estrela (a 55%). Observar.
