from Fonctions.GestionFichiers.fonctionajout import *
from Fonctions.GestionFichiers.fonctioncreer import *
from Fonctions.GestionFichiers.fonctionlire import *
from Fonctions.GestionFichiers.fonctionsupp import *
from Fonctions.Recherche.fonctionrecherchesequentielle import *
from Fonctions.Recherche.fonctionrecherchebinaire import *
from Fonctions.Tri.fonctiontriselectionnom import *
from Fonctions.Tri.fonctiontribulleprix import *
from Fonctions.Tri.fonctiontriinsertionquantite import *
from Fonctions.Tri.fonctiontrirapide import *
from Fonctions.Utilisateurs.utilisateurs import *
from Fonctions.Admin.usermodification import *
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import hashlib
import csv

# Fonction pour hacher un mot de passe
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Fonction pour vérifier le mot de passe
def verify_password(input_password, stored_hash):
    return hash_password(input_password) == stored_hash

def menu_principal(nom_utilisateur=None):
    while True:
        print("\n--- Menu principal ---")
        print("1- Inscription")
        print("2- Connexion")
        print("3- Quitter")
        choix = input("Entrez votre choix : ").strip()

        if choix == "1":
            inscription()  # Assurez-vous que cette fonction est définie
        elif choix == "2":
            nom_utilisateur = connexion()  # Assurez-vous que cette fonction retourne le nom d'utilisateur
            if nom_utilisateur:
                menu_utilisateur(nom_utilisateur)  # Passer le nom d'utilisateur
        elif choix == "3":
            print("Au revoir !")
            break
        else:
            print("Choix invalide. Veuillez réessayer.")

def menu_utilisateur(nom_utilisateur):
    while True:
        print(f"\n=== Menu Déroulant pour {nom_utilisateur} ===")
        print("1. Créer une liste")
        print("2. Ajouter un produit")
        print("3. Lire un fichier")
        print("4. Supprimer le contenu d'un fichier")
        print("5. Recherche")
        print("6. Trier par nom")
        print("7. Trier par prix")
        print("8. Trier par quantité")
        print("9. Modifier mes informations") 
        print("10. Retour au menu principal")

        choix = input("Entrez le numéro de la fonction que vous souhaitez effectuer : ").strip()

        if choix == "1":
            fonctioncreer()
        elif choix == "2":
            nom_fichier = input("Entrez le nom du fichier .csv dans lequel ajouter un produit : ").strip()
            produit = input("Entrez le nom du produit : ").strip()
            prix = float(input("Entrez le prix du produit (en euros) : ").strip())
            quantite = int(input("Entrez la quantité du produit : ").strip())
            fonctionajout(nom_fichier, produit, prix, quantite, nom_utilisateur)
        elif choix == "3":
            nom_fichier = input("Entrez le nom du fichier à lire : ").strip()
            fonctionlire(nom_fichier, nom_utilisateur)
        elif choix == "4":
            nom_fichier = input("Entrez le nom du fichier désiré : ").strip()
            fonctionsupp(nom_fichier)
        elif choix == "5":
            fichier = input("Entrez le nom du fichier où rechercher : ").strip()
            critere = input("Rechercher par (produit/prix/quantite) : ").strip().lower()
            valeur = input(f"Entrez la valeur à rechercher pour {critere}: ").strip()
            fonctionrecherchesequentielle(fichier, critere, valeur, nom_utilisateur)
        elif choix == "6":
            nom_fichier = input("Entrez le nom du fichier à trier : ").strip()
            fonctiontriparnom(nom_fichier, nom_utilisateur)
        elif choix == "7":
            nom_fichier = input("Entrez le nom du fichier à trier : ").strip()
            fonctiontriparprix(nom_fichier, nom_utilisateur)
        elif choix == "8":
            nom_fichier = input("Entrer le nom du fichier à trier : ").strip()
            fonctiontriparquantite(nom_fichier, nom_utilisateur)
        elif choix == "9":
            modifier_utilisateur(nom_utilisateur)
        elif choix == "10":
            break
        else:
            print("Choix invalide, veuillez entrer une valeur correcte.")

