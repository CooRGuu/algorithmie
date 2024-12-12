def fonctionrecherchesequentielle(nom_fichier, critere, valeur):
    try:
        # Lire le contenu du fichier
        with open(nom_fichier, 'r', encoding='utf-8') as file:
            lignes = file.readlines()

        # Vérifier si le fichier est vide
        if not lignes:
            print(f"Le fichier '{nom_fichier}' est vide.")
            return

        # Liste pour stocker les correspondances trouvées
        correspondances = []

        for ligne in lignes:
            try:
                ligne = ligne.strip()
                if not ligne or ligne.lower().startswith("liste de produits"):  # Ignorer les lignes vides ou d'en-tête
                    continue

                # Diviser la ligne en nom, prix et quantité
                parts = ligne.split(',')
                if len(parts) != 3:
                    print(f"Erreur de format dans la ligne : '{ligne}'")
                    continue  # Ignorer cette ligne si elle n'a pas 3 parties

                nom, prix_quantite, quantite = parts

                # Nettoyer les valeurs prix et quantité
                prix = prix_quantite.replace('€', '').strip()  # Enlever le symbole €
                quantite = quantite.replace('unités', '').strip()  # Enlever "unités"

                # Selon le critère, comparer la valeur
                if critere == "prix" and abs(float(prix) - float(valeur)) < 0.01:  # On tolère une petite marge d'erreur pour le prix
                    correspondances.append(f"Nom: {nom.strip()}, Prix: {prix}€, Quantité: {quantite} unités")
                elif critere == "quantite" and int(quantite) == int(valeur):
                    correspondances.append(f"Nom: {nom.strip()}, Prix: {prix}€, Quantité: {quantite} unités")
                elif critere == "nom" and valeur.lower() in nom.strip().lower():
                    correspondances.append(f"Nom: {nom.strip()}, Prix: {prix}€, Quantité: {quantite} unités")

            except ValueError as e:
                print(f"Erreur de format dans la ligne : '{ligne}' -> {e}")
                continue

        # Afficher les résultats de la recherche
        if correspondances:
            print(f"\nCorrespondances trouvées pour '{critere}' = {valeur} :")
            for correspondance in correspondances:
                print(correspondance)
        else:
            print(f"Aucune correspondance trouvée pour '{critere}' = {valeur}.")

    except FileNotFoundError:
        print(f"Erreur : Le fichier '{nom_fichier}' n'a pas été trouvé.")
    except Exception as e:
        print(f"Une erreur est survenue : {e}")
