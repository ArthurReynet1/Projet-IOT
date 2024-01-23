import flask
import sqlite3
import json
import datetime
import matplotlib.pyplot as plt

app = flask.Flask(__name__, template_folder='views')
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)


#fonction pour lire le fichier json et le mettre dans une liste
def read_file():
    with open('JSON/data.json', 'r') as fichier:
        data = json.load(fichier)
    return data
#fonction pour ecrire dans la base de donnée les données du fichier json
def write():
    data=json.loads(read_file())
    connection = sqlite3.connect('DATABASE')
    cursor = connection.cursor()
    for i in range(len(data)):
        date_releve=datetime.datetime.now()
        moy_temp=data[i]["moy_temp"]
        moy_humidite=data[i]["moy_humidite"]
        moy_pression=data[i]["moy_pression"]
        id_Sonde=data[i]["id_Sonde"]
        cursor.execute("""insert into Releve(date_releve,moy_temp,moy_humidite,moy_pression,id_Sonde) values (?,?,?,?,?);""",(date_releve,moy_temp,moy_humidite,moy_pression,id_Sonde))
        connection.commit()
        connection.close()


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
   write()
   connection=sqlite3.connect('DATABASE')
   cursor=connection.cursor()
   cursor.execute("""select moy_temp,moy_humidite,moy_pression from Releve order by desc limit 1;""")
   data=cursor.fetchall()
   connection.commit()
   connection.close()
   list_releve=[]
   for releve in data:
       list_releve.append({
       "moy_temp":releve[0],
       "moy_humidite":releve[1],
       "moy_pression":releve[2]

      })
   return flask.render_template('index.html',data)

#pour demain : faire des routes pour pouvoir supprimer et mettre a jour les données de la base de donnée via le site web
