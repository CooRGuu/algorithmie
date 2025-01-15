import pandas as pds

def fonctionrecherchesequentielle(nom_fichier, critere, valeur, proprietaire):
    chemin_fichier = f'data/{nom_fichier}'
    try:
        # Lire le fichier CSV avec pandas
        produits_df = pds.read_csv(chemin_fichier)

        # Vérifier que le fichier contient les bonnes colonnes
        colonnes_requises = {'Produit', 'Prix', 'Quantité', 'Propriétaire'}
        if not colonnes_requises.issubset(produits_df.columns):
            print(f"Erreur : Le fichier doit contenir les colonnes {', '.join(colonnes_requises)}.")
            return

        # Convertir les colonnes 'Prix' et 'Quantité' en types numériques
        produits_df['Prix'] = produits_df['Prix'].replace('[^0-9.,]', '', regex=True).astype(float)
        produits_df['Quantité'] = produits_df['Quantité'].replace('[^0-9]', '', regex=True).astype(int)

        # Normaliser la valeur pour la recherche
        valeur_normalisee = str(valeur).strip().lower()

        # Filtrer les produits par propriétaire
        produits_df = produits_df[produits_df['Propriétaire'].str.strip().str.lower() == proprietaire.lower()]

        # Recherche par critère et filtrage avec Pandas
        if critere.lower() == "prix":
            # Comparer le prix avec une tolérance de 0.01
            correspondances = produits_df[produits_df['Prix'].apply(lambda x: abs(x - float(valeur)) < 0.01)]

        elif critere.lower() == "quantite":
            # Recherche des produits ayant la même quantité
            correspondances = produits_df[produits_df['Quantité'] == int(valeur)]

        elif critere.lower() == "produit":
            # Recherche de produits contenant la valeur dans leur nom
            correspondances = produits_df[produits_df['Produit'].str.strip().str.lower().str.contains(valeur_normalisee)]

        # Affichage des résultats
        if not correspondances.empty:
            print(f"\nCorrespondances trouvées pour '{critere}' = {valeur} (Propriétaire: {proprietaire}) :")
            for _, row in correspondances.iterrows():
                print(f"Produit: {row['Produit']}, Prix: {row['Prix']}€, Quantité: {row['Quantité']} unités")
        else:
            print(f"Aucune correspondance trouvée pour '{critere}' = {valeur} (Propriétaire: {proprietaire}).")

    except FileNotFoundError:
        print(f"Erreur : Le fichier '{nom_fichier}' n'a pas été trouvé.")
    except pds.errors.EmptyDataError:
        print(f"Erreur : Le fichier '{nom_fichier}' est vide.")
    except pds.errors.ParserError:
        print(f"Erreur : Le fichier '{nom_fichier}' contient un format invalide.")
    except Exception as e:
        print(f"Une erreur est survenue : {e}")

