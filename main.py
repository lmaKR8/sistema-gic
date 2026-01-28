"""
=================
Acceso al Sistema
=================
"""
from modulos import (
    Cliente,
    ClienteRegular,
    ClientePremium,
    ClienteCorporativo,
    GestorClientes
)
from modulos.excepciones import (
    GICError,
    ValidacionError,
    EmailInvalidoError,
    TelefonoInvalidoError,
    NombreInvalidoError,
    DireccionInvalidaError,
    ClienteExistenteError,
    ClienteNoEncontradoError
)

"""
MENÚ
"""
def mostrar_encabezado():
    """
    Muestra el encabezado del sistema.
    """
    print("\n" + "=" * 60)
    print(" " * 8 + "SISTEMA GIC - GESTOR INTELIGENTE DE CLIENTES")
    print(" " * 23 + "SolutionTech")
    print("=" * 60)


def mostrar_menu():
    """
    Muestra el menú principal de opciones.
    """
    print("\n" + "-" * 40)
    print("           MENÚ PRINCIPAL")
    print("-" * 40)
    print("  1. Agregar cliente")
    print("  2. Listar clientes")
    print("  3. Buscar cliente")
    print("  4. Actualizar cliente")
    print("  5. Eliminar cliente")
    print("  6. Ver estadísticas")
    print("  7. Salir")
    print("-" * 40)


def mostrar_menu_tipo_cliente():
    """
    Muestra el submenú para seleccionar tipo de cliente.
    """
    print("\n--- Seleccione el tipo de cliente ---")
    print("  1. Cliente Regular (sin descuento)")
    print("  2. Cliente Premium (15% descuento + puntos)")
    print("  3. Cliente Corporativo (25% descuento)")
    print("  4. Cancelar")
    return input("  Opción: ").strip()


def mostrar_menu_listar():
    """
    Muestra el submenú para listar clientes.
    """
    print("\n--- Opciones de listado ---")
    print("  1. Listar todos los clientes")
    print("  2. Listar solo clientes Regular")
    print("  3. Listar solo clientes Premium")
    print("  4. Listar solo clientes Corporativo")
    print("  5. Volver al menú principal")
    return input("  Opción: ").strip()


"""
FUNCIONES DE SOLICITUD DE DATOS
"""
def solicitar_datos_cliente():
    """
    Solicita al usuario los datos para crear un nuevo cliente.
    
    Returns:
        tuple: (nombre, email, telefono, direccion) ingresados por el usuario
    """
    print("\n--- Ingreso de datos del cliente ---")
    nombre = input("  Nombre completo: ").strip()
    email = input("  Email: ").strip()
    telefono = input("  Teléfono: ").strip()
    direccion = input("  Dirección: ").strip()
    
    return nombre, email, telefono, direccion


def solicitar_datos_premium():
    """
    Solicita datos adicionales para cliente Premium.
    
    Returns:
        int: Puntos iniciales del cliente
    """
    print("\n--- Datos adicionales (Premium) ---")
    try:
        puntos = int(input("  Puntos iniciales (0 si es nuevo): ").strip() or "0")
        return max(0, puntos)  # No permitir puntos negativos
    except ValueError:
        print("[X] Valor inválido, se asignarán 0 puntos.")
        return 0


def solicitar_datos_corporativo():
    """
    Solicita datos adicionales para cliente Corporativo.
    
    Returns:
        tuple: (nombre_empresa, rut_empresa)
    """
    print("\n--- Datos adicionales (Corporativo) ---")
    nombre_empresa = input("  Nombre de la empresa: ").strip()
    rut_empresa = input("  RUT de la empresa: ").strip()
    return nombre_empresa, rut_empresa


"""
FUNCIONES DE OPERACIONES
"""
def agregar_cliente(gestor):
    """
    Maneja la opción de agregar un nuevo cliente.
    
    Args:
        gestor (GestorClientes): Instancia del gestor de clientes
    """
    tipo_opcion = mostrar_menu_tipo_cliente()
    
    if tipo_opcion == '4':
        print("\n[X] Operación cancelada.")
        return
    
    # Solicita datos básicos comunes a todos los tipos
    nombre, email, telefono, direccion = solicitar_datos_cliente()
    
    # Valida que los datos básicos estén completos
    if not all([nombre, email, telefono, direccion]):
        print("\n[X] Error: Los campos básicos son obligatorios.")
        return
    
    try:
        cliente = None
        
        if tipo_opcion == '1':
            # Cliente Regular
            cliente = ClienteRegular(nombre, email, telefono, direccion)
            
        elif tipo_opcion == '2':
            # Cliente Premium
            puntos = solicitar_datos_premium()
            cliente = ClientePremium(nombre, email, telefono, direccion, puntos)
            
        elif tipo_opcion == '3':
            # Cliente Corporativo
            nombre_empresa, rut_empresa = solicitar_datos_corporativo()
            if not all([nombre_empresa, rut_empresa]):
                print("\n[X] Error: Los datos de empresa son obligatorios para clientes corporativos.")
                return
            cliente = ClienteCorporativo(nombre, email, telefono, direccion, 
                                        nombre_empresa, rut_empresa)
        else:
            print("\n[X] Opcion no valida.")
            return
        
        # Agrega el cliente al gestor
        if cliente:
            gestor.agregar_cliente(cliente)

    # Manejo de excepciones
    except EmailInvalidoError as e:
        print(f"\n[X] {e}")
    except TelefonoInvalidoError as e:
        print(f"\n[X] {e}")
    except NombreInvalidoError as e:
        print(f"\n[X] {e}")
    except DireccionInvalidaError as e:
        print(f"\n[X] {e}")
    except ClienteExistenteError as e:
        print(f"\n[X] {e}")
    except ValidacionError as e:
        print(f"\n[X] Error de validacion: {e}")
    except GICError as e:
        print(f"\n[X] Error del sistema: {e}")


def listar_clientes(gestor):
    """
    Permite listar todos los clientes o filtrar por tipo.
    
    Args:
        gestor (GestorClientes): Instancia del gestor de clientes
    """
    opcion = mostrar_menu_listar()
    
    if opcion == '1':
        gestor.listar_clientes()
    elif opcion == '2':
        gestor.listar_por_tipo("Regular")
    elif opcion == '3':
        gestor.listar_por_tipo("Premium")
    elif opcion == '4':
        gestor.listar_por_tipo("Corporativo")
    elif opcion == '5':
        return
    else:
        print("\n[X] Opción no válida.")


def buscar_cliente(gestor):
    """
    Maneja la opción de buscar un cliente por email.
    
    Args:
        gestor (GestorClientes): Instancia del gestor de clientes
    """
    email = input("\n  Ingrese el email del cliente a buscar: ").strip()
    
    if not email:
        print("\n[X] Error: Debe ingresar un email.")
        return
    
    try:
        gestor.mostrar_cliente(email)
    except ClienteNoEncontradoError as e:
        print(f"\n[X] {e}")
    except GICError as e:
        print(f"\n[X] Error del sistema: {e}")


def actualizar_cliente(gestor):
    """
    Maneja la opción de actualizar los datos de un cliente.
    
    Args:
        gestor (GestorClientes): Instancia del gestor de clientes
    """
    email = input("\n  Ingrese el email del cliente a actualizar: ").strip()
    
    if not email:
        print("\n[X] Error: Debe ingresar un email.")
        return
    
    try:
        # Verifica que el cliente existe
        cliente = gestor.buscar_cliente(email)
        if not cliente:
            print(f"\n[X] No se encontro ningun cliente con el email '{email}'.")
            return
        
        print("\n--- Datos actuales del cliente ---")
        cliente.mostrar_info()
        
        print("\n--- Ingrese los nuevos datos (deje vacio para mantener el actual) ---")
        nombre = input(f"  Nombre [{cliente.nombre}]: ").strip()
        telefono = input(f"  Telefono [{cliente.telefono}]: ").strip()
        direccion = input(f"  Direccion [{cliente.direccion}]: ").strip()
        
        # Actualiza con los valores proporcionados (o None si estan vacios)
        gestor.actualizar_cliente(
            email,
            nombre=nombre if nombre else None,
            telefono=telefono if telefono else None,
            direccion=direccion if direccion else None
        )
    
    # Manejo de excepciones
    except NombreInvalidoError as e:
        print(f"\n[X] {e}")
    except TelefonoInvalidoError as e:
        print(f"\n[X] {e}")
    except DireccionInvalidaError as e:
        print(f"\n[X] {e}")
    except ClienteNoEncontradoError as e:
        print(f"\n[X] {e}")
    except ValidacionError as e:
        print(f"\n[X] Error de validacion: {e}")
    except GICError as e:
        print(f"\n[X] Error del sistema: {e}")


def eliminar_cliente(gestor):
    """
    Maneja la opción de eliminar un cliente.
    
    Args:
        gestor (GestorClientes): Instancia del gestor de clientes
    """
    email = input("\n  Ingrese el email del cliente a eliminar: ").strip()
    
    if not email:
        print("\n[X] Error: Debe ingresar un email.")
        return
    
    try:
        # Confirma eliminación
        cliente = gestor.buscar_cliente(email)
        if cliente:
            confirmacion = input(f"\n  Esta seguro de eliminar a '{cliente.nombre}'? (s/n): ").strip().lower()
            if confirmacion == 's':
                gestor.eliminar_cliente(email)
            else:
                print("\n  Operacion cancelada.")
        else:
            print(f"\n[X] No se encontro ningun cliente con el email '{email}'.")
    
    # Manejo de excepciones
    except ClienteNoEncontradoError as e:
        print(f"\n[X] {e}")
    except GICError as e:
        print(f"\n[X] Error del sistema: {e}")


def cargar_datos_prueba(gestor):
    """
    Carga datos de prueba con diferentes tipos de clientes.
    
    Args:
        gestor (GestorClientes): Instancia del gestor de clientes
    """
    try:
        clientes_prueba = [
            # Clientes Regulares
            ClienteRegular(
                "Juan Perez Garcia", 
                "juan.perez@email.com", 
                "+56912345678", 
                "Av. Libertador 1234, Iquique",
            ),
            ClienteRegular(
                "Ana Munoz Soto", 
                "ana.munoz@email.com", 
                "+56911112222", 
                "Calle Los Aromos 456, Antofagasta",
            ),
            
            # Clientes Premium
            ClientePremium(
                "Maria Gonzalez Lopez", 
                "maria.gonzalez@empresa.cl", 
                "+56987654321", 
                "Calle Principal 567, Valparaiso",
                puntos_iniciales=1500,
            ),
            ClientePremium(
                "Pedro Silva Ramirez", 
                "pedro.silva@premium.cl", 
                "+56933334444", 
                "Av. Marina 789, Vina del Mar",
                puntos_iniciales=3200,
            ),
            
            # Clientes Corporativos
            ClienteCorporativo(
                "Carlos Rodriguez Soto", 
                "carlos.rodriguez@techcorp.com", 
                "+56956781234", 
                "Paseo Ahumada 890, Santiago",
                nombre_empresa="TechCorp S.A.",
                rut_empresa="76.543.210-K",
            ),
            ClienteCorporativo(
                "Laura Fernandez Diaz", 
                "laura.fernandez@innovatech.cl", 
                "+56955556666", 
                "Av. Apoquindo 4500, Las Condes",
                nombre_empresa="InnovaTech SpA",
                rut_empresa="77.888.999-1",
            ),
        ]
        
        print("\n--- Cargando datos de prueba (lista heterogenea) ---")
        for cliente in clientes_prueba:
            gestor.agregar_cliente(cliente, silencioso=True)
        
        print(f"\n[OK] Se cargaron {len(clientes_prueba)} clientes de diferentes tipos.")
    
    # Manejo de excepciones
    except ClienteExistenteError as e:
        print(f"\n[!] Advertencia: {e}")
    except GICError as e:
        print(f"\n[X] Error al cargar datos de prueba: {e}")


def ver_estadisticas(gestor):
    """
    Muestra las estadísticas de clientes por tipo.
    
    Args:
        gestor (GestorClientes): Instancia del gestor de clientes
    """
    gestor.mostrar_estadisticas()


def ver_beneficios_cliente(gestor):
    """
    Muestra los beneficios exclusivos de un cliente.
    
    Args:
        gestor (GestorClientes): Instancia del gestor de clientes
    """
    email = input("\n  Ingrese el email del cliente: ").strip()
    
    if not email:
        print("\n[X] Error: Debe ingresar un email.")
        return
    
    try:
        cliente = gestor.buscar_cliente(email)
        if cliente:
            print("\n" + "=" * 60)
            print(f"  BENEFICIOS DE: {cliente.nombre}")
            print(f"  Tipo: {cliente.obtener_tipo()}")
            print("=" * 60)
            print(f"  {cliente.beneficio_exclusivo()}")
            print("=" * 60)
        else:
            print(f"\n[X] No se encontro ningun cliente con el email '{email}'.")
    
    # Manejo de excepciones
    except ClienteNoEncontradoError as e:
        print(f"\n[X] {e}")
    except GICError as e:
        print(f"\n[X] Error del sistema: {e}")


"""
FUNCION PRINCIPAL
"""
def main():
    """
    Implementa menú interactivo y coordina las operaciones del sistema
    """
    gestor = GestorClientes()
    
    mostrar_encabezado()
    
    # Pregunta si desea cargar datos de prueba
    cargar = input("\nDesea cargar datos de prueba? (s/n): ").strip().lower()
    if cargar == 's':
        cargar_datos_prueba(gestor)
    
    # Bucle principal del menú
    while True:
        mostrar_menu()
        opcion = input("  Seleccione una opción (1-7): ").strip()
        
        if opcion == '1':
            agregar_cliente(gestor)
        elif opcion == '2':
            listar_clientes(gestor)
        elif opcion == '3':
            buscar_cliente(gestor)
        elif opcion == '4':
            actualizar_cliente(gestor)
        elif opcion == '5':
            eliminar_cliente(gestor)
        elif opcion == '6':
            ver_estadisticas(gestor)
        elif opcion == '7':
            print("\n" + "=" * 60)
            print(" " * 15 + "¡Gracias por usar el sistema GIC!")
            print(" " * 20 + "Hasta pronto.")
            print("=" * 60 + "\n")
            break
        else:
            print("\n[X] Opción no válida. Por favor, seleccione una opción del 1 al 7.")


# Punto de entrada al programa
if __name__ == "__main__":
    main()
