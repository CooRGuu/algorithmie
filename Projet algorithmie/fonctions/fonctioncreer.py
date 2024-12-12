def fonctioncreer():
    try:
        nom_fichier = input("Entrez le nom du fichier en .txt à créer : ")
        with open(nom_fichier, 'w', encoding='utf-8') as fichier:
            fichier.write("Liste de produits :\n")
            print(f"Le fichier '{nom_fichier}' a été créé avec succès.")

    except Exception as e:
        print(f"Erreur Inconnue: {e}")
