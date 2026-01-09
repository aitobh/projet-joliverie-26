"""
Script : loginNormaliser.py
Objectif :
Normaliser des prénoms et noms complexes afin de générer
des logins conformes aux standards d'entreprise.
"""

import unicodedata
import re

def supprimer_accents(texte):
    texte = unicodedata.normalize('NFD', texte)
    return ''.join(c for c in texte if unicodedata.category(c) != 'Mn')

def initiales_prenom(prenom):
    # Séparation sur espaces et tirets
    parties = re.split(r"[ -]", prenom)
    return ''.join(p[0] for p in parties if p)

def normaliser_nom(nom):
    nom = supprimer_accents(nom)
    nom = nom.lower()
    # On conserve uniquement les lettres a-z
    nom = re.sub(r"[^a-z]", "", nom)
    return nom

with open("testEntreeSpeciaux.csv", "r", encoding="utf-8") as entree:
    lignes = entree.readlines()

with open("testSortieNormaliser.csv", "w", encoding="utf-8") as sortie:
    sortie.write("login\n")

    for ligne in lignes[1:]:
        prenom, nom = ligne.strip().split(";")
        login = initiales_prenom(prenom) + normaliser_nom(nom)
        sortie.write(login.lower() + "\n")
