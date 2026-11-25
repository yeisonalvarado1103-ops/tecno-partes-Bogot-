"""Gestion de usuarios de Tecno Partes Bogota."""


class Usuarios:

	def __init__(self, conexion):
		self.conexion = conexion

	@staticmethod
	def validar_datos(nombre, usuario, rol):

		nombre = nombre.strip()
		usuario = usuario.strip().lower()

		if not nombre or not usuario:
			raise ValueError("Completa todos los campos.")

		if len(nombre) > 100:
			raise ValueError("El nombre es demasiado largo.")

		if len(usuario) > 50:
			raise ValueError("El usuario es demasiado largo.")

		if rol not in ("administrador", "empleado"):
			raise ValueError("Rol incorrecto.")

		return nombre, usuario, rol

	@staticmethod
	def validar_contrasena(contrasena):

		if len(contrasena) < 8:
			raise ValueError(
				"La contrasena debe tener minimo 8 caracteres."
			)

		if len(contrasena.encode("utf-8")) > 72:
			raise ValueError("La contrasena es demasiado larga.")

	def crear_usuario(self, nombre, usuario, contrasena, rol):

		nombre, usuario, rol = self.validar_datos(
			nombre, usuario, rol
		)

		self.validar_contrasena(contrasena)

		with self.conexion.transaction():
			with self.conexion.cursor() as cursor:

				cursor.execute("""
					INSERT INTO usuarios
					(nombre, usuario, contrasena, rol)
					VALUES (
						%s,
						%s,
						crypt(%s, gen_salt('bf', 12)),
						%s
					)
					RETURNING id
				""", (nombre, usuario, contrasena, rol))

				return cursor.fetchone()[0]

	def iniciar_sesion(self, usuario, contrasena):

		usuario = usuario.strip().lower()

		if len(contrasena.encode("utf-8")) > 72:
			return None

		with self.conexion.transaction():
			with self.conexion.cursor() as cursor:

				cursor.execute("""
					SELECT id, nombre, usuario, rol
					FROM usuarios
					WHERE usuario = %s
					AND contrasena = crypt(%s, contrasena)
					AND activo = TRUE
				""", (usuario, contrasena))

				return cursor.fetchone()

	def listar_usuarios(self):

		with self.conexion.transaction():
			with self.conexion.cursor() as cursor:

				cursor.execute("""
					SELECT id, nombre, usuario, rol, activo
					FROM usuarios
					ORDER BY id
				""")

				return cursor.fetchall()

	def buscar_usuario(self, id_usuario):

		with self.conexion.transaction():
			with self.conexion.cursor() as cursor:

				cursor.execute("""
					SELECT id, nombre, usuario, rol, activo
					FROM usuarios
					WHERE id = %s
				""", (id_usuario,))

				return cursor.fetchone()

	def actualizar_usuario(
		self, id_usuario, nombre, usuario, rol,
		id_administrador
	):

		nombre, usuario, rol = self.validar_datos(
			nombre, usuario, rol
		)

		if id_usuario == id_administrador:
			if rol != "administrador":
				raise ValueError(
					"No puedes eliminar tu propio rol de administrador."
				)

		with self.conexion.transaction():
			with self.conexion.cursor() as cursor:

				cursor.execute("""
					UPDATE usuarios
					SET nombre = %s,
						usuario = %s,
						rol = %s
					WHERE id = %s
					RETURNING id
				""", (nombre, usuario, rol, id_usuario))

				if cursor.fetchone() is None:
					raise ValueError("Usuario no encontrado.")

				return True

	def cambiar_contrasena(self, id_usuario, contrasena):

		self.validar_contrasena(contrasena)

		with self.conexion.transaction():
			with self.conexion.cursor() as cursor:

				cursor.execute("""
					UPDATE usuarios
					SET contrasena = crypt(
						%s, gen_salt('bf', 12)
					)
					WHERE id = %s
					RETURNING id
				""", (contrasena, id_usuario))

				if cursor.fetchone() is None:
					raise ValueError("Usuario no encontrado.")

				return True

	def cambiar_estado(self, id_usuario, activo):

		with self.conexion.transaction():
			with self.conexion.cursor() as cursor:

				cursor.execute("""
					UPDATE usuarios
					SET activo = %s
					WHERE id = %s
					RETURNING id
				""", (activo, id_usuario))

				return cursor.fetchone() is not None

	def existe_administrador(self):

		with self.conexion.transaction():
			with self.conexion.cursor() as cursor:

				cursor.execute("""
					SELECT EXISTS (
						SELECT 1
						FROM usuarios
						WHERE rol = 'administrador'
						AND activo = TRUE
					)
				""")

				return cursor.fetchone()[0]
