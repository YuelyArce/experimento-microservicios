import sqlite3
from sqlite3 import Error

def create_connection():
    """Crea una conexión a la base de datos SQLite"""
    conn = None
    try:
        conn = sqlite3.connect('auditoria.db')
        print("Conexión exitosa a la base de datos SQLite")
    except Error as e:
        print(f"Error al conectar con la base de datos: {e}")
    return conn

def create_table(conn):
    """Crea una tabla en la base de datos"""
    try:
        sql_create_auditoria_table = """CREATE TABLE IF NOT EXISTS auditoria (
                                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                                            evento TEXT NOT NULL,
                                            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                                        );"""
        cursor = conn.cursor()
        cursor.execute(sql_create_auditoria_table)
        print("Tabla creada correctamente")
    except Error as e:
        print(f"Error al crear la tabla: {e}")

def main():
    conn = create_connection()
    if conn:
        create_table(conn)
        conn.close()

if __name__ == '__main__':
    main()
