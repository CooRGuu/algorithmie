import pandas as pd
import hashlib

# Fonction pour hasher un mot de passe avec un sel
def hash_password(password, salt):
    hashed_password = hashlib.sha256((salt + password).encode('utf-8')).hexdigest()
    return f"{salt}:{hashed_password}"  # Retourner le sel et le hachage concaténés

# Fonction pour générer un sel simple
def generate_simple_salt():
    """Génère un sel simple basé sur une chaîne prédéfinie."""
    return "fixed_salt"  # Utiliser une chaîne fixe comme sel

# Chemin du fichier texte contenant les mots de passe compromis
file_path = './Data/mdpcompromis.txt'
# Chemin du fichier CSV de sortie
csv_file_path = './Data/mdpcompromis_hashed.csv'

# Lire le contenu du fichier texte
try:
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.readlines()

    # Enlever les sauts de ligne et créer une liste de mots de passe
    passwords = [line.strip() for line in content]

    # Hacher les mots de passe et créer une liste de tuples (mot de passe, mot de passe haché)
    hashed_passwords = [(password, hash_password(password, generate_simple_salt())) for password in passwords]

    # Créer un DataFrame avec les mots de passe d'origine et les mots de passe hachés
    df_hashed = pd.DataFrame(hashed_passwords, columns=['password', 'hashed_password'])

    # Sauvegarder le DataFrame dans un fichier CSV
    df_hashed.to_csv(csv_file_path, index=False)
    print("Les mots de passe et leurs hachages ont été sauvegardés dans le fichier CSV.")

except FileNotFoundError:
    print(f"Erreur : Le fichier '{file_path}' est introuvable.")
except Exception as e:
    print(f"Une erreur est survenue : {e}")