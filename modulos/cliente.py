"""
=================
Módulo Cliente
=================
"""
from typing import Any
from modulos.validaciones import (
    validar_nombre,
    validar_email,
    validar_telefono,
    validar_direccion
)

class Cliente:
    """
    Clase que representa a un cliente en el sistema.

    Atributos privados:
        __nombre (str): Nombre completo del cliente
        __email (str): Correo electrónico del cliente
        __telefono (str): Número de teléfono del cliente
        __direccion (str): Dirección física del cliente
    """
    
    def __init__(self, nombre: str, email: str, telefono: str, direccion: str):
        validar_nombre(nombre)
        validar_email(email)
        validar_telefono(telefono)
        validar_direccion(direccion)
        
        self.__nombre = nombre.strip()
        self.__email = email.strip().lower()
        self.__telefono = telefono.strip()
        self.__direccion = direccion.strip()
    

    def __str__(self) -> str:
        return f"Cliente: {self.__nombre} |> Email: {self.__email}"


    """
    PROPIEDADES
    """
    # Nombre
    @property
    def nombre(self) -> str:
        return self.__nombre
    
    @nombre.setter
    def nombre(self, valor: str):
        self.__nombre = valor
    

    # Email
    @property
    def email(self) -> str:
        return self.__email
    
    @email.setter
    def email(self, valor: str):
        self.__email = valor
    

    # Teléfono
    @property
    def telefono(self) -> str:
        return self.__telefono
    
    @telefono.setter
    def telefono(self, valor: str):
        self.__telefono = valor
    

    # Dirección
    @property
    def direccion(self) -> str:
        return self.__direccion
    
    @direccion.setter
    def direccion(self, valor: str):
        self.__direccion = valor


    """
    MÉTODOS PÚBLICOS
    """
    def mostrar_info(self):
        print("=" * 50)
        print("INFORMACIÓN DEL CLIENTE")
        print("=" * 50)
        print(f"Nombre:    {self.__nombre}")
        print(f"Email:     {self.__email}")
        print(f"Teléfono:  {self.__telefono}")
        print(f"Dirección: {self.__direccion}")
        print("=" * 50)


    def obtener_tipo(self) -> str:
        """
        Este método está diseñado para ser sobrescrito por las subclases (default "Cliente").
        """
        return "Cliente"


    def obtener_datos(self) -> dict[str, Any]:
        """
        Retorna los datos del cliente como diccionario. Útil para exportación y serialización de datos.
        """
        return {
            'tipo': self.obtener_tipo(),
            'nombre': self.__nombre,
            'email': self.__email,
            'telefono': self.__telefono,
            'direccion': self.__direccion
        }
