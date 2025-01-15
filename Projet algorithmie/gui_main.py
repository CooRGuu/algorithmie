import os
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import pandas as pd
import hashlib
from datetime import datetime
import csv
import requests
import secrets
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Paths and Configurations
DATA_FOLDER = os.path.abspath("Data")
UTILISATEURS_FILE = os.path.join(DATA_FOLDER, "Utilisateurs.csv")
REQUETES_FILE = os.path.join(DATA_FOLDER, "requêtes.csv")
ADMIN_CREDENTIALS = {"nom_utilisateur": "root", "mot_de_passe": "root"}
EMAIL_CONFIG = {
    "smtp_server": "smtp.gmail.com",
    "port": 587,
    "login": "corentinguyard2002@gmail.com",
    "password": "hgmp phxw zagn pykg"
}
# Helper Functions
def hash_password(password):
    salt = secrets.token_hex(16)
    hashed = hashlib.sha256((salt + password).encode()).hexdigest()
    return f"{salt}:{hashed}"

def fonctionrecherchebinaire(file_name, critere, valeur):
    path = os.path.join(DATA_FOLDER, file_name if file_name.endswith('.csv') else f"{file_name}.csv")
    try:
        df = pd.read_csv(path)
        if critere not in df.columns:
            messagebox.showerror("Erreur", f"Critère '{critere}' non trouvé dans le fichier.")
            return

        df = df.dropna(subset=[critere])

        if critere.lower() == "prix":
            df[critere] = pd.to_numeric(df[critere], errors='coerce')
            df = df.sort_values(by=critere)
            filtered_df = df[df[critere] <= float(valeur)]
        elif critere.lower() == "quantité":
            df[critere] = pd.to_numeric(df[critere], errors='coerce')
            df = df.sort_values(by=critere)
            filtered_df = df[df[critere] == int(valeur)]
        elif critere.lower() == "nom":
            filtered_df = df[df[critere].str.contains(valeur, case=False, na=False)]
        else:
            messagebox.showerror("Erreur", "Critère non supporté pour la recherche.")
            return

        if not filtered_df.empty:
            display_csv_in_treeview(filtered_df, title=f"Résultats pour {critere} = {valeur}")
        else:
            messagebox.showinfo("Résultats", "Aucun résultat trouvé pour la recherche.")

    except FileNotFoundError:
        messagebox.showerror("Erreur", f"Le fichier '{file_name}' est introuvable.")
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur lors de la recherche : {e}")
        
def verify_password(stored_password, provided_password):
    try:
        salt, hashed = stored_password.split(":")
        return hashlib.sha256((salt + provided_password).encode()).hexdigest() == hashed
    except ValueError:
        return False

def send_email(recipient, subject, body):
    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_CONFIG["login"]
        msg["To"] = recipient
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP(EMAIL_CONFIG["smtp_server"], EMAIL_CONFIG["port"]) as server:
            server.starttls()
            server.login(EMAIL_CONFIG["login"], EMAIL_CONFIG["password"])
            server.sendmail(EMAIL_CONFIG["login"], recipient, msg.as_string())
        messagebox.showinfo("ALERTE !", "Votre mot de passe est compromis, un email vous a été envoyé avec des recommandations.")
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur lors de l'envoi de l'email : {e}")

def log_request(username, action, success, password_status=None):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    password_info = password_status if password_status else "N/A"
    try:
        with open(REQUETES_FILE, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, username, action, "Succès" if success else "Échec", password_info])
    except Exception as e:
        print(f"Erreur lors de l'enregistrement de la requête : {e}")

def check_password_compromised_csv(user_password: str, csv_file_path: str) -> bool:
    """Vérifie si le mot de passe haché de l'utilisateur correspond à un hachage présent dans le fichier CSV."""
    try:
        df = pd.read_csv(csv_file_path)
        for stored_password in df['hashed_password']:
            try:
                salt, hashed = stored_password.split(":")
                if hashlib.sha256((salt + user_password).encode()).hexdigest() == hashed:
                    return True
            except ValueError:
                continue
    except FileNotFoundError:
        print(f"Erreur : Le fichier '{csv_file_path}' est introuvable.")
    except Exception as e:
        print(f"Erreur : {e}")

    return False

def check_password_compromised_api(password):
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    prefix, suffix = sha1password[:5], sha1password[5:]
    try:
        response = requests.get(f'https://api.pwnedpasswords.com/range/{prefix}')
        response.raise_for_status()
        return any(suffix == line.split(":")[0] for line in response.text.splitlines())
    except requests.RequestException:
        return False

# Sorting Functions

def sort_by_price(file_name, username):
    path = os.path.join(DATA_FOLDER, file_name if file_name.endswith('.csv') else f"{file_name}.csv")
    try:
        df = pd.read_csv(path)
        if "Prix" not in df.columns or "Propriétaire" not in df.columns:
            messagebox.showerror("Erreur", "Les colonnes 'Prix' ou 'Propriétaire' sont introuvables dans le fichier.")
            return

        df = df[df["Propriétaire"] == username]
        df = df.dropna(subset=["Prix"])
        df["Prix"] = pd.to_numeric(df["Prix"], errors='coerce')
        sorted_df = df.sort_values(by="Prix")
        display_csv_in_treeview(sorted_df, title=f"Tri par prix - {file_name}")
    except FileNotFoundError:
        messagebox.showerror("Erreur", f"Le fichier '{file_name}' est introuvable.")
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur lors du tri par prix : {e}")

def sort_by_quantity(file_name, username):
    path = os.path.join(DATA_FOLDER, file_name if file_name.endswith('.csv') else f"{file_name}.csv")
    try:
        df = pd.read_csv(path)
        if "Quantité" not in df.columns or "Propriétaire" not in df.columns:
            messagebox.showerror("Erreur", "Les colonnes 'Quantité' ou 'Propriétaire' sont introuvables dans le fichier.")
            return

        df = df[df["Propriétaire"] == username]
        df = df.dropna(subset=["Quantité"])
        df["Quantité"] = pd.to_numeric(df["Quantité"], errors='coerce')
        sorted_df = df.sort_values(by="Quantité")
        display_csv_in_treeview(sorted_df, title=f"Tri par quantité - {file_name}")
    except FileNotFoundError:
        messagebox.showerror("Erreur", f"Le fichier '{file_name}' est introuvable.")
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur lors du tri par quantité : {e}")

def sort_by_name(file_name, username):
    path = os.path.join(DATA_FOLDER, file_name if file_name.endswith('.csv') else f"{file_name}.csv")
    try:
        df = pd.read_csv(path)
        if "Nom" not in df.columns or "Propriétaire" not in df.columns:
            messagebox.showerror("Erreur", "Les colonnes 'Nom' ou 'Propriétaire' sont introuvables dans le fichier.")
            return

        df = df[df["Propriétaire"] == username]
        df = df.dropna(subset=["Nom"])
        sorted_df = df.sort_values(by="Nom")
        display_csv_in_treeview(sorted_df, title=f"Tri par nom - {file_name}")
    except FileNotFoundError:
        messagebox.showerror("Erreur", f"Le fichier '{file_name}' est introuvable.")
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur lors du tri par nom : {e}")

# File Management Functions
def create_file(file_name):
    path = os.path.join(DATA_FOLDER, file_name if file_name.endswith('.csv') else f"{file_name}.csv")
    try:
        pd.DataFrame(columns=["Nom", "Prix", "Quantité"]).to_csv(path, index=False)
        messagebox.showinfo("Succès", f"Fichier '{file_name}' créé avec succès.")
    except Exception as e:
        messagebox.showerror("Erreur", f"Impossible de créer le fichier : {e}")
def add_to_file(file_name, row):
    path = os.path.join(DATA_FOLDER, file_name if file_name.endswith('.csv') else f"{file_name}.csv")
    try:
        df = pd.read_csv(path)
    except FileNotFoundError:
        df = pd.DataFrame(columns=row.keys())

    new_row = pd.DataFrame([row])
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(path, index=False)
    messagebox.showinfo("Succès", f"L'entrée a été ajoutée avec succès dans le fichier '{file_name}'.")
    
def display_csv_in_treeview(dataframe, title="Données", window_size="800x600"):
    display_window = tk.Toplevel()
    display_window.title(title)
    display_window.geometry(window_size)

    tree = ttk.Treeview(display_window)
    tree["columns"] = list(dataframe.columns)
    tree["show"] = "headings"

    for col in dataframe.columns:
        tree.heading(col, text=col)
        tree.column(col, width=150)

    for index, row in dataframe.iterrows():
        tree.insert("", "end", values=list(row))

    tree.pack(expand=True, fill="both")

    close_button = tk.Button(display_window, text="Fermer", command=display_window.destroy)
    close_button.pack(pady=10)

def read_file(file_name):
    path = os.path.join(DATA_FOLDER, file_name if file_name.endswith('.csv') else f"{file_name}.csv")
    try:
        df = pd.read_csv(path)
        display_csv_in_treeview(df, title=f"Contenu de {file_name}")
    except FileNotFoundError:
        messagebox.showerror("Erreur", "Fichier introuvable.")
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur lors de la lecture : {e}")

def read_user_products(file_name, username):
    path = os.path.join(DATA_FOLDER, file_name if file_name.endswith('.csv') else f"{file_name}.csv")
    try:
        df = pd.read_csv(path)
        user_products = df[df["Propriétaire"] == username]
        if user_products.empty:
            messagebox.showinfo("Vos produits", "Vous n'avez pas encore de produits dans ce fichier.")
            return

        # Créer une fenêtre pour afficher les données
        display_window = tk.Toplevel()
        display_window.title(f"Produits de {username}")
        display_window.geometry("600x400")

        # Ajouter un widget Treeview
        tree = tk.ttk.Treeview(display_window)
        tree["columns"] = list(user_products.columns)
        tree["show"] = "headings"  # Supprime la colonne vide par défaut

        # Ajouter les colonnes
        for col in user_products.columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)

        # Ajouter les données
        for index, row in user_products.iterrows():
            tree.insert("", "end", values=list(row))

        tree.pack(expand=True, fill="both")

        # Ajouter un bouton pour fermer la fenêtre
        close_button = tk.Button(display_window, text="Fermer", command=display_window.destroy)
        close_button.pack(pady=10)

    except FileNotFoundError:
        messagebox.showerror("Erreur", "Fichier introuvable.")
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur lors de la lecture : {e}")

def modify_user_product(file_name, username):
    path = os.path.join(DATA_FOLDER, file_name if file_name.endswith('.csv') else f"{file_name}.csv")
    try:
        # Charger toutes les données
        df = pd.read_csv(path)
        if "Nom" not in df.columns or "Propriétaire" not in df.columns:
            messagebox.showerror("Erreur", "Les colonnes 'Nom' ou 'Propriétaire' sont introuvables dans le fichier.")
            return

        # Filtrer les produits de l'utilisateur
        user_products = df[df["Propriétaire"] == username]
        if user_products.empty:
            messagebox.showinfo("Info", "Aucun produit à modifier pour cet utilisateur.")
            return

        product_name = simpledialog.askstring("Modifier un produit", "Entrez le nom du produit à modifier :")
        if not product_name or product_name not in user_products["Nom"].values:
            messagebox.showerror("Erreur", "Produit introuvable ou non spécifié.")
            return

        new_price = simpledialog.askfloat("Modifier un produit", "Entrez le nouveau prix :")
        new_quantity = simpledialog.askinteger("Modifier un produit", "Entrez la nouvelle quantité :")

        if new_price is not None and new_quantity is not None:
            # Mettre à jour les produits de l'utilisateur
            df.loc[(df["Propriétaire"] == username) & (df["Nom"] == product_name), ["Prix", "Quantité"]] = [new_price, new_quantity]
            df.to_csv(path, index=False)
            messagebox.showinfo("Succès", f"Le produit '{product_name}' a été modifié avec succès.")
        else:
            messagebox.showerror("Erreur", "Valeurs non spécifiées pour le prix ou la quantité.")

    except FileNotFoundError:
        messagebox.showerror("Erreur", f"Le fichier '{file_name}' est introuvable.")
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur lors de la modification : {e}")
def modify_product():
    file_name = simpledialog.askstring("Modifier un produit", "Entrez le nom du fichier :")
    if not file_name:
        messagebox.showerror("Erreur", "Nom du fichier non fourni.")
        return

    product_name = simpledialog.askstring("Modifier un produit", "Entrez le nom du produit à modifier :")
    if not product_name:
        messagebox.showerror("Erreur", "Nom du produit non fourni.")
        return

    path = os.path.join(DATA_FOLDER, file_name if file_name.endswith('.csv') else f"{file_name}.csv")
    try:
        df = pd.read_csv(path)
        if product_name not in df["Nom"].values:
            messagebox.showerror("Erreur", f"Le produit '{product_name}' n'existe pas dans le fichier '{file_name}'.")
            return

        new_price = simpledialog.askfloat("Modifier un produit", "Entrez le nouveau prix :")
        new_quantity = simpledialog.askinteger("Modifier un produit", "Entrez la nouvelle quantité :")

        if new_price is not None and new_quantity is not None:
            df.loc[df["Nom"] == product_name, ["Prix", "Quantité"]] = [new_price, new_quantity]
            df.to_csv(path, index=False)
            messagebox.showinfo("Succès", f"Le produit '{product_name}' a été modifié avec succès dans le fichier '{file_name}'.")
    except FileNotFoundError:
        messagebox.showerror("Erreur", "Fichier introuvable.")
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur lors de la modification : {e}")

def delete_product():
    file_name = simpledialog.askstring("Supprimer un produit", "Entrez le nom du fichier :")
    if not file_name:
        messagebox.showerror("Erreur", "Nom du fichier non fourni.")
        return

    product_name = simpledialog.askstring("Supprimer un produit", "Entrez le nom du produit à supprimer :")
    if not product_name:
        messagebox.showerror("Erreur", "Nom du produit non fourni.")
        return

    path = os.path.join(DATA_FOLDER, file_name if file_name.endswith('.csv') else f"{file_name}.csv")
    try:
        df = pd.read_csv(path)
        if product_name not in df["Nom"].values:
            messagebox.showerror("Erreur", f"Le produit '{product_name}' n'existe pas dans le fichier '{file_name}'.")
            return

        df = df[df["Nom"] != product_name]
        df.to_csv(path, index=False)
        messagebox.showinfo("Succès", f"Le produit '{product_name}' a été supprimé avec succès du fichier '{file_name}'.")
    except FileNotFoundError:
        messagebox.showerror("Erreur", "Fichier introuvable.")
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur lors de la suppression : {e}")
# New Function to Ask for File Name

def ask_and_read_file():
    file_name = simpledialog.askstring("Voir un fichier", "Entrez le nom du fichier :")
    if file_name:
        read_file(file_name)

# User Management Functions
def handle_registration():
    username = simpledialog.askstring("Inscription", "Entrez votre nom d'utilisateur :")
    email = simpledialog.askstring("Inscription", "Entrez votre email :")
    password = simpledialog.askstring("Inscription", "Entrez votre mot de passe :", show="*")

    if not username or not email or not password:
        log_request(username, "inscription", False, "champs manquants")
        messagebox.showerror("Erreur", "Tous les champs doivent être remplis.")
        return

    compromised_csv_path = os.path.join(DATA_FOLDER, "compromised_passwords.csv")
    if check_password_compromised_csv(password, compromised_csv_path):
        log_request(username, "inscription", False, "mot de passe compromis CSV")
        messagebox.showerror("Erreur", "Ce mot de passe est compromis selon nos enregistrements locaux. Veuillez en choisir un autre.")
        return

    hashed_password = hash_password(password)
    try:
        utilisateurs_df = pd.read_csv(UTILISATEURS_FILE)
    except FileNotFoundError:
        utilisateurs_df = pd.DataFrame(columns=["nom_utilisateur", "email", "mot_de_passe"])

    if username in utilisateurs_df["nom_utilisateur"].values:
        log_request(username, "inscription", False, "utilisateur existant")
        messagebox.showerror("Erreur", "Un utilisateur avec ce nom existe déjà.")
        return

    utilisateurs_df = pd.concat([utilisateurs_df, pd.DataFrame([{"nom_utilisateur": username, "email": email, "mot_de_passe": hashed_password}])], ignore_index=True)
    utilisateurs_df.to_csv(UTILISATEURS_FILE, index=False)
    log_request(username, "inscription", True, "non compromis")
    messagebox.showinfo("Succès", "Inscription réussie !")

def handle_login():
    username = simpledialog.askstring("Connexion", "Entrez votre nom d'utilisateur :")
    password = simpledialog.askstring("Connexion", "Entrez votre mot de passe :", show="*")

    if not username or not password:
        messagebox.showerror("Erreur", "Tous les champs doivent être remplis.")
        return

    if username == ADMIN_CREDENTIALS["nom_utilisateur"] and password == ADMIN_CREDENTIALS["mot_de_passe"]:
        messagebox.showinfo("Succès", "Connexion administrateur réussie !")
        open_admin_interface()
        return

    try:
        utilisateurs_df = pd.read_csv(UTILISATEURS_FILE)
    except FileNotFoundError:
        messagebox.showerror("Erreur", "Aucun utilisateur trouvé.")
        return

    user_data = utilisateurs_df[utilisateurs_df["nom_utilisateur"] == username]
    if user_data.empty or not verify_password(user_data["mot_de_passe"].values[0], password):
        log_request(username, "connexion", False)
        messagebox.showerror("Erreur", "Nom d'utilisateur ou mot de passe incorrect.")
        return

    password_status = "compromis" if check_password_compromised_api(password) else "non compromis"
    log_request(username, "connexion", True, password_status)
    messagebox.showinfo("Succès", "Connexion réussie !")
    open_user_interface(username)

    if password_status == "compromis":
        if not user_data.empty and "email" in user_data.columns and user_data["email"].values[0]:
            recipient = user_data["email"].values[0]
            subject = "Alerte de sécurité : Mot de passe compromis"
            body = (
                "Votre mot de passe est compromis. Nous vous recommandons de le changer immédiatement.\n\n"
                "Instructions pour créer un bon mot de passe :\n"
                "1. Longueur minimale :\n"
                "   Assurez-vous que votre mot de passe comporte au moins 12 caractères. Plus il est long, mieux c'est.\n"
                "2. Variez les types de caractères :\n"
                "   Utilisez une combinaison de :\n"
                "   - Lettres majuscules (A, B, C...)\n"
                "   - Lettres minuscules (a, b, c...)\n"
                "   - Chiffres (0, 1, 2...)\n"
                "   - Caractères spéciaux (!, @, #, $, %, etc.)\n"
                "3. Évitez les informations personnelles :\n"
                "   Ne pas inclure votre nom, prénom, date de naissance, adresse, ou toute information facilement devinable.\n"
                "4. Pas de mots courants ou suites logiques :\n"
                "   Évitez les mots simples comme 'password', '123456', ou des séquences comme 'abcdef', 'qwerty', etc.\n"
                "5. Utilisez une phrase secrète :\n"
                "   Combinez des mots aléatoires avec des chiffres et des caractères spéciaux, par exemple : C@f3Rouge!2025.\n"
                "6. Mettez à jour régulièrement :\n"
                "   Changez vos mots de passe tous les 6 à 12 mois ou immédiatement si vous soupçonnez une compromission.\n"
                "7. Utilisez un gestionnaire de mots de passe :\n"
                "   Si vous avez du mal à créer ou mémoriser vos mots de passe, utilisez un gestionnaire de mots de passe (ex. LastPass, Dashlane, Bitwarden).\n"
                "8. Un mot de passe unique pour chaque service :\n"
                "   Ne réutilisez pas le même mot de passe pour plusieurs comptes. Si un compte est compromis, les autres seront protégés.\n"
                "9. Testez la robustesse de votre mot de passe :\n"
                "   Certains sites comme https://haveibeenpwned.com/Passwords permettent de vérifier si un mot de passe est déjà connu des hackers.\n"
                "\nNote importante :\n"
                "   Ne partagez jamais vos mots de passe avec d’autres personnes et évitez de les noter sur papier. Si nécessaire, chiffrez-les."
            )
            send_email(recipient, subject, body)
        else:
            messagebox.showerror("Erreur", "Impossible d'envoyer un email : adresse email introuvable.")

# Interface Functions
def open_admin_interface():
    def view_users():
        try:
            utilisateurs_df = pd.read_csv(UTILISATEURS_FILE)
            display_csv_in_treeview(utilisateurs_df, title="Liste des utilisateurs")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la lecture des utilisateurs : {e}")

    def view_logs():
        try:
            if os.path.exists(REQUETES_FILE):
                logs_df = pd.read_csv(REQUETES_FILE)
                display_csv_in_treeview(logs_df, title="Logs des requêtes", window_size="1000x600")
            else:
                messagebox.showinfo("Logs des requêtes", "Aucun log trouvé.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la lecture des logs : {e}")

    def modify_user():
        username = simpledialog.askstring("Modifier un utilisateur", "Entrez le nom d'utilisateur à modifier :")
        if not username:
            messagebox.showerror("Erreur", "Nom d'utilisateur non fourni.")
            return

        try:
            utilisateurs_df = pd.read_csv(UTILISATEURS_FILE)
            if username not in utilisateurs_df["nom_utilisateur"].values:
                messagebox.showerror("Erreur", f"L'utilisateur '{username}' n'existe pas.")
                return

            new_email = simpledialog.askstring("Modifier email", "Entrez le nouvel email :")
            new_password = simpledialog.askstring("Modifier mot de passe", "Entrez le nouveau mot de passe :", show="*")

            if not new_email or not new_password:
                messagebox.showerror("Erreur", "Tous les champs doivent être remplis.")
                return

            utilisateurs_df.loc[utilisateurs_df["nom_utilisateur"] == username, ["email", "mot_de_passe"]] = [new_email, hash_password(new_password)]
            utilisateurs_df.to_csv(UTILISATEURS_FILE, index=False)
            messagebox.showinfo("Succès", f"Les informations de l'utilisateur '{username}' ont été modifiées avec succès.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la modification : {e}")

    def delete_user():
        username = simpledialog.askstring("Supprimer un utilisateur", "Entrez le nom d'utilisateur à supprimer :")
        if not username:
            messagebox.showerror("Erreur", "Nom d'utilisateur non fourni.")
            return

        try:
            utilisateurs_df = pd.read_csv(UTILISATEURS_FILE)
            if username not in utilisateurs_df["nom_utilisateur"].values:
                messagebox.showerror("Erreur", f"L'utilisateur '{username}' n'existe pas.")
                return

            utilisateurs_df = utilisateurs_df[utilisateurs_df["nom_utilisateur"] != username]
            utilisateurs_df.to_csv(UTILISATEURS_FILE, index=False)
            messagebox.showinfo("Succès", f"L'utilisateur '{username}' a été supprimé avec succès.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la suppression : {e}")

    admin_window = tk.Toplevel()
    admin_window.title("Interface Administrateur")
    admin_window.geometry("450x400")

    tk.Button(admin_window, text="Voir les utilisateurs", command=view_users).pack(pady=10)
    tk.Button(admin_window, text="Voir les logs", command=view_logs).pack(pady=10)
    tk.Button(admin_window, text="Voir les produits", command=ask_and_read_file).pack(pady=10)
    tk.Button(admin_window, text="Modifier un produit", command=modify_product).pack(pady=10)
    tk.Button(admin_window, text="Supprimer un produit", command=delete_product).pack(pady=10)
    tk.Button(admin_window, text="Modifier un utilisateur", command=modify_user).pack(pady=10)
    tk.Button(admin_window, text="Supprimer un utilisateur", command=delete_user).pack(pady=10)
    tk.Button(admin_window, text="Quitter", command=admin_window.destroy).pack(pady=10)

def open_user_interface(username):
    def choose_and_display_file():
        file_name = simpledialog.askstring("Choisir un fichier", "Entrez le nom du fichier à afficher :")
        if file_name:
            read_user_products(file_name, username)

    def create_new_file():
        file_name = simpledialog.askstring("Créer un fichier", "Entrez le nom du fichier à créer :")
        if file_name:
            create_file(file_name)

    def add_entry_to_file():
        file_name = simpledialog.askstring("Ajouter une entrée", "Entrez le nom du fichier :")
        if file_name:
            nom = simpledialog.askstring("Ajouter une entrée", "Entrez le nom :")
            prix = simpledialog.askfloat("Ajouter une entrée", "Entrez le prix :")
            quantite = simpledialog.askinteger("Ajouter une entrée", "Entrez la quantité :")
            if nom and prix is not None and quantite is not None:
                row = {"Nom": nom, "Prix": prix, "Quantité": quantite, "Propriétaire": username}
                add_to_file(file_name, row)

    def search_binary():
        file_name = simpledialog.askstring("Recherche binaire", "Entrez le nom du fichier :")
        critere = simpledialog.askstring("Recherche binaire", "Entrez le critère (Nom, Prix, Quantité) :")
        valeur = simpledialog.askstring("Recherche binaire", "Entrez la valeur à rechercher :")
        if file_name and critere and valeur:
            fonctionrecherchebinaire(file_name, critere, valeur)

    def sort_file_by_price():
        file_name = simpledialog.askstring("Tri par prix", "Entrez le nom du fichier :")
        if file_name:
            sort_by_price(file_name, username)

    def sort_file_by_quantity():
        file_name = simpledialog.askstring("Tri par quantité", "Entrez le nom du fichier :")
        if file_name:
            sort_by_quantity(file_name, username)

    def sort_file_by_name():
        file_name = simpledialog.askstring("Tri par nom", "Entrez le nom du fichier :")
        if file_name:
            sort_by_name(file_name, username)

    def clear_file_contents():
        file_name = simpledialog.askstring("Supprimer un produit", "Entrez le nom du fichier :")
        if file_name:
            product_name = simpledialog.askstring("Supprimer un produit", "Entrez le nom du produit à supprimer :")
            if product_name:
                path = os.path.join(DATA_FOLDER, file_name if file_name.endswith('.csv') else f"{file_name}.csv")
                try:
                    df = pd.read_csv(path)
                    if product_name not in df["Nom"].values:
                        messagebox.showerror("Erreur", f"Le produit '{product_name}' n'existe pas dans le fichier '{file_name}'.")
                        return

                    df = df[df["Nom"] != product_name]
                    df.to_csv(path, index=False)
                    messagebox.showinfo("Succès", f"Le produit '{product_name}' a été supprimé avec succès du fichier '{file_name}'.")
                except FileNotFoundError:
                    messagebox.showerror("Erreur", "Fichier introuvable.")
                except Exception as e:
                    messagebox.showerror("Erreur", f"Erreur lors de la suppression : {e}")
    def modify_product():
        file_name = simpledialog.askstring("Modifier un produit", "Entrez le nom du fichier :")
        if file_name:
            modify_user_product(file_name, username)

    user_window = tk.Toplevel()
    user_window.title(f"Interface Utilisateur - {username}")
    user_window.geometry("450x550")

    tk.Button(user_window, text="Voir mes produits", command=choose_and_display_file).pack(pady=10)
    tk.Button(user_window, text="Créer un fichier", command=create_new_file).pack(pady=10)
    tk.Button(user_window, text="Ajouter une entrée à un fichier", command=add_entry_to_file).pack(pady=10)
    tk.Button(user_window, text="Rechercher un produit", command=search_binary).pack(pady=10)
    tk.Button(user_window, text="Modifier un produit", command=modify_product).pack(pady=10)
    tk.Button(user_window, text="Tri par prix", command=sort_file_by_price).pack(pady=10)
    tk.Button(user_window, text="Tri par quantité", command=sort_file_by_quantity).pack(pady=10)
    tk.Button(user_window, text="Tri par nom", command=sort_file_by_name).pack(pady=10)
    tk.Button(user_window, text="Supprimer un produit", command=clear_file_contents).pack(pady=10)
    tk.Button(user_window, text="Quitter", command=user_window.destroy).pack(pady=10)

# Main Application
if __name__ == "__main__":
    if not os.path.exists(DATA_FOLDER):
        os.makedirs(DATA_FOLDER)

    root = tk.Tk()
    root.title("Gestion des utilisateurs")
    root.geometry("400x300")

    tk.Label(root, text="Bienvenue", wraplength=300, justify="center").pack(pady=10)
    tk.Button(root, text="S'inscrire", command=handle_registration).pack(pady=10)
    tk.Button(root, text="Se connecter", command=handle_login).pack(pady=10)
    tk.Button(root, text="Quitter", command=root.quit).pack(pady=10)

    root.mainloop()
