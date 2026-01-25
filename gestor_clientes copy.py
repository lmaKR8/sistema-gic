"""
Módulo Gestión de Clientes
"""
from modulos.cliente import Cliente

class GestorClientes:
    """
    Clase que gestiona una colección con los clientes
    
    Atributos privados:
        __clientes (list): Lista que almacena objetos Cliente
    """
    
    def __init__(self):
        self.__clientes = []
    
    def agregar_cliente(self, cliente):
        self.__clientes.append(cliente)
        print(f"\n✓ Cliente '{cliente._Cliente__nombre}' agregado exitosamente.")
    
    def listar_clientes(self):
        """
        Muestra la información básica de cada cliente usando __str__
        """
        if not self.__clientes:
            print("\n⚠ No hay clientes registrados en el sistema.")
            return
        
        print("\n" + "=" * 50)
        print("LISTA DE CLIENTES REGISTRADOS")
        print("=" * 50)
        for i, cliente in enumerate(self.__clientes, 1):
            print(f"{i}. {cliente}")
        print("=" * 50)
        print(f"Total de clientes: {self.obtener_total_clientes()}")
    
    def obtener_total_clientes(self):
        """
        Retorna la cantidad total de clientes registrados
        """
        return len(self.__clientes)
