import mysql.connector


def conectar_mysql(config):
    try:
        conexion = mysql.connector.connect(**config)
        return conexion
    except mysql.connector.Error as e:
        print(f"Error de conexión a MySQL: {e}")
        return None


def cerrar_conexion(conexion):
    if conexion:
        conexion.close()
