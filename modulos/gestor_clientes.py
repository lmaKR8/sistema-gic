"""
==========================
Módulo Gestión de Clientes
==========================
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


    """
    PROPIEDADES
    """
    @property
    def clientes(self) -> list[Cliente]:  # Obtiene la lista de clientes (solo lectura)
        return self.__clientes.copy()
    
    @property
    def total_clientes(self) -> int:
        return len(self.__clientes)


    """
    CRUD: CREATE
    """
    def agregar_cliente(self, cliente: Cliente, silencioso: bool = False) -> bool:
        """
        Agrega un nuevo cliente al sistema y verifica la existencia del email.
        
        Args:
            cliente (Cliente): Objeto Cliente a agregar
            silencioso (bool): Si es True, no muestra mensajes en consola
        Returns:
            bool: True si se agregó correctamente, False si ya existe
        """
        # Verificar si ya existe un cliente con ese email
        if self.buscar_cliente(cliente.email):
            if not silencioso:
                print(f"\n[X] Error: Ya existe un cliente con el email '{cliente.email}'.")
            return False
        
        self.__clientes.append(cliente)
        if not silencioso:
            print(f"\n[OK] Cliente '{cliente.nombre}' agregado exitosamente.")
        return True


    """
    CRUD: READ
    """
    def listar_clientes(self):
        """
        Lista todos los clientes registrados en el sistema usando su representación en cadena (__str__)
        """
        if not self.__clientes:
            print("\n[!] No hay clientes registrados en el sistema.")
            return
        
        print("\n" + "=" * 60)
        print(" " * 15 + "LISTA DE CLIENTES REGISTRADOS")
        print("=" * 60)

        for i, cliente in enumerate(self.__clientes, 1):
            print(f"  {i}. {cliente}")
        
        print("=" * 60)
        print(f"  Total de clientes: {self.total_clientes}")
        print("=" * 60)
    

    def buscar_cliente(self, email: str) -> Cliente | None:
        """
        Busca un cliente por su email. El email actúa como identificador único del cliente en el sistema
        
        Args:
            email (str): Email del cliente a buscar
        Returns:
            Cliente | None: Objeto Cliente si existe, None si no se encuentra
        """
        for cliente in self.__clientes:
            if cliente.email.lower() == email.lower():
                return cliente
        return None
    
    
    def mostrar_cliente(self, email: str) -> bool:
        """
        Muestra la información detallada de un cliente
        
        Args:
            email (str): Email del cliente a mostrar
        Returns:
            bool: True si se encontró y mostró, False si no existe
        """
        cliente = self.buscar_cliente(email)
        if cliente:
            cliente.mostrar_info()
            return True
        else:
            print(f"\n[X] No se encontro ningun cliente con el email '{email}'.")
            return False
        

    """
    CRUD: UPDATE
    """
    def actualizar_cliente(self, email: str, nombre: str, telefono: str, direccion: str) -> bool:
        """
        Actualiza los datos de un cliente existente
        
        Args:
            email (str): Email del cliente a actualizar
            nombre (str): Nuevo nombre del cliente
            telefono (str): Nuevo teléfono del cliente
            direccion (str): Nueva dirección del cliente
        Returns:
            bool: True si se actualizó correctamente, False si no existe
        """
        cliente = self.buscar_cliente(email)
        
        if not cliente:
            print(f"\n[X] No se encontro ningun cliente con el email '{email}'.")
            return False
        
        # Actualiza solo los campos proporcionados
        if nombre:
            cliente.nombre = nombre
        if telefono:
            cliente.telefono = telefono
        if direccion:
            cliente.direccion = direccion
        
        print(f"\n[OK] Cliente '{cliente.nombre}' actualizado exitosamente.")
        return True
    

    """
    CRUD: DELETE
    """
    def eliminar_cliente(self, email: str) -> bool:
        """
        Busca al cliente por su email y lo elimina de la lista.
        
        Args:
            email (str): Email del cliente a eliminar
        Returns:
            bool: True si se eliminó correctamente, False si no existe
        """
        cliente = self.buscar_cliente(email)
        
        if not cliente:
            print(f"\n[X] No se encontro ningun cliente con el email '{email}'.")
            return False
        
        nombre_cliente = cliente.nombre
        self.__clientes.remove(cliente)

        print(f"\n[OK] Cliente '{nombre_cliente}' eliminado exitosamente.")
        return True


    """
    MÉTODOS AUXILIARES
    """
    def obtener_total_clientes(self):
        return self.total_clientes
    

    def limpiar_lista(self):
        cantidad = self.total_clientes
        self.__clientes.clear()
        print(f"\n[OK] Se eliminaron {cantidad} cliente(s) del sistema.")


    """
    METODOS PARA LISTAS HETEROGENEAS Y POLIMORFISMO
    """
    def obtener_clientes_por_tipo(self, tipo: str) -> list:
        """
        Cada cliente tiene su propio metodo obtener_tipo() que retorna su tipo especifico.
        """
        return [c for c in self.__clientes if c.obtener_tipo() == tipo]
    

    def listar_por_tipo(self, tipo: str):
        """
        Muestra solo los clientes que coinciden con el tipo indicado.
        """
        clientes_filtrados = self.obtener_clientes_por_tipo(tipo)
        
        if not clientes_filtrados:
            print(f"\n[!] No hay clientes de tipo '{tipo}' registrados.")
            return
        
        print("\n" + "=" * 60)
        print(f" " * 10 + f"CLIENTES TIPO: {tipo.upper()}")
        print("=" * 60)

        for i, cliente in enumerate(clientes_filtrados, 1):
            cliente.mostrar_info()

        print("=" * 60)
        print(f"Total clientes {tipo}: {len(clientes_filtrados)}")
        print("=" * 60)
    

    def mostrar_estadisticas(self):
        """
        Muestra estadisticas de clientes por tipo.
        """
        tipos = {}
        
        for cliente in self.__clientes:
            tipo = cliente.obtener_tipo()
            tipos[tipo] = tipos.get(tipo, 0) + 1
        
        print("\n" + "=" * 60)
        print(" " * 15 + "ESTADISTICAS DE CLIENTES")
        print("=" * 60)
        
        if not tipos:
            print("[X] No hay clientes registrados.")
        else:
            for tipo, cantidad in sorted(tipos.items()):
                porcentaje = (cantidad / self.total_clientes) * 100
                barra = "#" * int(porcentaje / 5)
                print(f"  {tipo:15} | {cantidad:3} | {barra} {porcentaje:.1f}%")
        
        print("-" * 60)
        print(f"  {'TOTAL':15} | {self.total_clientes:3} |")
        print("=" * 60)
    

    def aplicar_a_todos(self, metodo: str, *args, **kwargs):
        """
        Aplica un metodo a todos los clientes.
        """
        for cliente in self.__clientes:
            if hasattr(cliente, metodo):
                func = getattr(cliente, metodo)
                if callable(func):
                    func(*args, **kwargs)
