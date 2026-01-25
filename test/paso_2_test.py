"""
Test del Paso 2 - Programación Orientada a Objetos en Python
=============================================================

Este módulo contiene pruebas para validar:
- Clase Cliente con encapsulamiento (@property)
- Clase GestorClientes con operaciones CRUD completas
"""

import sys
import os

# Agrega el directorio padre al path para importar módulos
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modulos.cliente import Cliente
from modulos.gestor_clientes import GestorClientes


def separador(titulo):
    """Imprime un separador con título para organizar las pruebas."""
    print("\n" + "=" * 60)
    print(f"  {titulo}")
    print("=" * 60)


def test_cliente_creacion():
    """Prueba la creación de instancias de Cliente."""
    separador("TEST: Creación de Cliente")
    
    cliente = Cliente(
        nombre="Ana María Torres",
        email="ana.torres@test.com",
        telefono="+56911111111",
        direccion="Calle Test 123, Santiago"
    )
    
    print(f"✓ Cliente creado: {cliente}")
    print(f"✓ Tipo de objeto: {type(cliente).__name__}")
    
    assert cliente is not None, "Error: Cliente no fue creado"
    print("\nTest de creación de Cliente: PASADO")


def test_cliente_properties_getters():
    """Prueba los getters (@property) de la clase Cliente."""
    separador("TEST: Getters de Cliente (@property)")
    
    cliente = Cliente(
        nombre="Pedro Sánchez",
        email="pedro.sanchez@test.com",
        telefono="+56922222222",
        direccion="Av. Principal 456, Valparaíso"
    )
    
    # Probar getters
    print(f"  nombre:    {cliente.nombre}")
    print(f"  email:     {cliente.email}")
    print(f"  telefono:  {cliente.telefono}")
    print(f"  direccion: {cliente.direccion}")
    
    assert cliente.nombre == "Pedro Sánchez", "Error en getter nombre"
    assert cliente.email == "pedro.sanchez@test.com", "Error en getter email"
    assert cliente.telefono == "+56922222222", "Error en getter telefono"
    assert cliente.direccion == "Av. Principal 456, Valparaíso", "Error en getter direccion"
    
    print("\nTest de Getters: PASADO")


def test_cliente_properties_setters():
    """Prueba los setters de la clase Cliente."""
    separador("TEST: Setters de Cliente")
    
    cliente = Cliente(
        nombre="Usuario Original",
        email="original@test.com",
        telefono="+56900000000",
        direccion="Dirección Original"
    )
    
    print("  Valores originales:")
    print(f"    nombre: {cliente.nombre}")
    print(f"    telefono: {cliente.telefono}")
    
    # Modificar valores usando setters
    cliente.nombre = "Usuario Modificado"
    cliente.telefono = "+56999999999"
    cliente.direccion = "Nueva Dirección 789"
    
    print("\n  Valores después de modificar:")
    print(f"    nombre: {cliente.nombre}")
    print(f"    telefono: {cliente.telefono}")
    print(f"    direccion: {cliente.direccion}")
    
    assert cliente.nombre == "Usuario Modificado", "Error en setter nombre"
    assert cliente.telefono == "+56999999999", "Error en setter telefono"
    assert cliente.direccion == "Nueva Dirección 789", "Error en setter direccion"
    
    print("\nTest de Setters: PASADO")


def test_cliente_metodos():
    """Prueba los métodos de la clase Cliente."""
    separador("TEST: Métodos de Cliente")
    
    cliente = Cliente(
        nombre="Laura Méndez",
        email="laura.mendez@test.com",
        telefono="+56933333333",
        direccion="Pasaje Test 321"
    )
    
    # Probar __str__
    print(f"  __str__(): {str(cliente)}")
    
    # Probar __repr__
    print(f"  __repr__(): {repr(cliente)}")
    
    # Probar mostrar_info()
    print("\n  mostrar_info():")
    cliente.mostrar_info()
    
    # Probar obtener_datos()
    datos = cliente.obtener_datos()
    print(f"\n  obtener_datos(): {datos}")
    
    assert isinstance(datos, dict), "Error: obtener_datos() debe retornar dict"
    assert datos['nombre'] == "Laura Méndez", "Error en obtener_datos()"
    assert datos['email'] == "laura.mendez@test.com", "Error en obtener_datos()"
    
    print("\nTest de Métodos de Cliente: PASADO")


def test_gestor_creacion():
    """Prueba la creación del GestorClientes."""
    separador("TEST: Creación de GestorClientes")
    
    gestor = GestorClientes()
    
    print(f"  Gestor creado: {type(gestor).__name__}")
    print(f"  Total clientes inicial: {gestor.total_clientes}")
    
    assert gestor.total_clientes == 0, "Error: Gestor debe iniciar vacío"
    
    print("\nTest de creación de GestorClientes: PASADO")


def test_gestor_agregar_cliente():
    """Prueba el método agregar_cliente() - CREATE."""
    separador("TEST: CRUD - CREATE (agregar_cliente)")
    
    gestor = GestorClientes()
    
    cliente1 = Cliente("Cliente Uno", "uno@test.com", "+56911111111", "Dir 1")
    cliente2 = Cliente("Cliente Dos", "dos@test.com", "+56922222222", "Dir 2")
    
    # Agregar clientes
    resultado1 = gestor.agregar_cliente(cliente1)
    resultado2 = gestor.agregar_cliente(cliente2)
    
    print(f"  Total clientes después de agregar 2: {gestor.total_clientes}")
    
    assert resultado1 == True, "Error: No se pudo agregar cliente1"
    assert resultado2 == True, "Error: No se pudo agregar cliente2"
    assert gestor.total_clientes == 2, "Error: Deben haber 2 clientes"
    
    # Probar duplicado
    print("\n  Intentando agregar cliente duplicado (mismo email)...")
    cliente_duplicado = Cliente("Duplicado", "uno@test.com", "+56900000000", "Dir X")
    resultado_dup = gestor.agregar_cliente(cliente_duplicado)
    
    assert resultado_dup == False, "Error: No debería permitir duplicados"
    assert gestor.total_clientes == 2, "Error: No debe aumentar con duplicados"
    
    print("\nTest CREATE (agregar_cliente): PASADO")


def test_gestor_listar_clientes():
    """Prueba el método listar_clientes() - READ."""
    separador("TEST: CRUD - READ (listar_clientes)")
    
    gestor = GestorClientes()
    
    # Listar vacío
    print("Listando gestor vacío:")
    gestor.listar_clientes()
    
    # Agregar clientes
    gestor.agregar_cliente(Cliente("Ana Test", "ana@test.com", "+56911111111", "Dir A"))
    gestor.agregar_cliente(Cliente("Beto Test", "beto@test.com", "+56922222222", "Dir B"))
    gestor.agregar_cliente(Cliente("Carla Test", "carla@test.com", "+56933333333", "Dir C"))
    
    # Listar con clientes
    print("\n  Listando con 3 clientes:")
    gestor.listar_clientes()
    
    print("\nTest READ (listar_clientes): PASADO")


def test_gestor_buscar_cliente():
    """Prueba el método buscar_cliente() - READ."""
    separador("TEST: CRUD - READ (buscar_cliente)")
    
    gestor = GestorClientes()
    gestor.agregar_cliente(Cliente("Diego Test", "diego@test.com", "+56944444444", "Dir D"))
    
    # Buscar cliente existente
    print("  Buscando cliente existente (diego@test.com)...")
    cliente_encontrado = gestor.buscar_cliente("diego@test.com")
    
    if cliente_encontrado:
        print(f"  ✓ Encontrado: {cliente_encontrado}")
    
    assert cliente_encontrado is not None, "Error: Debería encontrar al cliente"
    assert cliente_encontrado.nombre == "Diego Test", "Error: Nombre incorrecto"
    
    # Buscar cliente inexistente
    print("\n  Buscando cliente inexistente (noexiste@test.com)...")
    cliente_no_existe = gestor.buscar_cliente("noexiste@test.com")
    
    assert cliente_no_existe is None, "Error: No debería encontrar cliente"
    print("  ✓ Retornó None correctamente")
    
    # Probar búsqueda case-insensitive
    print("\n  Probando búsqueda case-insensitive (DIEGO@TEST.COM)...")
    cliente_mayus = gestor.buscar_cliente("DIEGO@TEST.COM")
    assert cliente_mayus is not None, "Error: Búsqueda debería ser case-insensitive"
    print("  ✓ Búsqueda case-insensitive funciona")
    
    print("\nTest READ (buscar_cliente): PASADO")


def test_gestor_actualizar_cliente():
    """Prueba el método actualizar_cliente() - UPDATE."""
    separador("TEST: CRUD - UPDATE (actualizar_cliente)")
    
    gestor = GestorClientes()
    gestor.agregar_cliente(Cliente("Elena Original", "elena@test.com", "+56955555555", "Dir Original"))
    
    print("  Datos originales:")
    gestor.mostrar_cliente("elena@test.com")
    
    # Actualizar parcialmente
    print("\n  Actualizando nombre y teléfono...")
    resultado = gestor.actualizar_cliente(
        email="elena@test.com",
        nombre="Elena Modificada",
        telefono="+56900000000"
    )
    
    print("\n  Datos después de actualizar:")
    cliente = gestor.buscar_cliente("elena@test.com")
    
    # Verificar que el cliente existe antes de acceder a sus atributos
    assert cliente is not None, "Error: Cliente debería existir"
    
    cliente.mostrar_info()
    
    assert resultado == True, "Error: Actualización debería ser exitosa"
    assert cliente.nombre == "Elena Modificada", "Error: Nombre no actualizado"
    assert cliente.telefono == "+56900000000", "Error: Teléfono no actualizado"
    assert cliente.direccion == "Dir Original", "Error: Dirección no debería cambiar"
    
    # Intentar actualizar cliente inexistente
    print("\n  Intentando actualizar cliente inexistente...")
    resultado_no_existe = gestor.actualizar_cliente("noexiste@test.com", nombre="X")
    assert resultado_no_existe == False, "Error: Debería retornar False"
    
    print("\nTest UPDATE (actualizar_cliente): PASADO")


def test_gestor_eliminar_cliente():
    """Prueba el método eliminar_cliente() - DELETE."""
    separador("TEST: CRUD - DELETE (eliminar_cliente)")
    
    gestor = GestorClientes()
    gestor.agregar_cliente(Cliente("Fernando Delete", "fernando@test.com", "+56966666666", "Dir F"))
    gestor.agregar_cliente(Cliente("Gabriela Keep", "gabriela@test.com", "+56977777777", "Dir G"))
    
    print(f"  Total antes de eliminar: {gestor.total_clientes}")
    
    # Eliminar cliente existente
    print("\n  Eliminando fernando@test.com...")
    resultado = gestor.eliminar_cliente("fernando@test.com")
    
    print(f"  Total después de eliminar: {gestor.total_clientes}")
    
    assert resultado == True, "Error: Eliminación debería ser exitosa"
    assert gestor.total_clientes == 1, "Error: Debería quedar 1 cliente"
    assert gestor.buscar_cliente("fernando@test.com") is None, "Error: Cliente debería estar eliminado"
    
    # Intentar eliminar cliente inexistente
    print("\n  Intentando eliminar cliente inexistente...")
    resultado_no_existe = gestor.eliminar_cliente("noexiste@test.com")
    assert resultado_no_existe == False, "Error: Debería retornar False"
    
    print("\nTest DELETE (eliminar_cliente): PASADO")


def test_gestor_propiedades():
    """Prueba las propiedades del GestorClientes."""
    separador("TEST: Propiedades de GestorClientes")
    
    gestor = GestorClientes()
    gestor.agregar_cliente(Cliente("Test 1", "t1@test.com", "+56911111111", "Dir 1"))
    gestor.agregar_cliente(Cliente("Test 2", "t2@test.com", "+56922222222", "Dir 2"))
    
    # Probar property clientes (copia de la lista)
    print(f"  total_clientes: {gestor.total_clientes}")
    print(f"  Cantidad en propiedad clientes: {len(gestor.clientes)}")
    
    # Verificar que retorna copia (no la lista original)
    lista_clientes = gestor.clientes
    lista_clientes.clear()  # Limpiar la copia
    
    print(f"  Total después de limpiar copia: {gestor.total_clientes}")
    
    assert gestor.total_clientes == 2, "Error: Property debe retornar copia, no referencia"
    
    print("\nTest de Propiedades: PASADO")


def ejecutar_todos_los_tests():
    """Ejecuta todas las pruebas del Paso 2."""
    print("\n" + "=" * 60)
    print(" " * 15 + "TESTS DEL PASO 2" + " " * 17)
    print(" " * 10 + "Programación Orientada a Objetos" + " " * 8)
    print("=" * 60)
    
    tests = [
        ("Creación de Cliente", test_cliente_creacion),
        ("Getters de Cliente", test_cliente_properties_getters),
        ("Setters de Cliente", test_cliente_properties_setters),
        ("Métodos de Cliente", test_cliente_metodos),
        ("Creación de GestorClientes", test_gestor_creacion),
        ("CRUD - CREATE", test_gestor_agregar_cliente),
        ("CRUD - READ (listar)", test_gestor_listar_clientes),
        ("CRUD - READ (buscar)", test_gestor_buscar_cliente),
        ("CRUD - UPDATE", test_gestor_actualizar_cliente),
        ("CRUD - DELETE", test_gestor_eliminar_cliente),
        ("Propiedades GestorClientes", test_gestor_propiedades),
    ]
    
    tests_pasados = 0
    tests_fallidos = 0
    
    for nombre, test_func in tests:
        try:
            test_func()
            tests_pasados += 1
        except AssertionError as e:
            print(f"\nTest '{nombre}' FALLIDO: {e}")
            tests_fallidos += 1
        except Exception as e:
            print(f"\nTest '{nombre}' ERROR: {e}")
            tests_fallidos += 1
    
    # Resumen final
    print("\n" + "=" * 60)
    print("#" + " " * 18 + "RESUMEN FINAL" + " " * 19 + "#")
    print("=" * 60)
    print(f"\n  Tests ejecutados: {len(tests)}")
    print(f"  Pasados: {tests_pasados}")
    print(f"  Fallidos: {tests_fallidos}")
    
    if tests_fallidos == 0:
        print("\n  ¡TODOS LOS TESTS PASARON EXITOSAMENTE!")
    else:
        print(f"\n  {tests_fallidos} test(s) requieren atención.")
    
    print("\n" + "=" * 60 + "\n")


# Punto de entrada
if __name__ == "__main__":
    ejecutar_todos_los_tests()
