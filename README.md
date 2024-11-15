# Examen
Sistema para el control de prestamos, usando MySQL y python  para interactuar con la base de datos.
# BASE DE DATOS

La base de datos cuenta con 3 tablas
cliente :
-id_cliente 
-nombre_cliente
-apellido_cliente
-telefono_cliente
-CURP_cliente 

prestamo:
-id_prestamo
-fecha_prestamo
-monto_prestamo
-formapago_prestamo
-fechafinal_prestamo
-id_cliente

abono:
-id_abono
-fecha_abono
-cantidad_abono
-id_prestamo

La tabla cliente cuent con el curp para poder identificar al usuario y que no pueda registrarse 2 veces como cliente, a su ves esta tabla se liga con prestamo con el id_cliente para poder registrar un prestamo, y la tabla prestamo se liga con abono para registrar los abonos que se hacen al prestamo del cliente que esta ligado a este.

# SISTEMA EN PYTHON 

Ahora en el codigo de Python creamos la conexio y funcines.
Funcion crear_cliente
Creamos la función crear_cliente la cual se encargará de registrar un cliente. Antes de insertar un nuevo cliente, verificamos si el CURP ya está registrado para evitar duplicados.

Fucion crear_prestamo
La función crear_prestamo crea un préstamo asociado a un cliente. La fecha final del préstamo se calcula según la frecuencia de pago (mensual, trimestral, etc.)

Funcion generar_fechas_cobro
La función generar_fechas_cobro genera las fechas en las que se deben realizar los pagos, basándose en la frecuencia y duración del préstamo.

Funcion generar_reporte
La función generar_reporte genera un reporte con los detalles de los préstamos y pagos realizados por un cliente.

### Código de Ejemplo

```python
# Ejecución de ejemplo
if __name__ == "__main__":
    # Crear un cliente y un préstamo, generar fechas, aplicar un pago y generar reporte
    crear_cliente("Pako", "Lopez", "123456789", "PAKOLOPEZ1234")
    crear_prestamo(1, "2023-01-12", 1000, "mensual", 12)
    fechas = generar_fechas_cobro("2023-01-12", "mensual", 12)
    print("Fechas de cobro:", fechas)
    aplicar_pago(1, 100)
    generar_reporte(1)
