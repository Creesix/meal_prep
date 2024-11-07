# models.py

import sqlite3

def create_db():
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    
    # Table pour les aliments
    c.execute('''
        CREATE TABLE IF NOT EXISTS aliments (
            id INTEGER PRIMARY KEY,
            nom TEXT NOT NULL,
            calories REAL,
            proteines REAL,
            glucides REAL,
            lipides REAL
        )
    ''')
    
    # Table pour les recettes
    c.execute('''
        CREATE TABLE IF NOT EXISTS recettes (
            id INTEGER PRIMARY KEY,
            nom TEXT NOT NULL
        )
    ''')

    # Table pour les ingrédients de recette
    c.execute('''
        CREATE TABLE IF NOT EXISTS ingredients (
            recette_id INTEGER,
            aliment_id INTEGER,
            quantite REAL,
            FOREIGN KEY (recette_id) REFERENCES recettes(id),
            FOREIGN KEY (aliment_id) REFERENCES aliments(id)
        )
    ''')
    
    conn.commit()
    conn.close()