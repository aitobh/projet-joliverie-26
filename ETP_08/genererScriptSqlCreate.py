#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Génère le fichier SQL `creerUsersBddAcces.sql` à partir de `loginToulouse.csv`.
- Colonnes attendues : login;password;lastname;firstname (séparateur ;) 
- Pour chaque utilisateur :
  * CREATE USER IF NOT EXISTS 'login'@'%' IDENTIFIED BY 'password';
  * CREATE DATABASE IF NOT EXISTS st_login;
  * GRANT CREATE, ALTER, DROP, INDEX, SELECT, INSERT, UPDATE, DELETE ON st_login.* TO 'login'@'%';
  * FLUSH PRIVILEGES (en fin de script)
"""
import pandas as pd, unicodedata, re, datetime

INPUT = 'loginToulouse.csv'
OUTPUT = 'creerUsersBddAcces.sql'

def strip_accents(s: str) -> str:
    import unicodedata
    s = unicodedata.normalize('NFD', str(s))
    return ''.join(c for c in s if unicodedata.category(c) != 'Mn')

def dbname(login: str) -> str:
    import re
    b = strip_accents(login.lower())
    b = re.sub(r'[^a-z0-9]', '', b)
    return f'st_{b}'

def main():
    df = pd.read_csv(INPUT, sep=';')
    ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    lines = [f"-- Script SQL généré automatiquement le {ts}"]
    for _, r in df.iterrows():
        lg = str(r['login'])
        pw = str(r['password'])
        db = dbname(lg)
        full = f"{r['firstname']} {r['lastname']}"
        lines.append(f"-- Utilisateur: {full}")
        lines.append(f"CREATE USER IF NOT EXISTS '{lg}'@'%' IDENTIFIED BY '{pw}';")
        lines.append(f"CREATE DATABASE IF NOT EXISTS {db};")
        lines.append(f"GRANT CREATE, ALTER, DROP, INDEX, SELECT, INSERT, UPDATE, DELETE ON {db}.* TO '{lg}'@'%';")
        lines.append("")
    lines.append("FLUSH PRIVILEGES;")
    with open(OUTPUT, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print(f"Fichier SQL généré: {OUTPUT}")

if __name__ == '__main__':
    main()
