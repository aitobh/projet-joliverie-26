#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generateur de logins pour MariaDB (Étape 07)
Usage :
    python genererLoginToulouse.py <users_csv> <passwords_csv> [output_csv]
Sortie :
    CSV avec séparateur `;` et colonnes : login;password;lastname;firstname
"""
import sys, re, unicodedata
import pandas as pd

USER_COLS_LAST = ['lastname','last_name','nom','sn','surname']
USER_COLS_FIRST = ['firstname','first_name','prenom','givenname','given_name']

def strip_accents(s: str) -> str:
    s = s.replace('œ', 'oe').replace('Œ', 'oe').replace('æ','ae').replace('Æ','ae')
    s = unicodedata.normalize('NFD', s)
    return ''.join(ch for ch in s if unicodedata.category(ch) != 'Mn')

def clean_name(name: str) -> str:
    if not isinstance(name, str): name = str(name) if name is not None else ''
    s = strip_accents(name.strip())
    s = re.sub(r"[-'`\.\s]", '', s)
    return re.sub(r"[^A-Za-z]", '', s)

def proper_case(name: str) -> str:
    if not name: return ''
    name = strip_accents(name).strip()
    parts = re.split(r'(\s|-)', name)
    out = []
    for p in parts:
        if p in [' ', '-']: out.append(p)
        else: out.append(p.capitalize())
    return ''.join(out)

def detect_column(df, candidates):
    for c in candidates:
        if c in df.columns: return c
    lower_map = {c.lower(): c for c in df.columns}
    for c in candidates:
        if c in lower_map: return lower_map[c]
    return None

def read_csv_anysep(path):
    # Essaie d'inférer le séparateur (`,` ou `;` principalement)
    try:
        return pd.read_csv(path, sep=None, engine='python')
    except Exception:
        # Repli sur `;` puis `,`
        try:
            return pd.read_csv(path, sep=';')
        except Exception:
            return pd.read_csv(path)

def main():
    if len(sys.argv) < 3:
        print('Usage: python genererLoginToulouse.py <users_csv> <passwords_csv> [output_csv]')
        sys.exit(1)
    users_csv = sys.argv[1]
    pw_csv = sys.argv[2]
    out_csv = sys.argv[3] if len(sys.argv) > 3 else 'loginToulouse.csv'

    users = read_csv_anysep(users_csv)
    pw = read_csv_anysep(pw_csv)
    if 'password' not in pw.columns:
        raise SystemExit("Le fichier des mots de passe doit contenir une colonne 'password'.")

    col_last = detect_column(users, USER_COLS_LAST)
    col_first = detect_column(users, USER_COLS_FIRST)
    if not col_last or not col_first:
        raise SystemExit('Impossible de détecter les colonnes nom/prénom dans users_csv.')

    ln_raw = users[col_last].astype(str)
    fn_raw = users[col_first].astype(str)
    ln_clean = ln_raw.apply(clean_name)
    fn_clean = fn_raw.apply(clean_name)
    login = (fn_clean.str[:1].str.lower() + ln_clean.str.lower())
    lastname_out = ln_raw.apply(lambda x: strip_accents(str(x)).upper())
    firstname_out = fn_raw.apply(lambda x: proper_case(str(x)))

    if len(pw) < len(users):
        raise SystemExit('Nombre de mots de passe insuffisant par rapport aux utilisateurs.')
    pw = pw.iloc[:len(users)].copy()

    out = pd.DataFrame({'login': login,
                        'password': pw['password'],
                        'lastname': lastname_out,
                        'firstname': firstname_out})
    out.to_csv(out_csv, index=False, sep=';')
    print(f'Fichier généré : {out_csv} ({len(out)} lignes)')

if __name__ == '__main__':
    main()
