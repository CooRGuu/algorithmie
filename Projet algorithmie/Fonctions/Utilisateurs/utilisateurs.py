import pandas as pds
import hashlib
import requests
import secrets
from datetime import datetime
import csv
import re
from Fonctions.Mail.Gestion_email import *

def check_password_compromised_api(password):
    # Hacher le mot de passe
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5chars = sha1password[:5]

    # Faire la requête à l'API
    response = requests.get(f'https://api.pwnedpasswords.com/range/{first5chars}')

    if response.status_code != 200:
        raise RuntimeError(f'Erreur lors de la vérification du mot de passe : {response.status_code}')

    # Vérifier si le hash du mot de passe est dans la réponse
    hashes = (line.split(':') for line in response.text.splitlines())
    for h, count in hashes:
        if h == sha1password[5:]:
            return True  # Mot de passe compromis
    return False  # Mot de passe non compromis

def generate_salt():
    """Génère un sel aléatoire sécurisé."""
    return secrets.token_hex(16)  # Génère un sel de 16 octets hexadécimaux (32 caractères)

def hash_password(password):
    """Hache un mot de passe avec un sel aléatoire sécurisé."""
    salt = generate_salt()
    hashed_password = hashlib.sha256((salt + password).encode('utf-8')).hexdigest()
    return f"{salt}:{hashed_password}"

def verify_password(password, stored_password):
    """Vérifie si un mot de passe correspond à un hachage stocké."""
    salt, hashed_password = stored_password.split(":")
    return hashlib.sha256((salt + password).encode('utf-8')).hexdigest() == hashed_password

def email_valide(email):
    """Vérifie si une adresse email est valide."""
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email)

# Gestion des utilisateurs
def charger_utilisateurs():
    """Charge les utilisateurs depuis un fichier CSV dans un DataFrame."""
    chemin_fichier = "Data/Utilisateurs.csv"
    try:
        return pds.read_csv(chemin_fichier)
    except FileNotFoundError:
        return pds.DataFrame(columns=["nom_utilisateur", "mot_de_passe"])

def sauvegarder_utilisateurs(df):
    """Sauvegarde les utilisateurs dans un fichier CSV."""
    chemin_fichier = "Data/Utilisateurs.csv"
    df.to_csv(chemin_fichier, index=False)

def verifier_utilisateur(nom_utilisateur, mot_de_passe):
    """Vérifie si un utilisateur et son mot de passe correspondent."""
    df = charger_utilisateurs()

    utilisateur = df[df["nom_utilisateur"] == nom_utilisateur]
    if utilisateur.empty:
        return False

    stored_password = utilisateur["mot_de_passe"].values[0]
    return verify_password(mot_de_passe, stored_password)

def inscription(username, email, hashed_password):

    nom_utilisateur = input("Entrez le nom d'utilisateur : ").strip()
    
    while True:
        email = input("Entrez votre adresse email : ").strip()
        if not email_valide(email):
            print("Adresse email invalide. Veuillez réessayer.")
        else:
            break

    while True:
        mot_de_passe = input("Entrez le mot de passe : ").strip()

        # Vérifier si le mot de passe est compromis
        if check_password_compromised_api(mot_de_passe):
            print("Ce mot de passe a été compromis. Veuillez en choisir un autre.")
            print("Suggestions pour renforcer votre mot de passe :")
            print("- Utilisez au moins 12 caractères.")
            print("- Incluez des majuscules, des minuscules, des chiffres et des symboles.")
            continue  # Recommencer la boucle pour demander un nouveau mot de passe

        # Si le mot de passe n'est pas compromis, sortir de la boucle
        break

    hashed_password = hash_password(mot_de_passe)
    utilisateurs_df = charger_utilisateurs()

    if nom_utilisateur in utilisateurs_df['nom_utilisateur'].values:
        print(f"L'utilisateur '{nom_utilisateur}' existe déjà.")
        return True

    nouveau_utilisateur = pds.DataFrame([[nom_utilisateur, email, hashed_password]],
    columns=['nom_utilisateur', 'email', 'mot_de_passe'])
    utilisateurs_df = pds.concat([utilisateurs_df, nouveau_utilisateur], ignore_index=True)
    sauvegarder_utilisateurs(utilisateurs_df)
    print(f"L'utilisateur '{nom_utilisateur}' a été inscrit avec succès.")
    log_request(nom_utilisateur, 'Inscription', mot_de_passe, success=True)

# Mot de passe administrateur pré-haché
admin_username = "root"

admin_password_stored = hash_password("root")  # Hacher une fois le mot de passe "root"
def connexion(username, password):
    nom_utilisateur = input("Entrez votre nom d'utilisateur : ").strip()
    mot_de_passe = input("Entrez votre mot de passe : ").strip()

    # Vérification des identifiants admin
    if nom_utilisateur == "root" and verify_password(mot_de_passe, admin_password_stored):
        print("Connexion administrateur réussie !")
        menu_admin()  # Redirige vers le menu admin
        return None  # Empêche l'accès au menu principal utilisateur
    
    # Vérification des utilisateurs classiques
    if verifier_utilisateur(nom_utilisateur, mot_de_passe):
        log_request(nom_utilisateur, 'Connexion', mot_de_passe, success=True)
        print("Connexion réussie !")

        if check_password_compromised_api(mot_de_passe):
            print("Votre mot de passe est compromis. Vous recevrez un email avec des instructions.")
            
            # Charger l'email de l'utilisateur
            utilisateurs_df = charger_utilisateurs()
            email = utilisateurs_df.loc[utilisateurs_df['nom_utilisateur'] == nom_utilisateur, 'email'].values[0]

            # Envoyer un email
            sujet = "Alerte : Mot de passe compromis"
            message = (
                f"Bonjour {nom_utilisateur},\n\n"
                "Nous avons détecté que votre mot de passe est compromis. "
                "Nous vous recommandons de le changer immédiatement.\n\n"
                "Merci de votre vigilance.\nL'équipe de sécurité."
            )
            envoyer_email(email, sujet, message)

        return nom_utilisateur
    else:
        log_request(nom_utilisateur, 'Connexion', mot_de_passe, success=False)
        print("Nom d'utilisateur ou mot de passe incorrect.")
        return None


def changer_mot_de_passe(nom_utilisateur):
    while True:
        nouveau_mot_de_passe = input("Entrez votre nouveau mot de passe : ").strip()

        if check_password_compromised_api(nouveau_mot_de_passe):
            print("Ce mot de passe a été compromis. Veuillez en choisir un autre.")
        else:
            hashed_password = hash_password(nouveau_mot_de_passe)
            utilisateurs_df = charger_utilisateurs()
            utilisateurs_df.loc[utilisateurs_df['nom_utilisateur'] == nom_utilisateur, 'mot_de_passe'] = hashed_password
            sauvegarder_utilisateurs(utilisateurs_df)
            print(f"Le mot de passe de l'utilisateur '{nom_utilisateur}' a été changé avec succès.")
            break


def modifier_utilisateur(nom_utilisateur):
    utilisateurs_df = charger_utilisateurs()

    # Vérifier si l'utilisateur existe
    utilisateur = utilisateurs_df[utilisateurs_df['nom_utilisateur'] == nom_utilisateur]

    if utilisateur.empty:
        print(f"Utilisateur '{nom_utilisateur}' non trouvé.")
        return

    print(f"Informations actuelles de l'utilisateur '{nom_utilisateur}':")
    print(utilisateur)

    # Demander à l'utilisateur ce qu'il souhaite modifier
    print("Options de modification :")
    print("1. Modifier le nom d'utilisateur")
    print("2. Modifier le mot de passe")
    print("3. Modifier l'adresse email")
    choix = input("Entrez le numéro correspondant à ce que vous souhaitez modifier : ")
    
    if choix == "1":
        nouveau_nom_utilisateur = input("Entrez le nouveau nom d'utilisateur : ").strip()
        # Vérifier si le nouveau nom d'utilisateur existe déjà
        if verifier_utilisateur(nouveau_nom_utilisateur, ""):
            print(f"L'utilisateur '{nouveau_nom_utilisateur}' existe déjà.")
            return
        utilisateurs_df.loc[utilisateurs_df['nom_utilisateur'] == nom_utilisateur, 'nom_utilisateur'] = nouveau_nom_utilisateur
        print(f"Le nom d'utilisateur a été modifié en '{nouveau_nom_utilisateur}'.")

    elif choix == "2":
        nouveau_mot_de_passe = input("Entrez le nouveau mot de passe : ").strip()

        # # Vérifier si le nouveau mot de passe est compromis
        # if check_password_compromised_api(nouveau_mot_de_passe):
        #     print("Ce mot de passe a été compromis. Veuillez en choisir un autre.")
        #     print("Suggestions pour renforcer votre mot de passe :")
        #     print("- Utilisez au moins 12 caractères.")
        #     print("- Incluez des majuscules, des minuscules, des chiffres et des symboles.")
        #     return

        hashed_password = hash_password(nouveau_mot_de_passe)
        utilisateurs_df.loc[utilisateurs_df['nom_utilisateur'] == nom_utilisateur, 'mot_de_passe'] = hashed_password
        print("Le mot de passe a été modifié avec succès.")
        
    elif choix == "3":
        while True:
            nouveau_email = input("Entrez le nouvel email : ").strip()
            if not email_valide(nouveau_email):
                print("Adresse email invalide. Veuillez réessayer.")
            else:
                utilisateurs_df.loc[utilisateurs_df['nom_utilisateur'] == nom_utilisateur, 'email'] = nouveau_email
                print("L'adresse email a été modifiée avec succès.")
                break
            
    else:
        print("Choix invalide. Aucune modification effectuée.")
        return

    # Sauvegarder les modifications dans le fichier des utilisateurs
    sauvegarder_utilisateurs(utilisateurs_df)

def check_password_compromised_csv(user_password: str, csv_file_path: str) -> bool:
    """Vérifie si le mot de passe haché de l'utilisateur correspond à un hachage présent dans le fichier CSV."""
    # Hacher le mot de passe de l'utilisateur avec le sel
    hashed_password = hash_password(user_password)

    try:
        # Ouvrir le fichier CSV
        df = pds.read_csv(csv_file_path)

        # Vérifier si le hachage du mot de passe est dans la colonne 'hashed_password'
        if hashed_password in df['hashed_password'].values:
            return True

    except FileNotFoundError:
        print(f"Erreur : Le fichier '{csv_file_path}' est introuvable.")
    except Exception as e:
        print(f"Erreur : {e}")

    return False  # Retourne False si le mot de passe n'est pas compromis
# Vérifier si un mot de passe est compromis via une API
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

# Ajouter une requête au fichier CSV
def log_request(user, action, password, success):
    
    # Définir le chemin du fichier CSV
    
    # Définir le chemin du fichier CSV
    filename = "Data/requêtes.csv"
    
    # Créer le dossier s'il n'existe pas
    
    

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