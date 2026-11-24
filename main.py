"""Sistema Tecno Partes Bogotá - Sprint 2."""

from modulos.inventario import Inventario


def pausar():
	input("\nPresiona ENTER para volver al menú principal...")


def pedir_cantidad(mensaje, permitir_cero=False):
	while True:
		try:
			cantidad = int(input(mensaje).strip())

			if cantidad < 0:
				print("La cantidad no puede ser negativa.")
				continue

			if cantidad == 0 and not permitir_cero:
				print("La cantidad debe ser mayor que cero.")
				continue

			return cantidad

		except ValueError:
			print("Debes escribir un número entero.")


def mostrar_inventario(inventario):
	productos = inventario.listar()

	print("\n" + "=" * 45)
	print("         INVENTARIO DE REPUESTOS")
	print("=" * 45)

	if not productos:
		print("El inventario está vacío.")
	else:
		for numero, (nombre, cantidad) in enumerate(
			sorted(productos.items()), start=1
		):
			print(f"{numero}. {nombre}: {cantidad} unidades")

	print("-" * 45)
	print(f"Total de productos: {inventario.total_productos()}")
	print(f"Total de unidades: {inventario.total_unidades()}")
	print("=" * 45)


def iniciar_sistema():

	try:
		inventario = Inventario()

	except (OSError, ValueError) as error:
		print(f"No se pudo cargar el inventario: {error}")
		print("Revisa el archivo inventario.json.")
		return

	print("=" * 45)
	print("          TECNO PARTES BOGOTÁ")
	print("      Sistema de Gestión de Inventario")
	print("          Sprint 2 - Universidad")
	print("=" * 45)

	while True:

		print("\n========== MENÚ PRINCIPAL ==========")
		print("1. Ver inventario")
		print("2. Agregar producto")
		print("3. Buscar producto")
		print("4. Retirar unidades")
		print("5. Actualizar cantidad")
		print("6. Eliminar producto")
		print("7. Salir")
		print("====================================")

		opcion = input("Selecciona una opción (1-7): ").strip()

		try:

			if opcion == "1":

				mostrar_inventario(inventario)

			elif opcion == "2":

				print("\n=== AGREGAR PRODUCTO ===")

				nombre = input("Nombre del repuesto: ").strip()

				if not nombre:
					raise ValueError("El nombre no puede estar vacío.")

				cantidad = pedir_cantidad("Cantidad a agregar: ")

				total = inventario.agregar(nombre, cantidad)

				print("\nProducto guardado correctamente.")
				print(f"Producto: {nombre}")
				print(f"Unidades disponibles: {total}")

			elif opcion == "3":

				print("\n=== BUSCAR PRODUCTO ===")

				nombre = input("Nombre del repuesto: ").strip()

				cantidad = inventario.buscar(nombre)

				if cantidad is None:
					print("Producto no encontrado.")
				else:
					print("\nProducto encontrado.")
					print(f"Producto: {nombre}")
					print(f"Cantidad disponible: {cantidad}")

			elif opcion == "4":

				print("\n=== RETIRAR UNIDADES ===")

				nombre = input("Nombre del repuesto: ").strip()

				if inventario.buscar(nombre) is None:
					raise ValueError("Producto no encontrado.")

				cantidad = pedir_cantidad("Cantidad a retirar: ")

				restante = inventario.retirar(nombre, cantidad)

				print("\nRetiro realizado correctamente.")
				print(f"Unidades restantes: {restante}")

			elif opcion == "5":

				print("\n=== ACTUALIZAR CANTIDAD ===")

				nombre = input("Nombre del repuesto: ").strip()

				if inventario.buscar(nombre) is None:
					raise ValueError("Producto no encontrado.")

				cantidad = pedir_cantidad(
					"Nueva cantidad: ",
					permitir_cero=True
				)

				inventario.actualizar(nombre, cantidad)

				print("\nCantidad actualizada correctamente.")
				print(f"Producto: {nombre}")
				print(f"Nueva cantidad: {cantidad}")

			elif opcion == "6":

				print("\n=== ELIMINAR PRODUCTO ===")

				nombre = input("Nombre del repuesto: ").strip()

				if inventario.buscar(nombre) is None:
					raise ValueError("Producto no encontrado.")

				confirmar = input(
					"¿Deseas eliminar el producto? (s/n): "
				).strip().lower()

				if confirmar == "s":
					inventario.eliminar(nombre)
					print("\nProducto eliminado correctamente.")
				else:
					print("\nEliminación cancelada.")

			elif opcion == "7":

				print("\nGracias por utilizar Tecno Partes Bogotá.")
				print("Hasta pronto.")
				break

			else:

				print("\nOpción incorrecta.")
				print("Selecciona un número del 1 al 7.")

		except (ValueError, OSError) as error:

			print(f"\nNo se completó la operación: {error}")

		pausar()


if __name__ == "__main__":

	try:
		iniciar_sistema()

	except (KeyboardInterrupt, EOFError):
		print("\nPrograma finalizado.")
