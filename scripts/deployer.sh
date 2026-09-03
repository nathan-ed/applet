#!/usr/bin/env bash
# Publication du catalogue sur la Forge (GitLab Pages) et, si present, sur origin.
#
#   scripts/deployer.sh "message de commit"
#   scripts/deployer.sh --verifier          # controle seul, sans rien pousser
#
# Prerequis, une seule fois :
#   git remote add forge git@forge.apps.education.fr:<groupe>/<projet>.git
set -euo pipefail

RACINE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$RACINE"

echo "== Verification du catalogue"
python3 scripts/catalogue.py verifier

if [ "${1:-}" = "--verifier" ]; then
  exit 0
fi

if ! git remote get-url forge >/dev/null 2>&1; then
  cat >&2 <<'MSG'

Aucun remote « forge » configure. Ajoutez-le une fois pour toutes :

  git remote add forge git@forge.apps.education.fr:<groupe>/<projet>.git

puis relancez ce script.
MSG
  exit 1
fi

BRANCHE="$(git rev-parse --abbrev-ref HEAD)"
MESSAGE="${1:-Mise a jour du catalogue}"

if [ -n "$(git status --porcelain)" ]; then
  echo "== Commit"
  git add -A
  git commit -m "$MESSAGE"
else
  echo "== Rien a committer, publication de l'etat courant"
fi

if git remote get-url origin >/dev/null 2>&1; then
  echo "== Push origin/$BRANCHE"
  git push origin "$BRANCHE"
fi

echo "== Push forge/$BRANCHE"
git push forge "$BRANCHE"

# URL probable des Pages : git@forge.apps.education.fr:groupe/sous/projet.git
#                       -> https://groupe.forge.apps.education.fr/sous/projet/
URL_FORGE="$(git remote get-url forge)"
CHEMIN="${URL_FORGE#*forge.apps.education.fr[:/]}"
CHEMIN="${CHEMIN%.git}"
GROUPE="${CHEMIN%%/*}"
RESTE="${CHEMIN#*/}"
if [ "$GROUPE" != "$CHEMIN" ]; then
  echo
  echo "Page : https://${GROUPE}.forge.apps.education.fr/${RESTE}/"
  echo "Pipeline : ${URL_FORGE%.git} -> CI/CD (la publication prend une a deux minutes)"
fi
