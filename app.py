import flask
import sqlite3

app = flask.Flask(__name__, template_folder='views')

@app.route('/', methods=['GET'])
def home():
   connection = sqlite3.connect('ma_base_mmo.db')
   cursor = connection.cursor()
   cursor.execute('SELECT * FROM Joueur')
   Joueurs = cursor.fetchall()

   connection.commit()
   connection.close()

   list_joueurs = []

   for Joueur in Joueurs:
      list_joueurs.append({
         "id": Joueur[0],
         "pseudo": Joueur[1],
         "arme": Joueur[3],
         "niveau": Joueur[5],
         "attaque": Joueur[8],
      }) 