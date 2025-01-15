import hashlib
import pandas as pds
import requests
import csv
from datetime import *
import secrets

# Fonction pour générer un sel aléatoire sécurisé
def generate_salt():
    return secrets.token_hex(16)

# Fonction pour hasher un mot de passe avec un sel
def hash_password(password):
    salt = generate_salt()
    hashed_password = hashlib.sha256((salt + password).encode('utf-8')).hexdigest()
    return f"{salt}:{hashed_password}"

# Fonction pour vérifier un mot de passe par rapport au hash stocké
def verify_password(password, stored_password):
    salt, hashed_password = stored_password.split(":")
    return hashlib.sha256((salt + password).encode('utf-8')).hexdigest() == hashed_password

# Fonction pour vérifier si un mot de passe est compromis via une API
def check_password_compromised_api(password):
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5chars = sha1password[:5]

    response = requests.get(f'https://api.pwnedpasswords.com/range/{first5chars}')
    if response.status_code != 200:
        raise RuntimeError(f'Erreur lors de la vérification du mot de passe : {response.status_code}')

    hashes = (line.split(':') for line in response.text.splitlines())
    for h, count in hashes:
        if h == sha1password[5:]:
            return True
    return False

# Définir le chemin du fichier
chemin_fichier_utilisateurs = 'Data/Utilisateurs.csv'

# Fonction pour lire le fichier des utilisateurs
def lire_utilisateurs():
    try:
        df = pds.read_csv(chemin_fichier_utilisateurs)
        df['mot_de_passe'] = df['mot_de_passe'].astype(str)
        return df
    except FileNotFoundError:
        print(f"Le fichier des utilisateurs est introuvable à l'emplacement : {chemin_fichier_utilisateurs}")
        return pds.DataFrame(columns=['nom_utilisateur', 'mot_de_passe'])

# Fonction pour enregistrer les utilisateurs après modification ou suppression
def enregistrer_utilisateurs(utilisateur_df):
    utilisateur_df.to_csv(chemin_fichier_utilisateurs, index=False)
    print("Les modifications ont été sauvegardées dans le fichier.")

# Fonction pour afficher les utilisateurs
def afficher_utilisateurs():
    utilisateurs_df = lire_utilisateurs()

    if utilisateurs_df.empty:
        print("Aucun utilisateur trouvé.")
    else:
        print("\nListe des utilisateurs :")
        print(utilisateurs_df)

# Fonction pour modifier un utilisateur
def modifier_utilisateurs():
    utilisateurs_df = lire_utilisateurs()

    if utilisateurs_df.empty:
        print("Aucun utilisateur trouvé.")
        return

    nom_utilisateur = input("Entrez le nom d'utilisateur à modifier : ").strip().lower()

    utilisateurs_df['nom_utilisateur'] = utilisateurs_df['nom_utilisateur'].astype(str).str.strip().str.lower()
    utilisateur = utilisateurs_df[utilisateurs_df['nom_utilisateur'] == nom_utilisateur]

    if utilisateur.empty:
        print(f"Utilisateur '{nom_utilisateur}' non trouvé.")
        return

    print(f"Informations actuelles de l'utilisateur '{nom_utilisateur}':")
    print(utilisateur)

    choix = input("Souhaitez-vous modifier (1) le nom d'utilisateur ou (2) le mot de passe ? (entrez 1 ou 2) : ")

    if choix == "1":
        nouveau_nom_utilisateur = input("Entrez le nouveau nom d'utilisateur : ").strip()
        utilisateurs_df.loc[utilisateurs_df['nom_utilisateur'] == nom_utilisateur, 'nom_utilisateur'] = nouveau_nom_utilisateur
        print(f"Le nom d'utilisateur a été modifié en '{nouveau_nom_utilisateur}'.")

    elif choix == "2":
        nouveau_mot_de_passe = input("Entrez le nouveau mot de passe : ").strip()
        if check_password_compromised_api(nouveau_mot_de_passe):
            print("Ce mot de passe a été compromis. Veuillez en choisir un autre.")
            return
        hashed_password = hash_password(nouveau_mot_de_passe)
        utilisateurs_df.loc[utilisateurs_df['nom_utilisateur'] == nom_utilisateur, 'mot_de_passe'] = hashed_password
        print("Le mot de passe a été modifié avec succès.")

    else:
        print("Choix invalide. Aucune modification effectuée.")
        return

    enregistrer_utilisateurs(utilisateurs_df)

# Fonction pour supprimer un utilisateur
def supprimer_utilisateur():
    utilisateurs_df = lire_utilisateurs()

    if utilisateurs_df.empty:
        print("Aucun utilisateur trouvé.")
        return

    nom_utilisateur = input("Entrez le nom d'utilisateur à supprimer : ").strip()
    utilisateur = utilisateurs_df[utilisateurs_df['nom_utilisateur'] == nom_utilisateur]

    if utilisateur.empty:
        print(f"Utilisateur '{nom_utilisateur}' non trouvé.")
        return

    confirmer = input(f"Êtes-vous sûr de vouloir supprimer l'utilisateur '{nom_utilisateur}' ? (oui/non) : ").strip().lower()
    if confirmer == 'oui':
        utilisateurs_df = utilisateurs_df[utilisateurs_df['nom_utilisateur'] != nom_utilisateur]
        enregistrer_utilisateurs(utilisateurs_df)
        print(f"L'utilisateur '{nom_utilisateur}' a été supprimé avec succès.")
    else:
        print("Suppression annulée.")

    afficher_utilisateurs()

# Fonction pour créer les fichiers CSV s'ils n'existent pas
def create_csv_files():
    with open('Data/queries.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'query', 'timestamp'])

    with open('Data/compromises.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'query_id', 'compromise', 'timestamp'])

# Fonction pour ajouter une requête
def add_query(query):
    with open('Data/queries.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        timestamp = time.time()
        query_id = int(time.time())
        writer.writerow([query_id, query, timestamp])
        return query_id

# Fonction pour ajouter un compromis
def add_compromise(query_id, compromise):
    with open('Data/compromises.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        timestamp = time.time()
        writer.writerow([int(time.time()), query_id, compromise, timestamp])

# Fonction pour lire les requêtes
def read_queries():
    with open('Data/queries.csv', mode='r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            print(f"ID: {row[0]}, Requête: {row[1]}, Timestamp: {row[2]}")

# Fonction pour lire les compromis associés aux requêtes
def read_compromises():
    with open('Data/compromises.csv', mode='r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            print(f"ID: {row[0]}, Requête ID: {row[1]}, Compromis: {row[2]}, Timestamp: {row[3]}")

# Fonction pour afficher les produits associés aux utilisateurs
def afficher_produits():
    chemin_fichier_produits = 'Data/Produits.csv'
    try:
        produits_df = pds.read_csv(chemin_fichier_produits)
        print("\nListe des produits :")
        print(produits_df)
    except FileNotFoundError:
        print(f"Le fichier des produits est introuvable à l'emplacement : {chemin_fichier_produits}")

# Fonction pour mettre à jour les produits lors de la modification d'un utilisateur
def mettre_a_jour_proprietaire_produit(ancien_nom, nouveau_nom):
    chemin_fichier_produits = 'Data/Produits.csv'
    try:
        produits_df = pds.read_csv(chemin_fichier_produits)
        produits_df.loc[produits_df['Propriétaire'].str.lower() == ancien_nom.lower(), 'Propriétaire'] = nouveau_nom
        produits_df.to_csv(chemin_fichier_produits, index=False)
        print(f"Le propriétaire des produits a été mis à jour de '{ancien_nom}' à '{nouveau_nom}'.")
    except FileNotFoundError:
        print(f"Le fichier des produits est introuvable à l'emplacement : {chemin_fichier_produits}")

# Fonction pour modifier les produits
def modifier_produit_admin():
    chemin_fichier_produits = 'Data/Produits.csv'
    try:
        produits_df = pds.read_csv(chemin_fichier_produits)
        if produits_df.empty:
            print("Le fichier des produits est vide.")
            return

        print("\nContenu actuel des produits :")
        print(produits_df)

        choix = int(input("Entrez le numéro de la ligne du produit à modifier (0 pour quitter) : "))
        if choix == 0 or choix > len(produits_df):
            print("Aucune modification effectuée.")
            return

        ligne = produits_df.iloc[choix - 1]
        print(f"Produit sélectionné : {ligne}")

        colonne = input("Quel attribut souhaitez-vous modifier ? (Produit/Prix/Quantité/Propriétaire) : ").strip()
        if colonne not in produits_df.columns:
            print("Attribut invalide.")
            return

        nouvelle_valeur = input(f"Entrez la nouvelle valeur pour {colonne} : ").strip()
        produits_df.at[choix - 1, colonne] = nouvelle_valeur
        produits_df.to_csv(chemin_fichier_produits, index=False)
        print("Modification enregistrée avec succès.")

    except FileNotFoundError:
        print(f"Le fichier des produits est introuvable à l'emplacement : {chemin_fichier_produits}")
    except ValueError:
        print("Entrée invalide. Veuillez réessayer.")
    except Exception as e:
        print(f"Erreur : {e}")

# Fonction pour supprimer un produit
def supprimer_produit():
    chemin_fichier_produits = 'Data/Produits.csv'
    try:
        produits_df = pds.read_csv(chemin_fichier_produits)
        if produits_df.empty:
            print("Le fichier des produits est vide.")
            return

        print("\nContenu actuel des produits :")
        print(produits_df)

        choix = int(input("Entrez le numéro de la ligne du produit à supprimer (0 pour quitter) : "))
        if choix == 0 or choix > len(produits_df):
            print("Aucune suppression effectuée.")
            return

        produit_supprime = produits_df.iloc[choix - 1]
        produits_df = produits_df.drop(produits_df.index[choix - 1])
        produits_df.to_csv(chemin_fichier_produits, index=False)
        print(f"Le produit '{produit_supprime['Produit']}' a été supprimé avec succès.")

    except FileNotFoundError:
        print(f"Le fichier des produits est introuvable à l'emplacement : {chemin_fichier_produits}")
    except ValueError:
        print("Entrée invalide. Veuillez réessayer.")
    except Exception as e:
        print(f"Erreur : {e}")


# Ajouter une requête au fichier CSV
def log_request(user, action, password, success):
    filename = 'requêtes.csv'

    # Vérification si le mot de passe est compromis
    is_compromised = check_password_compromised_api(password)

    # Générer l'heure actuelle
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Structure des données
    row = {
        "Utilisateur": user,
        "Action": action,
        "Date et Heure": timestamp,
        "Mot de passe compromis": "Oui" if is_compromised else "Non",
        "Succès de l'action": "Réussie" if success else "Échouée"
    }

    # Écriture dans le fichier CSV
    try:
        with open(filename, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=row.keys())

            # Écrire l'en-tête si le fichier est vide
            if file.tell() == 0:
                writer.writeheader()

            # Ajouter la ligne de requête
            writer.writerow(row)

        print("Requête enregistrée avec succès.")
    except Exception as e:
        print(f"Erreur lors de l'enregistrement de la requête : {e}")

