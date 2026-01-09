# Ouverture du fichier d'entrée en mode lecture
with open("testEntree.csv", "r", encoding="utf-8") as fichier_entree:
    lignes = fichier_entree.readlines()

# Ouverture du fichier de sortie en mode écriture
with open("testSortie.csv", "w", encoding="utf-8") as fichier_sortie:
    # Écriture de l'en-tête
    fichier_sortie.write("login\n")

    # Parcours des lignes en ignorant l'en-tête
    for ligne in lignes[1:]:
        # Suppression du retour à la ligne et séparation des champs
        prenom, nom = ligne.strip().split(";")

        # Génération du login
        login = (prenom[0] + nom).lower()

        # Écriture du login dans le fichier de sortie
        fichier_sortie.write(login + "\n")