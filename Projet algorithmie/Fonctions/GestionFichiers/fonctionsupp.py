import pandas as pds

def fonctionsupp(nom_fichier, proprietaire):
    try:
        # Ajouter le chemin relatif pour lire le fichier depuis le dossier Data
        chemin_fichier = f"Data/{nom_fichier}"

        # Lire le fichier CSV avec pandas
        df = pds.read_csv(chemin_fichier, encoding='utf-8')

        # Vérifier si le fichier est vide
        if df.empty:
            print(f"Le fichier '{chemin_fichier}' est vide.")
            return

        # Filtrer le DataFrame pour ne garder que les produits du propriétaire spécifié
        df_proprietaire = df[df['Propriétaire'] == proprietaire]

        if df_proprietaire.empty:
            print(f"Aucun produit trouvé pour le propriétaire '{proprietaire}'.")
            return

        print(f"Contenu du fichier '{chemin_fichier}' pour le propriétaire '{proprietaire}' :")
        # Afficher les produits
        for i, row in df_proprietaire.iterrows():
            print(f"{i+1}. {row['Produit']} | Prix: {row['Prix']} | Quantité: {row['Quantité']} unités | Propriétaire: {row['Propriétaire']}")

        # Demander à l'utilisateur de choisir un produit à supprimer
        choix = int(input("Entrez le numéro du produit à supprimer (0 pour tout supprimer) : "))
        
        if choix == 0:
            # Supprimer tout le contenu du fichier
            df.drop(df.index, inplace=True)
            df.to_csv(chemin_fichier, index=False, encoding='utf-8')
            print(f"Tout le contenu du fichier '{chemin_fichier}' a été supprimé.")
        elif 1 <= choix <= len(df_proprietaire):
            # Supprimer le produit sélectionné
            produit_supprime = df_proprietaire.iloc[choix - 1]['Produit']  # Sauvegarder le Produit du produit avant suppression
            df = df.drop(df.index[df.index[df['Produit'] == produit_supprime][0]])  # Supprimer le produit du DataFrame original
            df.to_csv(chemin_fichier, index=False, encoding='utf-8')
            print(f"Le produit '{produit_supprime}' a été supprimé du fichier '{chemin_fichier}'.")
        else:
            print("Choix invalide.")
    
    except ValueError:
        print("Erreur: Veuillez entrer un numéro valide.")
    except FileNotFoundError:
        print(f"Erreur: Le fichier '{chemin_fichier}' est introuvable.")
    except Exception as e:
        print(f'Erreur inconnue: {e}')
