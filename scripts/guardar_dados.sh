#!/usr/bin/env bash
# Guarda as alterações da pasta dados/ (checkout do ramo de dados) e envia-as para o GitHub.
# Uso: bash scripts/guardar_dados.sh "mensagem" [ours|theirs]
#   ours   (GitHub Actions): em conflito ganha a versão que já está no GitHub (ex.: análise do agente no recap);
#          a parte automática é refeita na execução seguinte.
#   theirs (rotinas do agente): em conflito ganha o texto do agente.
set -euo pipefail
BRANCH="${DADOS_BRANCH:-claude/dados}"
cd "$(dirname "$0")/../dados"
git config user.name "${GIT_AUTHOR_NAME:-agente-bets}"
git config user.email "${GIT_AUTHOR_EMAIL:-agente-bets@users.noreply.github.com}"
git add -A
if git diff --cached --quiet; then
  echo "dados: sem alterações"
  exit 0
fi
git commit -q -m "$1 ($(TZ=Europe/Lisbon date '+%Y-%m-%d %H:%M'))"
for i in 1 2 3 4 5; do
  if git push -q origin "HEAD:$BRANCH"; then
    echo "dados: enviados"
    exit 0
  fi
  echo "dados: o GitHub tem alterações novas, a juntar (tentativa $i)"
  git pull -q --rebase -X "${2:-ours}" origin "$BRANCH"
done
echo "dados: não consegui enviar" >&2
exit 1
