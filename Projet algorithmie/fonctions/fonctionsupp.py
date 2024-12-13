import pandas as pds

def fonctionsupp(nom_fichier):
    try:
        # Lire le fichier CSV avec pandas
        df = pds.read_csv(nom_fichier, encoding='utf-8')

        # Vérifier si le fichier est vide
        if df.empty:
            print(f"Le fichier '{nom_fichier}' est vide.")
            return

        print(f"Contenu du fichier '{nom_fichier}' :")
        # Afficher les produits
        for i, row in df.iterrows():
            print(f"{i+1}. {row['Nom']} | Prix: {row['Prix']} | Quantité: {row['Quantité']} unités")

        # Demander à l'utilisateur de choisir un produit à supprimer
        choix = int(input("Entrez le numéro du produit à supprimer (0 pour tout supprimer) : "))
        
        if choix == 0:
            # Supprimer tout le contenu du fichier
            df.drop(df.index, inplace=True)
            df.to_csv(nom_fichier, index=False, encoding='utf-8')
            print(f"Tout le contenu du fichier '{nom_fichier}' a été supprimé.")
        elif 1 <= choix <= len(df):
            # Supprimer le produit sélectionné
            df = df.drop(df.index[choix - 1])
            df.to_csv(nom_fichier, index=False, encoding='utf-8')
            print(f"Le produit '{df.iloc[choix - 1]['Nom']}' a été supprimé du fichier '{nom_fichier}'.")
        else:
            print("Choix invalide.")
    
    except ValueError:
        print("Erreur: Veuillez entrer un numéro valide.")
    except FileNotFoundError:
        print(f"Erreur: Le fichier '{nom_fichier}' est introuvable.")
    except Exception as e:
        print(f'Erreur inconnue: {e}')
