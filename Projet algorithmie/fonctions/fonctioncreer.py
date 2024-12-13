import pandas as pds

def fonctioncreer():
    try:
        # Demander à l'utilisateur de saisir le nom du fichier CSV à créer
        nom_fichier = input("Entrez le nom du fichier en .csv à créer : ")

        # Vérifier que l'utilisateur a bien spécifié l'extension .csv
        if not nom_fichier.lower().endswith('.csv'):
            nom_fichier += '.csv'

        # Créer un DataFrame vide avec des colonnes 'Nom', 'Prix', et 'Quantité'
        df = pds.DataFrame(columns=["Nom", "Prix", "Quantité"])

        # Sauvegarder le DataFrame dans un fichier CSV
        df.to_csv(nom_fichier, index=False, encoding='utf-8')

        print(f"Le fichier '{nom_fichier}' a été créé avec succès.")

    except Exception as e:
        print(f"Erreur inconnue : {e}")
