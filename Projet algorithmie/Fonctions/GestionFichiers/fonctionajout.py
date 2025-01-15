import pandas as pds

def fonctionajout(nom_fichier, produit, prix, quantite, proprietaire):
    # Spécifier directement le chemin du fichier
    chemin_fichier = f'data/{nom_fichier}'

    try:
        # Vérifier si le fichier existe en tentant de le lire
        df = pds.read_csv(chemin_fichier, encoding='utf-8')

    except FileNotFoundError:
        # Si le fichier n'existe pas, on crée un DataFrame vide avec les colonnes appropriées
        df = pds.DataFrame(columns=['Produit', 'Prix', 'Quantité', 'Propriétaire'])

    # Ajouter une nouvelle ligne avec les informations du produit
    nouvelle_ligne = {'Produit': produit, 'Prix': prix, 'Quantité': quantite, 'Propriétaire': proprietaire}
    
    # Utiliser pd.concat pour ajouter la nouvelle ligne
    df = pds.concat([df, pds.DataFrame([nouvelle_ligne])], ignore_index=True)

    # Sauvegarder le DataFrame mis à jour dans le fichier CSV
    df.to_csv(chemin_fichier, index=False, encoding='utf-8')
    print(f"Le produit '{produit}' a été ajouté avec succès au fichier '{nom_fichier}'.")