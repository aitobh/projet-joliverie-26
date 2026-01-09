#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Testeur de politiques de mots de passe (Phase 6.3)
Usage :
    python testPassword.py <input_csv>
- <input_csv> : chemin du CSV contenant une colonne `password`.
Sorties :
- validation_report.csv : résultats par mot de passe (valide / problèmes)
- validation_summary.txt : synthèse (totaux, doublons)
"""
import sys
import pandas as pd
import string
from collections import Counter

ALLOWED_SPECIALS = set("!@#$%&*+-=.<>/?")
LOWERS = set(string.ascii_lowercase)  # a-z
UPPERS = set([c for c in string.ascii_uppercase if c != 'O'])  # A-Z sans O
DIGITS = set('123456789')  # sans 0

ALL_ALLOWED = LOWERS | UPPERS | DIGITS | ALLOWED_SPECIALS


def validate_password(pw: str):
    issues = []
    if not isinstance(pw, str):
        return False, ["valeur non textuelle"]

    # Longueur
    if len(pw) < 12:
        issues.append("longueur < 12")

    # Caractères interdits
    if any(ch.isspace() for ch in pw):
        issues.append("espace interdit")
    if 'O' in pw:
        issues.append("contient 'O' majuscule interdit")
    if '0' in pw:
        issues.append("contient '0' interdit")

    # Caractères non autorisés (en dehors des classes ci-dessus)
    if any(ch not in ALL_ALLOWED for ch in pw):
        issues.append("caractères non autorisés")

    # Comptages
    lowers = sum(1 for ch in pw if ch in LOWERS)
    uppers = sum(1 for ch in pw if ch in UPPERS)
    digits = sum(1 for ch in pw if ch in DIGITS)
    specials = sum(1 for ch in pw if ch in ALLOWED_SPECIALS)

    if uppers < 2:
        issues.append("moins de 2 majuscules")
    if lowers < 2:
        issues.append("moins de 2 minuscules")
    if digits < 2:
        issues.append("moins de 2 chiffres (1-9)")
    if specials < 2:
        issues.append("moins de 2 caractères spéciaux")

    # Spéciaux en début/fin
    if pw and pw[0] in ALLOWED_SPECIALS:
        issues.append("caractère spécial en début")
    if pw and pw[-1] in ALLOWED_SPECIALS:
        issues.append("caractère spécial en fin")

    return (len(issues) == 0), issues


def main():
    if len(sys.argv) < 2:
        print("Usage: python testPassword.py <input_csv>")
        sys.exit(1)

    input_csv = sys.argv[1]
    df = pd.read_csv(input_csv)
    if 'password' not in df.columns:
        raise SystemExit("Le fichier doit contenir une colonne 'password'.")

    # Validation par mot de passe
    results = []
    for idx, pw in enumerate(df['password'], start=1):
        valid, issues = validate_password(str(pw))
        results.append({
            'ligne': idx,
            'password': pw,
            'valide': bool(valid),
            'problemes': '; '.join(issues)
        })

    rep = pd.DataFrame(results)
    rep.to_csv('validation_report.csv', index=False)

    # Détection de doublons
    counts = df['password'].value_counts()
    dups = counts[counts > 1]

    # Résumé
    total = len(df)
    valides = rep['valide'].sum()
    invalides = total - valides

    lines = [
        f"Total mots de passe : {total}",
        f"Valides : {valides}",
        f"Invalides : {invalides}",
        f"Doublons : {int(dups.sum()) - int(len(dups)) if not dups.empty else 0} occurrences supplémentaires"  # nb extra occurrences
    ]
    if not dups.empty:
        lines.append("Détails des doublons (password -> occurrences) :")
        for pw, c in dups.items():
            lines.append(f"- {pw} -> {c}")

    with open('validation_summary.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    print("Rapport écrit : validation_report.csv")
    print("Résumé écrit : validation_summary.txt")

if __name__ == '__main__':
    main()
