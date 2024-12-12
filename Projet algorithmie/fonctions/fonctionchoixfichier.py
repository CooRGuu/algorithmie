def fonctionchoixfichier():

    fichiers = []
    
    if not fichiers:
        print("Aucun fichier trouvé.")
        return None

    print("\n--- Fichiers disponibles ---")
    for i, fichier in enumerate(fichiers, 1):
        print(f"{i}. {fichier}")

    choix = input("Choisissez le fichier (numéro) : ")
    try:
        index = int(choix) - 1
        return fichiers[index]
    except (ValueError, IndexError):
        print("Choix invalide.")
        return None
