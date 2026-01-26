"""
Tests del Paso 4 - Sistema GIC (Gestor Inteligente de Clientes)
================================================================

Este archivo contiene pruebas para validar la implementación de:
- HERENCIA: Subclases heredan correctamente de Cliente
- POLIMORFISMO: Métodos sobrescritos funcionan según el tipo
- Listas heterogéneas: GestorClientes maneja diferentes tipos

Conceptos probados según Lección-4.pdf:
1. Herencia con super().__init__()
2. Sobrescritura de métodos (override)
3. Polimorfismo en mostrar_info() y obtener_tipo()
4. Métodos específicos por tipo de cliente

Autor: Desarrollador Fullstack Python
Fecha: 26 de enero de 2026
Proyecto: Evaluación Módulo 4 - SolutionTech
Paso: 4 - Herencia y polimorfismo
"""

import unittest
import sys
import os

# Agregar el directorio padre al path para importar módulos
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modulos import (
    Cliente,
    ClienteRegular,
    ClientePremium,
    ClienteCorporativo,
    GestorClientes
)


class TestHerenciaCliente(unittest.TestCase):
    """
    Pruebas de HERENCIA: Verificar que las subclases heredan de Cliente.
    """
    
    def test_cliente_regular_es_instancia_de_cliente(self):
        """Verificar que ClienteRegular hereda de Cliente."""
        cliente = ClienteRegular("Juan", "juan@test.com", "123456789", "Dirección")
        self.assertIsInstance(cliente, Cliente)
        self.assertIsInstance(cliente, ClienteRegular)
    
    def test_cliente_premium_es_instancia_de_cliente(self):
        """Verificar que ClientePremium hereda de Cliente."""
        cliente = ClientePremium("María", "maria@test.com", "987654321", "Dirección", 100)
        self.assertIsInstance(cliente, Cliente)
        self.assertIsInstance(cliente, ClientePremium)
    
    def test_cliente_corporativo_es_instancia_de_cliente(self):
        """Verificar que ClienteCorporativo hereda de Cliente."""
        cliente = ClienteCorporativo(
            "Carlos", "carlos@test.com", "456789123", "Dirección",
            "Empresa S.A.", "12.345.678-9"
        )
        self.assertIsInstance(cliente, Cliente)
        self.assertIsInstance(cliente, ClienteCorporativo)
    
    def test_subclases_heredan_atributos_base(self):
        """Verificar que las subclases heredan los atributos de Cliente."""
        cliente_regular = ClienteRegular("Juan", "juan@test.com", "123", "Dir1")
        cliente_premium = ClientePremium("María", "maria@test.com", "456", "Dir2", 0)
        cliente_corp = ClienteCorporativo("Carlos", "carlos@test.com", "789", "Dir3", "Emp", "RUT")
        
        # Todos deben tener los atributos heredados
        for cliente in [cliente_regular, cliente_premium, cliente_corp]:
            self.assertTrue(hasattr(cliente, 'nombre'))
            self.assertTrue(hasattr(cliente, 'email'))
            self.assertTrue(hasattr(cliente, 'telefono'))
            self.assertTrue(hasattr(cliente, 'direccion'))


class TestPolimorfismoObtenerTipo(unittest.TestCase):
    """
    Pruebas de POLIMORFISMO: Método obtener_tipo() retorna tipo específico.
    """
    
    def test_obtener_tipo_regular(self):
        """Verificar que ClienteRegular retorna 'Regular'."""
        cliente = ClienteRegular("Juan", "juan@test.com", "123456789", "Dirección")
        self.assertEqual(cliente.obtener_tipo(), "Regular")
    
    def test_obtener_tipo_premium(self):
        """Verificar que ClientePremium retorna 'Premium'."""
        cliente = ClientePremium("María", "maria@test.com", "987654321", "Dirección", 0)
        self.assertEqual(cliente.obtener_tipo(), "Premium")
    
    def test_obtener_tipo_corporativo(self):
        """Verificar que ClienteCorporativo retorna 'Corporativo'."""
        cliente = ClienteCorporativo(
            "Carlos", "carlos@test.com", "456789123", "Dirección",
            "Empresa S.A.", "12.345.678-9"
        )
        self.assertEqual(cliente.obtener_tipo(), "Corporativo")
    
    def test_polimorfismo_en_lista(self):
        """Verificar polimorfismo: diferentes tipos en una lista."""
        clientes = [
            ClienteRegular("Juan", "juan@test.com", "123", "Dir1"),
            ClientePremium("María", "maria@test.com", "456", "Dir2", 100),
            ClienteCorporativo("Carlos", "carlos@test.com", "789", "Dir3", "Emp", "RUT")
        ]
        
        tipos = [c.obtener_tipo() for c in clientes]
        self.assertEqual(tipos, ["Regular", "Premium", "Corporativo"])


class TestPolimorfismoBeneficioExclusivo(unittest.TestCase):
    """
    Pruebas de POLIMORFISMO: Método beneficio_exclusivo() específico por tipo.
    """
    
    def test_beneficio_regular(self):
        """Verificar beneficio exclusivo de ClienteRegular."""
        cliente = ClienteRegular("Juan", "juan@test.com", "123456789", "Dirección")
        beneficio = cliente.beneficio_exclusivo()
        self.assertIsInstance(beneficio, str)
        self.assertIn("promociones", beneficio.lower())
    
    def test_beneficio_premium(self):
        """Verificar beneficio exclusivo de ClientePremium."""
        cliente = ClientePremium("María", "maria@test.com", "987654321", "Dirección", 500)
        beneficio = cliente.beneficio_exclusivo()
        self.assertIsInstance(beneficio, str)
        self.assertIn("15%", beneficio)
        self.assertIn("puntos", beneficio.lower())
    
    def test_beneficio_corporativo(self):
        """Verificar beneficio exclusivo de ClienteCorporativo."""
        cliente = ClienteCorporativo(
            "Carlos", "carlos@test.com", "456789123", "Dirección",
            "TechCorp S.A.", "76.543.210-K"
        )
        beneficio = cliente.beneficio_exclusivo()
        self.assertIsInstance(beneficio, str)
        self.assertIn("25%", beneficio)
        self.assertIn("TechCorp S.A.", beneficio)


class TestCalcularDescuento(unittest.TestCase):
    """
    Pruebas de POLIMORFISMO: Método calcular_descuento() específico por tipo.
    """
    
    def test_descuento_regular_cero(self):
        """Verificar que ClienteRegular tiene 0% de descuento."""
        cliente = ClienteRegular("Juan", "juan@test.com", "123456789", "Dirección")
        monto = 100000
        descuento = cliente.calcular_descuento(monto)
        self.assertEqual(descuento, 0.0)
    
    def test_descuento_premium_quince_porciento(self):
        """Verificar que ClientePremium tiene 15% de descuento."""
        cliente = ClientePremium("María", "maria@test.com", "987654321", "Dirección", 0)
        monto = 100000
        descuento = cliente.calcular_descuento(monto)
        self.assertEqual(descuento, 15000.0)
    
    def test_descuento_corporativo_veinticinco_porciento(self):
        """Verificar que ClienteCorporativo tiene 25% de descuento."""
        cliente = ClienteCorporativo(
            "Carlos", "carlos@test.com", "456789123", "Dirección",
            "Empresa S.A.", "12.345.678-9"
        )
        monto = 100000
        descuento = cliente.calcular_descuento(monto)
        self.assertEqual(descuento, 25000.0)
    
    def test_polimorfismo_descuentos_lista(self):
        """Verificar polimorfismo en cálculo de descuentos."""
        clientes = [
            ClienteRegular("Juan", "juan@test.com", "123", "Dir1"),
            ClientePremium("María", "maria@test.com", "456", "Dir2", 0),
            ClienteCorporativo("Carlos", "carlos@test.com", "789", "Dir3", "Emp", "RUT")
        ]
        
        monto = 100000
        descuentos = [c.calcular_descuento(monto) for c in clientes]
        self.assertEqual(descuentos, [0.0, 15000.0, 25000.0])


class TestAtributosEspecificos(unittest.TestCase):
    """
    Pruebas de atributos específicos de cada subclase.
    """
    
    def test_premium_puntos_iniciales(self):
        """Verificar puntos iniciales de ClientePremium."""
        cliente = ClientePremium("María", "maria@test.com", "123456789", "Dir", 1500)
        self.assertEqual(cliente.puntos_acumulados, 1500)
    
    def test_premium_agregar_puntos(self):
        """Verificar que se pueden agregar puntos a ClientePremium."""
        cliente = ClientePremium("María", "maria@test.com", "123456789", "Dir", 100)
        cliente.agregar_puntos(500)
        self.assertEqual(cliente.puntos_acumulados, 600)
    
    def test_premium_canjear_puntos_exitoso(self):
        """Verificar canje de puntos exitoso."""
        cliente = ClientePremium("María", "maria@test.com", "123456789", "Dir", 1000)
        resultado = cliente.canjear_puntos(300)
        self.assertTrue(resultado)
        self.assertEqual(cliente.puntos_acumulados, 700)
    
    def test_premium_canjear_puntos_insuficientes(self):
        """Verificar que no se pueden canjear más puntos de los disponibles."""
        cliente = ClientePremium("María", "maria@test.com", "123456789", "Dir", 100)
        resultado = cliente.canjear_puntos(500)
        self.assertFalse(resultado)
        self.assertEqual(cliente.puntos_acumulados, 100)
    
    def test_corporativo_datos_empresa(self):
        """Verificar datos de empresa en ClienteCorporativo."""
        cliente = ClienteCorporativo(
            "Carlos", "carlos@test.com", "456789123", "Dirección",
            "TechCorp S.A.", "76.543.210-K"
        )
        self.assertEqual(cliente.nombre_empresa, "TechCorp S.A.")
        self.assertEqual(cliente.rut_empresa, "76.543.210-K")
    
    def test_corporativo_generar_factura_info(self):
        """Verificar información de factura de ClienteCorporativo."""
        cliente = ClienteCorporativo(
            "Carlos", "carlos@test.com", "456789123", "Dirección",
            "TechCorp S.A.", "76.543.210-K"
        )
        factura = cliente.generar_factura_info()
        
        self.assertIsInstance(factura, dict)
        self.assertEqual(factura['nombre_empresa'], "TechCorp S.A.")
        self.assertEqual(factura['rut_empresa'], "76.543.210-K")
        self.assertEqual(factura['contacto'], "Carlos")
        self.assertEqual(factura['email'], "carlos@test.com")


class TestObtenerDatosPolimorfismo(unittest.TestCase):
    """
    Pruebas de POLIMORFISMO: Método obtener_datos() incluye datos específicos.
    """
    
    def test_obtener_datos_regular(self):
        """Verificar obtener_datos incluye tipo para Regular."""
        cliente = ClienteRegular("Juan", "juan@test.com", "123456789", "Dirección")
        datos = cliente.obtener_datos()
        
        self.assertEqual(datos['tipo'], "Regular")
        self.assertEqual(datos['descuento'], 0.0)
    
    def test_obtener_datos_premium(self):
        """Verificar obtener_datos incluye puntos para Premium."""
        cliente = ClientePremium("María", "maria@test.com", "987654321", "Dirección", 750)
        datos = cliente.obtener_datos()
        
        self.assertEqual(datos['tipo'], "Premium")
        self.assertEqual(datos['descuento'], 0.15)
        self.assertEqual(datos['puntos_acumulados'], 750)
    
    def test_obtener_datos_corporativo(self):
        """Verificar obtener_datos incluye empresa para Corporativo."""
        cliente = ClienteCorporativo(
            "Carlos", "carlos@test.com", "456789123", "Dirección",
            "TechCorp S.A.", "76.543.210-K"
        )
        datos = cliente.obtener_datos()
        
        self.assertEqual(datos['tipo'], "Corporativo")
        self.assertEqual(datos['descuento'], 0.25)
        self.assertEqual(datos['nombre_empresa'], "TechCorp S.A.")
        self.assertEqual(datos['rut_empresa'], "76.543.210-K")


class TestGestorClientesHeterogeneo(unittest.TestCase):
    """
    Pruebas de GestorClientes con listas heterogéneas.
    """
    
    def setUp(self):
        """Configurar gestor con clientes de diferentes tipos."""
        self.gestor = GestorClientes()
        
        # Agregar clientes de diferentes tipos
        self.gestor.agregar_cliente(
            ClienteRegular("Juan Regular", "juan@test.com", "111", "Dir1")
        )
        self.gestor.agregar_cliente(
            ClienteRegular("Ana Regular", "ana@test.com", "222", "Dir2")
        )
        self.gestor.agregar_cliente(
            ClientePremium("María Premium", "maria@test.com", "333", "Dir3", 500)
        )
        self.gestor.agregar_cliente(
            ClienteCorporativo("Carlos Corp", "carlos@test.com", "444", "Dir4", "Emp", "RUT")
        )
    
    def test_total_clientes_heterogeneos(self):
        """Verificar total de clientes en lista heterogénea."""
        self.assertEqual(self.gestor.total_clientes, 4)
    
    def test_obtener_clientes_por_tipo_regular(self):
        """Verificar filtrado de clientes Regular."""
        regulares = self.gestor.obtener_clientes_por_tipo("Regular")
        self.assertEqual(len(regulares), 2)
        for c in regulares:
            self.assertEqual(c.obtener_tipo(), "Regular")
    
    def test_obtener_clientes_por_tipo_premium(self):
        """Verificar filtrado de clientes Premium."""
        premium = self.gestor.obtener_clientes_por_tipo("Premium")
        self.assertEqual(len(premium), 1)
        self.assertEqual(premium[0].obtener_tipo(), "Premium")
    
    def test_obtener_clientes_por_tipo_corporativo(self):
        """Verificar filtrado de clientes Corporativo."""
        corporativos = self.gestor.obtener_clientes_por_tipo("Corporativo")
        self.assertEqual(len(corporativos), 1)
        self.assertEqual(corporativos[0].obtener_tipo(), "Corporativo")
    
    def test_obtener_clientes_tipo_inexistente(self):
        """Verificar filtrado con tipo inexistente retorna lista vacía."""
        resultado = self.gestor.obtener_clientes_por_tipo("Inexistente")
        self.assertEqual(resultado, [])
    
    def test_buscar_cliente_heterogeneo(self):
        """Verificar búsqueda funciona con diferentes tipos."""
        cliente = self.gestor.buscar_cliente("maria@test.com")
        self.assertIsNotNone(cliente)
        assert cliente is not None  # Para que Pylance reconozca que no es None
        self.assertIsInstance(cliente, ClientePremium)
        self.assertEqual(cliente.obtener_tipo(), "Premium")
    
    def test_eliminar_cliente_heterogeneo(self):
        """Verificar eliminación funciona con lista heterogénea."""
        resultado = self.gestor.eliminar_cliente("carlos@test.com")
        self.assertTrue(resultado)
        self.assertEqual(self.gestor.total_clientes, 3)
        
        # Verificar que ya no hay corporativos
        corporativos = self.gestor.obtener_clientes_por_tipo("Corporativo")
        self.assertEqual(len(corporativos), 0)


class TestRepresentacionCadena(unittest.TestCase):
    """
    Pruebas de __str__ y __repr__ para cada tipo de cliente.
    """
    
    def test_str_regular(self):
        """Verificar representación string de ClienteRegular."""
        cliente = ClienteRegular("Juan", "juan@test.com", "123456789", "Dirección")
        str_cliente = str(cliente)
        self.assertIn("Regular", str_cliente)
        self.assertIn("Juan", str_cliente)
    
    def test_str_premium(self):
        """Verificar representación string de ClientePremium."""
        cliente = ClientePremium("María", "maria@test.com", "987654321", "Dirección", 500)
        str_cliente = str(cliente)
        self.assertIn("Premium", str_cliente)
        self.assertIn("María", str_cliente)
        self.assertIn("pts", str_cliente)
    
    def test_str_corporativo(self):
        """Verificar representación string de ClienteCorporativo."""
        cliente = ClienteCorporativo(
            "Carlos", "carlos@test.com", "456789123", "Dirección",
            "TechCorp S.A.", "76.543.210-K"
        )
        str_cliente = str(cliente)
        self.assertIn("Corporativo", str_cliente)
        self.assertIn("TechCorp S.A.", str_cliente)
    
    def test_repr_contiene_clase(self):
        """Verificar que __repr__ contiene el nombre de la clase."""
        clientes = [
            ClienteRegular("Juan", "juan@test.com", "123", "Dir"),
            ClientePremium("María", "maria@test.com", "456", "Dir", 0),
            ClienteCorporativo("Carlos", "carlos@test.com", "789", "Dir", "Emp", "RUT")
        ]
        
        for cliente in clientes:
            repr_cliente = repr(cliente)
            self.assertIn(type(cliente).__name__, repr_cliente)


class TestConstantesTipoCliente(unittest.TestCase):
    """
    Pruebas de constantes de clase TIPO_CLIENTE.
    """
    
    def test_constante_tipo_regular(self):
        """Verificar constante TIPO_CLIENTE en ClienteRegular."""
        self.assertEqual(ClienteRegular.TIPO_CLIENTE, "Regular")
    
    def test_constante_tipo_premium(self):
        """Verificar constante TIPO_CLIENTE en ClientePremium."""
        self.assertEqual(ClientePremium.TIPO_CLIENTE, "Premium")
    
    def test_constante_tipo_corporativo(self):
        """Verificar constante TIPO_CLIENTE en ClienteCorporativo."""
        self.assertEqual(ClienteCorporativo.TIPO_CLIENTE, "Corporativo")


# ==================== EJECUCIÓN DE TESTS ====================

if __name__ == "__main__":
    print("=" * 70)
    print(" " * 15 + "TESTS PASO 4: HERENCIA Y POLIMORFISMO")
    print(" " * 20 + "Sistema GIC - SolutionTech")
    print("=" * 70)
    
    # Ejecutar tests con verbosidad
    unittest.main(verbosity=2)
