"""
Módulo de pruebas para el Paso 1.
=================================
Aquí se realizan pruebas unitarias básicas para validar la funcionalidad de las clases Cliente y GestorClientes
"""
from cliente import Cliente
from gestor_clientes import GestorClientes


def test_paso_1():
    """
    Función que realiza las pruebas del Paso 1.
    
    Crea instancias de clientes y las gestiona usando el GestorClientes
    para validar el correcto funcionamiento de las clases implementadas.
    """
    print("\n>>> INICIANDO PRUEBAS DEL PASO 1 <<<\n")
    
    # Crear el gestor de clientes
    gestor = GestorClientes()
    print("✓ Gestor de clientes inicializado correctamente.")
    
    # Crear instancias de clientes de prueba
    print("\n--- Creando clientes de prueba ---")
    
    cliente1 = Cliente(
        nombre="Juan Pérez García",
        email="juan.perez@email.com",
        telefono="+56912345678",
        direccion="Av. Libertador 1234, Iquique"
    )
    
    cliente2 = Cliente(
        nombre="María González López",
        email="maria.gonzalez@empresa.cl",
        telefono="+56987654321",
        direccion="Calle Principal 567, Valparaíso"
    )
    
    cliente3 = Cliente(
        nombre="Carlos Rodríguez Soto",
        email="carlos.rodriguez@corporativo.com",
        telefono="+56956781234",
        direccion="Paseo Ahumada 890, Santiago"
    )
    
    print("✓ Tres instancias de Cliente creadas exitosamente.")
    
    # Agregar clientes al gestor
    print("\n--- Agregando clientes al gestor ---")
    gestor.agregar_cliente(cliente1)
    gestor.agregar_cliente(cliente2)
    gestor.agregar_cliente(cliente3)
    
    # Listar todos los clientes
    print("\n--- Listando todos los clientes ---")
    gestor.listar_clientes()
    
    # Mostrar información detallada de cada cliente
    print("\n--- Información detallada de cada cliente ---")
    cliente1.mostrar_info()
    print()
    cliente2.mostrar_info()
    print()
    cliente3.mostrar_info()
    
    # Probar el método __str__()
    print("\n--- Probando representación en cadena (__str__) ---")
    print(f"Cliente 1: {cliente1}")
    print(f"Cliente 2: {cliente2}")
    print(f"Cliente 3: {cliente3}")
    
    # Mostrar total de clientes
    print(f"\n✓ Total de clientes registrados: {gestor.obtener_total_clientes()}")
    
    print("\n>>> PRUEBAS DEL PASO 1 FINALIZADAS EXITOSAMENTE <<<\n")
