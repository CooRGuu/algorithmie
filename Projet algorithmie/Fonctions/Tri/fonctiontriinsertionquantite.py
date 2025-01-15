import pandas as pds

# Fonction principale pour trier par quantité avec Pandas
def fonctiontriparquantite(nom_fichier, proprietaire):
    chemin_fichier = f'data/{nom_fichier}'

    try:
        # Lire le fichier CSV avec pandas
        produits_df = pds.read_csv(chemin_fichier)

        # Vérification des colonnes requises
        colonnes_requises = {'Produit', 'Prix', 'Quantité', 'Propriétaire'}
        if not colonnes_requises.issubset(produits_df.columns):
            print(f"Erreur : Le fichier doit contenir les colonnes {', '.join(colonnes_requises)}.")
            return

        # Filtrer les produits appartenant au propriétaire spécifié
        df_proprietaire = produits_df[produits_df['Propriétaire'] == proprietaire].copy()

        # Si aucun produit n'est trouvé pour ce propriétaire
        if df_proprietaire.empty:
            print(f"Aucun produit trouvé pour le propriétaire '{proprietaire}'.")
            return

        # Nettoyage et conversion des colonnes 'Prix' et 'Quantité'
        try:
            df_proprietaire['Prix'] = df_proprietaire['Prix'].replace('[^0-9.,]', '', regex=True).astype(float)
            df_proprietaire['Quantité'] = df_proprietaire['Quantité'].replace('[^0-9]', '', regex=True).astype(int)
        except ValueError as e:
            print("Erreur lors de la conversion des données. Vérifiez le format des colonnes.")
            print(f"Détail de l'erreur : {e}")
            return

        # Trier les produits par la colonne 'Quantité' de manière croissante
        df_proprietaire_sorted = df_proprietaire.sort_values(by='Quantité', ascending=True)

        # Affichage des produits triés par quantité
        print(f"\nProduits triés par quantité pour le propriétaire '{proprietaire}' :")
        for _, produit in df_proprietaire_sorted.iterrows():
            print(f"{produit['Produit']} | Prix: {produit['Prix']}€ | Quantité: {produit['Quantité']} unités")

    except FileNotFoundError:
        print(f"Erreur : Le fichier '{nom_fichier}' n'a pas été trouvé.")
    except pds.errors.EmptyDataError:
        print(f"Erreur : Le fichier '{nom_fichier}' est vide.")
    except pds.errors.ParserError:
        print(f"Erreur : Le fichier '{nom_fichier}' contient un format invalide.")
    except Exception as e:
        print(f"Une erreur est survenue : {e}")

