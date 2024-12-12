# fonctionsupp.py
def fonctionsupp(nom_fichier):
    try:
        with open(nom_fichier, 'r') as fichier:
            contenu = fichier.readlines()

        if not contenu:
            print(f"Le fichier '{nom_fichier}' est vide.")
            return

        print(f"Contenu du fichier '{nom_fichier}' :")
        for i, ligne in enumerate(contenu, start=1):
            print(f"{i}. {ligne.strip()}")  

        choix = int(input("Entrez le numéro du produit à supprimer (0 pour tout supprimer) : "))
        
        if choix == 0:
            with open(nom_fichier, 'w') as fichier:
                fichier.write("")  # Supprimer tout le contenu
            print(f"Tout le contenu du fichier '{nom_fichier}' a été supprimé.")
        elif 1 <= choix <= len(contenu):
            produit_a_supprimer = contenu[choix - 1]
            contenu.pop(choix - 1)  # Supprimer le produit

            with open(nom_fichier, 'w') as fichier:
                fichier.writelines(contenu)  # Réécrire le fichier sans le produit supprimé

            print(f"Le produit '{produit_a_supprimer.strip()}' a été supprimé du fichier '{nom_fichier}'.")
        else:
            print("Choix invalide.")
    except ValueError:
        print("Erreur: Veuillez entrer un numéro valide.")
    except FileNotFoundError:
        print(f"Erreur: Le fichier '{nom_fichier}' est introuvable.")
    except Exception as e:
        print(f'Erreur inconnue: {e}')
