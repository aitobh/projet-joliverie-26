#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generateur du script SQL de suppression : lit loginToulouseDelete.csv et écrit supprimerUsersBddAcces.sql
Usage:
    python genererScriptSqlDrop.py [input_csv] [output_sql]
"""
import sys, pandas as pd, unicodedata, re, datetime

INPUT = 'loginToulouseDelete.csv'
OUTPUT = 'supprimerUsersBddAcces.sql'
if len(sys.argv) > 1:
    INPUT = sys.argv[1]
if len(sys.argv) > 2:
    OUTPUT = sys.argv[2]

def strip_accents(s: str) -> str:
    s = unicodedata.normalize('NFD', str(s))
    return ''.join(c for c in s if unicodedata.category(c) != 'Mn')

def dbname(login: str) -> str:
    b = strip_accents(login.lower())
    b = re.sub(r'[^a-z0-9]', '', b)
    return f'st_{b}'

def main():
    df = pd.read_csv(INPUT, sep=';')
    ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    lines = [f"-- Script SQL de suppression généré automatiquement le {ts}"]
    for _, r in df.iterrows():
        lg = str(r['login'])
        db = dbname(lg)
        full = f"{r['firstname']} {r['lastname']}"
        lines.append(f"-- Suppression pour: {full} (login: {lg})")
        lines.append(f"DROP DATABASE IF EXISTS {db};")
        lines.append(f"DROP USER IF EXISTS '{lg}'@'%';")
        lines.append("")
    with open(OUTPUT, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print(f"Fichier SQL écrit: {OUTPUT}")

if __name__ == '__main__':
    main()
