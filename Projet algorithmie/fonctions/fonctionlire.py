import pandas as pds

def fonctionlire(nom_fichier):
    try:
        # Charger le fichier CSV avec pandas
        df = pds.read_csv(nom_fichier, encoding='utf-8')

        print(f"Contenu du fichier '{nom_fichier}' :")
        print(df)  # Afficher tout le contenu du DataFrame

    except FileNotFoundError:
        print(f"Erreur: Le fichier '{nom_fichier}' est introuvable.")
    except Exception as e:
        print(f"Erreur inconnue: {e}")
