import pandas as pds

def fonctionrecherchesequentielle(nom_fichier, critere, valeur):
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

        # Recherche selon le critère (prix, quantite, nom)
        correspondances = []

        # Normalisation de la valeur recherchée et du nom des produits (pour la casse)
        valeur_normalisee = valeur.strip().lower()

        for index, row in produits_df.iterrows():
            # Normaliser le nom pour la comparaison
            nom_produit = row['Nom'].strip().lower()

            # Comparer la valeur selon le critère choisi
            if critere == "prix":
                # Comparer en prenant en compte une tolérance pour les erreurs de précision
                if abs(row['Prix'] - float(valeur)) < 0.01:  # On tolère une petite marge d'erreur pour le prix
                    correspondances.append(f"Nom: {row['Nom']}, Prix: {row['Prix']}€, Quantité: {row['Quantité']} unités")
            elif critere == "quantite":
                if row['Quantité'] == int(valeur):
                    correspondances.append(f"Nom: {row['Nom']}, Prix: {row['Prix']}€, Quantité: {row['Quantité']} unités")
            elif critere == "nom":
                if valeur_normalisee in nom_produit:  # Recherche insensible à la casse
                    correspondances.append(f"Nom: {row['Nom']}, Prix: {row['Prix']}€, Quantité: {row['Quantité']} unités")

        # Affichage des résultats de la recherche
        if correspondances:
            print(f"\nCorrespondances trouvées pour '{critere}' = {valeur} :")
            for correspondance in correspondances:
                print(correspondance)
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
