"""
Módulo Cliente
"""

class Cliente:
    """
    Clase que representa a un cliente en el sistema
    
    Atributos privados:
        __nombre (str): Nombre completo del cliente
        __email (str): Correo electrónico del cliente
        __telefono (str): Número de teléfono del cliente
        __direccion (str): Dirección física del cliente
    """
    
    def __init__(self, nombre, email, telefono, direccion):
        self.__nombre = nombre
        self.__email = email
        self.__telefono = telefono
        self.__direccion = direccion
    
    def __str__(self):
        return f"Cliente: {self.__nombre} |> Email: {self.__email}"
    
    def mostrar_info(self):
        print("=" * 50)
        print("INFORMACIÓN DEL CLIENTE")
        print("=" * 50)
        print(f"Nombre:    {self.__nombre}")
        print(f"Email:     {self.__email}")
        print(f"Teléfono:  {self.__telefono}")
        print(f"Dirección: {self.__direccion}")
        print("=" * 50)
