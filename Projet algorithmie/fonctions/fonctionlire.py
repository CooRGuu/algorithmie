def fonctionlire(nom_fichier):
    try:
        with open(nom_fichier, 'r', encoding='utf-8') as fichier:
            contenu = fichier.readlines()
        print(f"Contenu du fichier '{nom_fichier}' :")
        for ligne in contenu:
            print(ligne.strip())
    except FileNotFoundError:
        print(f"Erreur: Le fichier '{nom_fichier}' est introuvable.")
    except Exception as e:
        print(f"Erreur inconnue: {e}")
