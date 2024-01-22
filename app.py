import flask
import sqlite3
import json


app = flask.Flask(__name__, template_folder='views')
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

def read_file():
    with open('JSON/data.json', 'r') as fichier:
        data = json.load(fichier)
    return data
def write():
    data=json.loads(read_file())
    connection = sqlite3.connect('DATABASE')
    cursor = connection.cursor()
    id_sonde= data["id_sonde"]
    date_sonde= data["date_sonde"]
    temp_sonde= data["temp_sonde"]
    humidite_sonde= data["humidite_sonde"]
    pression_sonde= data["pression_sonde"]
    cursor.execute("""insert into Sonde(id_sonde,date_sonde,temp_sonde,humidite_sonde,pression_sonde) values (?,?,?,?,?);""",(id_sonde,date_sonde,temp_sonde,humidite_sonde,pression_sonde))

"""
Temporaire juste pour voir sans changer de fenetre
CREATION DE LA TABLE "Sonde"
sqlite> CREATE TABLE IF NOT EXISTS Sonde(id_Sonde INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, date_sonde DATETIME NOT NULL,
 temp_sonde FLOAT NOT NULL, humidite_sonde INTEGRER NOT NULL, pression_sonde INTEGER NOT NULL );


sqlite> CREATE TABLE IF NOT EXISTS Releve(id_Releve INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, date_releve DATETIME NOT NULL,
moy_temp FLOAT NOT NULL, moy_humidite FLOAT NOT NULL, moy_pression FLOAT NOT NULL );

##(BONUS)CREATION DE LA TABLE "Login"*
sqlite> CREATE TABLE IF NOT EXISTS Login(id_Login INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, date_log DATETIME NOT NULL, 
mail_log TEXT NOT NULL, mdp_log TEXT NOT NULL);
"""


@app.route('/', methods=['GET'])
def home():
   connection = sqlite3.connect('DATABASE')
   cursor = connection.cursor()
   return flask.render_template('index.html')