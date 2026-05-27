# Visualisations

Catalogue statique de visualisations classees par categorie (`1M`, `2M`, `3M`, `4M`) et par statut (`non-publie`, `brouillon`, `pret`).

## Ajouter une visualisation

1. Placer le fichier HTML dans le dossier de categorie, par exemple `visualisations/3M/ma-visualisation.html`.
2. Ajouter une entree dans `visualisations.json`.
3. Commit et push sur `main`.

GitHub Pages publie automatiquement le site apres chaque push sur `main`.

## Statuts

- `non-publie`: la visualisation n'apparait pas sur la page catalogue.
- `brouillon`: la visualisation apparait avec le tag `Brouillon`.
- `pret`: la visualisation apparait avec le tag `Prêt`.

## Exemple d'entree

```json
{
  "title": "Ma visualisation",
  "category": "3M",
  "status": "brouillon",
  "path": "visualisations/3M/ma-visualisation.html",
  "description": "Courte description."
}
```
