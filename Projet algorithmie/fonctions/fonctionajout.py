def fonctionajout(nom_fichier, produit, prix, quantite):
    try:
        print(f"\nAjout du produit dans le fichier '{nom_fichier}'...")
        print(f"Produit: {produit}, Prix: {prix}, Quantité: {quantite}")

        ligne = f"{produit}, {prix}€, {quantite} unités\n"

        with open(nom_fichier, 'a', encoding='utf-8') as fichier:
            fichier.write(ligne)  
            print(f"Produit '{produit}', prix '{prix}€', quantité '{quantite}' ajoutés au fichier '{nom_fichier}'.")
    
    except FileNotFoundError:
        print(f"Erreur : Le fichier '{nom_fichier}' est introuvable.")
    except Exception as e:
        print(f"Erreur inconnue : {e}")
