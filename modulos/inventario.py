"""Gestión de inventario de Tecno Partes Bogotá."""
import json
import math
import os
from pathlib import Path
 
 
class Inventario:
    """Administra productos y sus cantidades disponibles."""
 
    def __init__(self):
        self._productos = {}
        self.archivo = Path(__file__).resolve().parent.parent / 'inventario.json'
        self.cargar()
 
    @staticmethod
    def _nombre(nombre):
        nombre = str(nombre).strip()
        if not nombre:
            raise ValueError('El nombre del producto no puede estar vacío.')
        return nombre
 
    @staticmethod
    def _cantidad(cantidad):
        if (isinstance(cantidad, bool) or
                not isinstance(cantidad, (int, float)) or
                not math.isfinite(cantidad) or cantidad < 0):
            raise ValueError('La cantidad debe ser un número mayor o igual que cero.')
        return cantidad
 
    def guardar(self):
        """Guarda el inventario de forma segura en un archivo JSON."""
        temporal = self.archivo.with_suffix('.json.tmp')
        try:
            with open(temporal, 'w', encoding='utf-8') as archivo:
                json.dump(self._productos, archivo, indent=4,
                          ensure_ascii=False, allow_nan=False)
            os.replace(temporal, self.archivo)
        finally:
            if temporal.exists():
                temporal.unlink()
 
    def cargar(self):
        """Recupera los datos previamente guardados, si existen."""
        if not self.archivo.exists():
            return
        with open(self.archivo, 'r', encoding='utf-8') as archivo:
            datos = json.load(archivo)
        if not isinstance(datos, dict):
            raise ValueError('Formato de inventario incorrecto.')
        productos = {}
        for nombre, cantidad in datos.items():
            productos[self._nombre(nombre)] = self._cantidad(cantidad)
        self._productos = productos
 
    def agregar(self, nombre, cantidad=1):
        """Agrega unidades de un producto al inventario."""
        nombre = self._nombre(nombre)
        cantidad = self._cantidad(cantidad)
        anterior = self._productos.copy()
        self._productos[nombre] = self._productos.get(nombre, 0) + cantidad
        try:
            self.guardar()
        except OSError:
            self._productos = anterior
            raise
        return self._productos[nombre]
 
    def retirar(self, nombre, cantidad=1):
        """Retira unidades si hay existencias suficientes."""
        nombre = self._nombre(nombre)
        cantidad = self._cantidad(cantidad)
        disponible = self._productos.get(nombre, 0)
        if cantidad > disponible:
            raise ValueError('No hay existencias suficientes.')
        if nombre not in self._productos or cantidad == 0:
            return disponible
        anterior = self._productos.copy()
        restante = disponible - cantidad
        if restante == 0:
            del self._productos[nombre]
        else:
            self._productos[nombre] = restante
        try:
            self.guardar()
        except OSError:
            self._productos = anterior
            raise
        return restante
 
    def consultar(self, nombre):
        """Devuelve la cantidad disponible de un producto."""
        return self._productos.get(str(nombre).strip(), 0)
 
    def listar(self):
        """Devuelve una copia del inventario actual."""
        return dict(self._productos)
 
    def buscar(self, nombre):
        """Devuelve la cantidad o None si el producto no existe."""
        return self._productos.get(str(nombre).strip())
 
    def actualizar(self, nombre, cantidad):
        """Reemplaza la cantidad registrada de un repuesto."""
        nombre = self._nombre(nombre)
        cantidad = self._cantidad(cantidad)
        if nombre not in self._productos:
            raise ValueError('El producto no está registrado.')
        anterior = self._productos.copy()
        self._productos[nombre] = cantidad
        try:
            self.guardar()
        except OSError:
            self._productos = anterior
            raise
        return cantidad
 
    def eliminar(self, nombre):
        """Elimina un producto del inventario."""
        nombre = self._nombre(nombre)
        if nombre not in self._productos:
            raise ValueError('El producto no está registrado.')
        anterior = self._productos.copy()
        del self._productos[nombre]
        try:
            self.guardar()
        except OSError:
            self._productos = anterior
            raise
        return True
 
    def total_productos(self):
        return len(self._productos)
 
    def total_unidades(self):
        return sum(self._productos.values())
