"""Creacion del administrador de Tecno Partes Bogota."""

from getpass import getpass

from conexion import conectar
from modulos.usuarios import Usuarios


def crear_administrador():
	with conectar() as conexion:
		usuarios = Usuarios(conexion)

		if usuarios.existe_administrador():
			print("Ya existe un administrador activo.")
			return

		print("\n===== TECNO PARTES BOGOTA =====")
		print("CREACION DEL ADMINISTRADOR")
		print("==============================")

		nombre = input("Nombre completo: ").strip()
		usuario = input("Nombre de usuario: ").strip()
		contrasena = getpass("Nueva contrasena: ")
		confirmar = getpass("Confirmar contrasena: ")

		if contrasena != confirmar:
			print("Las contrasenas no coinciden.")
			return

		id_usuario = usuarios.crear_usuario(
			nombre,
			usuario,
			contrasena,
			"administrador",
		)

		print("\nAdministrador creado correctamente.")
		print(f"ID: {id_usuario}")
		print(f"Nombre: {nombre}")
		print(f"Usuario: {usuario}")
		print("Rol: administrador")


if __name__ == "__main__":
	try:
		crear_administrador()
	except Exception as error:
		print("Error:", error)
