import pandas as pds

# Fonction de tri par bulle (Bubble Sort) pour trier par prix
def tri_bulle(prix_list):
    n = len(prix_list)
    for i in range(n):
        for j in range(0, n-i-1):
            if prix_list[j]['Prix'] > prix_list[j+1]['Prix']:
                prix_list[j], prix_list[j+1] = prix_list[j+1], prix_list[j]
    return prix_list

# Fonction principale pour trier par prix en utilisant le tri par bulle
def fonctiontriparprix(nom_fichier):
    try:
        # Lire le fichier CSV avec pandas
        produits_df = pds.read_csv(nom_fichier)

        # Vérifier que le fichier contient les bonnes colonnes
        if not all(col in produits_df.columns for col in ['Nom', 'Prix', 'Quantité']):
            print("Erreur : Le fichier doit contenir les colonnes 'Nom', 'Prix' et 'Quantité'.")
            return

        # Convertir la colonne 'Prix' en numérique (supprimer le symbole '€')
        produits_df['Prix'] = produits_df['Prix'].replace('€', '', regex=True).astype(float)

        # Convertir DataFrame en liste de dictionnaires
        produits_list = produits_df.to_dict(orient='records')

        # Appliquer le tri par bulle sur les prix
        produits_sorted = tri_bulle(produits_list)

        # Affichage des produits triés par prix dans le terminal
        print(f"\nProduits triés par prix (tri par bulle) dans le fichier '{nom_fichier}' :")
        for produit in produits_sorted:
            print(f"{produit['Nom']} | Prix: {produit['Prix']}€ | Quantité: {produit['Quantité']} unités")

    except FileNotFoundError:
        print(f"Erreur : Le fichier '{nom_fichier}' n'a pas été trouvé.")
    except pds.errors.EmptyDataError:
        print(f"Erreur : Le fichier '{nom_fichier}' est vide.")
    except pds.errors.ParserError:
        print(f"Erreur : Le fichier '{nom_fichier}' contient un format invalide.")
    except Exception as e:
        print(f"Une erreur est survenue : {e}")

