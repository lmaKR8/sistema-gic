"""
Este paquete contiene los módulos principales del sistema:

- cliente: Clase base Cliente con encapsulamiento
- gestor_clientes: Gestión CRUD de clientes
"""

from modulos.cliente import Cliente
from modulos.gestor_clientes import GestorClientes

__all__ = ['Cliente', 'GestorClientes']
