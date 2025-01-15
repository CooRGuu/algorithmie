import pandas as pds
from datetime import datetime
import csv
import hashlib

DATA_DIR = "Data"  # Dossier pour stocker les fichiers
LOG_FILE = "log.csv"  # Nom du fichier journal

def is_valid_filename(filename: str) -> bool:
    """
    Vérifie si le nom de fichier est valide (sans caractères spéciaux).
    
    Args:
        filename (str): Le nom du fichier à vérifier.
    
    Returns:
        bool: True si le nom est valide, False sinon.
    """
    invalid_chars = '<>:"/\\|?*'  # Caractères invalides pour les noms de fichiers
    return not any(char in filename for char in invalid_chars)

def fonctioncreer(nom_fichier):
    try:
        # Demander à l'utilisateur de saisir le nom du fichier CSV à créer
        nom_fichier = input("Entrez le nom du fichier en .csv à créer : ")

        # Vérifier que l'utilisateur a bien spécifié l'extension .csv
        if not nom_fichier.lower().endswith('.csv'):
            nom_fichier += '.csv'

        # Vérifier que le nom de fichier ne contient pas de caractères invalides
        if not is_valid_filename(nom_fichier):
            print("Erreur : Le nom de fichier contient des caractères invalides.")
            return

        # Spécifier le chemin complet pour enregistrer le fichier dans le dossier Data
        chemin_fichier = f"{DATA_DIR}/{nom_fichier}"

        # Créer un DataFrame vide avec des colonnes 'Prix', 'Quantité', et 'Propriétaire'
        df = pds.DataFrame(columns=["Prix", "Quantité", "Propriétaire"])

        # Sauvegarder le DataFrame dans un fichier CSV dans le dossier Data
        df.to_csv(chemin_fichier, index=False, encoding='utf-8')

        print(f"Le fichier '{chemin_fichier}' a été créé avec succès.")

    except Exception as e:
        print(f"Erreur inconnue : {e}")

def load_hashed_passwords(csv_file_path: str) -> set:
    """
    Charge les hachages de mots de passe depuis un fichier CSV.

    Args:
        csv_file_path (str): Le chemin vers le fichier CSV contenant les hachages.

    Returns:
        set: Un ensemble de hachages de mots de passe.
    """
    hashed_passwords = set()
    try:
        with open(csv_file_path, mode='r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row:
                    hashed_passwords.add(row[0])
    except FileNotFoundError:
        print(f"Erreur : Le fichier '{csv_file_path}' est introuvable.")
    except Exception as e:
        print(f"Erreur lors du chargement des hachages : {e}")
    return hashed_passwords

def check_password_compromised_csv(user_password: str, csv_file_path: str, log_file_path: str) -> bool:
    """
    Vérifie si le mot de passe haché de l'utilisateur correspond à un hachage présent dans le fichier CSV
    et enregistre la requête dans un fichier journal.

    Args:
        user_password (str): Le mot de passe de l'utilisateur.
        csv_file_path (str): Le chemin vers le fichier CSV contenant les hachages compromis.
        log_file_path (str): Le chemin vers le fichier journal local.

    Returns:
        bool: True si le mot de passe est compromis, False sinon.
    """
    # Hacher le mot de passe de l'utilisateur avec SHA-256
    hashed_password = hashlib.sha256(user_password.encode('utf-8')).hexdigest()

    # Charger les hachages depuis le fichier CSV
    compromised_hashes = load_hashed_passwords(csv_file_path)

    is_compromised = hashed_password in compromised_hashes

    # Enregistrer la requête dans le fichier journal
    record_query(log_file_path, user_password, hashed_password, is_compromised)

    return is_compromised

def record_query(log_file_path: str, user_password: str, hashed_password: str, is_compromised: bool):
    """
    Enregistre une requête dans un fichier journal.

    Args:
        log_file_path (str): Le chemin vers le fichier journal.
        user_password (str): Le mot de passe non haché de l'utilisateur.
        hashed_password (str): Le mot de passe haché de l'utilisateur.
        is_compromised (bool): Résultat de la vérification (True si compromis, False sinon).
    """
    try:
        # Aj outer une entrée dans le fichier journal
        with open(log_file_path, mode='a', encoding='utf-8', newline='') as logfile:
            writer = csv.writer(logfile)
            writer.writerow([datetime.now(), user_password, hashed_password, is_compromised])
    except Exception as e:
        print(f"Erreur lors de l'enregistrement dans le journal : {e}")
