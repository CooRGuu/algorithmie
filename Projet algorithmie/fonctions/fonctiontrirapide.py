import pandas as pds

def fonctiontrirapide(nom_fichier):
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

        # Fonction de partitionnement pour le tri rapide
        def partition(df, low, high):
            pivot = df.iloc[high]['Quantité']
            i = low - 1
            for j in range(low, high):
                if df.iloc[j]['Quantité'] < pivot:
                    i += 1
                    df.iloc[i], df.iloc[j] = df.iloc[j], df.iloc[i]  # Échanger les lignes
            df.iloc[i + 1], df.iloc[high] = df.iloc[high], df.iloc[i + 1]
            return i + 1

        # Fonction de tri rapide
        def quicksort(df, low, high):
            if low < high:
                pi = partition(df, low, high)
                quicksort(df, low, pi - 1)
                quicksort(df, pi + 1, high)

        # Appliquer le tri rapide sur les produits par quantité
        quicksort(produits_df, 0, len(produits_df) - 1)

        # Affichage des produits triés par quantité
        print(f"\nProduits triés par quantité dans le fichier '{nom_fichier}' :")
        for index, row in produits_df.iterrows():
            print(f"{row['Nom']} | Prix: {row['Prix']} | Quantité: {row['Quantité']} unités")

    except FileNotFoundError:
        print(f"Erreur : Le fichier '{nom_fichier}' n'a pas été trouvé.")
    except pds.errors.EmptyDataError:
        print(f"Erreur : Le fichier '{nom_fichier}' est vide.")
    except pds.errors.ParserError:
        print(f"Erreur : Le fichier '{nom_fichier}' contient un format invalide.")
    except Exception as e:
        print(f"Une erreur est survenue : {e}")
