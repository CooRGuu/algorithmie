import pandas as pds

def fonctionchoixfichier():
    """Choisir un fichier CSV et charger avec pandas."""
    
    # Demander à l'utilisateur de saisir le nom ou chemin du fichier CSV
    fichier_choisi = input("Veuillez entrer le chemin du fichier CSV : ")

    try:
        # Charger le fichier CSV choisi avec pandas
        df = pds.read_csv(fichier_choisi)
        print(f"\nAperçu du fichier '{fichier_choisi}':")
        print(df.head())  # Affiche les 5 premières lignes du fichier CSV
        return fichier_choisi  # Retourne le chemin du fichier sélectionné
    except Exception as e:
        print(f"Erreur lors du chargement du fichier CSV : {e}")
        return None
