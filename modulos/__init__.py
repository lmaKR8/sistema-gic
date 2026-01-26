"""
Este paquete contiene los módulos principales del sistema:

- cliente: Clase base Cliente con encapsulamiento
- cliente_regular: Clase ClienteRegular (sin descuento)
- cliente_premium: Clase ClientePremium (15% descuento + puntos)
- cliente_corporativo: Clase ClienteCorporativo (25% descuento)
- gestor_clientes: Gestión CRUD de clientes
"""

from modulos.cliente import Cliente
from modulos.cliente_regular import ClienteRegular
from modulos.cliente_premium import ClientePremium
from modulos.cliente_corporativo import ClienteCorporativo
from modulos.gestor_clientes import GestorClientes

__all__ = [
    'Cliente',
    'ClienteRegular',
    'ClientePremium',
    'ClienteCorporativo',
    'GestorClientes'
]
