import flask
import sqlite3
import json
import datetime
import os
import uuid
from flask import request
from flask import jsonify
from flask import send_from_directory

app = flask.Flask(__name__, template_folder='views', static_url_path='', static_folder='static')

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
    cursor.execute("""INSERT INTO Releve(
                   date_releve,
                   moy_temp,
                   moy_humidite,
                   moy_pression,
                   id_Sonde
                   ) 
                   VALUES (?,?,?,?,?);""",(date_releve,moy_temp,moy_humidite,moy_pression,1))
    connection.commit()
    connection.close()



def pictogramme():
    connection=sqlite3.connect('Station_meteo.db')
    cursor=connection.cursor()
    cursor.execute("""SELECT moy_temp,moy_humidite,moy_pression FROM Releve ORDER BY date_releve DESC LIMIT 1;""")
    data=cursor.fetchall()
    connection.commit()
    connection.close()
    for releve in data:
        temperature=releve[0]
        humidite=releve[1]
        pression=releve[2]
    if temperature >= 25 and pression <= 10 and humidite <= 50:
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
   actif=0
   write()
   connection=sqlite3.connect('Station_meteo.db')
   cursor=connection.cursor()
   cursor.execute("""SELECT moy_temp,moy_humidite,moy_pression FROM Releve ORDER BY id_Releve DESC LIMIT 1;""")
   data=cursor.fetchall()
   connection.commit()
   connection.close()
   connection=sqlite3.connect('Station_meteo.db')
   cursor=connection.cursor()
   
   cursor.execute("""SELECT COUNT(*) FROM Utilisateur WHERE actif_utilisateur=1;""")
   data2=cursor.fetchall()
   if data2[0][0] == 1:
       actif=1
   connection.commit()
   connection.close()
   table_releve=[]
   for releve in data:
       table_releve.append({
       "moy_temp":releve[0],
       "moy_humidite":releve[1],
       "moy_pression":releve[2]})
   #print(table_releve)
   return flask.render_template('index.html',releve=table_releve,emoji=pictogramme(),actif=actif)



@app.route('/list', methods=['GET','POST'])
def list_sonde():
   connection=sqlite3.connect('Station_meteo.db')
   cursor=connection.cursor()
   cursor.execute("""SELECT * FROM Sonde;""")
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
        cursor.execute("""INSERT INTO Sonde(
                       name_sonde,
                       actif_sonde
                       ) 
                       VALUES (?, ?)""", (name_sonde,0))
        connection.commit()
        connection.close()

        return flask.redirect('/list')
    else:
        return flask.render_template('add.html')
    


@app.route('/api/data', methods=['GET'])
def get_data():
    connection=sqlite3.connect('Station_meteo.db')
    cursor=connection.cursor()
    cursor.execute("""SELECT * FROM Releve;""")
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



@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'POST':
        mail=flask.request.values.get("mail")
        mdp=flask.request.values.get("mdp")
        connection=sqlite3.connect('Station_meteo.db')
        cursor=connection.cursor()
        cursor.execute("""SELECT mail_utilisateur,mdp_utilisateur FROM Utilisateur;""")
        data=cursor.fetchall()
        connection.commit()
        connection.close()

        for i in range (len(data)):
            if mail == data[i][0] and mdp == data[i][1]:
                connection=sqlite3.connect('Station_meteo.db')
                cursor=connection.cursor()
                cursor.execute("""UPDATE Utilisateur SET actif_utilisateur=1 
                                WHERE mail_utilisateur = ? AND mdp_utilisateur=?;""",(mail,mdp,))
                connection.commit()
                connection.close()
        return flask.redirect('/')
    return flask.render_template('login.html')



@app.route('/logout', methods=['GET', 'POST'])
def logout():
    connection=sqlite3.connect('Station_meteo.db')
    cursor=connection.cursor()
    cursor.execute("""UPDATE Utilisateur SET actif_utilisateur=0;""")
    connection.commit()
    connection.close()

    return flask.redirect('/')




@app.route('/inscription', methods=['GET', 'POST'])
def inscription():
    if flask.request.method == 'POST':
        mail=flask.request.values.get("mail")
        nom=flask.request.values.get("nom")
        mdp=flask.request.values.get("mdp")
        connection=sqlite3.connect('Station_meteo.db')
        cursor=connection.cursor()
        cursor.execute("""SELECT mail_utilisateur FROM Utilisateur;""")
        data=cursor.fetchall()
        for utilisateur in data:
            if mail == utilisateur[0]:
                return flask.redirect('/inscription')
        cursor.execute("""INSERT INTO Utilisateur(
                       name_utilisateur,
                       mail_utilisateur,
                       mdp_utilisateur,
                       date_inscription_utilisateur,
                       actif_utilisateur
                       ) 
                       VALUES (?,?,?,?,?);""",(nom,mail,mdp,datetime.datetime.now().strftime("%H:%M:%S"),0))
        connection.commit()
        connection.close()

        return flask.redirect('/login')
    return flask.render_template('register.html')

@app.route('/api/save-graph', methods=['POST'])
def save_graph():
    try:
        if 'graphImage' not in request.files:
            return jsonify({'success': False, 'error': 'Aucun fichier trouvé'})

        file = request.files['graphImage']

        # Assurez-vous que le dossier d'uploads existe
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

        # Générez un nom de fichier unique
        filename = 'graph.png'

        # Enregistrez le fichier dans le dossier d'uploads
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Générez un lien permanent vers le fichier sauvegardé
        permanent_link = f'/uploads/{filename}'

        return jsonify({'success': True, 'permanentLink': permanent_link})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/uploads/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

    
