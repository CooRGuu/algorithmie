import pandas as pds

# Fonction de recherche binaire
def recherche_binaire(arr, critere, valeur):
    gauche, droite = 0, len(arr) - 1

    while gauche <= droite:
        milieu = (gauche + droite) // 2
        element = arr[milieu]

        # Comparer l'élément central avec la valeur recherchée
        if critere == "prix":
            if element['Prix'] == float(valeur):
                return element
            elif element['Prix'] < float(valeur):
                gauche = milieu + 1
            else:
                droite = milieu - 1
        elif critere == "quantite":
            if element['Quantité'] == int(valeur):
                return element
            elif element['Quantité'] < int(valeur):
                gauche = milieu + 1
            else:
                droite = milieu - 1
        elif critere == "nom":
            if element['Nom'].lower() == valeur.lower():
                return element
            elif element['Nom'].lower() < valeur.lower():
                gauche = milieu + 1
            else:
                droite = milieu - 1

    return None  # Si aucune correspondance n'est trouvée

# Fonction pour effectuer la recherche binaire
def fonctionrecherchebinaire(nom_fichier, critere, valeur):
    try:
        # Lire le fichier CSV avec pandas
        produits_df = pds.read_csv(nom_fichier)

        # Vérifier que le fichier contient les bonnes colonnes
        if not all(col in produits_df.columns for col in ['Nom', 'Prix', 'Quantité']):
            print("Erreur : Le fichier doit contenir les colonnes 'Nom', 'Prix' et 'Quantité'.")
            return

        # Convertir les valeurs de la colonne 'Prix' et 'Quantité' en types numériques
        produits_df['Prix'] = produits_df['Prix'].replace('€', '', regex=True).astype(float)
        produits_df['Quantité'] = produits_df['Quantité'].replace('unités', '', regex=True).astype(int)

        # Trier les produits par le critère choisi
        if critere == "prix":
            produits_df = produits_df.sort_values(by='Prix')
        elif critere == "quantite":
            produits_df = produits_df.sort_values(by='Quantité')
        elif critere == "nom":
            produits_df = produits_df.sort_values(by='Nom')

        # Convertir le DataFrame en une liste de dictionnaires
        produits_list = produits_df.to_dict(orient='records')

        # Recherche binaire
        produit_trouve = recherche_binaire(produits_list, critere, valeur)

        # Affichage du résultat
        if produit_trouve:
            print(f"\nProduit trouvé pour '{critere}' = {valeur} :")
            print(f"Nom: {produit_trouve['Nom']}, Prix: {produit_trouve['Prix']}€, Quantité: {produit_trouve['Quantité']} unités")
        else:
            print(f"Aucune correspondance trouvée pour '{critere}' = {valeur}.")

    except FileNotFoundError:
        print(f"Erreur : Le fichier '{nom_fichier}' n'a pas été trouvé.")
    except pds.errors.EmptyDataError:
        print(f"Erreur : Le fichier '{nom_fichier}' est vide.")
    except pds.errors.ParserError:
        print(f"Erreur : Le fichier '{nom_fichier}' contient un format invalide.")
    except Exception as e:
        print(f"Une erreur est survenue : {e}")