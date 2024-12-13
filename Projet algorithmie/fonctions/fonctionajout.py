import pandas as pds

def fonctionajout(nom_fichier, produit, prix, quantite):
    try:
        print(f"\nAjout du produit dans le fichier '{nom_fichier}'...")
        print(f"Produit: {produit}, Prix: {prix}, Quantité: {quantite}")
        
        # Création d'une nouvelle ligne avec les informations du produit
        nouvelle_ligne = pds.DataFrame({'Nom': [produit], 'Prix': [f"{prix}€"], 'Quantité': [f"{quantite} unités"]})

        # Si le fichier existe déjà, on charge les données existantes
        try:
            produits_df = pds.read_csv(nom_fichier)
        except FileNotFoundError:
            # Si le fichier n'existe pas, on crée un DataFrame vide
            produits_df = pds.DataFrame(columns=['Nom', 'Prix', 'Quantité'])
        
        # Ajouter la nouvelle ligne au DataFrame
        produits_df = pds.concat([produits_df, nouvelle_ligne], ignore_index=True)

        # Sauvegarder le DataFrame mis à jour dans le fichier CSV
        produits_df.to_csv(nom_fichier, index=False, encoding='utf-8')
        
        print(f"Produit '{produit}', prix '{prix}', quantité '{quantite}' ajoutés au fichier '{nom_fichier}'.")
    
    except Exception as e:
        print(f"Erreur inconnue : {e}")
