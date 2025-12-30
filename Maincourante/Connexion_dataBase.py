import psycopg2

def connexion():
    return psycopg2.connect(
        dbname="spelo_app",
        user="admin",
        password="admin",
        host="localhost",
        port=5432
    )
