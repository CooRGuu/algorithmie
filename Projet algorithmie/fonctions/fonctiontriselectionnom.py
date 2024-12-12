import re

def fonctiontriparnom(nom_fichier):
    try:
        # Lire le contenu du fichier
        with open(nom_fichier, 'r', encoding='utf-8') as file:
            lignes = file.readlines()

        # Afficher les lignes lues pour diagnostic
        print("Lignes lues depuis le fichier :")
        for ligne in lignes:
            print(f"'{ligne}'")  # Afficher chaque ligne pour identifier les problèmes potentiels

        # Si le fichier est vide ou ne contient que des lignes vides
        if not lignes or all(ligne.strip() == "" for ligne in lignes):
            print("Le fichier est vide, aucun tri à effectuer.")
            return

        # Convertir les lignes du fichier en une liste de produits
        produits = []
        for ligne in lignes:
            try:
                # Enlever les espaces ou retours à la ligne inutiles
                ligne = ligne.strip()
                if not ligne:  # Ignorer les lignes vides
                    continue

                # Diviser la ligne en nom, prix, et quantité
                # Vérification de la structure de la ligne
                parts = ligne.split(',')
                if len(parts) != 3:
                    print(f"Erreur de format dans la ligne : '{ligne}'")
                    continue  # Ignorer cette ligne et passer à la suivante

                nom, prix_quantite, quantite = parts

                # Nettoyer les valeurs prix et quantité
                prix = prix_quantite.replace('€', '').strip()  # Enlever le symbole €
                quantite = quantite.replace('unités', '').strip()  # Enlever "unités"
                
                # Ajouter à la liste des produits
                produits.append([nom.strip(), float(prix), int(quantite)])

            except ValueError as e:
                print(f"Erreur de format dans la ligne : '{ligne}' -> {e}")
                continue  # Ignorer cette ligne et passer à la suivante

        if not produits:
            print("Aucun produit valide n'a été trouvé dans le fichier.")
            return

        # Algorithme de tri par sélection (selection sort)
        for i in range(len(produits)):
            min_idx = i
            for j in range(i + 1, len(produits)):
                if produits[j][0].lower() < produits[min_idx][0].lower():
                    min_idx = j
            produits[i], produits[min_idx] = produits[min_idx], produits[i]

        # Affichage des produits triés dans le terminal
        print(f"\nProduits triés par nom dans le fichier '{nom_fichier}' :")
        for produit in produits:
            print(f"{produit[0]} | Prix: {produit[1]} | Quantité: {produit[2]}")
    
    except FileNotFoundError:
        print(f"Erreur : Le fichier '{nom_fichier}' n'a pas été trouvé.")
    except Exception as e:
        print(f"Une erreur est survenue : {e}")
