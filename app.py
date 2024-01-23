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
        date_sonde= data[i]["date_sonde"]
        temp_sonde= data[i]["temp_sonde"]
        humidite_sonde= data[i]["humidite_sonde"]
        pression_sonde= data[i]["pression_sonde"]
        cursor.execute("""insert into Sonde(date_sonde,temp_sonde,humidite_sonde,pression_sonde) values (?,?,?,?,?);""",(date_sonde,temp_sonde,humidite_sonde,pression_sonde))
        connection.commit()
        connection.close()
#fonction pour avoir la moyenne des données de la base de donnée et les mettre dans la table Releve
def moyenne():
    connection = sqlite3.connect('DATABASE')
    cursor = connection.cursor()
    moyenne_temp=cursor.execute("""select avg(temp_sonde) from Sonde;""")
    moyenne_humidite=cursor.execute("""select avg(humidite_sonde) from Sonde;""")
    moyenne_pression=cursor.execute("""select avg(pression_sonde) from Sonde;""")
    cursor.execute("""insert into Releve(date_releve,moy_temp,moy_humidite,moy_pression) values (?,?,?,?);""",(datetime.datetime.now(),moyenne_temp,moyenne_humidite,moyenne_pression)) #datetime.datetime.now() sert a avoir la date et l'heure actuelle et donc la date du relevé
    connection.commit()
    connection.close()

#fonction qui génére un graphique avec les données de la base de donnée
def graphique():
    connection = sqlite3.connect('DATABASE')
    cursor = connection.cursor()
    cursor.execute("""select moy_humidite from Releve order by desc limit 5;""")
    abscisse = cursor.fetchall()
    cursor.execute("""select moy_temp from Releve order by desc limit 5;""")
    ordonnee= cursor.fetchall()
    plt.plot(abscisse,ordonnee, color='b', marker='+')
    plt.title("Evolution de la température en fonction de l'humidité")
    plt.show()
    connection.commit()
    connection.close()
def pictogramme():




    



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
   moyenne()
   graphique = graphique()
   return flask.render_template('index.html', graphique=graphique)

#pour demain : faire des routes pour pouvoir supprimer et mettre a jour les données de la base de donnée via le site web
