import pandas as pds

# Fonction de recherche binaire avec Pandas
def recherche_binaire_pandas(df, critere, valeur):
    if critere == "prix":
        # Utilisation de la méthode Pandas pour effectuer une recherche binaires sur la colonne 'Prix'
        df = df[df['Prix'] <= float(valeur)]  # Filtrage par prix inférieur ou égal à la valeur
        if not df.empty:
            # Retourner l'élément avec le prix le plus proche de la valeur recherchée
            return df.iloc[df['Prix'].idxmin()]
    elif critere == "quantite":
        # Recherche basée sur la quantité
        df = df[df['Quantité'] == int(valeur)]  # Filtrage par quantité exacte
        if not df.empty:
            return df.iloc[0]
    elif critere == "produit":
        # Recherche basée sur le nom du produit
        df = df[df['Produit'].str.strip().str.lower() == valeur.strip().lower()]  # Filtrage par produit
        if not df.empty:
            return df.iloc[0]
    
    return None  # Retourne None si rien n'a été trouvé

# Fonction principale avec Pandas
def fonctionrecherchebinaire(nom_fichier, critere, valeur):
    chemin_fichier = f'data/{nom_fichier}'
    try:
        # Lire le fichier CSV avec pandas
        produits_df = pds.read_csv(chemin_fichier)

        # Vérifier que le fichier contient les bonnes colonnes
        if not all(col in produits_df.columns for col in ['Produit', 'Prix', 'Quantité']):
            print("Erreur : Le fichier doit contenir les colonnes 'Produit', 'Prix' et 'Quantité'.")
            return

        # Supprimer les lignes où le produit est manquant
        produits_df = produits_df.dropna(subset=['Produit'])

        # Convertir les valeurs de la colonne 'Prix' et 'Quantité' en types numériques
        produits_df['Prix'] = produits_df['Prix'].replace('[^0-9.,]', '', regex=True).astype(float)
        produits_df['Quantité'] = produits_df['Quantité'].replace('[^0-9]', '', regex=True).astype(int)

        # Trier les produits par le critère choisi (s'assurer que c'est bien trié)
        if critere.lower() == "prix":
            produits_df = produits_df.sort_values(by='Prix')
        elif critere.lower() == "quantite":
            produits_df = produits_df.sort_values(by='Quantité')
        elif critere.lower() == "produit":
            produits_df = produits_df.sort_values(by='Produit')

        # Recherche binaire avec Pandas
        produit_trouve = recherche_binaire_pandas(produits_df, critere.lower(), valeur)

        # Affichage du résultat
        if produit_trouve is not None:
            print(f"\nProduit trouvé pour '{critere}' = {valeur} :")
            print(f"Produit: {produit_trouve['Produit']}, Prix: {produit_trouve['Prix']}€, Quantité: {produit_trouve['Quantité']} unités")
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

