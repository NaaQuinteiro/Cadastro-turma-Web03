from mysql import connector

def conectar():
    return connector.connect(
        host="localhost",
        user="root",
        password="senai",
        database="pwbe_escola"
    )