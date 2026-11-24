"""Gestion de inventario de Tecno Partes Bogota."""

from decimal import Decimal, InvalidOperation


class Inventario:

	def __init__(self, conexion):
		self.conexion = conexion

	def listar(self):
		with self.conexion.transaction():
			with self.conexion.cursor() as cursor:
				cursor.execute("""
					SELECT id, nombre, cantidad, precio
					FROM productos
					ORDER BY id
				""")
				return cursor.fetchall()

	def agregar(self, nombre, cantidad, precio):
		nombre = nombre.strip()

		if not nombre:
			raise ValueError("El nombre no puede estar vacio.")

		if cantidad <= 0:
			raise ValueError("La cantidad debe ser mayor que cero.")

		try:
			precio = Decimal(str(precio))
		except InvalidOperation:
			raise ValueError("Precio incorrecto.")

		if not precio.is_finite() or precio < 0:
			raise ValueError("Precio incorrecto.")

		with self.conexion.transaction():
			with self.conexion.cursor() as cursor:
				cursor.execute("""
					INSERT INTO productos
					(nombre, cantidad, precio)
					VALUES (%s, %s, %s)
					RETURNING id
				""", (nombre, cantidad, precio))

				return cursor.fetchone()[0]

	def buscar(self, nombre):
		with self.conexion.transaction():
			with self.conexion.cursor() as cursor:
				cursor.execute("""
					SELECT id, nombre, cantidad, precio
					FROM productos
					WHERE nombre ILIKE %s
					ORDER BY id
				""", (f"%{nombre}%",))

				return cursor.fetchall()

	def ingresar_unidades(self, id_producto, cantidad):
		if cantidad <= 0:
			raise ValueError("Cantidad incorrecta.")

		with self.conexion.transaction():
			with self.conexion.cursor() as cursor:
				cursor.execute("""
					UPDATE productos
					SET cantidad = cantidad + %s
					WHERE id = %s
					RETURNING cantidad
				""", (cantidad, id_producto))

				resultado = cursor.fetchone()

				if resultado is None:
					raise ValueError("Producto no encontrado.")

				return resultado[0]

	def retirar(self, id_producto, cantidad):
		if cantidad <= 0:
			raise ValueError("Cantidad incorrecta.")

		with self.conexion.transaction():
			with self.conexion.cursor() as cursor:
				cursor.execute("""
					UPDATE productos
					SET cantidad = cantidad - %s
					WHERE id = %s
					AND cantidad >= %s
					RETURNING cantidad
				""", (cantidad, id_producto, cantidad))

				resultado = cursor.fetchone()

				if resultado is None:
					raise ValueError(
						"Producto inexistente o stock insuficiente."
					)

				return resultado[0]

	def actualizar(self, id_producto, cantidad):
		if cantidad < 0:
			raise ValueError("La cantidad no puede ser negativa.")

		with self.conexion.transaction():
			with self.conexion.cursor() as cursor:
				cursor.execute("""
					UPDATE productos
					SET cantidad = %s
					WHERE id = %s
					RETURNING cantidad
				""", (cantidad, id_producto))

				resultado = cursor.fetchone()

				if resultado is None:
					raise ValueError("Producto no encontrado.")

				return resultado[0]

	def eliminar(self, id_producto):
		with self.conexion.transaction():
			with self.conexion.cursor() as cursor:
				cursor.execute("""
					DELETE FROM productos
					WHERE id = %s
					RETURNING id
				""", (id_producto,))

				if cursor.fetchone() is None:
					raise ValueError("Producto no encontrado.")

				return True

	def total_productos(self):
		with self.conexion.transaction():
			with self.conexion.cursor() as cursor:
				cursor.execute("SELECT COUNT(*) FROM productos")
				return cursor.fetchone()[0]

	def total_unidades(self):
		with self.conexion.transaction():
			with self.conexion.cursor() as cursor:
				cursor.execute("""
					SELECT COALESCE(SUM(cantidad), 0)
					FROM productos
				""")
				return cursor.fetchone()[0]
