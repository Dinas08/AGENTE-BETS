# Rotina de conteúdo — vídeos para TikTok, Instagram, YouTube Shorts e X

Tu (o agente, na nuvem) escreves **1–2 guiões de vídeo por dia**. O GitHub Actions renderiza-os com a voz da
ElevenLabs e manda-os em privado aos admins do Telegram, com as legendas de cada rede. **Os admins aprovam e
publicam à mão: tu nunca publicas em lado nenhum.**

## Preparação (sessão na nuvem)
```bash
git fetch origin claude/dados && git worktree add --detach dados FETCH_HEAD
python3.13 -m pip install -q -r requirements-video.txt
```
Usa `python3.13`. Não corras `tudo`, `prever` nem `resultados`.

## Passos
1. `python3.13 run.py conteudo candidatos` → jogos acabados nas últimas 36 h ordenados pelo potencial de views,
   jogos dos 3 grandes a seguir, os últimos vídeos feitos (não repetir) e ideias.
   Lê também `dados/conteudo/licoes_conteudo.md` (o que deu mais views; cria-o se não existir) e
   `docs/redes_sociais.md` (formatos, horários, chamadas para a ação).
2. **Escolhe** (no máximo 2 por execução, 1 por defeito):
   - **Sempre** que um dos 3 grandes (Benfica, Porto, Sporting) jogou e ainda não tem vídeo.
   - Jogos importantes de ligas importantes: Champions, seleção de Portugal, clássicos e jogos com história
     (reviravolta, golo nos descontos, goleada, surpresa). O `pontos` dos candidatos ajuda, não decide sozinho.
   - Sem jogo forte: **conteúdo geral** (melhor 11 da jornada, melhor 11 de sempre, duelo de números,
     antevisão do jogo grande com a previsão do Agente…). **Inova**: experimenta formatos novos e regista-os.
   - Se nada vale a pena, não faças vídeo nesse dia. Qualidade antes de quantidade.
3. **Pesquisa** (como no Rotina 1 de `CLAUDE.md`): ESPN (`site.api.espn.com/apis/site/v2/sports/soccer/<liga>/summary?event=<id>`
   dá onzes, keyEvents, comentário e estatísticas) e 2+ crónicas recentes (WebSearch `extended`, depois abrir os
   artigos). **Não inventes táticas nem números.** Fontes a divergir: segue a maioria e escreve qual seguiste no
   docstring. Polémicas e críticas só com fonte. Confirma o resultado final antes de escrever.
4. **Escreve o guião** em `dados/videos/AAAAMMDD_<nome>.py` (ex.: `20261118_benfica_porto.py`). Modelo:
   `docs/video/jogos/dinamarca_noruega.py` (jogo) e `docs/video/jogos/onze_portugal.py` (melhor 11).
   O guião tem de definir, além de `FALAS`, `REF_VOZ` e `construir()`:
   ```python
   TIPO = "jogo"            # jogo | onze | antevisao | duelo | outro
   TEMA = "Benfica 2-1 Porto: o meio-campo que decidiu"
   MATCH_ID = "20261118-P1-benfica-porto"   # vazio se não for um jogo
   HORA = "21:30"           # hora sugerida para publicar (ver docs/redes_sociais.md)
   POSTS = {
       "tiktok": "legenda curta com gancho + 3-5 hashtags",
       "instagram": "legenda um pouco maior + 3-5 hashtags + '+18'",
       "youtube": {"titulo": "título até 70 caracteres com #shorts", "descricao": "2-3 linhas + hashtags"},
       "x": "frase de impacto até 250 caracteres + 1-2 hashtags",
   }
   ```
   **Memes (posts estáticos) — OBRIGATÓRIO em todos os guiões**: junta 1–2 memes do Agente Claudio ligados ao vídeo, com humor leve (um trocadilho,
   o "expectativa vs realidade" do jogo, o robô a reagir a um lance). Desenhados com `docs/video/memes.py`
   (lê o docstring: modelos `reacao` e `expectativa`, desenhos prontos `parede`, `placar:<texto>`, `trofeu`,
   `relogio:<minuto>`, `bola`, `lagrima`, `fogo`, `zero`, ou uma função tua `f(d, caixa)` para um desenho novo):
   ```python
   MEMES = [{"modelo": "reacao", "topo": "...", "desenho": "parede", "baixo": "...", "fala": "...",
             "legenda": "texto do post para Instagram/X, com 3-5 hashtags e +18"}]
   ```
   Sem fotos de jogadores, emblemas ou logótipos; não gozes com jogadores (lesões, erros pessoais, choro). Revê
   com `python3.13 -c "import sys; sys.path[:0]=['docs/video','docs/video/jogos','dados/videos']; import memes, <guiao>; [memes.meme(c, __import__('pathlib').Path(f'/tmp/meme{i}.png')) for i, c in enumerate(<guiao>.MEMES)]"`
   e abre as imagens com Read.
   A frase de fecho vai no próprio guião (não podes mexer no `main`):
   `cena_fecho(jogadores({}), placar="2–1", minuto="FIM", frase=("[laughs] Manda isto ao teu amigo que…", ["Manda isto ao teu amigo", "que …", "e …|destaque|."]))`.
   Uma frase **nova** em cada vídeo (vê as anteriores em `FRASES_FECHO` e nos guiões de `dados/videos/`).
5. **Tempos**: `python3.13 docs/video/medir_voz.py dados/videos/<guiao>.py --estimar` dá a duração estimada de
   cada fala e o tempo de cada palavra (tempo na cena = tempo da palavra + 0,15). Põe essas durações em `REF_VOZ`:
   no render a sério as animações esticam para a voz real.
6. **Revê**: `python3.13 docs/video/quadro_tatico.py dados/videos/<guiao>.py --capas --saida /tmp/capas` e abre
   as imagens das cenas (Read). Corrige textos sobrepostos, nomes trocados, placar na ordem casa–fora.
7. **Antes de guardar, confirma**: o guião tem `MEMES` com 1–2 memes revistos em imagem, `POSTS` para as 4 redes, `HORA`, e a frase de fecho nova. Um vídeo sem memes chega aos admins com um aviso.
   Memes de um jogo que já teve vídeo: um guião só com `TIPO = "memes"`, `TEMA`, `MATCH_ID` e `MEMES` (sem `construir()`); o circuito manda só as imagens.
8. **Guarda**: `bash scripts/guardar_dados.sh "conteudo" theirs`. Em até 10 min o vídeo chega ao Telegram dos admins.

## Regras do conteúdo (iguais aos vídeos feitos à mão)
- Formato: **análise tática, não resumo golo a golo**. Plano das equipas e 2–3 detalhes táticos no quadro, cartão
  do Agente Claudio, pergunta A/B curta, fecho com humor. **55–65 s** (até 80 s só se a história o pedir).
- **Gancho** (segue a secção "Gancho" de `docs/redes_sociais.md`): uma frase até ~5 s com uma lacuna de
  curiosidade que só se resolve mais à frente; o primeiro frame já mostra o contraste em letras grandes, sem
  fade-in; começa pelo momento mais forte; nada de contexto no início. Modelo: `docs/video/jogos/taca_grandes.py`.
- Humor leve e trocadilhos/rimas quando saem naturais ("Contra o Paredes… uma parede"), sem gozar com jogadores.
- Voz: nomes escritos como se dizem ("Chélderup", "Hólan", "Ódegor"), sem acentos a forçar a sílaba errada;
  **"grande penalidade"**, nunca "penálti"; números por extenso na voz e em algarismos nas legendas. Etiquetas de
  emoção (`[laughs]`) só onde ajudam.
- Visual: cores do equipamento em `v.sp["casa"/"fora"]`; a casa ataca sempre para cima; `abrev=(casa, fora)` e
  placares na ordem casa–fora; sem clarão nem "GOLO" gigante. Rodapé "Ilustração · dados ESPN, <fontes>".
  Nunca "Sporting Lisbon": é "Sporting" (SCP).
- **Cartão do Agente**: só a dica que saiu mesmo no canal (`dados/telegram.json`, com `message_id`) e/ou a
  previsão de resultado do modelo **se acertou**. Nunca mostrar previsões falhadas não publicadas.
- **Chamada para a ação**: o vídeo é o mesmo para as 4 redes, por isso no vídeo usa **"as previsões estão na
  rede vizinha, link na bio"** e mostra **percentagens, não odds** (o TikTok e o YouTube castigam conteúdo de
  apostas). Nunca dizer "Telegram", "dashboard", nomes de casas de apostas nem prometer lucros. As odds e a
  palavra "dica" podem ir só nas legendas do Instagram e do X, com "+18".
- Um aviso "+18 · joga com responsabilidade" por peça chega (já está no fecho). Tom confiante e divertido.
- Sem dados pessoais do Dinis em nada.

## Aprender com as analytics
- **O objetivo são views e inscritos novos no canal.** O `run.py conteudo candidatos` mostra no fim o
  "Desempenho dos últimos vídeos" (inscritos nas 24 h a seguir a cada publicação vs o ritmo normal, e as views
  registadas). Antes de escolher, vê que temas, ganchos e horas trouxeram mais inscritos e puxa nessa direção.
- A análise semanal dos prints segue a skill `.claude/skills/analytics-conteudo/SKILL.md` e escreve as lições.
- O Dinis manda, uma vez por semana, prints das estatísticas de cada rede. Nessa sessão atualiza
  `dados/conteudo/licoes_conteudo.md`: views, retenção, gostos, comentários e partilhas por vídeo (nome do guião),
  e conclusões curtas ("antevisões dos 3 grandes dão 3x mais views", "ganchos com números retêm mais").
- Antes de escolher temas, lê esse ficheiro e aplica as conclusões. Experimenta 1 coisa nova por semana e regista
  o resultado.
