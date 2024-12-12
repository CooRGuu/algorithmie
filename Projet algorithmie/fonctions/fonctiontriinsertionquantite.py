def fonctiontriparquantite(nom_fichier):
    try:
        # Lire le contenu du fichier
        with open(nom_fichier, 'r', encoding='utf-8') as file:
            lignes = file.readlines()

        # Vérification si le fichier est vide
        if not lignes:
            print("Le fichier est vide, aucun tri à effectuer.")
            return

        # Convertir les lignes du fichier en une liste de produits
        produits = []
        for ligne in lignes:
            try:
                # Nettoyage de la ligne
                ligne = ligne.strip()
                if not ligne:  # Ignorer les lignes vides
                    continue
                
                # Si la ligne est une ligne d'en-tête, on l'ignore
                if ligne.lower().startswith("liste de produits"):
                    continue

                # Diviser la ligne en nom, prix et quantité
                parts = ligne.split(',')
                if len(parts) != 3:
                    print(f"Erreur de format dans la ligne : '{ligne}'")
                    continue  # Ignorer cette ligne si elle n'a pas 3 parties

                nom, prix_quantite, quantite = parts

                # Nettoyer les valeurs prix et quantité
                prix = prix_quantite.replace('€', '').strip()  # Enlever le symbole €
                quantite = quantite.replace('unités', '').strip()  # Enlever "unités"
                
                # Ajouter à la liste des produits
                produits.append([nom.strip(), float(prix), int(quantite)])

            except ValueError as e:
                print(f"Erreur de format dans la ligne : '{ligne}' -> {e}")
                continue  # Ignorer cette ligne et passer à la suivante

        # Vérifier si des produits valides ont été ajoutés
        if not produits:
            print("Aucun produit valide n'a été trouvé dans le fichier.")
            return

        # Algorithme de tri par insertion pour trier par quantité
        for i in range(1, len(produits)):
            current = produits[i]
            j = i - 1
            # Déplacer les éléments plus grands que current vers la droite
            while j >= 0 and produits[j][2] > current[2]:  # Comparer les quantités
                produits[j + 1] = produits[j]
                j -= 1
            produits[j + 1] = current

        # Affichage des produits triés par quantité dans le terminal
        print(f"\nProduits triés par quantité dans le fichier '{nom_fichier}' :")
        for produit in produits:
            print(f"{produit[0]} | Prix: {produit[1]}€ | Quantité: {produit[2]} unités")

    except FileNotFoundError:
        print(f"Erreur : Le fichier '{nom_fichier}' n'a pas été trouvé.")
    except Exception as e:
        print(f"Une erreur est survenue : {e}")
