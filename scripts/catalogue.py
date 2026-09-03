#!/usr/bin/env python3
"""Gestion de visualisations.json : ajout, statut, verification.

Arborescence attendue : visualisations/<annee>/<chapitre>/<nom>.html
  annee    : 4M1, 3M2, ... (code de classe)
  chapitre : slug sans accent, en minuscules

Usage :
  scripts/catalogue.py ajouter --titre "..." --annee 4M1 --chapitre "Trigonométrie" \
      --fichier visualisations/4M1/trigonometrie/cercle.html \
      --statut brouillon
  scripts/catalogue.py statut visualisations/4M1/trigonometrie/cercle.html en-ligne
  scripts/catalogue.py chemin --annee 4M1 --chapitre "Trigonométrie" --nom "Cercle trigo"
  scripts/catalogue.py lister [--annee 4M1] [--statut brouillon]
  scripts/catalogue.py verifier
"""

import argparse
import json
import os
import re
import sys
import unicodedata

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOGUE = os.path.join(RACINE, "visualisations.json")
STATUTS = ("non-publie", "brouillon", "en-ligne")
# statuts historiques encore tolérés en lecture
ALIAS = {"pret": "en-ligne", "draft": "brouillon"}


def slug(texte):
    texte = unicodedata.normalize("NFKD", texte)
    texte = "".join(c for c in texte if not unicodedata.combining(c))
    texte = texte.lower().replace("'", " ").replace("’", " ")
    texte = re.sub(r"[^a-z0-9]+", "-", texte).strip("-")
    return texte


def charger():
    with open(CATALOGUE, encoding="utf-8") as f:
        return json.load(f)


def sauver(items):
    with open(CATALOGUE, "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2, ensure_ascii=False)
        f.write("\n")


def normaliser_statut(valeur):
    valeur = ALIAS.get(valeur, valeur)
    if valeur not in STATUTS:
        sys.exit("Statut inconnu : %s (attendu : %s)" % (valeur, ", ".join(STATUTS)))
    return valeur


def cmd_chemin(args):
    print("visualisations/%s/%s/%s.html" % (args.annee, slug(args.chapitre), slug(args.nom)))


def cmd_ajouter(args):
    chemin = args.fichier.replace(os.sep, "/").lstrip("./")
    if not os.path.exists(os.path.join(RACINE, chemin)):
        sys.exit("Fichier introuvable : %s" % chemin)

    items = charger()
    statut = normaliser_statut(args.statut)
    entree = {
        "title": args.titre,
        "category": args.annee,
        "chapter": args.chapitre,
        "status": statut,
        "path": chemin,
    }

    for i, item in enumerate(items):
        if item.get("path") == chemin:
            items[i] = entree
            sauver(items)
            print("Mise a jour : %s" % chemin)
            return

    items.append(entree)
    sauver(items)
    print("Ajout : %s [%s]" % (chemin, statut))


def cmd_statut(args):
    items = charger()
    statut = normaliser_statut(args.valeur)
    cible = args.chemin.replace(os.sep, "/").lstrip("./")
    for item in items:
        if item.get("path") == cible:
            item["status"] = statut
            sauver(items)
            print("%s -> %s" % (cible, statut))
            return
    sys.exit("Aucune entree pour %s" % cible)


def cmd_lister(args):
    for item in charger():
        statut = ALIAS.get(item.get("status"), item.get("status"))
        if args.annee and item.get("category") != args.annee:
            continue
        if args.statut and statut != normaliser_statut(args.statut):
            continue
        print("%-9s %-9s %-22s %-38s %s" % (
            item.get("category", "?"), statut,
            (item.get("chapter") or "-")[:22], item.get("path", "?"), item.get("title", "?")))


def cmd_verifier(_args):
    items = charger()
    erreurs = []
    vus = set()
    for item in items:
        chemin = item.get("path", "")
        for cle in ("title", "category", "status", "path"):
            if not item.get(cle):
                erreurs.append("%s : champ %s manquant" % (chemin or "?", cle))
        if chemin in vus:
            erreurs.append("%s : chemin en double" % chemin)
        vus.add(chemin)
        if chemin and not os.path.exists(os.path.join(RACINE, chemin)):
            erreurs.append("%s : fichier absent" % chemin)
        statut = ALIAS.get(item.get("status"), item.get("status"))
        if statut not in STATUTS:
            erreurs.append("%s : statut invalide (%s)" % (chemin, item.get("status")))

    orphelins = []
    for dossier, _sous, fichiers in os.walk(os.path.join(RACINE, "visualisations")):
        for nom in fichiers:
            if not nom.endswith(".html"):
                continue
            rel = os.path.relpath(os.path.join(dossier, nom), RACINE).replace(os.sep, "/")
            if rel not in vus:
                orphelins.append(rel)

    for e in erreurs:
        print("ERREUR  %s" % e)
    for o in orphelins:
        print("ORPHELIN %s (present sur le disque, absent du catalogue)" % o)

    if erreurs:
        sys.exit(1)
    print("Catalogue valide : %d entrees, %d orphelins." % (len(items), len(orphelins)))


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="commande", required=True)

    a = sub.add_parser("ajouter", help="ajouter ou mettre a jour une entree")
    a.add_argument("--titre", required=True)
    a.add_argument("--annee", required=True, help="4M1, 3M2, ...")
    a.add_argument("--chapitre", required=True)
    a.add_argument("--fichier", required=True)
    a.add_argument("--statut", default="brouillon", help=" | ".join(STATUTS))
    a.set_defaults(func=cmd_ajouter)

    s = sub.add_parser("statut", help="changer le statut d'une visualisation")
    s.add_argument("chemin")
    s.add_argument("valeur", help=" | ".join(STATUTS))
    s.set_defaults(func=cmd_statut)

    c = sub.add_parser("chemin", help="calculer le chemin normalise d'une visualisation")
    c.add_argument("--annee", required=True)
    c.add_argument("--chapitre", required=True)
    c.add_argument("--nom", required=True)
    c.set_defaults(func=cmd_chemin)

    l = sub.add_parser("lister", help="lister le catalogue")
    l.add_argument("--annee")
    l.add_argument("--statut")
    l.set_defaults(func=cmd_lister)

    v = sub.add_parser("verifier", help="controler la coherence du catalogue")
    v.set_defaults(func=cmd_verifier)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
