from flask import Blueprint, render_template

# Créer un blueprint pour la page d'accueil
base_bp = Blueprint('base', __name__)

# Définir la route pour afficher la page HTML
@base_bp.route('/')
def base():
    return render_template('base.html')