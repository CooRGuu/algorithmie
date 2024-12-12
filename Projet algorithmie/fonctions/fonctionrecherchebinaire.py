def fonctionrecherchebinaire(nom_fichier, critere, valeur):
    try:
        # Lire le contenu du fichier
        with open(nom_fichier, 'r', encoding='utf-8') as file:
            lignes = file.readlines()

        # Vérifier si le fichier est vide
        if not lignes:
            print(f"Le fichier '{nom_fichier}' est vide.")
            return

        # Liste pour stocker les produits après nettoyage et extraction
        produits = []

        for ligne in lignes:
            try:
                ligne = ligne.strip()
                if not ligne or ligne.lower().startswith("liste de produits"):  # Ignorer les lignes vides ou d'en-tête
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

                produits.append([nom.strip(), float(prix), int(quantite)])

            except ValueError as e:
                print(f"Erreur de format dans la ligne : '{ligne}' -> {e}")
                continue

        # Vérifier si des produits valides ont été extraits
        if not produits:
            print(f"Aucun produit valide n'a été trouvé dans le fichier '{nom_fichier}'.")
            return

        # Trier les produits selon le critère de recherche choisi
        if critere == "prix":
            produits.sort(key=lambda x: x[1])  # Trier par prix
        elif critere == "quantite":
            produits.sort(key=lambda x: x[2])  # Trier par quantité
        elif critere == "nom":
            produits.sort(key=lambda x: x[0].lower())  # Trier par nom

        # Recherche binaire
        def recherche_binaire(arr, key, valeur):
            low, high = 0, len(arr) - 1
            correspondances = []

            while low <= high:
                mid = (low + high) // 2
                mid_value = arr[mid]

                # Comparer la valeur en fonction du critère
                if critere == "prix":
                    mid_value = mid_value[1]  # Comparer par prix
                elif critere == "quantite":
                    mid_value = mid_value[2]  # Comparer par quantité
                elif critere == "nom":
                    mid_value = mid_value[0].lower()  # Comparer par nom

                # Comparer la valeur à rechercher avec la valeur au milieu
                if mid_value == valeur:
                    correspondances.append(arr[mid])  # Correspondance trouvée
                    # Chercher d'autres correspondances à gauche et à droite
                    l, r = mid - 1, mid + 1
                    while l >= 0 and (arr[l][1] == valeur if critere == 'prix' else arr[l][2] == valeur or arr[l][0].lower() == valeur):
                        correspondances.append(arr[l])
                        l -= 1
                    while r < len(arr) and (arr[r][1] == valeur if critere == 'prix' else arr[r][2] == valeur or arr[r][0].lower() == valeur):
                        correspondances.append(arr[r])
                        r += 1
                    break
                elif mid_value < valeur:
                    low = mid + 1
                else:
                    high = mid - 1

            return correspondances

        # Effectuer la recherche binaire
        if critere == "prix":
            correspondances = recherche_binaire(produits, "prix", float(valeur))
        elif critere == "quantite":
            correspondances = recherche_binaire(produits, "quantite", int(valeur))
        elif critere == "nom":
            correspondances = recherche_binaire(produits, "nom", valeur.lower())

        # Affichage des résultats de la recherche
        if correspondances:
            print(f"\nCorrespondances trouvées pour '{critere}' = {valeur} :")
            for correspondance in correspondances:
                print(f"Nom: {correspondance[0]}, Prix: {correspondance[1]}€, Quantité: {correspondance[2]} unités")
        else:
            print(f"Aucune correspondance trouvée pour '{critere}' = {valeur}.")

    except FileNotFoundError:
        print(f"Erreur : Le fichier '{nom_fichier}' n'a pas été trouvé.")
    except Exception as e:
        print(f"Une erreur est survenue : {e}")
