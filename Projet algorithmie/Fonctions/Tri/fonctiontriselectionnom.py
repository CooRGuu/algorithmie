import pandas as pds

def fonctiontriparnom(nom_fichier, proprietaire):
    chemin_fichier = f'data/{nom_fichier}'
    try:
        # Lire le fichier CSV dans un DataFrame
        df = pds.read_csv(chemin_fichier)
        
        # Vérification si le DataFrame est vide
        if df.empty:
            print("Le fichier est vide, aucun tri à effectuer.")
            return

        # Vérification de la structure des colonnes
        colonnes_requises = {'Produit', 'Prix', 'Quantité', 'Propriétaire'}
        if not colonnes_requises.issubset(df.columns):
            print(f"Erreur : Le fichier doit contenir les colonnes {', '.join(colonnes_requises)}.")
            return

        # Filtrer le DataFrame pour ne garder que les produits du propriétaire spécifié
        df_proprietaire = df[df['Propriétaire'] == proprietaire]

        if df_proprietaire.empty:
            print(f"Aucun produit trouvé pour le propriétaire '{proprietaire}'.")
            return

        # Trier les produits du propriétaire par la colonne 'Produit'
        df_sorted = df_proprietaire.sort_values(by='Produit')

        # Affichage des produits triés
        print(f"\nProduits triés pour le propriétaire '{proprietaire}' dans le fichier '{nom_fichier}' :")
        print(df_sorted[['Produit', 'Prix', 'Quantité']].to_string(index=False))

    except FileNotFoundError:
        print(f"Erreur : Le fichier '{nom_fichier}' n'a pas été trouvé.")
    except Exception as e:
        print(f"Une erreur est survenue : {e}")
