from datetime import datetime, timedelta
import mysql.connector
from mysql.connector import Error

# Conectar a la base de datos
def conectar_bd():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            password="root",
            database="cobraton"
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print("Error al conectar a la base de datos:", e)
        return None


# Verificar si el CURP ya existe
def verificar_curp_existente(curp):
    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()
            query = "SELECT COUNT(*) FROM cliente WHERE CURP_cliente = %s"
            cursor.execute(query, (curp,))
            resultado = cursor.fetchone()
            return resultado[0] > 0
        except Error as e:
            print("Error al verificar CURP:", e)
        finally:
            cursor.close()
            conexion.close()
    return False


# Función para crear un cliente
def crear_cliente(nombre, apellido, telefono, curp):
    if verificar_curp_existente(curp):
        print("El CURP ya está registrado. No se puede crear el cliente.")
        return

    conexion = conectar_bd()
    if conexion:
        try:
            cursor = conexion.cursor()
            query = "INSERT INTO cliente (nombre_cliente, apellido_cliente, telefono_cliente, CURP_cliente) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (nombre, apellido, telefono, curp))
            conexion.commit()
            print("Cliente creado exitosamente.")
        except Error as e:
            print("Error al insertar cliente:", e)
        finally:
            cursor.close()
            conexion.close()
            print("Conexión cerrada.")


# Crear un nuevo préstamo
def crear_prestamo(id_cliente, fecha_inicio, monto, frecuencia, duracion):
    conexion = conectar_bd()
    if not conexion:
        return

    try:
        cursor = conexion.cursor()
        fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
        
        # Calcular la fecha final según la frecuencia y duración
        if frecuencia == "mensual":
            fecha_final = fecha_inicio + timedelta(days=30*duracion)
        elif frecuencia == "trimestral":
            fecha_final = fecha_inicio + timedelta(days=90*duracion)
        elif frecuencia == "semestral":
            fecha_final = fecha_inicio + timedelta(days=180*duracion)
        elif frecuencia == "anual":
            fecha_final = fecha_inicio + timedelta(days=365*duracion)
        else:
            fecha_final = fecha_inicio + timedelta(weeks=duracion)

        query = """
            INSERT INTO prestamo (id_cliente, fecha_prestamo, monto_prestamo, formapago_prestamo, fechafinal_prestamo)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (id_cliente, fecha_inicio, monto, frecuencia, fecha_final))
        conexion.commit()
        print("Préstamo creado exitosamente.")
    except Error as e:
        print("Error al crear préstamo:", e)
    finally:
        cursor.close()
        conexion.close()


# Generar fechas de cobro según la frecuencia
def generar_fechas_cobro(fecha_inicio, frecuencia, duracion):
    fechas = []
    fecha_actual = datetime.strptime(fecha_inicio, "%Y-%m-%d")
    
    for _ in range(duracion):
        if frecuencia == "mensual":
            fecha_actual += timedelta(days=30)
        elif frecuencia == "trimestral":
            fecha_actual += timedelta(days=90)
        elif frecuencia == "semestral":
            fecha_actual += timedelta(days=180)
        elif frecuencia == "anual":
            fecha_actual += timedelta(days=365)
        else:  # semanal
            fecha_actual += timedelta(weeks=1)
        
        # Si cae en domingo, mover al lunes
        if fecha_actual.weekday() == 6:
            fecha_actual += timedelta(days=1)
        
        fechas.append(fecha_actual.strftime("%Y-%m-%d"))
    return fechas


# Aplicar un pago
def aplicar_pago(id_prestamo, cantidad):
    conexion = conectar_bd()
    if not conexion:
        return

    try:
        cursor = conexion.cursor()
        fecha_abono = datetime.now().strftime("%Y-%m-%d")
        query = "INSERT INTO abono (id_prestamo, fecha_abono, cantidad_abono) VALUES (%s, %s, %s)"
        cursor.execute(query, (id_prestamo, fecha_abono, cantidad))
        conexion.commit()
        print("Pago registrado exitosamente.")
    except Error as e:
        print("Error al registrar pago:", e)
    finally:
        cursor.close()
        conexion.close()


# Generar reporte de pagos por cliente
def generar_reporte(id_cliente):
    conexion = conectar_bd()
    if not conexion:
        return

    try:
        cursor = conexion.cursor()
        query = """
            SELECT p.id_prestamo, p.fecha_prestamo, p.formapago_prestamo, a.fecha_abono, a.cantidad_abono 
            FROM prestamo p
            LEFT JOIN abono a ON p.id_prestamo = a.id_prestamo
            WHERE p.id_cliente = %s
        """
        cursor.execute(query, (id_cliente,))
        resultado = cursor.fetchall()

        print("\nReporte de pagos:")
        for row in resultado:
            print(f"Préstamo {row[0]}, Fecha inicio: {row[1]}, Frecuencia: {row[2]}, Fecha abono: {row[3]}, Cantidad: {row[4]}")
    except Error as e:
        print("Error al generar reporte:", e)
    finally:
        cursor.close()
        conexion.close()


# Ejecución de ejemplo
if __name__ == "__main__":
    # Crear un cliente y un préstamo, generar fechas, aplicar un pago y generar reporte
    crear_cliente("Pako", "Lopez", "123456789", "PAKOLOPEZ1234")
    crear_prestamo(1, "2023-01-12", 1000, "mensual", 12)
    fechas = generar_fechas_cobro("2023-01-12", "mensual", 12)
    print("Fechas de cobro:", fechas)
    aplicar_pago(1, 100)
    generar_reporte(1)
