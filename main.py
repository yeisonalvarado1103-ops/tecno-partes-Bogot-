"""Sistema Tecno Partes Bogota - Sprint 2."""

import psycopg
from getpass import getpass
from decimal import Decimal, InvalidOperation

from conexion import conectar
from modulos.inventario import Inventario
from modulos.usuarios import Usuarios


def pausar():
    input("\nPresiona ENTER para continuar...")


def pedir_entero(mensaje, minimo=1):
    while True:
        try:
            numero = int(input(mensaje).strip())

            if numero < minimo:
                print(f"El valor minimo es {minimo}.")
                continue

            return numero

        except ValueError:
            print("Debes escribir un numero entero.")


def pedir_precio():
    while True:
        try:
            precio = Decimal(
                input("Precio del producto: ").strip()
            )

            if not precio.is_finite() or precio < 0:
                print("Precio incorrecto.")
                continue

            return precio

        except InvalidOperation:
            print("Debes escribir un precio valido.")


def mostrar_productos(productos):

    print("\n" + "=" * 50)
    print("        INVENTARIO DE REPUESTOS")
    print("=" * 50)

    if not productos:
        print("No hay productos registrados.")

    for producto in productos:
        print(f"ID: {producto[0]}")
        print(f"Nombre: {producto[1]}")
        print(f"Cantidad: {producto[2]}")
        print(f"Precio: ${producto[3]:,.2f}")
        print("-" * 50)


def mostrar_inventario(inventario):

    mostrar_productos(inventario.listar())

    print(f"Total de productos: {inventario.total_productos()}")
    print(f"Total de unidades: {inventario.total_unidades()}")
    print("=" * 50)


def iniciar_sesion(usuarios):

    print("\n" + "=" * 50)
    print("          TECNO PARTES BOGOTA")
    print("             INICIO DE SESION")
    print("=" * 50)

    for intento in range(3):

        usuario = input("Usuario: ").strip()
        contrasena = getpass("Contrasena: ")

        if len(contrasena.encode("utf-8")) <= 72:
            resultado = usuarios.iniciar_sesion(
                usuario, contrasena
            )
        else:
            resultado = None

        if resultado:
            print(f"\nBienvenido, {resultado[1]}")
            print(f"Rol: {resultado[3]}")
            return resultado

        restantes = 2 - intento

        print("\nUsuario o contrasena incorrectos.")
        print(f"Intentos restantes: {restantes}")

    print("\nLimite de intentos alcanzado.")
    return None


def mostrar_usuarios(usuarios):

    print("\n========== USUARIOS ==========")

    registros = usuarios.listar_usuarios()

    for registro in registros:

        estado = "Activo" if registro[4] else "Inactivo"

        print(f"ID: {registro[0]}")
        print(f"Nombre: {registro[1]}")
        print(f"Usuario: {registro[2]}")
        print(f"Rol: {registro[3]}")
        print(f"Estado: {estado}")
        print("-" * 40)


def administrar_usuarios(usuarios, sesion):

    if sesion[3] != "administrador":
        print("Acceso denegado.")
        return

    while True:

        print("\n======= ADMINISTRACION DE USUARIOS =======")
        print("1. Crear usuario")
        print("2. Listar usuarios")
        print("3. Activar usuario")
        print("4. Desactivar usuario")
        print("5. Volver al menu principal")

        opcion = input("Selecciona una opcion: ").strip()

        try:

            if opcion == "1":

                nombre = input("Nombre completo: ").strip()
                usuario = input("Nombre de usuario: ").strip()

                print("\n1. Administrador")
                print("2. Empleado")

                seleccion = input("Selecciona el rol: ").strip()

                if seleccion == "1":
                    rol = "administrador"

                elif seleccion == "2":
                    rol = "empleado"

                else:
                    raise ValueError("Rol incorrecto.")

                contrasena = getpass("Nueva contrasena: ")
                confirmar = getpass("Confirmar contrasena: ")

                if contrasena != confirmar:
                    raise ValueError(
                        "Las contrasenas no coinciden."
                    )

                id_usuario = usuarios.crear_usuario(
                    nombre,
                    usuario,
                    contrasena,
                    rol
                )

                print("\nUsuario creado correctamente.")
                print(f"ID asignado: {id_usuario}")
                print(f"Usuario: {usuario.lower()}")
                print(f"Rol: {rol}")

            elif opcion == "2":

                mostrar_usuarios(usuarios)

            elif opcion == "3":

                mostrar_usuarios(usuarios)

                id_usuario = pedir_entero(
                    "ID del usuario a activar: "
                )

                if usuarios.cambiar_estado(id_usuario, True):
                    print("Usuario activado correctamente.")
                else:
                    print("Usuario no encontrado.")

            elif opcion == "4":

                mostrar_usuarios(usuarios)

                id_usuario = pedir_entero(
                    "ID del usuario a desactivar: "
                )

                if id_usuario == sesion[0]:
                    raise ValueError(
                        "No puedes desactivar tu propia cuenta."
                    )

                confirmar = input(
                    "Confirmar desactivacion (s/n): "
                ).strip().lower()

                if confirmar == "s":

                    if usuarios.cambiar_estado(id_usuario, False):
                        print("Usuario desactivado correctamente.")
                    else:
                        print("Usuario no encontrado.")

                else:
                    print("Operacion cancelada.")

            elif opcion == "5":

                break

            else:

                print("Opcion incorrecta.")

        except (ValueError, psycopg.Error) as error:

            print(f"\nError: {error}")

        pausar()


def menu_principal(inventario, usuarios, sesion):

    administrador = sesion[3] == "administrador"

    while True:

        print("\n" + "=" * 50)
        print("          TECNO PARTES BOGOTA")
        print("       SISTEMA DE GESTION DE INVENTARIO")
        print("           SPRINT 2 - UNIVERSIDAD")
        print("=" * 50)

        print(f"Usuario: {sesion[1]}")
        print(f"Rol: {sesion[3]}")

        print("\n========== MENU PRINCIPAL ==========")
        print("1. Ver inventario")
        print("2. Registrar nuevo producto")
        print("3. Buscar producto")
        print("4. Ingresar unidades")
        print("5. Retirar unidades")

        if administrador:

            print("6. Actualizar cantidad")
            print("7. Eliminar producto")
            print("8. Administrar usuarios")

        print("9. Cerrar sesion")
        print("0. Salir del sistema")
        print("====================================")

        opcion = input("Selecciona una opcion: ").strip()

        try:

            if opcion in ("6", "7", "8") and not administrador:

                print("Acceso denegado.")
                pausar()
                continue

            if opcion == "1":

                mostrar_inventario(inventario)

            elif opcion == "2":

                print("\n=== REGISTRAR PRODUCTO ===")

                nombre = input("Nombre del producto: ").strip()

                if not nombre:
                    raise ValueError("El nombre no puede estar vacio.")

                cantidad = pedir_entero("Cantidad: ")
                precio = pedir_precio()

                id_producto = inventario.agregar(
                    nombre, cantidad, precio
                )

                print("\nProducto registrado correctamente.")
                print(f"ID asignado: {id_producto}")
                print(f"Producto: {nombre}")
                print(f"Cantidad: {cantidad}")
                print(f"Precio: ${precio:,.2f}")

            elif opcion == "3":

                print("\n=== BUSCAR PRODUCTO ===")

                nombre = input("Nombre del producto: ").strip()

                if not nombre:
                    raise ValueError("Escribe un nombre.")

                mostrar_productos(
                    inventario.buscar(nombre)
                )

            elif opcion == "4":

                print("\n=== INGRESAR UNIDADES ===")

                mostrar_inventario(inventario)

                id_producto = pedir_entero("ID del producto: ")
                cantidad = pedir_entero("Cantidad a ingresar: ")

                total = inventario.ingresar_unidades(
                    id_producto, cantidad
                )

                print("Unidades ingresadas correctamente.")
                print(f"Total disponible: {total}")

            elif opcion == "5":

                print("\n=== RETIRAR UNIDADES ===")

                mostrar_inventario(inventario)

                id_producto = pedir_entero("ID del producto: ")
                cantidad = pedir_entero("Cantidad a retirar: ")

                restante = inventario.retirar(
                    id_producto, cantidad
                )

                print("Retiro realizado correctamente.")
                print(f"Unidades restantes: {restante}")

            elif opcion == "6":

                print("\n=== ACTUALIZAR CANTIDAD ===")

                mostrar_inventario(inventario)

                id_producto = pedir_entero("ID del producto: ")

                cantidad = pedir_entero(
                    "Nueva cantidad: ", minimo=0
                )

                inventario.actualizar(
                    id_producto, cantidad
                )

                print("Cantidad actualizada correctamente.")
                print(f"Nueva cantidad: {cantidad}")

            elif opcion == "7":

                print("\n=== ELIMINAR PRODUCTO ===")

                mostrar_inventario(inventario)

                id_producto = pedir_entero("ID del producto: ")

                confirmar = input(
                    "Deseas eliminar el producto? (s/n): "
                ).strip().lower()

                if confirmar == "s":

                    inventario.eliminar(id_producto)
                    print("Producto eliminado correctamente.")

                else:

                    print("Eliminacion cancelada.")

            elif opcion == "8":

                administrar_usuarios(usuarios, sesion)

            elif opcion == "9":

                print("\nSesion cerrada correctamente.")
                return True

            elif opcion == "0":

                print("\nGracias por utilizar Tecno Partes Bogota.")
                print("Hasta pronto.")
                return False

            else:

                print("Opcion incorrecta.")

        except (ValueError, psycopg.Error) as error:

            print(f"\nNo se completo la operacion: {error}")

        pausar()


def iniciar_sistema():

    with conectar() as conexion:

        print("\nConexion exitosa a PostgreSQL")

        inventario = Inventario(conexion)
        usuarios = Usuarios(conexion)

        while True:

            sesion = iniciar_sesion(usuarios)

            if sesion is None:
                break

            continuar = menu_principal(
                inventario,
                usuarios,
                sesion
            )

            if not continuar:
                break


if __name__ == "__main__":

    try:

        iniciar_sistema()

    except (KeyboardInterrupt, EOFError):

        print("\nPrograma finalizado.")

    except psycopg.Error as error:

        print(f"\nError de conexion: {error}")