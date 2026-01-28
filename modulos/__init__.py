"""
Este paquete contiene los módulos principales del sistema
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
