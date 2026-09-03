---
name: visualisation-jsxgraph
description: Creer une visualisation mathematique interactive en JSXGraph pour ce depot, la classer par classe (4M1, 3M2) et par chapitre, puis la publier sur la Forge. A utiliser des qu'on demande une visualisation, une animation ou une figure interactive, ou qu'on demande de mettre en ligne le catalogue.
---

# Visualisation JSXGraph

## 1. Ce qu'il faut demander avant d'ecrire

Trois informations, a demander en une fois si elles manquent :

- **la classe** et **le chapitre**. Pour l'instant tout va dans l'un des deux :

  | classe | chapitre | dossier |
  |---|---|---|
  | `3M2` | `C1 Boîte à outils` | `visualisations/3M2/c1-boite-a-outils/` |
  | `4M1` | `1 Calcul intégral` | `visualisations/4M1/1-calcul-integral/` |

  D'autres classes et chapitres pourront s'ajouter ; demander lequel si le sujet
  ne colle a aucun des deux. Les anciennes visualisations non classees restent
  dans `visualisations/brouillon/` en `non-publie` ;

- **le statut** : `brouillon` ou `en-ligne`. Toujours demander, ne jamais choisir a la place.

Statuts possibles :

| statut | effet sur la page |
|---|---|
| `non-publie` | n'apparait pas |
| `brouillon` | apparait avec le tag « Brouillon » |
| `en-ligne` | apparait avec le tag « En ligne » |

## 2. Regles de forme (non negociables)

- **Pas de texte explicatif.** Un titre, la figure, les reglages, rien d'autre.
  Aucun paragraphe de cours, aucun encadre « ce qui se passe », aucun verdict
  commente, aucune note pedagogique. La figure explique, pas le texte.
- **Pas de style genere.** Pas d'emoji, pas de gras rhetorique, pas de listes a
  puces, pas de ton enthousiaste.
- **Francais sans anglicismes.** « Animer / Arreter », pas « Play / Pause ».
  Virgule decimale.
- **Une seule colonne**, largeur maximale 720 px, la figure en haut.
- **Source en une ligne** en bas de carte quand la visualisation vient d'une video
  ou d'un article : `D'après <a href="...">Titre</a>, Auteur.` Sinon, pas de ligne.

## 3. Ecrire le fichier

Partir de `references/gabarit.html` (dans ce dossier de skill) : c'est la mise en
page de reference, deja conforme aux regles ci-dessus.

Emplacement, calcule par le script :

```bash
python3 scripts/catalogue.py chemin --annee 4M1 --chapitre "1 Calcul intégral" --nom "Somme de Riemann"
# -> visualisations/4M1/1-calcul-integral/somme-de-riemann.html
```

Creer le dossier si besoin, puis ecrire le fichier HTML autonome a ce chemin.

### Points techniques JSXGraph

- `initBoard` avec `axis:false, showCopyright:false, showNavigation:false`,
  `keepaspectratio:true`, `pan`/`zoom` desactives sauf besoin explicite.
- Beaucoup d'objets : les creer **une seule fois**, puis les deplacer avec
  `setPosition(JXG.COORDS_BY_USER, [x, y])` et masquer les inutiles avec
  `setAttribute({visible:false})`. Ne jamais recreer le plateau a chaque image.
- Encadrer toute mise a jour de `board.suspendUpdate()` / `board.unsuspendUpdate()`.
- Reglages : `<input type="range">` HTML plutot que les curseurs JSXGraph, avec la
  valeur affichee en chasse fixe a droite.
- Animation : `setInterval` (~60 ms) pilote par un bouton qui bascule
  « Animer » / « Arreter ».
- Au-dela de ~800 objets mobiles, l'affichage devient lent : plafonner le curseur.

## 4. Enregistrer au catalogue

```bash
python3 scripts/catalogue.py ajouter \
  --titre "Somme de Riemann" \
  --annee 4M1 \
  --chapitre "1 Calcul intégral" \
  --fichier visualisations/4M1/1-calcul-integral/somme-de-riemann.html \
  --statut brouillon
```

La commande refuse un fichier absent et remplace l'entree si le chemin existe deja.
Ne jamais editer `visualisations.json` a la main.

Changer le statut plus tard :

```bash
python3 scripts/catalogue.py statut visualisations/4M1/1-calcul-integral/somme-de-riemann.html en-ligne
```

Autres commandes : `lister [--annee 4M1] [--statut brouillon]`, `verifier`.

## 5. Publier sur la Forge

```bash
scripts/deployer.sh "Ajout : somme de Riemann (4M1, calcul intégral)"
```

Le script verifie le catalogue, commit, pousse sur `origin` s'il existe et sur
`forge`, puis affiche l'adresse de la page. La publication GitLab Pages est faite
par `.gitlab-ci.yml` et prend une a deux minutes.

Verification seule, sans rien pousser : `scripts/deployer.sh --verifier`.

Si le remote manque (message d'erreur explicite du script) :

```bash
git remote add forge git@forge.apps.education.fr:<groupe>/<projet>.git
```

Ne pas publier sans que l'utilisateur l'ait demande.
