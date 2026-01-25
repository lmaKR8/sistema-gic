"""
Acceso al Sistema GIC (Gestor Inteligente de Clientes)
======================================================
"""
from modulos.cliente import Cliente
from modulos.gestor_clientes import GestorClientes

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
    print("  6. Salir")
    print("-" * 40)


"""
FUNCIONES
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


def agregar_cliente(gestor):
    """
    Maneja la opción de agregar un nuevo cliente.
    
    Args:
        gestor (GestorClientes): Instancia del gestor de clientes
    """
    nombre, email, telefono, direccion = solicitar_datos_cliente()
    
    # Valida que todos los campos estén completos
    if not all([nombre, email, telefono, direccion]):
        print("\nError: Todos los campos son obligatorios.")
        return
    
    # Crea y agrega el cliente
    cliente = Cliente(nombre, email, telefono, direccion)
    gestor.agregar_cliente(cliente)


def buscar_cliente(gestor):
    """
    Maneja la opción de buscar un cliente por email.
    
    Args:
        gestor (GestorClientes): Instancia del gestor de clientes
    """
    email = input("\n  Ingrese el email del cliente a buscar: ").strip()
    
    if not email:
        print("\nError: Debe ingresar un email.")
        return
    
    gestor.mostrar_cliente(email)


def actualizar_cliente(gestor):
    """
    Maneja la opción de actualizar los datos de un cliente.
    
    Args:
        gestor (GestorClientes): Instancia del gestor de clientes
    """
    email = input("\n  Ingrese el email del cliente a actualizar: ").strip()
    
    if not email:
        print("\nError: Debe ingresar un email.")
        return
    
    # Verifica que el cliente existe
    cliente = gestor.buscar_cliente(email)
    if not cliente:
        print(f"\nNo se encontró ningún cliente con el email '{email}'.")
        return
    
    print("\n--- Datos actuales del cliente ---")
    cliente.mostrar_info()
    
    print("\n--- Ingrese los nuevos datos (deje vacío para mantener el actual) ---")
    nombre = input(f"  Nombre [{cliente.nombre}]: ").strip()
    telefono = input(f"  Teléfono [{cliente.telefono}]: ").strip()
    direccion = input(f"  Dirección [{cliente.direccion}]: ").strip()
    
    # Actualiza con los valores proporcionados (o None si están vacíos)
    gestor.actualizar_cliente(
        email,
        nombre=nombre if nombre else None,
        telefono=telefono if telefono else None,
        direccion=direccion if direccion else None
    )


def eliminar_cliente(gestor):
    """
    Maneja la opción de eliminar un cliente.
    
    Args:
        gestor (GestorClientes): Instancia del gestor de clientes
    """
    email = input("\n  Ingrese el email del cliente a eliminar: ").strip()
    
    if not email:
        print("\nError: Debe ingresar un email.")
        return
    
    # Confirma la eliminación
    cliente = gestor.buscar_cliente(email)
    if cliente:
        confirmacion = input(f"\n  ¿Está seguro de eliminar a '{cliente.nombre}'? (s/n): ").strip().lower()
        if confirmacion == 's':
            gestor.eliminar_cliente(email)
        else:
            print("\n  Operación cancelada.")
    else:
        print(f"\nNo se encontró ningún cliente con el email '{email}'.")


def cargar_datos_prueba(gestor):
    """
    Carga datos de prueba para demostrar el funcionamiento del sistema.
    
    Args:
        gestor (GestorClientes): Instancia del gestor de clientes
    """
    clientes_prueba = [
        Cliente("Juan Pérez García", "juan.perez@email.com", "+56912345678", "Av. Libertador 1234, Iquique"),
        Cliente("María González López", "maria.gonzalez@empresa.cl", "+56987654321", "Calle Principal 567, Valparaíso"),
        Cliente("Carlos Rodríguez Soto", "carlos.rodriguez@corporativo.com", "+56956781234", "Paseo Ahumada 890, Santiago"),
    ]
    
    print("\n--- Cargando datos de prueba ---")
    for cliente in clientes_prueba:
        gestor.agregar_cliente(cliente)


"""
FUNCION PRINCIPAL
"""
def main():
    """
    Implementa menú interactivo y coordina las operaciones del sistema
    """
    gestor = GestorClientes()
    
    mostrar_encabezado()
    
    # Preguntar si cargar datos de prueba
    cargar = input("\n¿Desea cargar datos de prueba? (s/n): ").strip().lower()
    if cargar == 's':
        cargar_datos_prueba(gestor)
    
    # Bucle principal del menú
    while True:
        mostrar_menu()
        opcion = input("  Seleccione una opción (1-6): ").strip()
        
        if opcion == '1':
            agregar_cliente(gestor)
        elif opcion == '2':
            gestor.listar_clientes()
        elif opcion == '3':
            buscar_cliente(gestor)
        elif opcion == '4':
            actualizar_cliente(gestor)
        elif opcion == '5':
            eliminar_cliente(gestor)
        elif opcion == '6':
            print("\n" + "=" * 60)
            print(" " * 15 + "¡Gracias por usar el sistema GIC!")
            print(" " * 20 + "Hasta pronto.")
            print("=" * 60 + "\n")
            break
        else:
            print("\nOpción no válida. Por favor, seleccione una opción del 1 al 6.")


# Punto de entrada del programa
if __name__ == "__main__":
    main()
