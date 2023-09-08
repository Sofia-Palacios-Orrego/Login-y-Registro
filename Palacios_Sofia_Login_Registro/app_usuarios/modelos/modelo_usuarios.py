from app_usuarios.config.mysqlconnection import connectToMySQL
from flask import flash, session
from app_usuarios import BASE_DE_DATOS, EMAIL_REGEX, NOMBRE_REGEX

class Usuario:
    def __init__( self, data ):
        self.id = data["id"]
        self.nombre = data["nombre"]
        self.apellido = data["apellido"]
        self.contraseña = data["contraseña"]
        self.email = data["email"]
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def crear_uno( cls, data ):
        query = """
                INSERT INTO usuarios ( nombre, apellido, email, contraseña )
                VALUES ( %(nombre)s, %(apellido)s, %(email)s, %(contraseña)s );
                """
        resultado = connectToMySQL( BASE_DE_DATOS ).query_db( query, data )
        return resultado
    
    @classmethod
    def selecciona_uno( cls, data ):
        query = """
                SELECT *
                FROM usuarios
                WHERE id = %(id)s;
                """
        resultado = connectToMySQL( BASE_DE_DATOS ).query_db( query, data )
        usuario_actual = Usuario( resultado[0] )
        return usuario_actual
    
    @classmethod
    def obtener_uno_con_email( cls, data ):    #en modelo ERD indicamos que el campo de email es unico, por eso es posible el siguiente query 
        query = """
                SELECT *
                FROM usuarios
                WHERE email = %(email)s;
                """
        resultado = connectToMySQL( BASE_DE_DATOS ).query_db( query, data )  #regresara dos posibles resultados: 1.objeto/instancia pq existe el usuario 2.una lista vacia
        if len( resultado ) == 0:
            return None
        else:
            return Usuario( resultado[0] )

    @staticmethod
    def validar_registro( data ):
        es_valido = True

        if len( data['nombre'] ) < 2:
            es_valido = False
            flash( "Tu nombre debe tener al menos dos caracteres.", "error_nombre" )
        if not NOMBRE_REGEX.match( data['nombre'] ):
            es_valido = False
            flash( "Por favor porporciona un nombre válido (solo letras)", "error_nombre" )
        if len( data['apellido'] ) < 2:
            es_valido = False
            flash( "Tu apellido debe tener al menos dos caracteres.", "error_apellido" )
        if not NOMBRE_REGEX.match( data['apellido'] ):
            es_valido = False
            flash( "Por favor porporciona un apellido válido (solo letras)", "error_apellido" )
        if len( data['contraseña'] ) < 8:
            es_valido = False
            flash( "Tu contraseña necesita tener al menos 8 caracteres.", "error_contraseña" )
        if data['contraseña'] != data['confirmar_contraseña']:
            es_valido = False
            flash( "Los passwords no coincided.", "error_contraseña" )
        if not EMAIL_REGEX.match( data['email'] ):
            es_valido = False
            flash( "Por favor porporciona un email válido", "error_email" )
        
        return es_valido
    
    @staticmethod
    def validar_login( data ):
        es_valido = True
        if data == None:
            flash( "Este correo no existe.", "error_email_login" )
            es_valido = False
        
        return es_valido
    
    @staticmethod 
    def valida_sesion():
        if 'id' in session:
            return True
        else:
            return False