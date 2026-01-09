#
# SCRIPT_NAME : extractUsersPerpignan.ps1
# AUTHOR : Joliverie
# DATE : 16/12/2025
# VERSION : 1.0
# DESCRIPTION :
# Ce script extrait les informations des utilisateurs de l'OU Perpignan
# et les exporte dans un fichier CSV avec les attributs suivants :
# Prenom, Nom, Nom complet, Email, Telephone.
# Fichier encode en UTF-8, separateur virgule, fins de ligne au format Unix (LF)
# NOTES :
# Necessite le module ActiveDirectory.
# Le fichier CSV sera genere dans D:\powershell\usersPerpignan.csv
# Parametres
$Server = "10.15.11.210"
$OUPath = "OU=Toulouse,OU=Finances,DC=stesio,DC=jol"
$OutputFile = "D:\powershell\usersToulouse.csv"
# Recupere les utilisateurs et exporte en CSV
try {
 Get-ADUser -Server $Server -SearchBase $OUPath -Filter * -Properties givenName,
sn, displayName, mail, telephoneNumber |
 Select-Object givenName, sn, displayName, mail, telephoneNumber |
 Export-Csv -Path $OutputFile -Delimiter ";" -Encoding UTF8
-NoTypeInformation -Force
 # Convertit les fins de ligne en format Unix (LF)
 (Get-Content $OutputFile -Raw).Replace("`r`n", "`n") | Set-Content $OutputFile
-NoNewline
 Write-Host "Export reussi : $OutputFile" -ForegroundColor Green
} catch {
 Write-Host "Erreur : $_" -ForegroundColor Red
 Write-Host "Verifie :"
 Write-Host "1. Le chemin de l'OU : $OUPath"
 Write-Host "2. Tes droits d'acces sur ce serveur et cette OU."
 Write-Host "3. Que le module ActiveDirectory est installe."
}
