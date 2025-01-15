import os
import tkinter as tk
from tkinter import messagebox, simpledialog
from Fonctions.GestionFichiers.fonctioncreer import fonctioncreer as create_file
from Fonctions.GestionFichiers.fonctionajout import fonctionajout as add_product
from Fonctions.GestionFichiers.fonctionlire import fonctionlire as read_file
from Fonctions.GestionFichiers.fonctionsupp import fonctionsupp as delete_product

# Chemin vers le dossier 'Data'
DATA_FOLDER = os.path.abspath("Data")
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

def create_csv_file():
    nom_fichier = simpledialog.askstring("Créer un fichier", "Entrez le nom du fichier en .csv à créer :")
    if nom_fichier:
        if not nom_fichier.lower().endswith('.csv'):
            nom_fichier += '.csv'
        chemin_complet = os.path.join(DATA_FOLDER, os.path.basename(nom_fichier))
        create_file(chemin_complet)
        messagebox.showinfo("Succès", f"Le fichier '{nom_fichier}' a été créé dans le dossier 'Data'.")

def add_product_to_file():
    nom_fichier = simpledialog.askstring("Ajouter un produit", "Entrez le nom du fichier .csv :")
    if nom_fichier:
        chemin_complet = os.path.join(DATA_FOLDER, nom_fichier)
        produit = simpledialog.askstring("Ajouter un produit", "Entrez le nom du produit :")
        prix = simpledialog.askfloat("Ajouter un produit", "Entrez le prix du produit (en euros):")
        quantite = simpledialog.askinteger("Ajouter un produit", "Entrez la quantité du produit :")
        if produit and prix and quantite:
            add_product(chemin_complet, produit, prix, quantite, "Utilisateur")
            messagebox.showinfo("Succès", f"Le produit '{produit}' a été ajouté avec succès.")

def read_file_content():
    nom_fichier = simpledialog.askstring("Lire un fichier", "Entrez le nom du fichier à lire :")
    if nom_fichier:
        chemin_complet = os.path.join(DATA_FOLDER, nom_fichier)
        try:
            contenu = read_file(chemin_complet, "Utilisateur")
            text_window = tk.Toplevel()
            text_window.title(f"Contenu du fichier - {nom_fichier}")
            text_area = tk.Text(text_window, wrap=tk.WORD, width=80, height=20)
            text_area.insert(tk.END, contenu)
            text_area.pack(padx=10, pady=10)
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de lire le fichier : {e}")

def delete_product_from_file():
    nom_fichier = simpledialog.askstring("Supprimer un produit", "Entrez le nom du fichier :")
    if nom_fichier:
        chemin_complet = os.path.join(DATA_FOLDER, nom_fichier)
        try:
            result = delete_product(chemin_complet, "Utilisateur")
            messagebox.showinfo("Succès", result)
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de supprimer : {e}")

root = tk.Tk()
root.title("Gestion des utilisateurs")
root.geometry("400x300")

tk.Button(root, text="Créer un fichier", command=create_csv_file).pack(pady=10)
tk.Button(root, text="Ajouter un produit", command=add_product_to_file).pack(pady=10)
tk.Button(root, text="Lire un fichier", command=read_file_content).pack(pady=10)
tk.Button(root, text="Supprimer un produit", command=delete_product_from_file).pack(pady=10)
tk.Button(root, text="Quitter", command=root.quit).pack(pady=10)

root.mainloop()
