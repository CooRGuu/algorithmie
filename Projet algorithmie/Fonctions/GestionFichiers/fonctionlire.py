import pandas as pds

def fonctionlire(chemin_complet, proprietaire):
    """
    Lire un fichier CSV et afficher les produits associés à un propriétaire spécifique.

    Args:
        chemin_complet (str): Chemin complet vers le fichier CSV.
        proprietaire (str): Nom du propriétaire à filtrer.
    """
    print(f"Lecture du fichier {chemin_complet} pour le propriétaire {proprietaire}.")

    try:
        # Charger le fichier CSV avec pandas en utilisant le chemin complet
        df = pds.read_csv(chemin_complet, encoding='utf-8')

        # Vérifier si le fichier contient une colonne 'Propriétaire'
        if 'Propriétaire' not in df.columns:
            print(f"Erreur: La colonne 'Propriétaire' est absente dans le fichier '{chemin_complet}'.")
            return

        # Filtrer le DataFrame pour ne garder que les produits du propriétaire spécifié
        df_proprietaire = df[df['Propriétaire'] == proprietaire]

        print(f"Contenu du fichier '{chemin_complet}' pour le propriétaire '{proprietaire}':")
        
        if df_proprietaire.empty:
            print("Aucun produit trouvé pour ce propriétaire.")
        else:
            print(df_proprietaire)  # Afficher tout le contenu du DataFrame filtré

    except FileNotFoundError:
        print(f"Erreur: Le fichier '{chemin_complet}' est introuvable.")
    except Exception as e:
        print(f"Erreur inconnue: {e}")
