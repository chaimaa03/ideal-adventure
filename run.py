from app import create_app
from flask import render_template
from app.extensions import db
from flask_migrate import Migrate, init, migrate, upgrade

app = create_app()
#for rule in app.url_map.iter_rules():
 #   print(rule)

if __name__ == '__main__':
    app.run(debug=True)