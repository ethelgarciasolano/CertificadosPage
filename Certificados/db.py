import sqlite3
from sqlite3 import Error
from flask import g

def get_db():
    try:
        if 'db' not in g:
            gdb = sqlite3.connect('certificadosgob.db')
            print('conect')
            cursor = gdb.cursor()
            #sql = '''CREATE TABLE datospersonas (user_id serial PRIMARY KEY, username VARCHAR ( 50 ) UNIQUE NOT NULL, email VARCHAR ( 255 ) UNIQUE NOT NULL);'''
            #cursor.execute(sql)
            #sql = '''CREATE TABLE Usuarios (user_id serial PRIMARY KEY, username VARCHAR ( 50 ) UNIQUE NOT NULL, passwords INT, email VARCHAR ( 255 ) UNIQUE NOT NULL);'''
            #cursor.execute(sql)
            #sql = '''INSERT INTO Usuarios (user_id, username, passwords, email) VALUES (321, 'Camilo', 321,'camiloe@gmail.com');'''
            #cursor.execute(sql) 
            #sql = '''INSERT INTO datospersonas (user_id, username,email) VALUES (123, 'Manuel', 'ererwe@gmail.com');'''
            #cursor.execute(sql) 
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            print(cursor.fetchall())
            cursor.execute("SELECT * FROM datospersonas;")
            print(cursor.fetchall())
            cursor.execute("SELECT * FROM Usuarios;")
            print(cursor.fetchall())
        return gdb
    except Error:
        print('error conexion')
        print(Error)


def close_db():
    db = g.pop('db', None)
    if db is not None:
        db.close()


#INSERT INTO Usuario(Codigo, Nombre,Apellido, Contrasena, Celular,Email,Rol)
#VALUES (2112,'Ethel', 'Garcia', 'wsw',3123,'Barranquilla','Administrador')
#CREATE TABLE datospersonas (
#	user_id serial PRIMARY KEY,
#	username VARCHAR ( 50 ) UNIQUE NOT NULL,
#	email VARCHAR ( 255 ) UNIQUE NOT NULL
#);
#INSERT INTO datospersonas (user_id, username,email)
#VALUES (123, 'Manuel', 'ererwe@gmail.com');