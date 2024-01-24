import flask
import sqlite3
import json
import datetime

app = flask.Flask(__name__, template_folder='views', static_url_path='', static_folder='static')

#fonction pour lire le fichier json et le mettre dans une liste
def read_file():
    with open('JSON/data.json', 'r') as fichier:
        data = fichier.read()
    return data
#fonction pour ecrire dans la base de donnée les données du fichier json
def write():
    data=json.loads(read_file())
    connection = sqlite3.connect('Station_meteo.db')
    cursor = connection.cursor()
    for i in range(len(data["data"])):
        date_releve=datetime.datetime.now().strftime("%H:%M:%S")
        moy_temp=data["data"][i]["temperature"]
        moy_humidite=data["data"][i]["humidity"]
        moy_pression=data["data"][i]["pressure"]
        id_Sonde=data["data"][i]["sensor_id"]
        cursor.execute("""insert into Releve(date_releve,moy_temp,moy_humidite,moy_pression,id_Sonde) values (?,?,?,?,?);""",(date_releve,moy_temp,moy_humidite,moy_pression,id_Sonde))
    connection.commit()
    connection.close()

def pictogramme():
    connection=sqlite3.connect('Station_meteo.db')
    cursor=connection.cursor()
    cursor.execute("""select moy_temp,moy_humidite,moy_pression from Releve order by date_releve desc limit 1;""")
    data=cursor.fetchall()
    connection.commit()
    connection.close()
    for releve in data:
        temperature=releve[0]
        humidite=releve[1]
        pression=releve[2]
    if temperature >= 25 and pression <= 101325 and humidite <= 50:
        pictogramme = "☀️"
    elif temperature < 10 and pression <= 101325 and humidite <= 70:
        pictogramme = "❄️"
    elif pression > 101325:
        pictogramme = "☁️"
    elif humidite > 80:
        pictogramme = "🌧️"
    else:
        pictogramme = "☁️"
    return pictogramme


@app.route('/', methods=['GET'])
def home():
   write()
   connection=sqlite3.connect('Station_meteo.db')
   cursor=connection.cursor()
   cursor.execute("""select moy_temp,moy_humidite,moy_pression from Releve order by date_releve desc limit 1;""")
   data=cursor.fetchall()
   connection.commit()
   connection.close()
   table_releve=[]
   for releve in data:
       table_releve.append({
       "moy_temp":releve[0],
       "moy_humidite":releve[1],
       "moy_pression":releve[2]})
   return flask.render_template('index.html',releve=table_releve,emoji=pictogramme())

@app.route('/api/data', methods=['GET'])
def get_data():
    connection=sqlite3.connect('Station_meteo.db')
    cursor=connection.cursor()
    cursor.execute("""select * from Releve;""")
    data=cursor.fetchall()
    connection.commit()
    connection.close()
    return flask.jsonify({"data": data})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
#pour demain : faire des routes pour pouvoir supprimer et mettre a jour les données de la base de donnée via le site web
