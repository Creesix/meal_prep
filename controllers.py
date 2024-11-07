# controllers.py

import sqlite3
from models import create_db

def ajouter_aliment(nom, calories, proteines, glucides, lipides):
    """Ajoute un aliment dans la base de données."""
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute('INSERT INTO aliments (nom, calories, proteines, glucides, lipides) VALUES (?, ?, ?, ?, ?)', 
              (nom, calories, proteines, glucides, lipides))
    conn.commit()
    conn.close()
    print(f"Aliment ajouté : {nom}")

def ajouter_recette(nom):
    """Ajoute une nouvelle recette à la base de données."""
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute('INSERT INTO recettes (nom) VALUES (?)', (nom,))
    recette_id = c.lastrowid
    conn.commit()
    conn.close()
    print(f"Recette ajoutée : {nom} (ID: {recette_id})")
    return recette_id  # Retourne l'ID de la recette pour ajouter des ingrédients

def ajouter_ingredient(recette_id, aliment_id, quantite):
    """Ajoute un ingrédient (aliment avec une quantité) à une recette existante."""
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute('INSERT INTO ingredients (recette_id, aliment_id, quantite) VALUES (?, ?, ?)',
              (recette_id, aliment_id, quantite))
    conn.commit()
    conn.close()
    print(f"Ingrédient ajouté : aliment ID {aliment_id} à la recette ID {recette_id} avec quantité {quantite}g")

def calculer_valeurs_nutritionnelles(recette_id):
    """Calcule les valeurs nutritionnelles totales d'une recette en additionnant chaque ingrédient."""
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    
    # Requête pour obtenir les informations nutritionnelles et les quantités de chaque ingrédient de la recette
    c.execute('''
        SELECT a.calories, a.proteines, a.glucides, a.lipides, i.quantite
        FROM ingredients i
        JOIN aliments a ON i.aliment_id = a.id
        WHERE i.recette_id = ?
    ''', (recette_id,))
    
    total_calories = 0
    total_proteines = 0
    total_glucides = 0
    total_lipides = 0
    
    for row in c.fetchall():
        calories, proteines, glucides, lipides, quantite = row
        # Conversion des valeurs nutritionnelles en fonction de la quantité d'ingrédient
        facteur = quantite / 100.0  # On part du principe que les valeurs sont pour 100g
        total_calories += calories * facteur
        total_proteines += proteines * facteur
        total_glucides += glucides * facteur
        total_lipides += lipides * facteur
    
    conn.close()
    
    # Retourner les valeurs nutritionnelles totales
    return {
        "calories": total_calories,
        "proteines": total_proteines,
        "glucides": total_glucides,
        "lipides": total_lipides
    }

# Fonctions pour gérer les aliments
def modifier_aliment(aliment_id, nom, calories, proteines, glucides, lipides):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute('''
        UPDATE aliments SET nom = ?, calories = ?, proteines = ?, glucides = ?, lipides = ? WHERE id = ?
    ''', (nom, calories, proteines, glucides, lipides, aliment_id))
    conn.commit()
    conn.close()

def supprimer_aliment(aliment_id):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute('DELETE FROM aliments WHERE id = ?', (aliment_id,))
    conn.commit()
    conn.close()

# Fonctions pour gérer les recettes
def modifier_recette(recette_id, nom):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute('UPDATE recettes SET nom = ? WHERE id = ?', (nom, recette_id))
    conn.commit()
    conn.close()

def supprimer_recette(recette_id):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute('DELETE FROM recettes WHERE id = ?', (recette_id,))
    # Supprimer également les ingrédients associés
    c.execute('DELETE FROM ingredients WHERE recette_id = ?', (recette_id,))
    conn.commit()
    conn.close()

# Fonctions pour gérer les ingrédients
def modifier_ingredient(recette_id, aliment_id, quantite):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute('''
        UPDATE ingredients SET quantite = ? WHERE recette_id = ? AND aliment_id = ?
    ''', (quantite, recette_id, aliment_id))
    conn.commit()
    conn.close()

def supprimer_ingredient(recette_id, aliment_id):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute('DELETE FROM ingredients WHERE recette_id = ? AND aliment_id = ?', (recette_id, aliment_id))
    conn.commit()
    conn.close()
