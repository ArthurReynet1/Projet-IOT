
import sqlite3
import json
import datetime
import os

from flask import Flask, render_template, request, redirect, session, jsonify, send_from_directory
from flask_session import Session




#Création de l'application Flask et parametrage de celle-ci.
app = Flask(__name__, template_folder='views', static_url_path='', static_folder='static')

app.config['SESSION_TYPE'] = 'filesystem' #pour que les sessions soient stockées dans le système de fichiers (au meme endroit que le programme)
app.config['SESSION_PERMANENT'] = False #pour que les sessions ne soient pas permanentes c'est a dire qu'elles expirent quand le navigateur est fermé
Session(app) #pour initialiser de l'extension flask-session avec les paramètres ci-dessus définis

app.secret_key = 'seed_projet_iot' #clé secrète pour signer les cookies de session

UPLOAD_FOLDER = 'uploads' #dossier d'uploads pour le graphique.png
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER #enregistrement de la variable UPLOAD_FOLDER dans la configuration de l'application Flask


#Fonction pour lire le fichier json et le mettre dans une liste.
def read_file():
    with open('data.json', 'r') as fichier:
        data = fichier.read()
    return data


#Fonction pour ecrire dans la base de donnée les données du fichier json.
def write():
    data=json.loads(read_file())
    connection = sqlite3.connect('Station_meteo.db')
    cursor = connection.cursor()
    date_releve=datetime.datetime.now().strftime("%H:%M:%S")

    moy_temp=round(data["data"][0]["temperature"],2)
    moy_humidite=round(data["data"][1]["humidity"],2)
    moy_pression=round(data["data"][2]["pressure"],2)
    cursor.execute("""select actif_Sonde from Sonde where id_Sonde=1;""")
    data=cursor.fetchall()
    if data[0][0] == 1:
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


#Création de la fonction "pictogramme"
def pictogramme():
    connection=sqlite3.connect('Station_meteo.db')
    cursor=connection.cursor()
    cursor.execute("""SELECT moy_temp,moy_humidite,moy_pression FROM Releve ORDER BY id_Releve DESC LIMIT 1;""")
    data=cursor.fetchall()
    connection.commit()
    connection.close()
    for releve in data:
        temperature=releve[0]
        humidite=releve[1]
        pression=releve[2]
    if temperature >= 25 and humidite <= 50:
        pictogramme = "☀️"
    elif temperature < 0 and humidite <= 70:
        pictogramme = "❄️"
    elif pression > 1025:
        pictogramme = "☁️"
    elif humidite > 80:
        pictogramme = "🌧️"
    else:
        pictogramme = "☁️"
    return pictogramme

def est_admin():
    connection=sqlite3.connect('Station_meteo.db')
    cursor=connection.cursor()
    cursor.execute("""SELECT id_Utilisateur FROM Utilisateur WHERE admin_utilisateur=1;""")
    data=cursor.fetchall()
    connection.commit()
    connection.close()
    for utilisateur in data:
        if session.get('id_Utilisateur') == utilisateur[0]:
            return True
    return False
    

#Création de la route "/"(home) qui permet de renvoyer les données de la table Releve, le pictogramme ainsi que l'etat de l'utilisateur si il est actif ou non.
@app.route('/', methods=['GET'])
def home():
   write()
   connection=sqlite3.connect('Station_meteo.db')
   cursor=connection.cursor()
   cursor.execute("""SELECT moy_temp,moy_humidite,moy_pression FROM Releve ORDER BY id_Releve DESC LIMIT 1;""")
   data=cursor.fetchall()
   connection.commit()
   connection.close()
   admin=est_admin()

   actif = session.get('actif_utilisateur', False) #récupération de l'état de l'utilisateur


   table_releve=[]
   for releve in data:
       table_releve.append({
       "moy_temp":releve[0],
       "moy_humidite":releve[1],
       "moy_pression":releve[2]})
   return render_template('index.html',releve=table_releve,emoji=pictogramme(),actif=actif,admin=admin)


#Création de la route "/list" pour lister les sondes.
@app.route('/list', methods=['GET','POST'])
def list_sonde():
   admin=est_admin()
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
   return render_template('modification.html',table_sonde=table_sonde,admin=admin)


#Création de la route "/edit" pour modifier l'etat d'une sonde.
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

    return redirect('/list')




#Création de la route "delete" pour supprimer une sonde.
@app.route('/delete/<id_Sonde>')
def delete_sonde(id_Sonde):
   connection=sqlite3.connect('Station_meteo.db')
   cursor=connection.cursor()
   cursor.execute('DELETE FROM Sonde WHERE id_Sonde = ?', (id_Sonde,))
   connection.commit()
   connection.close()
   return redirect('/list')


#Création de la route "/add" pour ajouter une sonde.
@app.route('/add', methods=['GET','POST'])
def add_sonde():
    if request.method == 'POST':
        name_sonde=request.values.get("nom")
        connection=sqlite3.connect('Station_meteo.db')
        cursor=connection.cursor()
        cursor.execute("""INSERT INTO Sonde(
                       name_sonde,
                       actif_sonde
                       ) 
                       VALUES (?, ?)""", (name_sonde,0))
        connection.commit()
        connection.close()

        return redirect('/list')
    else:
        return render_template('add.html')
    

#Création de la route "/api/data" pour renvoyer toutes les entrées en json.
@app.route('/api/data', methods=['GET'])
def get_data():
    connection=sqlite3.connect('Station_meteo.db')
    cursor=connection.cursor()
    cursor.execute("""SELECT * FROM Releve;""")
    data=cursor.fetchall()
    connection.commit()
    connection.close()
    return jsonify({"data": data})


#Création de la route "/writejson" qui permet de modifier le fichier json qu'on recoit de l'ESP.
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
    with open('data.json', 'w') as json_file:
        json_file.write(str(modified_str))

    return "JSON data received successfully"


#Création de la route "/login" qui permet de se connecter au site.
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        mail=request.values.get("mail")
        mdp=request.values.get("mdp")
        connection=sqlite3.connect('Station_meteo.db')
        cursor=connection.cursor()
        cursor.execute("""SELECT id_Utilisateur,mail_utilisateur,mdp_utilisateur FROM Utilisateur;""")
        data=cursor.fetchall()


        for i in range (len(data)):
            if mail == data[i][1] and mdp == data[i][2]:
                session['actif_utilisateur'] = True #enregistrement de l'état de l'utilisateur dans la session
                session['id_Utilisateur'] = data[i][0] #enregistrement de l'id de l'utilisateur dans la session
                cursor.execute("""UPDATE Utilisateur SET actif_utilisateur=1 WHERE mail_utilisateur=?;""",(mail,))
                
        connection.commit()
        connection.close()

        return redirect('/')
    return render_template('login.html')


#Création de la table "/logout" qui permet de se déconnecter du site.
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    connection=sqlite3.connect('Station_meteo.db')
    cursor=connection.cursor()
    cursor.execute("""UPDATE Utilisateur SET actif_utilisateur=0 where id_Utilisateur=? ;""",(session.get('id_Utilisateur'),)) 
    session.pop('actif_utilisateur', None)#suppression de l'état de l'utilisateur dans la session car si on fait session['actif_utilisateur'] = False, la session ne sera pas supprimée
    connection.commit()
    connection.close()

    return redirect('/')



#Création de la table "inscription" qui permet de crée un compte.
@app.route('/inscription', methods=['GET', 'POST'])
def inscription():
    if request.method == 'POST':
        mail=request.values.get("mail")
        nom=request.values.get("nom")
        mdp=request.values.get("mdp")
        connection=sqlite3.connect('Station_meteo.db')
        cursor=connection.cursor()
        cursor.execute("""SELECT mail_utilisateur FROM Utilisateur;""")
        data=cursor.fetchall()
        for utilisateur in data:
            if mail == utilisateur[0]:
                return redirect('/inscription')
        cursor.execute("""INSERT INTO Utilisateur(
                       name_utilisateur,
                       mail_utilisateur,
                       mdp_utilisateur,
                       date_inscription_utilisateur,
                       actif_utilisateur
                       ) 
                       VALUES (?,?,?,?,?);""",(nom,mail,mdp,datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),0))
        connection.commit()
        connection.close()

        return redirect('/login')
    return render_template('register.html')

@app.route('/api/save-graph', methods=['POST'])
def save_graph():
    try:
        if 'graphImage' not in request.files: #Vérifie si le fichier est présent dans la requête
            return jsonify({'success': False, 'error': 'Aucun fichier trouvé'}) #Si le fichier n'est pas trouvé, on renvoie une erreur
        file = request.files['graphImage'] #Récupère le fichier envoyé par l'utilisateur
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True) #Assurez-vous que le dossier d'uploads existe
        filename = 'graph.png' #Générez un nom de fichier unique
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename)) #Enregistre le fichier dans le dossier d'uploads
        permanent_link = f'/uploads/{filename}' #Génère un lien permanent vers le fichier sauvegardé

        return jsonify({'success': True, 'permanentLink': permanent_link})  #Renvoie le lien permanent vers le fichier sauvegardé

    except Exception as e: #Si une erreur se produit, on renvoie une erreur
        return jsonify({'success': False, 'error': str(e)})

@app.route('/graph/<filename>')
def graph_page(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, mimetype='image/png') #envoie le fichier graph.png dans le dossier uploads

@app.route('/connexion', methods=['GET'])
def list_utilisateur():
   connection=sqlite3.connect('Station_meteo.db')
   cursor=connection.cursor()
   cursor.execute("""SELECT id_Utilisateur, name_utilisateur, mail_utilisateur, actif_utilisateur, admin_utilisateur FROM Utilisateur;""")
   data=cursor.fetchall()
   connection.commit()
   connection.close()
   id_Utilisateur=session.get('id_Utilisateur')
   table_utilisateur=[]
   for utilisateur in data:
       table_utilisateur.append({
       "id_Utilisateur":utilisateur[0],
       "name_utilisateur":utilisateur[1],
       "mail_utilisateur":utilisateur[2],
       "actif_utilisateur":utilisateur[3],
       "admin_utilisateur":utilisateur[4]}) 
   return render_template('connexion.html',table_utilisateur=table_utilisateur,id_Utilisateur=id_Utilisateur)


@app.route('/edit/admin/<id_Utilisateur>')
def edit_admin(id_Utilisateur):
    connection=sqlite3.connect('Station_meteo.db')
    cursor=connection.cursor()
    cursor.execute('SELECT admin_utilisateur FROM Utilisateur WHERE id_Utilisateur = ?', (id_Utilisateur,))
    data=cursor.fetchall()
    if data[0][0] == 0:
        cursor.execute('UPDATE Utilisateur SET admin_utilisateur = 1 WHERE id_Utilisateur = ?', (id_Utilisateur,))
    else:
        cursor.execute('UPDATE Utilisateur SET admin_utilisateur = 0 WHERE id_Utilisateur = ?', (id_Utilisateur,))
    connection.commit()
    connection.close()

    return redirect('/connexion')


#Lance le serveur web que si le programme est exécuter en tant que programme principale.
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

    
