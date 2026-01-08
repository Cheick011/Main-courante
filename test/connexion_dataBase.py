from Connexion_dataBase import connexion

# Exemple d'utilisation directe
conn = connexion()
cur = conn.cursor()
cur.execute("SELECT * FROM utilisateurs;")
print(cur.fetchall())
cur.close()
conn.close()
