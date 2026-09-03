# Visualisations

Catalogue statique de visualisations interactives, classees par classe et par
chapitre, avec un statut de publication.

| classe | chapitre | dossier |
|---|---|---|
| `3M2` | `C1 Boîte à outils` | `visualisations/3M2/c1-boite-a-outils/` |
| `4M1` | `1 Calcul intégral` | `visualisations/4M1/1-calcul-integral/` |

`visualisations/brouillon/` regroupe les anciennes visualisations pas encore
classees, toutes en `non-publie`.

La page `index.html` lit `visualisations.json` et construit ses filtres a partir
du contenu du catalogue.

## Ajouter une visualisation

```bash
# 1. chemin normalise
python3 scripts/catalogue.py chemin --annee 4M1 --chapitre "1 Calcul intégral" --nom "Somme de Riemann"
# -> visualisations/4M1/1-calcul-integral/somme-de-riemann.html

# 2. ecrire le fichier HTML a ce chemin (voir le skill visualisation-jsxgraph)

# 3. enregistrer au catalogue
python3 scripts/catalogue.py ajouter \
  --titre "Somme de Riemann" --annee 4M1 --chapitre "1 Calcul intégral" \
  --fichier visualisations/4M1/1-calcul-integral/somme-de-riemann.html  --statut brouillon
```

## Statuts

- `non-publie` : n'apparait pas sur la page.
- `brouillon` : apparait avec le tag « Brouillon ».
- `en-ligne` : apparait avec le tag « En ligne ».

Changer le statut :

```bash
python3 scripts/catalogue.py statut visualisations/4M1/1-calcul-integral/somme-de-riemann.html en-ligne
```

## Publier

```bash
scripts/deployer.sh "message de commit"
```

Verification, commit, push sur `origin` puis sur `forge`. La mise en ligne est
faite par `.gitlab-ci.yml` (GitLab Pages de la Forge) ; GitHub Pages continue de
publier via `.github/workflows/pages.yml`.

Configuration du remote, une seule fois :

```bash
git remote add forge git@forge.apps.education.fr:<groupe>/<projet>.git
```

Controle sans publication : `scripts/deployer.sh --verifier`.

## Scripts

- `scripts/catalogue.py` : `chemin`, `ajouter`, `statut`, `lister`, `verifier`.
- `scripts/deployer.sh` : verification, commit, push, adresse de la page.
