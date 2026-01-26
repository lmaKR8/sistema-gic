"""
======================
Módulo Cliente Premium
======================
"""
from typing import Any
from modulos.cliente import Cliente


class ClientePremium(Cliente):
    """
    Hereda de la clase base Cliente y agrega funcionalidades premium como programa de puntos y descuentos especiales.
    
    HERENCIA:
    - Hereda: nombre, email, telefono, direccion
    - Hereda: mostrar_info(), obtener_datos()
    
    POLIMORFISMO:
    - Sobrescribe: obtener_tipo() -> retorna "Premium"
    - Sobrescribe: calcular_descuento() -> retorna 0.15 (15%)
    
    EXTENSION:
    - Agrega: puntos_acumulados (sistema de fidelidad)
    - Agrega: agregar_puntos(), canjear_puntos()
    """
    TIPO_CLIENTE = "Premium"
    DESCUENTO = 0.15  # 15% de descuento
    

    def __init__(self, nombre: str, email: str, telefono: str, 
                direccion: str, puntos_iniciales: int = 0):
        super().__init__(nombre, email, telefono, direccion)
        self.__puntos_acumulados = puntos_iniciales


    def __str__(self) -> str:
        return f"[{self.TIPO_CLIENTE}] {self.nombre} - {self.email} ({self.__puntos_acumulados} pts)"
    
    
    def __repr__(self) -> str:
        return f"ClientePremium(nombre='{self.nombre}', email='{self.email}', puntos={self.__puntos_acumulados})"


    """
    PROPIEDADES
    """
    # Puntos Acumulados
    @property
    def puntos_acumulados(self) -> int:
        return self.__puntos_acumulados
    

    """
    MÉTODOS POLIMÓRFICOS
    """
    def obtener_tipo(self) -> str:
        """
        Sobrescribe el metodo de la clase padre.

        Returns:
            str: "Premium"
        """
        return self.TIPO_CLIENTE
    

    def calcular_descuento(self, monto: float = 0) -> float:
        """
        Calcula el monto de descuento del cliente.
        
        Args:
            monto (float): Monto sobre el cual calcular el descuento
        Returns:
            float: Monto del descuento (15% del monto)
        """
        return monto * self.DESCUENTO
    

    def beneficio_exclusivo(self) -> str:
        """
        Retorna el beneficio exclusivo para clientes premium.
        
        Returns:
            str: Descripcion del beneficio incluyendo puntos
        """
        return f"Descuento del 15% en todas las compras y {self.__puntos_acumulados} puntos acumulados."
    

    """
    MÉTODOS
    """
    def mostrar_info(self):
        print("=" * 50)
        print("[*] INFORMACION DEL CLIENTE PREMIUM [*]")
        print("=" * 50)
        print(f"  Nombre:    {self.nombre}")
        print(f"  Email:     {self.email}")
        print(f"  Telefono:  {self.telefono}")
        print(f"  Direccion: {self.direccion}")
        print("-" * 50)
        print("  BENEFICIOS PREMIUM:")
        print(f"  Tipo:              {self.obtener_tipo()}")
        print(f"  Descuento:         {self.calcular_descuento():.0%}")
        print(f"  Puntos acumulados: {self.__puntos_acumulados} pts")
        print("=" * 50)
    

    def agregar_puntos(self, puntos: int):
        """
        Agrega puntos al programa de fidelidad.
        
        Args:
            puntos (int): Cantidad de puntos a agregar
        """
        if puntos > 0:
            self.__puntos_acumulados += puntos
            print(f"[OK] Se agregaron {puntos} puntos. Total: {self.__puntos_acumulados} pts")
    

    def canjear_puntos(self, puntos: int) -> bool:
        """
        Canjea puntos del programa de fidelidad.
        
        Args:
            puntos (int): Cantidad de puntos a canjear
        Returns:
            bool: True si se pudieron canjear, False si no hay suficientes
        """
        if puntos <= self.__puntos_acumulados:
            self.__puntos_acumulados -= puntos
            print(f"[OK] Se canjearon {puntos} puntos. Restantes: {self.__puntos_acumulados} pts")
            return True
        else:
            print(f"[X] Puntos insuficientes. Disponibles: {self.__puntos_acumulados} pts")
            return False
    

    def obtener_datos(self) -> dict[str, Any]:
        """
        Extiende el metodo de la clase padre agregando datos premium.
        
        Returns:
            dict: Diccionario con todos los datos del cliente
        """
        datos = super().obtener_datos()
        datos["tipo"] = self.obtener_tipo()
        datos["descuento"] = self.DESCUENTO
        datos["puntos_acumulados"] = self.__puntos_acumulados
        return datos
