"""Gestion de usuarios de Tecno Partes Bogota."""


class Usuarios:

	def __init__(self, conexion):
		self.conexion = conexion

	def crear_usuario(self, nombre, usuario, contrasena, rol):

		nombre = nombre.strip()
		usuario = usuario.strip().lower()

		if not nombre or not usuario:
			raise ValueError("Completa todos los campos.")

		if len(contrasena) < 8:
			raise ValueError(
				"La contrasena debe tener minimo 8 caracteres."
			)

		if len(contrasena.encode("utf-8")) > 72:
			raise ValueError("La contrasena es demasiado larga.")

		if rol not in ("administrador", "empleado"):
			raise ValueError("Rol incorrecto.")

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
