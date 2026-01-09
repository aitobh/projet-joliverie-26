#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
createPassword.py
Usage :
    python createPassword.py <N> [length]
- <N>     : nombre de mots de passe à générer (obligatoire)
- [length]: longueur minimale (par défaut 12)
Génère usersPassword2.csv avec une seule colonne `password`.
"""
import sys
import random
import string
import pandas as pd

LOWERS = list(string.ascii_lowercase)  # inclut 'o'
UPPERS = [c for c in string.ascii_uppercase if c != 'O']
DIGITS = list('123456789')
SPECIALS = list('!@#$%&*+-=.<>/?')
COMMON_SUBSTRINGS = {
    'mot','test','azerty','bonjour','admin','util','pass','mdp','secret',
    'word','qwerty','hello','user','love','name'
}

def generate_password(length=12):
    if length < 12:
        length = 12
    chars = [random.choice(UPPERS), random.choice(UPPERS),
             random.choice(LOWERS), random.choice(LOWERS),
             random.choice(DIGITS), random.choice(DIGITS),
             random.choice(SPECIALS), random.choice(SPECIALS)]
    allowed_pool = UPPERS + LOWERS + DIGITS + SPECIALS
    while len(chars) < length:
        chars.append(random.choice(allowed_pool))
    for _ in range(100):
        random.shuffle(chars)
        if chars[0] not in SPECIALS and chars[-1] not in SPECIALS:
            break
    candidate = ''.join(chars)
    lower_cand = candidate.lower()
    for sub in COMMON_SUBSTRINGS:
        if sub in lower_cand:
            return generate_password(length)
    return candidate


def create_password_list(n, length=12):
    seen = set()
    res = []
    attempts = 0
    while len(res) < n and attempts < n*20:
        attempts += 1
        pwd = generate_password(length)
        if pwd not in seen:
            seen.add(pwd)
            res.append(pwd)
    return res


def main():
    if len(sys.argv) < 2:
        print('Usage: python createPassword.py <N> [length]')
        sys.exit(1)
    n = int(sys.argv[1])
    length = int(sys.argv[2]) if len(sys.argv) > 2 else 12
    lst = create_password_list(n, length)
    df = pd.DataFrame({'password': lst})
    df.to_csv('usersPassword2.csv', index=False)
    print(f'Generated {len(lst)} passwords into usersPassword2.csv')

if __name__ == '__main__':
    main()
