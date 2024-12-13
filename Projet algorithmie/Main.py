from fonctions.fonctionajout import *
from fonctions.fonctioncreer import *
from fonctions.fonctionlire import *
from fonctions.fonctionsupp import *
from fonctions.fonctionrecherchesequentielle import *
from fonctions.fonctionrecherchebinaire import *
from fonctions.fonctiontriselectionnom import *
from fonctions.fonctiontribulleprix import *
from fonctions.fonctiontriinsertionquantite import *
from fonctions.fonctiontrirapide import *

def menuderoulant():
    print("\n--- Menu ---")
    print("1- Créer une nouvelle liste")
    print("2- Ajouter un nouveau produit à la liste")
    print("3- Lire le contenu de la liste")
    print("4- Supprimer le contenu de la liste")
    print("5- Rechercher un produit (Séquentielle)")
    print("6- Rechercher un produit (Binaire)")
    print("7- Trier les produits par nom")
    print("8- Trier les produits par prix")
    print("9- Trier les produits par quantité")
    print("10- Trier les produits par qantité avec le tri rapide")
    print("11- Quitter")
    
def main():
    while True: 
        menuderoulant()
        choix = input("Entrez le numéro de la fonction que vous souhaitez effectuer : ")
        
        if choix == "1":
            fonctioncreer()

        elif choix == "2":
            print("Option 2 choisie : Ajouter un produit.")
            nom_fichier = input("Entrez le nom du fichier .csv dans lequel ajouter un produit : ")
            print(f"Fichier choisi : {nom_fichier}")

            produit = input("Entrez le nom du produit à ajouter : ")
            print(f"Produit choisi : {produit}")
            prix = None
            while prix is None:
                try:
                    prix = float(input("Entrez le prix du produit (en euros): "))
                    print(f"Prix choisi : {prix}")
                except ValueError:
                    print("Erreur : veuillez entrer un nombre valide pour le prix.")
            quantite = None
            while quantite is None:
                try:
                    quantite = int(input("Entrez la quantité du produit : "))
                    print(f"Quantité choisie : {quantite}")
                except ValueError:
                    print("Erreur : veuillez entrer un nombre entier pour la quantité.")
            fonctionajout(nom_fichier, produit, prix, quantite)

        elif choix == "3":
            nom_fichier = input("Entrez le nom du fichier à lire : ")
            fonctionlire(nom_fichier)

        elif choix == "4":
            nom_fichier = input("Entrez le nom du fichier désiré : ")
            confirmer = input(f"Confirmer la suppression de contenu du fichier '{nom_fichier}' ? (oui/non) : ")
            if confirmer.lower() == "oui":
                fonctionsupp(nom_fichier)
                print(f"Le contenu du fichier '{nom_fichier}' a été supprimé.")
            else:
                print("Suppression annulée.")

        elif choix == "5":
            # Recherche séquentielle
            fichier = input("Entrez le nom du fichier où rechercher : ").strip()
            critere = input("Rechercher par (nom/prix/quantite) : ").strip().lower()
            valeur = input(f"Entrez la valeur à rechercher pour {critere}: ").strip()
            fonctionrecherchesequentielle(fichier, critere, valeur)
        elif choix == "6":
            # Recherche binaire
            fichier = input("Entrez le nom du fichier où rechercher : ").strip()
            critere = input("Rechercher par (nom/prix/quantite) : ").strip().lower()
            valeur = input(f"Entrez la valeur à rechercher pour {critere}: ").strip()
            fonctionrecherchebinaire(fichier, critere, valeur)
        elif choix == "7":
            nom_fichier = input("Entrez le nom du fichier à trier : ")
            fonctiontriparnom(nom_fichier)
        elif choix == "8":
            nom_fichier = input('Entrez le nom du fichier à trier : ')
            fonctiontriparprix(nom_fichier)
        elif choix == "9":
            nom_fichier = input('Entrer le nom du fichier à trier : ')
            fonctiontriparquantite(nom_fichier)
        elif choix == "10":
            nom_fichier = input('Entrer le nom du fichier à trier : ')
            fonctiontrirapide(nom_fichier)
        elif choix == "11":
            print("Au revoir !")
            break

        else:
            print("Choix invalide, veuillez entrer une valeur correcte.")

if __name__ == "__main__":
    main()