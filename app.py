# app.py

from models import create_db

# Crée la base de données au démarrage
create_db()

# Importer l'interface utilisateur
import views
