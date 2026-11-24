---
name: analytics-conteudo
description: Analisa o desempenho dos vídeos e memes do Agente Claudio nas redes (TikTok, Instagram, YouTube Shorts, X) e a conversão para o canal de Telegram, e ajusta a estratégia (temas, gancho, palavras, duração, hora de publicação). Usar quando o Dinis manda prints das analytics, pede "analisa os posts", "como estão os vídeos", "o que resulta mais", "ajusta o conteúdo", ou escreve /analytics-conteudo.
---

# Analytics do conteúdo → ajustes

**O que conta (por esta ordem):** 1) inscritos novos no canal de Telegram; 2) views. Gostos, comentários e
partilhas só interessam como sinais do que leva a views e a inscritos.

## Fontes de dados
- **Prints das redes** que o Dinis manda no chat (normalmente 1x por semana): por post, views, retenção média /
  % que viu até ao fim, gostos, comentários, partilhas, guardados, seguidores novos, visitas ao perfil e cliques
  no link da bio (quando a rede mostra). Se faltar a hora a que cada post saiu, pergunta.
- **Inscritos do canal** de hora a hora: `dados/conteudo/membros.json` (escrito pelo workflow Resultados).
- **Registo dos vídeos**: `dados/conteudo/registo.json` (tema, tipo, hora sugerida, duração, voz) e os guiões em
  `dados/videos/*.py` (gancho = `FALAS[0]`, legendas = `POSTS`, memes = `MEMES`).
- `python run.py conteudo candidatos` mostra no fim "Desempenho dos últimos vídeos": inscritos nas 24 h a seguir
  a cada publicação vs o ritmo normal, e as views já registadas.
- Local: `git fetch origin claude/dados` e lê os ficheiros com `git show origin/claude/dados:<caminho>`, ou usa
  um worktree do ramo de dados para escrever (como em `CLAUDE.md`, secção "Na nuvem").

## Passos
1. **Registar os números**: acrescenta uma linha por post e rede a `dados/conteudo/metricas.csv`
   (cabeçalho: `video,rede,publicado_em,views,retencao,gostos,comentarios,partilhas,guardados,seguidores_novos,cliques_link`).
   `video` = nome do guião (ex.: `20261124_taca_grandes`). Se souberes a hora real de publicação, escreve-a em
   `registo.json` → `videos.<nome>.publicado_em` (ISO, hora de Lisboa): melhora o cálculo dos inscritos.
2. **Inscritos por vídeo**: para cada vídeo, inscritos nas 24 h a seguir vs o ritmo normal (média diária dos 7
   dias antes). Vídeos publicados à mesma hora/dia partilham o efeito: diz isso em vez de atribuir tudo a um.
3. **Comparar** (só com 3+ vídeos por grupo; com menos, regista como "em observação"):
   - tipo de gancho (curiosidade, número/paradoxo, pergunta, polémica), primeira frase e o que aparecia no frame 0;
   - tema (3 grandes, seleção, Champions, outras ligas, conteúdo geral), clube;
   - duração, hora e dia de publicação, rede;
   - voz (ElevenLabs vs Microsoft), se houve meme, se o cartão do Agente tinha dica do canal;
   - retenção vs views (gancho fraco = muita gente sai nos primeiros 3 s).
4. **Pesquisar** (WebSearch `extended`) o que está a funcionar agora em contas de futebol de vídeo curto em
   Portugal/Brasil: formatos, temas do momento, sons/tendências, horários, ganchos; e mudanças recentes nos
   algoritmos do TikTok/Reels/Shorts. Só fontes deste mês; nada de copiar conteúdo de outros criadores.
5. **Escrever as lições** em `dados/conteudo/licoes_conteudo.md` (a rotina de conteúdo lê-o antes de cada
   vídeo). Formato curto:
   - `## Ativas` — regras com 3+ vídeos de evidência, cada uma com o número que a sustenta e o que fazer
     (ex.: "Ganchos com curiosidade: 2,1x views vs números (5 vs 4 vídeos). Usar por defeito.").
   - `## Em observação` — padrões com 1–2 vídeos.
   - `## Experiência da semana` — UMA coisa nova a testar (ex.: publicar às 13h; meme antes do vídeo).
   - `## Horários` — melhores janelas por rede, segundo os nossos dados.
   Apaga lições que deixaram de se confirmar em 3+ vídeos.
6. **Ajustar as regras**: se uma lição ativa contraria `docs/redes_sociais.md` ou `docs/conteudo_rotina.md`,
   propõe ao Dinis a mudança nesses ficheiros (estão no `main`; não os mudes sem ele aprovar).
7. **Guardar**: `bash scripts/guardar_dados.sh "analytics conteudo" theirs` (ou commit no worktree do ramo de dados).
8. **Resumo para o Dinis**: top 3 posts (views e inscritos), o que resultou e porquê, o que muda na próxima
   semana e a experiência da semana. Sem promessas de crescimento.

## Regras
- Nunca escrevas dados pessoais (nomes de seguidores, mensagens privadas) nos ficheiros.
- Correlação não é causa: com poucos vídeos, diz que é cedo para conclusões.
- As regras de conteúdo mantêm-se: +18, sem promessas de lucro, sem nomes de casas de apostas, "rede vizinha" nos
  vídeos, percentagens e não odds no TikTok/YouTube.
