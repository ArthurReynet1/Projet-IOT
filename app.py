import flask
import sqlite3
import json
import datetime
from flask import request
app = flask.Flask(__name__, template_folder='views', static_url_path='', static_folder='static')

#fonction pour lire le fichier json et le mettre dans une liste
def read_file():
    with open('data.json', 'r') as fichier:
        data = fichier.read()
    return data
#fonction pour ecrire dans la base de donnée les données du fichier json
def write():
    data=json.loads(read_file())
    connection = sqlite3.connect('Station_meteo.db')
    cursor = connection.cursor()
    date_releve=datetime.datetime.now().strftime("%H:%M:%S")
    moy_temp=round(data["data"][0]["temperature"],2)
    moy_humidite=round(data["data"][1]["humidity"],2)
    moy_pression=round(data["data"][2]["pressure"],2)
    cursor.execute("""insert into Releve(date_releve,moy_temp,moy_humidite,moy_pression,id_Sonde) values (?,?,?,?,?);""",(date_releve,moy_temp,moy_humidite,moy_pression,1))
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
   #print(table_releve)
   return flask.render_template('index.html',releve=table_releve,emoji=pictogramme())

@app.route('/list', methods=['GET','POST'])
def list_sonde():
   connection=sqlite3.connect('Station_meteo.db')
   cursor=connection.cursor()
   cursor.execute("""select * from Sonde;""")
   data=cursor.fetchall()
   connection.commit()
   connection.close()
   table_sonde=[]
   for sonde in data:
       table_sonde.append({
       "id_Sonde":sonde[0],
       "name_sonde":sonde[1],
       "actif_sonde":sonde[2]}) 
   return flask.render_template('modification.html',table_sonde=table_sonde)


@app.route('/edit/<id_Sonde>')
def edit_sonde(id_Sonde):
    connection=sqlite3.connect('Station_meteo.db')
    cursor=connection.cursor()
    cursor.execute('SELECT actif_sonde FROM Sonde WHERE id_Sonde = ?', (id_Sonde,))
    data=cursor.fetchall()
    if data[0][0] == 0:
        cursor.execute('UPDATE Sonde SET actif_sonde = 1 WHERE id_Sonde = ?', (id_Sonde,))
    else:
        cursor.execute('UPDATE Sonde SET actif_sonde = 0 WHERE id_Sonde = ?', (id_Sonde,))
    connection.commit()
    connection.close()
    print(data)

    return flask.redirect('/list')

@app.route('/delete/<id_Sonde>')
def delete_sonde(id_Sonde):
   connection=sqlite3.connect('Station_meteo.db')
   cursor=connection.cursor()
   cursor.execute('DELETE FROM Sonde WHERE id_Sonde = ?', (id_Sonde,))
   connection.commit()
   connection.close()

   return flask.redirect('/list')

@app.route('/add', methods=['GET','POST'])
def add_sonde():
    if flask.request.method == 'POST':
        name_sonde=flask.request.values.get("nom")
        connection=sqlite3.connect('Station_meteo.db')
        cursor=connection.cursor()
        cursor.execute('INSERT INTO Sonde(name_sonde, actif_sonde) VALUES (?, ?)', (name_sonde,0))
        connection.commit()
        connection.close()

        return flask.redirect('/list')
    else:
        return flask.render_template('add.html')

@app.route('/api/data', methods=['GET'])
def get_data():
    connection=sqlite3.connect('Station_meteo.db')
    cursor=connection.cursor()
    cursor.execute("""select * from Releve;""")
    data=cursor.fetchall()
    connection.commit()
    connection.close()
    return flask.jsonify({"data": data})


@app.route('/writejson', methods=['POST'])
def write_json():
    data = request.get_json()
    print("Received JSON data:", data)
    modified_str =''
    for char in str(data):
        if char == "'":
            modified_str += '"'
        else:
            modified_str += char
    #print("modified JSON data:", modified_str)
    with open('data.json', 'w') as json_file:
        json_file.write(str(modified_str))

    return "JSON data received successfully"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
#pour demain : faire des routes pour pouvoir supprimer et mettre a jour les données de la base de donnée via le site web
