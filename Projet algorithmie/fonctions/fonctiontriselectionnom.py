import pandas as pds

def fonctiontriparnom(nom_fichier):
    try:
        # Lire le fichier CSV dans un DataFrame
        df = pds.read_csv(nom_fichier)

        # Afficher les données lues pour diagnostic
        print("Données lues depuis le fichier :")
        print(df)

        # Vérifier si le DataFrame est vide
        if df.empty:
            print("Le fichier est vide, aucun tri à effectuer.")
            return

        # Vérification de la structure des colonnes
        if 'Nom' not in df.columns or 'Prix' not in df.columns or 'Quantité' not in df.columns:
            print("Erreur : Le fichier doit contenir les colonnes 'Nom', 'Prix' et 'Quantité'.")
            return

        # Trier le DataFrame par la colonne 'Nom'
        df_sorted = df.sort_values(by='Nom')

        # Affichage des produits triés
        print(f"\nProduits triés par nom dans le fichier '{nom_fichier}' :")
        for index, row in df_sorted.iterrows():
            print(f"{row['Nom']} | Prix: {row['Prix']} | Quantité: {row['Quantité']} unités")

    except FileNotFoundError:
        print(f"Erreur : Le fichier '{nom_fichier}' n'a pas été trouvé.")
    except Exception as e:
        print(f"Une erreur est survenue : {e}")