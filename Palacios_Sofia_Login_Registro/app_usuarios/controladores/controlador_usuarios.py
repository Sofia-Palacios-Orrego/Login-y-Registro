from flask import render_template, session, request, redirect, flash
from app_usuarios import app
from flask_bcrypt import Bcrypt
from app_usuarios.modelos.modelo_usuarios import Usuario

bcrypt = Bcrypt( app )

@app.route( '/', methods = ['GET'] )
def desplegar_login_registro():
    return render_template( 'home.html' )


@app.route( '/nuevo/usuario', methods = ['POST'] )
def crear_usuario():
    data = {
            **request.form,        #copia todo el diccionario de request.form y lo pega en un nuevo diccionario (incluye el password no encriptado)
        }
    if Usuario.validar_registro( data ) == False:
        return redirect ('/')
    else:
        password_encriptado = bcrypt.generate_password_hash( data['contraseña'] ) #esta linea genera el password encriptado
        data['contraseña'] = password_encriptado     #reescribe el password no encriptado y lo envia al diccionario "data" de arriba
        id_usuario = Usuario.crear_uno( data ) #el id que nos devuelve el query le ponemos "id_uduario"

        session['nombre'] = data['nombre']
        session['apellido'] = data['apellido']
        session['id_usuario'] = id_usuario
        return redirect( '/success' )
    

@app.route('/success', methods=['GET'])
def desplegar_success():
        if 'nombre' not in session:     #esta validacion se hace para todas las rutas GET excepto login y registro
            return redirect ('/')
        else:
            return render_template('success.html')
        

@app.route( '/login', methods = ['POST'] )  #user's email and password are extracted from the form data 
def procesa_login():
    data = {
        "email" : request.form['email_login'],
    }
    usuario = Usuario.obtener_uno_con_email( data )    #method is called to retrieve the user's information based on the provided email
    
    if usuario == None:
        flash ( "Email invalido.", "error_contraseña_login")
        return redirect('/') 
    else:
        if not bcrypt.check_password_hash( usuario.contraseña, request.form['contraseña_login'] ):  #compara el password encriptado hash con el que esta ingresando el usuario. Parametros:  1. es el que esta encriptado y en la base de datos 2.es el que viene en el formulario 
            flash( "Credenciales incorrectas.", "error_contraseña_login") 
            return redirect('/') 
        else: #If the passwords match, the user is considered authenticated, and their session data (name, email, and ID) is stored using the Flask session object.
            session['nombre'] = usuario.nombre     #guardamos estos datos para ver con que usuario estamos haciendo login y se saca del objeto en la linea 51
            session['apellido'] = usuario.apellido
            session['id_usuario'] = usuario.id
            return redirect( '/success' )


@app.route( '/logout', methods = ['POST'] )
def procesa_logout():
    session.clear()
    return redirect( '/' )