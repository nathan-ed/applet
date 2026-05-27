# Visualisations

Catalogue statique de visualisations classees par categorie (`1M`, `2M`, `3M`, `4M`) et par statut (`brouillon`, `prêt`).

## Ajouter une visualisation

1. Placer le fichier HTML dans le dossier de categorie, par exemple `visualisations/3M/ma-visualisation.html`.
2. Ajouter une entree dans `visualisations.json`.
3. Commit et push sur `main`.

GitHub Pages publie automatiquement le site apres chaque push sur `main`.

## Statuts

- `brouillon`: visualisation en cours de preparation.
- `pret`: visualisation prête a etre utilisee.

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
