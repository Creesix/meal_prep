# views.py

import tkinter as tk
from tkinter import ttk, messagebox
from controllers import (
    ajouter_aliment, ajouter_recette, ajouter_ingredient, 
    calculer_valeurs_nutritionnelles, modifier_aliment, supprimer_aliment,
    modifier_recette, supprimer_recette, modifier_ingredient, supprimer_ingredient
)
import sqlite3

# Fonction pour vider les champs de saisie
def clear_entries(*entries):
    for entry in entries:
        entry.delete(0, tk.END)

# Fonction pour ajouter un aliment et vider les champs
def ajouter_aliment_vue():
    nom = entry_nom.get()
    calories = float(entry_calories.get())
    proteines = float(entry_proteines.get())
    glucides = float(entry_glucides.get())
    lipides = float(entry_lipides.get())
    ajouter_aliment(nom, calories, proteines, glucides, lipides)
    label_message['text'] = f"Aliment ajouté : {nom}"
    clear_entries(entry_nom, entry_calories, entry_proteines, entry_glucides, entry_lipides)
    afficher_aliments_disponibles()
    mettre_a_jour_menu_aliments()

# Fonction pour ajouter une recette et vider les champs
def ajouter_recette_vue():
    nom_recette = entry_nom_recette.get()
    recette_id = ajouter_recette(nom_recette)
    label_message['text'] = f"Recette ajoutée : {nom_recette} (ID: {recette_id})"
    clear_entries(entry_nom_recette)
    afficher_recettes_disponibles()
    mettre_a_jour_menu_recettes()

# Fonction pour afficher les aliments disponibles
def afficher_aliments_disponibles():
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute('SELECT nom FROM aliments')
    aliments = c.fetchall()
    conn.close()
    
    list_aliments.delete(0, tk.END)
    for aliment in aliments:
        list_aliments.insert(tk.END, aliment[0])

# Fonction pour afficher les recettes disponibles
def afficher_recettes_disponibles():
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute('SELECT nom FROM recettes')
    recettes = c.fetchall()
    conn.close()
    
    list_recettes.delete(0, tk.END)
    for recette in recettes:
        list_recettes.insert(tk.END, recette[0])

# Fonction pour mettre à jour les options de menu déroulant des aliments
def mettre_a_jour_menu_aliments():
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute('SELECT id, nom FROM aliments')
    aliments = c.fetchall()
    conn.close()
    menu_aliments['values'] = [aliment[1] for aliment in aliments]
    global aliments_dict
    aliments_dict = {aliment[1]: aliment[0] for aliment in aliments}  # dictionnaire pour récupérer les IDs

# Fonction pour mettre à jour les options de menu déroulant des recettes
def mettre_a_jour_menu_recettes():
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute('SELECT id, nom FROM recettes')
    recettes = c.fetchall()
    conn.close()
    menu_recettes['values'] = [recette[1] for recette in recettes]
    global recettes_dict
    recettes_dict = {recette[1]: recette[0] for recette in recettes}  # dictionnaire pour récupérer les IDs

# Fonction pour afficher les détails d'une recette sélectionnée
def afficher_details_recette():
    recette_nom = menu_recettes.get()
    if recette_nom:
        recette_id = recettes_dict[recette_nom]
        details = calculer_valeurs_nutritionnelles(recette_id)
        
        # Affichage des valeurs nutritionnelles
        label_calories['text'] = f"Calories : {details['calories']:.2f} kcal"
        label_proteines['text'] = f"Protéines : {details['proteines']:.2f} g"
        label_glucides['text'] = f"Glucides : {details['glucides']:.2f} g"
        label_lipides['text'] = f"Lipides : {details['lipides']:.2f} g"
        
        # Récupérer et afficher la liste des ingrédients
        conn = sqlite3.connect('db.sqlite3')
        c = conn.cursor()
        c.execute('''
            SELECT a.nom, i.quantite
            FROM ingredients i
            JOIN aliments a ON i.aliment_id = a.id
            WHERE i.recette_id = ?
        ''', (recette_id,))
        
        ingredients = c.fetchall()
        conn.close()
        
        list_ingredients.delete(0, tk.END)
        for ingredient in ingredients:
            list_ingredients.insert(tk.END, f"{ingredient[0]} : {ingredient[1]} g")

# Fonction pour ajouter un ingrédient à une recette et mettre à jour l'affichage
def ajouter_ingredient_vue():
    recette_nom = menu_recettes.get()
    aliment_nom = menu_aliments.get()
    quantite = float(entry_quantite.get())
    
    if recette_nom and aliment_nom and quantite:
        recette_id = recettes_dict[recette_nom]
        aliment_id = aliments_dict[aliment_nom]
        ajouter_ingredient(recette_id, aliment_id, quantite)
        label_message['text'] = f"Ingrédient ajouté : {aliment_nom} ({quantite}g) dans {recette_nom}"
        clear_entries(entry_quantite)
        afficher_details_recette()  # Mettre à jour les détails de la recette

# Fonction pour modifier un aliment
def modifier_aliment_vue():
    aliment_nom = menu_aliments.get()
    if aliment_nom:
        aliment_id = aliments_dict[aliment_nom]
        nom = entry_nom.get()
        calories = float(entry_calories.get())
        proteines = float(entry_proteines.get())
        glucides = float(entry_glucides.get())
        lipides = float(entry_lipides.get())
        modifier_aliment(aliment_id, nom, calories, proteines, glucides, lipides)
        label_message['text'] = f"Aliment modifié : {nom}"
        afficher_aliments_disponibles()

# Fonction pour supprimer un aliment
def supprimer_aliment_vue():
    aliment_nom = menu_aliments.get()
    if aliment_nom:
        aliment_id = aliments_dict[aliment_nom]
        supprimer_aliment(aliment_id)
        label_message['text'] = f"Aliment supprimé : {aliment_nom}"
        afficher_aliments_disponibles()

# Fonction pour modifier une recette
def modifier_recette_vue():
    recette_nom = menu_recettes.get()
    if recette_nom:
        recette_id = recettes_dict[recette_nom]
        nom = entry_nom_recette.get()
        modifier_recette(recette_id, nom)
        label_message['text'] = f"Recette modifiée : {nom}"
        afficher_recettes_disponibles()

# Fonction pour supprimer une recette
def supprimer_recette_vue():
    recette_nom = menu_recettes.get()
    if recette_nom:
        recette_id = recettes_dict[recette_nom]
        supprimer_recette(recette_id)
        label_message['text'] = f"Recette supprimée : {recette_nom}"
        afficher_recettes_disponibles()

# Fonction pour modifier un ingrédient
def modifier_ingredient_vue():
    recette_nom = menu_recettes.get()
    aliment_nom = menu_aliments.get()
    quantite = float(entry_quantite.get())
    if recette_nom and aliment_nom:
        recette_id = recettes_dict[recette_nom]
        aliment_id = aliments_dict[aliment_nom]
        modifier_ingredient(recette_id, aliment_id, quantite)
        label_message['text'] = f"Ingrédient modifié : {aliment_nom} ({quantite}g) dans {recette_nom}"
        afficher_details_recette()

# Fonction pour supprimer un ingrédient
def supprimer_ingredient_vue():
    recette_nom = menu_recettes.get()
    aliment_nom = menu_aliments.get()
    if recette_nom and aliment_nom:
        recette_id = recettes_dict[recette_nom]
        aliment_id = aliments_dict[aliment_nom]
        supprimer_ingredient(recette_id, aliment_id)
        label_message['text'] = f"Ingrédient supprimé : {aliment_nom} dans {recette_nom}"
        afficher_details_recette()

# Initialiser la fenêtre principale en plein écran
root = tk.Tk()
root.title("Gestion Nutritionnelle")
root.attributes('-fullscreen', True)  # Lancer en plein écran
root.config(bg="#f0f4f8")  # Couleur de fond douce

# Style général
style = ttk.Style()
style.configure("TLabel", background="#f0f4f8", font=("Arial", 10))
style.configure("TButton", font=("Arial", 10, "bold"), padding=5)
style.configure("TEntry", font=("Arial", 10), padding=5)

# Label de notification en haut de la fenêtre
label_message = ttk.Label(root, text="", foreground="green", background="#f0f4f8")
label_message.grid(row=0, column=0, columnspan=3, pady=(0, 15), sticky="we")

# Frame pour les Aliments
frame_aliment = ttk.LabelFrame(root, text="Gérer les Aliments", padding=10)
frame_aliment.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

# Entrées et boutons pour ajouter/modifier des aliments
ttk.Label(frame_aliment, text="Nom").grid(row=0, column=0, sticky="w")
entry_nom = ttk.Entry(frame_aliment)
entry_nom.grid(row=0, column=1, pady=2)

ttk.Label(frame_aliment, text="Calories (pour 100g)").grid(row=1, column=0, sticky="w")
entry_calories = ttk.Entry(frame_aliment)
entry_calories.grid(row=1, column=1, pady=2)

ttk.Label(frame_aliment, text="Protéines (g)").grid(row=2, column=0, sticky="w")
entry_proteines = ttk.Entry(frame_aliment)
entry_proteines.grid(row=2, column=1, pady=2)

ttk.Label(frame_aliment, text="Glucides (g)").grid(row=3, column=0, sticky="w")
entry_glucides = ttk.Entry(frame_aliment)
entry_glucides.grid(row=3, column=1, pady=2)

ttk.Label(frame_aliment, text="Lipides (g)").grid(row=4, column=0, sticky="w")
entry_lipides = ttk.Entry(frame_aliment)
entry_lipides.grid(row=4, column=1, pady=2)

btn_ajouter_aliment = ttk.Button(frame_aliment, text="Ajouter Aliment", command=lambda: ajouter_aliment_vue())
btn_ajouter_aliment.grid(row=5, column=0, columnspan=2, pady=(10, 0))

btn_modifier_aliment = ttk.Button(frame_aliment, text="Modifier Aliment", command=lambda: modifier_aliment_vue())
btn_modifier_aliment.grid(row=6, column=0, columnspan=2, pady=(5, 0))

btn_supprimer_aliment = ttk.Button(frame_aliment, text="Supprimer Aliment", command=lambda: supprimer_aliment_vue())
btn_supprimer_aliment.grid(row=7, column=0, columnspan=2, pady=(5, 0))

# Liste des aliments disponibles
ttk.Label(frame_aliment, text="Aliments Disponibles").grid(row=8, column=0, columnspan=2, sticky="w")
list_aliments = tk.Listbox(frame_aliment, width=40, height=8, bg="lightgray", selectbackground="blue")
list_aliments.grid(row=9, column=0, columnspan=2, padx=10, pady=5)

# Frame pour les Recettes
frame_recette = ttk.LabelFrame(root, text="Gérer les Recettes", padding=10)
frame_recette.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

ttk.Label(frame_recette, text="Nom de la recette").grid(row=0, column=0, sticky="w")
entry_nom_recette = ttk.Entry(frame_recette)
entry_nom_recette.grid(row=0, column=1, pady=2)

btn_ajouter_recette = ttk.Button(frame_recette, text="Ajouter Recette", command=lambda: ajouter_recette_vue())
btn_ajouter_recette.grid(row=1, column=0, columnspan=2, pady=(10, 0))

btn_modifier_recette = ttk.Button(frame_recette, text="Modifier Recette", command=lambda: modifier_recette_vue())
btn_modifier_recette.grid(row=2, column=0, columnspan=2, pady=(5, 0))

btn_supprimer_recette = ttk.Button(frame_recette, text="Supprimer Recette", command=lambda: supprimer_recette_vue())
btn_supprimer_recette.grid(row=3, column=0, columnspan=2, pady=(5, 0))

# Liste des recettes disponibles
ttk.Label(frame_recette, text="Recettes Disponibles").grid(row=4, column=0, columnspan=2, sticky="w")
list_recettes = tk.Listbox(frame_recette, width=40, height=5, bg="lightgray", selectbackground="blue")
list_recettes.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

# Frame pour Ajouter un Ingrédient à une Recette
frame_ingredient = ttk.LabelFrame(root, text="Ajouter un Ingrédient à une Recette", padding=10)
frame_ingredient.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

# Menu déroulant pour sélectionner une recette
ttk.Label(frame_ingredient, text="Sélectionnez une recette").grid(row=0, column=0, sticky="w")
menu_recettes = ttk.Combobox(frame_ingredient, state="readonly", width=30)
menu_recettes.grid(row=0, column=1, pady=2)

# Menu déroulant pour sélectionner un aliment
ttk.Label(frame_ingredient, text="Sélectionnez un aliment").grid(row=1, column=0, sticky="w")
menu_aliments = ttk.Combobox(frame_ingredient, state="readonly", width=30)
menu_aliments.grid(row=1, column=1, pady=2)

# Entrée pour la quantité
ttk.Label(frame_ingredient, text="Quantité (g)").grid(row=2, column=0, sticky="w")
entry_quantite = ttk.Entry(frame_ingredient)
entry_quantite.grid(row=2, column=1, pady=2)

# Boutons pour ajouter, modifier, et supprimer un ingrédient
btn_ajouter_ingredient = ttk.Button(frame_ingredient, text="Ajouter Ingrédient", command=lambda: ajouter_ingredient_vue())
btn_ajouter_ingredient.grid(row=3, column=0, columnspan=2, pady=(10, 0))

btn_modifier_ingredient = ttk.Button(frame_ingredient, text="Modifier Ingrédient", command=lambda: modifier_ingredient_vue())
btn_modifier_ingredient.grid(row=4, column=0, columnspan=2, pady=(5, 0))

btn_supprimer_ingredient = ttk.Button(frame_ingredient, text="Supprimer Ingrédient", command=lambda: supprimer_ingredient_vue())
btn_supprimer_ingredient.grid(row=5, column=0, columnspan=2, pady=(5, 0))

# Frame pour les Détails de Recette
frame_details = ttk.LabelFrame(root, text="Détails de la Recette", padding=10)
frame_details.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

label_calories = ttk.Label(frame_details, text="Calories : ")
label_calories.grid(row=0, column=0, sticky="w")
label_proteines = ttk.Label(frame_details, text="Protéines : ")
label_proteines.grid(row=1, column=0, sticky="w")
label_glucides = ttk.Label(frame_details, text="Glucides : ")
label_glucides.grid(row=2, column=0, sticky="w")
label_lipides = ttk.Label(frame_details, text="Lipides : ")
label_lipides.grid(row=3, column=0, sticky="w")

# Liste des ingrédients de la recette
ttk.Label(frame_details, text="Ingrédients de la Recette").grid(row=4, column=0, columnspan=2, pady=(10, 5))
list_ingredients = tk.Listbox(frame_details, width=50, height=8, bg="lightgray", selectbackground="blue")
list_ingredients.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

# Fonction d'initialisation pour remplir les menus et listes
def initialize():
    afficher_aliments_disponibles()
    afficher_recettes_disponibles()
    mettre_a_jour_menu_aliments()
    mettre_a_jour_menu_recettes()

# Appel de l'initialisation après la création de tous les widgets
initialize()
root.mainloop()