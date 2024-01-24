import sqlite3

# Établir une connexion à la base de données
# et créer un objet de connexion
connection = sqlite3.connect('Station_meteo.db')

# Créer un curseur vers la base de données
cursor = connection.cursor()

print("Ouverture de la base de données")
#Création de la table "Sonde"
cursor.execute ("""
                CREATE TABLE IF NOT EXISTS Sonde(
                id_Sonde INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                name_sonde TEXT NOT NULL,
                actif BOOLEEN NOT NULL)
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

#Création de la table "User"
cursor.execute ("""CREATE TABLE IF NOT EXISTS User(
                id_User INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                date_user DATETIME NOT NULL, 
                mail_user TEXT NOT NULL,
                mdp_user TEXT NOT NULL)
                ;               
""")

connection.commit()

cursor.execute ("""ALTER TABLE Sonde DROP COLUMN actif""")

connection.commit()

"""cursor.execute (""""""DELETE FROM Sonde WHERE id_Sonde = 2"""""")"""

connection.commit()

connection.close()

