import psycopg
from getpass import getpass


def conectar():
    return psycopg.connect(
        host="::1",
        dbname="tecno_partes_bogota ",
        user="postgres",
        password=getpass("Contraseña de PostgreSQL: "),
        port=5432,
        connect_timeout=5
    )


def consultar_productos(conexion):
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT id, nombre, cantidad, precio FROM productos"
        )
        productos = cursor.fetchall()

        print("\n===== TECNO PARTES BOGOTA =====")
        print("INVENTARIO DE PRODUCTOS")
        print("--------------------------------")

        if not productos:
            print("No hay productos registrados.")

        for producto in productos:
            print(f"ID: {producto[0]}")
            print(f"Nombre: {producto[1]}")
            print(f"Cantidad: {producto[2]}")
            print(f"Precio: ${producto[3]:,.2f}")
            print("--------------------------------")


if __name__ == "__main__":
    try:
        with conectar() as conexion:
            print("\nConexion exitosa a PostgreSQL")
            consultar_productos(conexion)

    except Exception as error:
        print("Error de conexion:", error)