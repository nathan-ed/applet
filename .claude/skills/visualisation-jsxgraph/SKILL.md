---
name: visualisation-jsxgraph
description: Creer une visualisation mathematique interactive en JSXGraph pour ce depot, la classer par classe (4M1, 3M2) et par chapitre, puis la publier sur la Forge. A utiliser des qu'on demande une visualisation, une animation ou une figure interactive, ou qu'on demande de mettre en ligne le catalogue.
---

# Visualisation JSXGraph

## 0. Tenir ce fichier a jour

Des qu'une correction, une preference ou une contrainte technique apparait en
cours de travail, l'ecrire ici dans la foulee, sans attendre qu'on le demande :

- une remarque sur la forme (« pas ce mot », « pas ce genre de texte ») va dans
  les regles de forme, formulee comme une regle et pas comme un exemple ;
- un piege technique (limite d'une bibliotheque, perte de precision, chose qui ne
  marche pas dans le navigateur) va dans les points techniques, avec la parade ;
- un changement d'organisation (nouvelle classe, nouveau chapitre, nouveau
  script, nouveau statut) va dans les sections concernees.

Une correction repetee deux fois est une regle manquante dans ce fichier.
Corriger aussi `references/gabarit.html` quand la regle touche la mise en page.

## 1. Ce qu'il faut demander avant d'ecrire

- **la classe** et **le chapitre**. Pour l'instant tout va dans l'un des deux :

  | classe | chapitre | dossier |
  |---|---|---|
  | `3M2` | `C1 Boîte à outils` | `visualisations/3M2/c1-boite-a-outils/` |
  | `4M1` | `1 Calcul intégral` | `visualisations/4M1/1-calcul-integral/` |

  D'autres classes et chapitres pourront s'ajouter ; demander lequel si le sujet
  ne colle a aucun des deux. Les anciennes visualisations non classees restent
  dans `visualisations/brouillon/` en `non-publie` ;
- **le statut** : `brouillon` ou `en-ligne`. Toujours demander, ne jamais choisir a la place.

| statut | effet sur la page |
|---|---|
| `non-publie` | n'apparait pas |
| `brouillon` | n'apparait pas |
| `en-ligne` | apparait dans le tableau |

Seul `en-ligne` s'affiche : la page ne montre aucune pastille de statut.

## 2. Regles de forme (non negociables)

- **Pas de texte explicatif.** Un titre, la figure, les reglages, les mesures.
  Aucun paragraphe de cours, aucun encadre « ce qui se passe », aucun verdict
  commente, aucune note pedagogique, aucune description. La figure explique.
- **Pas de style genere.** Pas d'emoji, pas de gras rhetorique, pas de listes a
  puces, pas de ton enthousiaste.
- **Francais sans anglicismes.** « Animer / Arreter », pas « Play / Pause ».
  Virgule decimale, signe moins typographique (`−`).
- **Marquer `≈`** devant toute valeur qui n'est pas exacte a l'affichage :
  resultat d'un calcul numerique (integrale, dichotomie) toujours, valeur
  ponctuelle seulement si l'arrondi la change.

  ```js
  function arrondi(x) {   // « ≈ » seulement si l'arrondi n'est pas exact
    return (Math.abs(x - Math.round(x * 100) / 100) < 5e-13 ? '' : '≈ ') + fmt(x);
  }
  ```
- **Plusieurs valeurs dans une meme case** : nommer chacune avec son indice —
  `c₁ ≈ 0,24   c₂ ≈ 2,90`. Jamais une liste entre parentheses ni separee par des
  points-virgules seuls : on la lit comme les coordonnees d'un point. Une seule
  valeur reste nue, l'intitule de la case suffit.
- **Une seule colonne**, largeur maximale 720 px, la figure en haut.
- **Lien de retour** en haut de page :
  `<a class="retour" href="../../../index.html">← Retour au catalogue</a>`
  (trois niveaux depuis `visualisations/<classe>/<chapitre>/`). Deja dans le gabarit.
- **Source en une ligne** en bas de carte quand la visualisation vient d'une video
  ou d'un article : `D'après <a href="...">Titre</a>, Auteur.` Sinon, pas de ligne.

## 3. Ecrire le fichier

Partir de `references/gabarit.html` (dans ce dossier de skill). Emplacement calcule
par le script :

```bash
python3 scripts/catalogue.py chemin --annee 4M1 --chapitre "1 Calcul intégral" --nom "Somme de Riemann"
# -> visualisations/4M1/1-calcul-integral/somme-de-riemann.html
```

### Points techniques JSXGraph

- `initBoard` avec `axis:false` (ou `true` pour un graphe de fonction),
  `showCopyright:false, showNavigation:false`, `pan`/`zoom` desactives sauf besoin.
  `keepaspectratio:true` pour une figure geometrique, `false` pour un graphe.
- Beaucoup d'objets : les creer **une seule fois**, puis les deplacer avec
  `setPosition(JXG.COORDS_BY_USER, [x, y])` et masquer les inutiles avec
  `setAttribute({visible:false})`. Ne jamais recreer le plateau a chaque image.
- Meme chose pour un nombre **variable** de solutions : creer un pool
  (`MAXC = 12`) et n'en afficher que ce qui est utile. Toujours montrer **toutes**
  les solutions du probleme, jamais la premiere seulement.
- Aires et polygones : un `curve` dont on remplace `dataX` / `dataY`, avec
  `fillColor` et `fillOpacity`, plutot qu'un `polygon` recree.
- Encadrer toute mise a jour de `board.suspendUpdate()` / `board.unsuspendUpdate()`.
- Cadrage adaptatif : `board.setBoundingBox([x0, y1, x1, y0], false)` calcule
  depuis un echantillonnage de la fonction.
- Marquer les elements que l'enonce nomme, avec la lettre du cours : bornes `a`
  et `b`, images `f(a)`, `f(b)`, solutions `c` — point + verticale pointillee +
  `text` avec `text-shadow:0 0 3px #fff` pour rester lisible sur la courbe.
  Plusieurs solutions : les indicer `c₁`, `c₂`, … (indices Unicode), et
  garder la lettre nue quand il n'y en a qu'une.
- Reglages : `<input type="range">` HTML plutot que les curseurs JSXGraph, valeur
  affichee a droite en chasse fixe.
- Animation : `setInterval` (~60 ms) pilote par un bouton « Animer » / « Arreter ».
- Au-dela de ~800 objets mobiles, l'affichage devient lent : plafonner le curseur.

### Saisie de valeurs et de fonctions

L'utilisateur veut **taper** ses valeurs, pas les choisir dans une liste. Un
`<input type="text">` et un bouton « Appliquer » (plus la touche Entree) ; les
boutons de raccourci se contentent de remplir le champ. Bordure rouge
(`classList.toggle('erreur', …)`) quand l'expression ne se lit pas — aucun
message d'erreur ecrit.

- **Grandeur calculee** : quand une valeur affichee se laisse inverser (fraction
  continue, coordonnees, coefficients), en faire un champ editable plutot qu'un
  simple affichage — on doit pouvoir la reecrire et l'appliquer, la figure se
  recalculant dans l'autre sens. Le champ est reecrit sous forme canonique au
  rendu suivant.
- **Fonction** : `board.jc.snippet(texte, true, 'x', true)` (JessieCode) accepte
  `x^2+1`, `sin`, `sqrt`, `exp`, `abs`. Verifier que l'appel rend bien un nombre.
- **Nombre** : analyseur maison en fractions exactes sur `BigInt` (`{n, d}`),
  voir `visualisations/3M2/c1-boite-a-outils/nombre-d-or-tournesol.html`.
  Indispensable des qu'on affiche une fraction continue : en flottant les termes
  deviennent faux vers le quinzieme. Les constantes (`pi`, `e`, `phi`) sont
  donnees a 60 chiffres, les racines calculees par `isqrt` sur `BigInt`.

## 4. Verifier

Aucun navigateur n'est disponible : extraire le `<script>` et le passer a Node.

```bash
python3 - <<'PY'
import re
s = open('visualisations/4M1/1-calcul-integral/ma-visu.html', encoding='utf-8').read()
open('/tmp/verif.js', 'w').write(re.search(r'<script>\n(.*?)</script>', s, re.S).group(1))
PY
node --check /tmp/verif.js
```

Pour la partie calculatoire (integrale, dichotomie, fraction continue), extraire
les fonctions pures et les comparer a des valeurs exactes connues avant de
conclure que la visualisation est juste.

## 5. Enregistrer au catalogue

```bash
python3 scripts/catalogue.py ajouter \
  --titre "Somme de Riemann" \
  --annee 4M1 \
  --chapitre "1 Calcul intégral" \
  --fichier visualisations/4M1/1-calcul-integral/somme-de-riemann.html \
  --statut brouillon
```

La commande refuse un fichier absent, remplace l'entree si le chemin existe deja,
et regenere `visualisations.js` — la copie JavaScript du catalogue qui permet
d'ouvrir `index.html` en double-clic, `fetch` etant interdit en `file://`.
Ne jamais editer `visualisations.json` ni `visualisations.js` a la main.

Changer le statut plus tard :

```bash
python3 scripts/catalogue.py statut visualisations/4M1/1-calcul-integral/somme-de-riemann.html en-ligne
```

Autres commandes : `chemin`, `lister [--annee 4M1] [--statut brouillon]`, `verifier`.

## 6. Publier sur la Forge

```bash
scripts/deployer.sh "Ajout : somme de Riemann (4M1, calcul intégral)"
```

Verification du catalogue, commit, push sur `origin` (GitHub) puis sur `forge`
(`git@forge.apps.education.fr:nathan.scheinmann-ext/visualisation.git`), et
affichage de l'adresse de la page. La publication GitLab Pages vient de
`.gitlab-ci.yml` et prend une a deux minutes.

Verification seule : `scripts/deployer.sh --verifier`.

Ne pas publier sans que l'utilisateur l'ait demande.
