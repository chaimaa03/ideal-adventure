from app import create_app
from flask import render_template

app = create_app()
#for rule in app.url_map.iter_rules():
 #   print(rule)

if __name__ == '__main__':
    app.run(debug=True)