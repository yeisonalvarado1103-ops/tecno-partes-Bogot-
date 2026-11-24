# TECNO PARTES BOGOTÁ

## Sistema de Gestión y Control Seguro de la Información

Proyecto académico - Sprint 2

## 1. Descripción del proyecto

Tecno Partes Bogotá es un sistema de gestión de inventario
desarrollado en Python y PostgreSQL, diseñado para administrar
productos, controlar existencias y gestionar usuarios mediante
roles y permisos de acceso.

El sistema permite almacenar información de manera permanente
en una base de datos relacional.

## 2. Objetivo general

Desarrollar un sistema de información que permita gestionar
el inventario de repuestos y componentes de computadores,
incorporando mecanismos de autenticación, almacenamiento
y control de acceso mediante roles.

## 3. Tecnologías utilizadas

- Python
- PostgreSQL 18
- Psycopg 3
- pgAdmin 4
- Visual Studio Code
- Git
- GitHub
- PostgreSQL pgcrypto

## 4. Funcionalidades del sistema

### Gestión de inventario

- Consultar inventario.
- Registrar nuevos productos.
- Buscar productos por nombre.
- Registrar cantidades y precios.
- Ingresar unidades.
- Retirar unidades.
- Actualizar cantidades.
- Eliminar productos.
- Consultar el total de productos y unidades.
- Almacenar información en PostgreSQL.

### Gestión de usuarios

- Inicio de sesión.
- Cierre de sesión.
- Creación de administradores.
- Creación de empleados.
- Consulta de usuarios registrados.
- Activación de usuarios.
- Desactivación de usuarios.
- Protección de contraseñas mediante bcrypt.
- Control de acceso por roles.
- Límite de tres intentos por inicio de sesión.

## 5. Roles y permisos

| Funcionalidad | Administrador | Empleado |
|---|---|---|
| Consultar inventario | Sí | Sí |
| Registrar productos | Sí | Sí |
| Buscar productos | Sí | Sí |
| Ingresar unidades | Sí | Sí |
| Retirar unidades | Sí | Sí |
| Actualizar cantidades | Sí | No |
| Eliminar productos | Sí | No |
| Administrar usuarios | Sí | No |

## 6. Estructura del proyecto

- main.py: Menú principal e inicio de sesión.
- conexion.py: Conexión con PostgreSQL.
- crear_admin.py: Creación del primer administrador.
- modulos/inventario.py: Gestión de inventario.
- modulos/usuarios.py: Gestión de usuarios.
- inventario.json: Respaldo del inventario anterior.
- README.md: Documentación del proyecto.
- .gitignore: Exclusión de archivos en Git.

## 7. Base de datos

Motor: PostgreSQL.

### Tabla productos

- id
- nombre
- cantidad
- precio

### Tabla usuarios

- id
- nombre
- usuario
- contrasena
- rol
- activo
- fecha_creacion

## 8. Requisitos de instalación

- Python instalado.
- PostgreSQL instalado.
- Base de datos configurada.
- Tablas productos y usuarios creadas.
- Extensión pgcrypto habilitada.
- Biblioteca Psycopg instalada.

Para instalar Psycopg:

    python -m pip install "psycopg[binary]"

## 9. Ejecución del sistema

Configurar los datos de conexión en conexion.py.

El nombre de la base de datos debe coincidir exactamente
con el registrado en PostgreSQL, incluyendo los espacios
si existen.

Para crear el primer administrador:

    python crear_admin.py

Para iniciar el sistema:

    python main.py

Introducir la contraseña de PostgreSQL y posteriormente
las credenciales del usuario registrado.

## 10. Seguridad de la información

El sistema incorpora:

- Autenticación de usuarios.
- Contraseñas protegidas mediante hash bcrypt.
- Consultas SQL parametrizadas.
- Control de acceso por roles en Python.
- Restricción de funciones administrativas.
- Bloqueo del acceso a cuentas desactivadas.
- Contraseñas ocultas durante su escritura.

## 11. Pruebas funcionales realizadas

- [x] Conexión con PostgreSQL.
- [x] Consulta de inventario.
- [x] Registro de productos.
- [x] Búsqueda de productos.
- [x] Ingreso de unidades.
- [x] Retiro de unidades.
- [x] Actualización de cantidades.
- [x] Eliminación de productos.
- [x] Creación de administrador.
- [x] Creación de empleado.
- [x] Inicio de sesión.
- [x] Cierre de sesión.
- [x] Restricción de permisos.
- [x] Desactivación de usuarios.
- [x] Reactivación de usuarios.
- [x] Almacenamiento permanente.
- [x] Publicación del código en GitHub.

## 12. Control de versiones

El proyecto utiliza Git y GitHub para almacenar
y gestionar los avances del desarrollo.

### Sprint 1

- Desarrollo inicial del sistema de inventario.
- Almacenamiento mediante archivos JSON.

### Sprint 2

- Integración con PostgreSQL.
- Gestión de usuarios.
- Autenticación.
- Roles y permisos.
- Protección de contraseñas.
- Pruebas funcionales.

## 13. Mejoras futuras

- Implementar una interfaz gráfica.
- Generar reportes de inventario.
- Incorporar historial de movimientos.
- Implementar auditoría de operaciones.
- Automatizar la configuración de la base de datos.
- Utilizar una cuenta de PostgreSQL con permisos limitados.
- Fortalecer la seguridad para entornos de producción.

## 14. Estado del proyecto

Sprint 2: Desarrollo funcional completado.

Sistema académico en entorno local de pruebas.
No destinado todavía a producción.

## 15. Equipo de desarrollo

Proyecto académico desarrollado en equipo.

## 16. Fecha de actualización

24 de noviembre de 2026.

---

TECNO PARTES BOGOTÁ

Sistema de Gestión y Control Seguro de la Información.
