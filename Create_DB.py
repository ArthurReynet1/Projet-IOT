import sqlite3

#Établir une connexion à la base de données
#et créer un objet de connexion
connection = sqlite3.connect('Station_meteo.db')

#Créer un curseur vers la base de données
cursor = connection.cursor()

print("Ouverture de la base de données")
#Création de la table "Sonde"
cursor.execute ("""
                CREATE TABLE IF NOT EXISTS Sonde(
                id_Sonde INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                name_sonde TEXT NOT NULL)
                ;
""")

connection.commit()

#Création de la table "Relevé"
cursor.execute ("""CREATE TABLE IF NOT EXISTS Releve(
                id_Releve INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                date_releve DATETIME NOT NULL,
                moy_temp FLOAT NOT NULL,
                moy_humidite FLOAT NOT NULL,
                moy_pression FLOAT NOT NULL,
                id_Sonde INTEGER NOT NULL, 
                FOREIGN KEY(id_Sonde) REFERENCES Sonde(id_Sonde)
                );
""")

connection.commit()

#Création de la table "Utilisateur"
"""
curosr.execute (""""""CREATE TABLE IF NOT EXISTS Utilisateur(
                id_Utilisateur INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                name_utilisateur TEXT NOT NULL,
                mail_utilisateur TEXT NOT NULL,
                mdp_utilisateur TEXT NOT NULL,
                date_inscription_utilisateur DATETIME NOT NULL,
                actif_utilisateur INTEGER NOT NULL)
                ;
"""""")
"""

connection.commit()

#Supression de la ligne qui a pour pour resultat "2" dans la colonne "id_Sonde" dans la table "Sonde"  
"""cursor.execute (""""""DELETE FROM Sonde WHERE id_Sonde = 2"""""")

connection.commit()"""

connection.close()

#creation de la vraie sonde dans laquel on va inserer les données envoyées par l'ESP
"""
connection = sqlite3.connect('Station_meteo.db')
cursor = connection.cursor()
cursor.execute(""""""INSERT INTO Sonde(id_Sonde,name_sonde,actif_sonde) VALUES(1,'Vrai Sonde',1)"""""")
connection.commit()
connection.close()
"""
#modification de la table pour ajouter la colonne "admin_utilisateur" a la table "Utilisateur"
"""
connection = sqlite3.connect('Station_meteo.db')
cursor = connection.cursor()
cursor.execute(""""""ALTER TABLE Utilisateur ADD COLUMN admin_utilisateur INTEGER NOT NULL DEFAULT 0"""""")
connection.commit()
connection.close()

"""
"""
connection = sqlite3.connect('Station_meteo.db')
cursor = connection.cursor()
cursor.execute(""""""UPDATE Utilisateur SET admin_utilisateur = 1 WHERE id_Utilisateur = 11"""""")
connection.commit()
connection.close()

"""