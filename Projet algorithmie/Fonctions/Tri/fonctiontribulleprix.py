import pandas as pds

# Fonction principale pour trier par prix en utilisant les fonctionnalités de tri de Pandas
def fonctiontriparprix(nom_fichier, proprietaire):
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

        print(f"\nContenu du fichier '{nom_fichier}' pour le propriétaire '{proprietaire}' :")
        if df_proprietaire.empty:
            print("Aucun produit trouvé pour ce propriétaire.")
            return

        # Nettoyage et conversion des prix
        try:
            df_proprietaire['Prix'] = df_proprietaire['Prix'].replace('[^0-9.,]', '', regex=True).astype(float)
        except ValueError as e:
            print("Erreur lors de la conversion des prix. Vérifiez le format des données.")
            print(f"Détail de l'erreur : {e}")
            return

        # Trier le DataFrame par prix en ordre croissant
        df_proprietaire_sorted = df_proprietaire.sort_values(by='Prix')

        # Affichage des produits triés par prix
        print(f"\nProduits triés par prix pour le propriétaire '{proprietaire}' :")
        for _, row in df_proprietaire_sorted.iterrows():
            print(f"{row['Produit']} | Prix: {row['Prix']}€ | Quantité: {row['Quantité']} unités")

    except FileNotFoundError:
        print(f"Erreur : Le fichier '{nom_fichier}' n'a pas été trouvé.")
    except pds.errors.EmptyDataError:
        print(f"Erreur : Le fichier '{nom_fichier}' est vide.")
    except pds.errors.ParserError:
        print(f"Erreur : Le fichier '{nom_fichier}' contient un format invalide.")
    except Exception as e:
        print(f"Une erreur est survenue : {e}")

