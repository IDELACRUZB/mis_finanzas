import sqlite3
import pandas as pd


class DataBase():
    def crearBD(self):
        conn = sqlite3.connect('Finanzas_Personales.db') #crea la Bd
        conn.commit() #Guarda CAmbios
        conn.close()
    
    def crearTabla_categorias(self):
        conn = sqlite3.connect('Finanzas_Personales.db') #crea la Bd
        cursor = conn.cursor() #el cursor ayuda a hacer acciones dentro de la bd
        cursor.execute(
            """
                CREATE TABLE categorias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL UNIQUE,
                estado TEXT CHECK(estado IN ('activo', 'inactivo')) NOT NULL DEFAULT 'activo'
            );

         """)
        conn.commit() 
        conn.close()
    
    def insertar_categorias(self):
        conn = sqlite3.connect('Finanzas_Personales.db') #crea la Bd
        cursor = conn.cursor() #el cursor ayuda a hacer acciones dentro de la bd
        cursor.execute(
            """
            insert into categorias values
            (1, 'Alimentación', 'activo'),
            (2, 'Educación', 'activo'),
            (3, 'Entretenimiento', 'activo'),
            (4, 'Finanzas', 'activo'),
            (5, 'Ingresos extra', 'activo'),
            (6, 'Mascotas', 'activo'),
            (7, 'Ropa y cuidado personal', 'activo'),
            (8, 'Salario o sueldo', 'activo'),
            (9, 'Salud', 'activo'),
            (10, 'Servicios', 'activo'),
            (11, 'Transporte', 'activo'),
            (12, 'Vivienda', 'activo');

         """)
        conn.commit() 
        conn.close()


    def crearTabla_movimientos(self):
        conn = sqlite3.connect('Finanzas_Personales.db') #crea la Bd
        cursor = conn.cursor() #el cursor ayuda a hacer acciones dentro de la bd
        cursor.execute(
            """
                CREATE TABLE movimientos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tipo TEXT CHECK(tipo IN ('ingreso', 'egreso')) NOT NULL,
                    monto REAL NOT NULL,
                    descripcion TEXT,
                    fecha DATE NOT NULL DEFAULT (DATE('now')),
                    categoria_id INTEGER,
                    FOREIGN KEY (categoria_id) REFERENCES categorias(id) ON DELETE SET NULL
                );
         """)
        conn.commit() 
        conn.close()

    def agregar_movimiento(self, tipo, monto, descripcion, fecha, categoria_id):
        conn = sqlite3.connect('Finanzas_Personales.db') #crea la Bd
        cursor = conn.cursor() #el cursor ayuda a hacer acciones dentro de la bd
        cursor.execute(f"INSERT INTO movimientos (tipo, monto, descripcion, fecha, categoria_id) values ('{tipo}', {monto}, '{descripcion}', '{fecha}', {categoria_id});")
        conn.commit() 
        conn.close() 

    def agregarVariosDatos(self, lista):
        conn = sqlite3.connect('Finanzas_Personales.db') #crea la Bd
        cursor = conn.cursor() #el cursor ayuda a hacer acciones dentro de la bd
        consulta = f"insert into movimientos values(?, ?, ?, ?, ?)"
        cursor.executemany(consulta, lista)
        conn.commit() 
        conn.close() 

    def truncateTable(self, ):
        conn = sqlite3.connect('Finanzas_Personales.db') #crea la Bd
        cursor = conn.cursor() #el cursor ayuda a hacer acciones dentro de la bd
        cursor.execute(f"delete from movimientos")
        conn.commit() 
        conn.close()

    def deleteTable(self, fecha):
        conn = sqlite3.connect('Finanzas_Personales.db') #crea la Bd
        cursor = conn.cursor() #el cursor ayuda a hacer acciones dentro de la bd
        cursor.execute(f"delete from movimientos where fecha = '{fecha}'")
        conn.commit() 
        conn.close()

    def leerDatos(self):
        conn = sqlite3.connect('Finanzas_Personales.db') #crea la Bd
        cursor = conn.cursor() #el cursor ayuda a hacer acciones dentro de la bd
        consulta = f"SELECT * FROM movimientos;"
        cursor.execute(consulta)
        data = cursor.fetchall() #selecciona todos los datos (fetch all = buscar todo)
        conn.commit() 
        conn.close()
        return data

    def dropTable(self):
        conn = sqlite3.connect('Finanzas_Personales.db') #crea la Bd
        cursor = conn.cursor() #el cursor ayuda a hacer acciones dentro de la bd
        cursor.execute(f"drop table movimientos")
        conn.commit() 
        conn.close()

    def obtener_categorias_activas(self):
        conn = sqlite3.connect('Finanzas_Personales.db')
        c = conn.cursor()
        c.execute("SELECT nombre FROM categorias WHERE estado = 'activo'")
        categorias = [fila[0] for fila in c.fetchall()]
        conn.close()
        return categorias

    def agregar_categoria(self, nombre):
        conn = sqlite3.connect('Finanzas_Personales.db')
        c = conn.cursor()
        try:
            c.execute("INSERT INTO categorias (nombre) VALUES (?)", (nombre,))
            conn.commit()
            resultado = "Categoría agregada"
        except sqlite3.IntegrityError:
            resultado = "La categoría ya existe"
        conn.close()
        return resultado

    def desactivar_categoria(self, nombre):
        conn = sqlite3.connect('Finanzas_Personales.db')
        c = conn.cursor()
        c.execute("UPDATE categorias SET estado = 'inactivo' WHERE nombre = ?", (nombre,))
        conn.commit()
        conn.close()

    def selecciona_categoria_id(self, categoria):
        conn = sqlite3.connect('Finanzas_Personales.db')
        c = conn.cursor()
        c.execute(f"SELECT id FROM categorias WHERE nombre ='{categoria}' and estado = 'activo' limit 1;")
        categoria_id = c.fetchone()
        conn.close()
        return categoria_id[0]
    
    def calcular_movimiento(self, tipo_movimiento, fecha_inicio=None, fecha_fin=None):
        if fecha_inicio:
            consulta =f"select sum(monto) from movimientos where tipo = '{tipo_movimiento}' and fecha >= '{fecha_inicio}' and fecha <= '{fecha_fin}';"
        else:
            consulta =f"select sum(monto) from movimientos where tipo = '{tipo_movimiento}';"
    
        conn = sqlite3.connect('Finanzas_Personales.db')
        c = conn.cursor()
        c.execute(consulta)
        categoria_id = c.fetchone()
        conn.close()
        return categoria_id[0]
        
    def generar_tabla_movimiento(self, fecha_inicio=None, fecha_fin=None):
        if fecha_inicio and fecha_fin:
            consulta = f"""
                SELECT 
                    m.fecha AS Fecha,
                    c.nombre AS Categoria,
                    m.tipo AS 'Tipo Movimiento',
                    m.descripcion AS Descripcion,
                    m.monto AS Monto
                FROM movimientos m
                LEFT JOIN categorias c ON m.categoria_id = c.id
                WHERE m.fecha >= '{fecha_inicio}' AND m.fecha <= '{fecha_fin}'
                order by m.fecha;
            """
        else:
            consulta = """
                SELECT 
                    m.fecha AS Fecha,
                    c.nombre AS Categoria,
                    m.tipo AS 'Tipo Movimiento',
                    m.descripcion AS Descripcion,
                    m.monto AS Monto
                FROM movimientos m
                LEFT JOIN categorias c ON m.categoria_id = c.id
                order by m.fecha;
            """

        conn = sqlite3.connect('Finanzas_Personales.db')
        
        # ✅ Leer directamente a un DataFrame con pandas
        df = pd.read_sql_query(consulta, conn)
        
        conn.close()
        return df
