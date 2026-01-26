"""
==========================
Módulo Cliente Corporativo
==========================
"""
from typing import Any
from modulos.cliente import Cliente


class ClienteCorporativo(Cliente):
    """
    Hereda de la clase Cliente y agrega funcionalidades para empresas como datos de facturación y descuentos corporativos.
    
    HERENCIA:
    - Hereda: nombre, email, telefono, direccion
    - Hereda: mostrar_info(), obtener_datos()
    
    POLIMORFISMO:
    - Sobrescribe: obtener_tipo() -> retorna "Corporativo"
    - Sobrescribe: calcular_descuento() -> retorna 0.25 (25%)
    
    EXTENSION:
    - Agrega: nombre_empresa, rut_empresa
    - Agrega: generar_factura_info()
    """
    TIPO_CLIENTE = "Corporativo"
    DESCUENTO = 0.25 # 25% de descuento
    

    def __init__(self, nombre: str, email: str, telefono: str, 
                direccion: str, nombre_empresa: str = "", rut_empresa: str = ""):
        super().__init__(nombre, email, telefono, direccion)
        self.__nombre_empresa = nombre_empresa
        self.__rut_empresa = rut_empresa


    def __str__(self) -> str:
        return f"[{self.TIPO_CLIENTE}] {self.nombre} - {self.email} ({self.__nombre_empresa})"


    def __repr__(self) -> str:
        return f"ClienteCorporativo(nombre='{self.nombre}', email='{self.email}', empresa='{self.__nombre_empresa}')"


    """
    PROPIEDADES
    """
    # Nombre Empresa
    @property
    def nombre_empresa(self) -> str:
        return self.__nombre_empresa

    @nombre_empresa.setter
    def nombre_empresa(self, valor: str):
        self.__nombre_empresa = valor


    # RUT Empresa
    @property
    def rut_empresa(self) -> str:
        return self.__rut_empresa
    
    @rut_empresa.setter
    def rut_empresa(self, valor: str):
        self.__rut_empresa = valor
    

    """
    MÉTODOS POLIMÓRFICOS
    """
    def obtener_tipo(self) -> str:
        """
        Sobrescribe el metodo de la clase padre.

        Returns:
            str: "Corporativo"
        """
        return self.TIPO_CLIENTE
    

    def calcular_descuento(self, monto: float = 0) -> float:
        """
        Calcula el monto de descuento del cliente.

        Args:
            monto (float): Monto sobre el cual calcular el descuento
        Returns:
            float: Monto del descuento (25% del monto)
        """
        return monto * self.DESCUENTO
    

    def beneficio_exclusivo(self) -> str:
        return f"Descuento del 25% para {self.__nombre_empresa} en todas las compras corporativas."
    

    """
    MÉTODOS
    """
    def mostrar_info(self):
        print("=" * 50)
        print("[B] INFORMACION DEL CLIENTE CORPORATIVO [B]")
        print("=" * 50)
        print("  DATOS DE CONTACTO:")
        print(f"  Nombre:    {self.nombre}")
        print(f"  Email:     {self.email}")
        print(f"  Telefono:  {self.telefono}")
        print(f"  Direccion: {self.direccion}")
        print("-" * 50)
        print("  DATOS DE LA EMPRESA:")
        print(f"  Empresa:   {self.__nombre_empresa}")
        print(f"  RUT:       {self.__rut_empresa}")
        print("-" * 50)
        print("  BENEFICIOS CORPORATIVOS:")
        print(f"  Tipo:      {self.obtener_tipo()}")
        print(f"  Descuento: {self.calcular_descuento():.0%}")
        print("=" * 50)
    

    def generar_factura_info(self) -> dict[str, str]:
        """
        Genera informacion para facturacion. Retorna un diccionario con los datos necesarios para emitir una factura a nombre de la empresa.
        
        Returns:
            dict: Datos de facturacion (nombre_empresa, rut_empresa, direccion)
        """
        return {
            "nombre_empresa": self.__nombre_empresa,
            "rut_empresa": self.__rut_empresa,
            "direccion": self.direccion,
            "contacto": self.nombre,
            "email": self.email
        }
    

    def obtener_datos(self) -> dict[str, Any]:
        """
        Extiende el metodo de la clase padre agregando datos corporativos.
        
        Returns:
            dict: Diccionario con todos los datos del cliente
        """
        datos = super().obtener_datos()
        datos["tipo"] = self.obtener_tipo()
        datos["descuento"] = self.DESCUENTO
        datos["nombre_empresa"] = self.__nombre_empresa
        datos["rut_empresa"] = self.__rut_empresa
        return datos
