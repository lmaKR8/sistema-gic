"""
======================
Módulo Cliente Regular
======================
"""
from typing import Any
from modulos.cliente import Cliente


class ClienteRegular(Cliente):
    """
    Hereda de la clase base Cliente sin agregar atributos adicionales.
    
    HERENCIA:
    - Hereda: nombre, email, telefono, direccion
    - Hereda: mostrar_info(), obtener_datos()
    
    POLIMORFISMO:
    - Sobrescribe: obtener_tipo() -> retorna "Regular"
    - Sobrescribe: calcular_descuento() -> retorna 0.0
    """
    TIPO_CLIENTE = "Regular"
    DESCUENTO = 0.0
    

    def __init__(self, nombre: str, email: str, telefono: str, direccion: str):
        super().__init__(nombre, email, telefono, direccion)
    

    def __str__(self) -> str:
        return f"[{self.TIPO_CLIENTE}] {self.nombre} - {self.email}"
    

    def __repr__(self) -> str:
        return f"ClienteRegular(nombre='{self.nombre}', email='{self.email}')"


    """
    MÉTODOS POLIMÓRFICOS
    """
    def obtener_tipo(self) -> str:
        """
        Sobrescribe el metodo de la clase padre.
        
        Returns:
            str: "Regular"
        """
        return self.TIPO_CLIENTE
    

    def calcular_descuento(self, monto: float = 0) -> float:
        """
        Calcula el monto de descuento del cliente.
        
        Args:
            monto (float): Monto sobre el cual calcular el descuento
        Returns:
            float: 0.0 (sin descuento)
        """
        return monto * self.DESCUENTO
    

    def beneficio_exclusivo(self) -> str:
        """
        Retorna el beneficio exclusivo para clientes regulares.
        
        Returns:
            str: Descripcion del beneficio
        """
        return "Acceso a promociones y ofertas especiales para clientes regulares."
    

    """
    MÉTODOS
    """
    def mostrar_info(self):
        print("=" * 50)
        print("INFORMACION DEL CLIENTE REGULAR")
        print("=" * 50)
        print(f"  Nombre:    {self.nombre}")
        print(f"  Email:     {self.email}")
        print(f"  Telefono:  {self.telefono}")
        print(f"  Direccion: {self.direccion}")
        print(f"  Tipo:      {self.obtener_tipo()}")
        print(f"  Descuento: {self.calcular_descuento():.0%}")
        print("=" * 50)
    
    def obtener_datos(self) -> dict[str, Any]:
        """
        Extiende el metodo de la clase padre agregando datos de cliente regular.

        Returns:
            dict: Diccionario con todos los datos del cliente
        """
        datos = super().obtener_datos()
        datos["tipo"] = self.obtener_tipo()
        datos["descuento"] = self.calcular_descuento()
        return datos
    