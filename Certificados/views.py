import functools
import os
#https://code.visualstudio.com/docs/python/tutorial-flask
from . import db
from flask import (Flask, current_app, flash, g, make_response, redirect,
                   render_template, request, send_from_directory, session,
                   url_for)
from numpy import isin
from werkzeug.security import check_password_hash, generate_password_hash
from . import app



@app.route('/')
def index():
    return render_template('log.html')


@app.before_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        dba = db.get_db()
        g.user = dba.execute('SELECT * FROM Usuario WHERE Codigo = ?', (user_id,)).fetchone()
        
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('login'))
        return view(**kwargs)

    return wrapped_view



@app.route('/log', methods=('GET', 'POST'))
def log():
    try:
        print('aqui')
        if request.method == 'POST':
            flash('', 'error')
            tipo_documento = request.form["tipo_documento"]
            numero_documento = request.form["numero_documento"]
            print(tipo_documento)
            print(numero_documento)
                
            error = None
            
            if tipo_documento not in ['cc','nit']:
                error = 'Debe seleccionar el tipo de documento'
                flash(error, 'error')
                return render_template('log.html')

            if not numero_documento:
                error = 'Debe ingresar el número de documento'
                flash(error, 'error')
                return render_template('log.html')
            dba = db.get_db()
            print('pas1')
            user = dba.execute("SELECT * FROM datospersonas WHERE user_id = ?", (numero_documento,)).fetchone()
            dba = db.close_db()
            print('paso')
            print(user)
            if user is None:
                flash('No existe registro para este documento', 'error')
            else:
                uploads = os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'])
                print('variable')
                print(uploads)
                return send_from_directory(directory=uploads, path='certificado.pdf', as_attachment=True)
            
        return render_template('log.html',error= error)

    except Exception as ex:
        print("ex")
        print(ex)
        return render_template('log.html')
    
    
@app.route('/login', methods=('GET', 'POST'))
def login():
    try:
        print('aqui')
        print('aqui')
        if request.method == 'POST':
            userid = request.form['id']
            password = request.form['password']

            error = None
            if not userid:
                error = 'Debes ingresar un usuario'

                flash(error)
                return render_template('login.html')

            if not password:
                error = 'Debes ingresar una contraseña'
                flash(error)
                return render_template('login.html')
            dba = db.get_db()

            user = dba.execute("SELECT * FROM Usuarios WHERE user_id= ?", (userid,)).fetchone()
            dba = db.close_db()
            print(user)
            if user is None:
                error = 'Usuario o contraseña inválidos'
            else:
                store_password = user[2]
                result = check_password_hash(store_password, password)
                if result is False:
                    error = 'Usuario o contraseña inválidos'
                else:
                    session.clear()
                    session['user_id'] = user[0]
                    session['user_name'] = user[2]
                    session['tipo_usuario'] = user[6]
                    resp = make_response(redirect(url_for('buscarProducto')))
                    resp.set_cookie('username', userid)
                    return resp
            flash(error)

        return render_template('login.html')

    except Exception as ex:
        print("ex")
        print(ex)
        return render_template('login.html')



if __name__ == '__main__':
    app.run(host="0.0.0.0", port= 5000)
