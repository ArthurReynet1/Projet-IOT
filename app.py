import flask
import sqlite3
import json
import datetime

app = flask.Flask(__name__, template_folder='views')
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)


#fonction pour lire le fichier json et le mettre dans une liste
def read_file():
    with open('JSON/data.json', 'r') as fichier:
        data = json.loads(fichier)
    return data
#fonction pour ecrire dans la base de donnée les données du fichier json
def write():
    data=read_file()
    connection = sqlite3.connect('Station_meteo.db')
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



@app.route('/', methods=['GET'])

def home():
   write()
   connection=sqlite3.connect('Station_meteo.db')
   cursor=connection.cursor()
   cursor.execute("""select moy_temp,moy_humidite,moy_pression from Releve order by desc limit 1;""")
   data=cursor.fetchall()
   connection.commit()
   connection.close()
   table_releve=[]
   for releve in data:
       table_releve.append({
       "moy_temp":releve[0],
       "moy_humidite":releve[1],
       "moy_pression":releve[2]})
   return flask.render_template('index.html',releve=table_releve)

@app.route('/api/data', methods=['POST'])
def get_data():
    connection=sqlite3.connect('Station_meteo.db')
    cursor=connection.cursor()
    cursor.execute("""select * from releve;""")
    data=cursor.fetchall()
    connection.commit()
    connection.close()
    return flask.jsonify(data)

@app.route('/api/modifications', methods=['POST'])
def get_modifications():
    connection=sqlite3.connect('Station_meteo.db')
    cursor=connection.cursor()
    cursor.execute("""select id_Releve, moy_temp, moy_humidite, moy_pression,id_sonde from modifications;""")
    data=cursor.fetchall()
    connection.commit()
    connection.close()
    return flask.jsonify(data)



#pour demain : faire des routes pour pouvoir supprimer et mettre a jour les données de la base de donnée via le site web
