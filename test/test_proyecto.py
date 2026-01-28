"""
========================================
Suite de Tests Completa - Sistema GIC
========================================
Ejecutar con: 
    python -m pytest test/test_proyecto.py -v
O con unittest: 
    python -m unittest test.test_proyecto -v

Para ejecutar con información de cobertura:
    pytest test/test_proyecto.py -v --tb=short

Los tests están organizados por módulo y funcionalidad:
    1. Tests de Excepciones Personalizadas
    2. Tests de Validaciones
    3. Tests de la Clase Cliente (Base)
    4. Tests de ClienteRegular
    5. Tests de ClientePremium
    6. Tests de ClienteCorporativo
    7. Tests del GestorClientes (CRUD)
    8. Tests de Archivos (CSV, Reportes, Logs)
    9. Tests de Integración
"""

import unittest
import os
import sys
import csv
import tempfile
import shutil
from io import StringIO
from unittest.mock import patch, MagicMock

# Asegurar que el módulo principal está en el path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importar módulos del sistema
from modulos.cliente import Cliente
from modulos.cliente_regular import ClienteRegular
from modulos.cliente_premium import ClientePremium
from modulos.cliente_corporativo import ClienteCorporativo
from modulos.gestor_clientes import GestorClientes
from modulos.excepciones import (
    GICError,
    ValidacionError,
    EmailInvalidoError,
    TelefonoInvalidoError,
    NombreInvalidoError,
    DireccionInvalidaError,
    RutInvalidoError,
    PuntosInvalidosError,
    ClienteError,
    ClienteExistenteError,
    ClienteNoEncontradoError,
    ListaVaciaError,
    ArchivoError,
    ArchivoNoEncontradoError,
    PermisoArchivoError,
    FormatoArchivoError
)
from modulos.validaciones import (
    validar_email,
    validar_telefono,
    validar_nombre,
    validar_direccion,
    validar_rut,
    validar_puntos,
    validar_datos_cliente,
    validar_datos_corporativo
)
from modulos.archivos import (
    exportar_clientes_csv,
    importar_clientes_csv,
    generar_reporte,
    registrar_log,
    registrar_alta_cliente,
    registrar_baja_cliente,
    registrar_modificacion_cliente,
    registrar_error,
    leer_log,
    crear_directorios,
    crear_cliente_desde_fila
)


# ============================================================================
# SECCIÓN 1: TESTS DE EXCEPCIONES PERSONALIZADAS
# ============================================================================
class TestExcepciones(unittest.TestCase):
    """Tests para verificar el correcto funcionamiento de las excepciones personalizadas."""
    
    def test_gic_error_base(self):
        """Verifica que GICError funciona correctamente como clase base."""
        error = GICError("Error de prueba", "TEST001")
        self.assertEqual(error.mensaje, "Error de prueba")
        self.assertEqual(error.codigo, "TEST001")
        self.assertEqual(str(error), "[TEST001] Error de prueba")
    
    def test_gic_error_valores_default(self):
        """Verifica valores por defecto de GICError."""
        error = GICError()
        self.assertEqual(error.mensaje, "Error en el sistema GIC")
        self.assertEqual(error.codigo, "GIC000")
    
    def test_validacion_error(self):
        """Verifica que ValidacionError hereda correctamente de GICError."""
        error = ValidacionError("Error de validación")
        self.assertIsInstance(error, GICError)
        self.assertEqual(error.codigo, "VAL000")
    
    def test_email_invalido_error(self):
        """Verifica EmailInvalidoError con email inválido."""
        error = EmailInvalidoError("correo_invalido")
        self.assertEqual(error.email, "correo_invalido")
        self.assertEqual(error.codigo, "VAL001")
        self.assertIn("correo_invalido", str(error))
    
    def test_telefono_invalido_error(self):
        """Verifica TelefonoInvalidoError."""
        error = TelefonoInvalidoError("123")
        self.assertEqual(error.telefono, "123")
        self.assertEqual(error.codigo, "VAL002")
    
    def test_nombre_invalido_error(self):
        """Verifica NombreInvalidoError."""
        error = NombreInvalidoError("X")
        self.assertEqual(error.nombre, "X")
        self.assertEqual(error.codigo, "VAL003")
    
    def test_direccion_invalida_error(self):
        """Verifica DireccionInvalidaError."""
        error = DireccionInvalidaError("Dir")
        self.assertEqual(error.direccion, "Dir")
        self.assertEqual(error.codigo, "VAL004")
    
    def test_rut_invalido_error(self):
        """Verifica RutInvalidoError."""
        error = RutInvalidoError("12345")
        self.assertEqual(error.rut, "12345")
        self.assertEqual(error.codigo, "VAL005")
    
    def test_puntos_invalidos_error_canjear(self):
        """Verifica PuntosInvalidosError para operación canjear."""
        error = PuntosInvalidosError(100, 50, "canjear")
        self.assertEqual(error.puntos, 100)
        self.assertEqual(error.disponibles, 50)
        self.assertIn("canjear", str(error))
    
    def test_puntos_invalidos_error_agregar(self):
        """Verifica PuntosInvalidosError para operación agregar."""
        error = PuntosInvalidosError(-10, 0, "agregar")
        self.assertIn("agregar", str(error).lower())
    
    def test_cliente_existente_error(self):
        """Verifica ClienteExistenteError."""
        error = ClienteExistenteError("test@test.com")
        self.assertEqual(error.email, "test@test.com")
        self.assertEqual(error.codigo, "CLI001")
    
    def test_cliente_no_encontrado_error(self):
        """Verifica ClienteNoEncontradoError."""
        error = ClienteNoEncontradoError("noexiste@test.com")
        self.assertEqual(error.email, "noexiste@test.com")
        self.assertEqual(error.codigo, "CLI002")
    
    def test_lista_vacia_error(self):
        """Verifica ListaVaciaError."""
        error = ListaVaciaError()
        self.assertEqual(error.codigo, "CLI003")
    
    def test_archivo_no_encontrado_error(self):
        """Verifica ArchivoNoEncontradoError."""
        error = ArchivoNoEncontradoError("/ruta/archivo.csv")
        self.assertEqual(error.ruta, "/ruta/archivo.csv")
        self.assertEqual(error.codigo, "ARC001")
    
    def test_permiso_archivo_error(self):
        """Verifica PermisoArchivoError."""
        error = PermisoArchivoError("/ruta/archivo.csv", "escritura")
        self.assertEqual(error.ruta, "/ruta/archivo.csv")
        self.assertEqual(error.operacion, "escritura")
        self.assertEqual(error.codigo, "ARC002")
    
    def test_formato_archivo_error(self):
        """Verifica FormatoArchivoError."""
        error = FormatoArchivoError("/ruta/archivo.csv", "Columnas faltantes")
        self.assertEqual(error.ruta, "/ruta/archivo.csv")
        self.assertIn("Columnas faltantes", error.detalle)


# ============================================================================
# SECCIÓN 2: TESTS DE VALIDACIONES
# ============================================================================
class TestValidaciones(unittest.TestCase):
    """Tests para el módulo de validaciones."""
    
    # --- Tests de validación de Email ---
    def test_email_valido(self):
        """Verifica que emails válidos pasen la validación."""
        emails_validos = [
            "usuario@dominio.com",
            "nombre.apellido@empresa.cl",
            "test123@mail.org",
            "user_name@domain.co.uk",
            "mi-correo@test.net"
        ]
        for email in emails_validos:
            with self.subTest(email=email):
                self.assertTrue(validar_email(email))
    
    def test_email_invalido_sin_arroba(self):
        """Verifica que email sin @ lance excepción."""
        with self.assertRaises(EmailInvalidoError):
            validar_email("correosinArroba.com")
    
    def test_email_invalido_sin_dominio(self):
        """Verifica que email sin dominio lance excepción."""
        with self.assertRaises(EmailInvalidoError):
            validar_email("correo@")
    
    def test_email_invalido_vacio(self):
        """Verifica que email vacío lance excepción."""
        with self.assertRaises(EmailInvalidoError):
            validar_email("")
    
    def test_email_invalido_none(self):
        """Verifica que email None lance excepción."""
        with self.assertRaises(EmailInvalidoError):
            validar_email(None)
    
    def test_email_invalido_formato_incorrecto(self):
        """Verifica emails con formato incorrecto."""
        emails_invalidos = [
            "correo@dominio",
            "@dominio.com",
            "correo@.com",
            "correo correo@mail.com",
            "correo@@mail.com"
        ]
        for email in emails_invalidos:
            with self.subTest(email=email):
                with self.assertRaises(EmailInvalidoError):
                    validar_email(email)
    
    # --- Tests de validación de Teléfono ---
    def test_telefono_valido(self):
        """Verifica que teléfonos válidos pasen la validación."""
        telefonos_validos = [
            "912345678",
            "+56912345678",
            "(09) 1234-5678",
            "56 9 1234 5678",
            "123456789012"
        ]
        for telefono in telefonos_validos:
            with self.subTest(telefono=telefono):
                self.assertTrue(validar_telefono(telefono))
    
    def test_telefono_invalido_muy_corto(self):
        """Verifica que teléfono muy corto lance excepción."""
        with self.assertRaises(TelefonoInvalidoError):
            validar_telefono("123")
    
    def test_telefono_invalido_vacio(self):
        """Verifica que teléfono vacío lance excepción."""
        with self.assertRaises(TelefonoInvalidoError):
            validar_telefono("")
    
    def test_telefono_invalido_none(self):
        """Verifica que teléfono None lance excepción."""
        with self.assertRaises(TelefonoInvalidoError):
            validar_telefono(None)
    
    def test_telefono_invalido_letras(self):
        """Verifica que teléfono con letras lance excepción."""
        with self.assertRaises(TelefonoInvalidoError):
            validar_telefono("abc12345")
    
    # --- Tests de validación de Nombre ---
    def test_nombre_valido(self):
        """Verifica que nombres válidos pasen la validación."""
        nombres_validos = [
            "Juan Pérez",
            "María José",
            "Ana-María",
            "José Luis García",
            "Ñoño Muñoz"
        ]
        for nombre in nombres_validos:
            with self.subTest(nombre=nombre):
                self.assertTrue(validar_nombre(nombre))
    
    def test_nombre_invalido_muy_corto(self):
        """Verifica que nombre muy corto lance excepción."""
        with self.assertRaises(NombreInvalidoError):
            validar_nombre("J")
    
    def test_nombre_invalido_vacio(self):
        """Verifica que nombre vacío lance excepción."""
        with self.assertRaises(NombreInvalidoError):
            validar_nombre("")
    
    def test_nombre_invalido_numeros(self):
        """Verifica que nombre solo con números lance excepción."""
        with self.assertRaises(NombreInvalidoError):
            validar_nombre("12345")
    
    def test_nombre_invalido_none(self):
        """Verifica que nombre None lance excepción."""
        with self.assertRaises(NombreInvalidoError):
            validar_nombre(None)
    
    # --- Tests de validación de Dirección ---
    def test_direccion_valida(self):
        """Verifica que direcciones válidas pasen la validación."""
        direcciones_validas = [
            "Av. Principal 123",
            "Calle Los Aromos #456",
            "Pasaje Norte 789, Depto 5",
            "Av. Libertador Bernardo OHiggins 1234"  # Nota: Apóstrofe no permitido por PATRON_DIRECCION
        ]
        for direccion in direcciones_validas:
            with self.subTest(direccion=direccion):
                self.assertTrue(validar_direccion(direccion))
    
    def test_direccion_con_apostrofe_falla(self):
        """
        NOTA: Este test documenta un posible bug/limitación.
        El patrón PATRON_DIRECCION no permite apóstrofes, lo cual puede ser problemático
        para direcciones como "O'Higgins". Considerar agregar ' al patrón si es necesario.
        Patrón actual en validaciones.py usa caracteres alfanuméricos y algunos símbolos.
        """
        with self.assertRaises(DireccionInvalidaError):
            validar_direccion("Av. Libertador Bernardo O'Higgins 1234")
    
    def test_direccion_invalida_muy_corta(self):
        """Verifica que dirección muy corta lance excepción."""
        with self.assertRaises(DireccionInvalidaError):
            validar_direccion("Av")
    
    def test_direccion_invalida_vacia(self):
        """Verifica que dirección vacía lance excepción."""
        with self.assertRaises(DireccionInvalidaError):
            validar_direccion("")
    
    def test_direccion_invalida_none(self):
        """Verifica que dirección None lance excepción."""
        with self.assertRaises(DireccionInvalidaError):
            validar_direccion(None)
    
    # --- Tests de validación de RUT ---
    def test_rut_valido(self):
        """Verifica que RUTs válidos pasen la validación."""
        ruts_validos = [
            "12.345.678-9",
            "76.543.210-K",
            "12345678-9",
            "1.234.567-0"
        ]
        for rut in ruts_validos:
            with self.subTest(rut=rut):
                self.assertTrue(validar_rut(rut))
    
    def test_rut_invalido_formato_incorrecto(self):
        """Verifica que RUT con formato incorrecto lance excepción."""
        ruts_invalidos = [
            "12345678",
            "12.345.678",
            "12-345-678-9",
            "abc.def.ghi-j"
        ]
        for rut in ruts_invalidos:
            with self.subTest(rut=rut):
                with self.assertRaises(RutInvalidoError):
                    validar_rut(rut)
    
    def test_rut_invalido_vacio(self):
        """Verifica que RUT vacío lance excepción."""
        with self.assertRaises(RutInvalidoError):
            validar_rut("")
    
    # --- Tests de validación de Puntos ---
    def test_puntos_validos_agregar(self):
        """Verifica que puntos positivos para agregar pasen."""
        self.assertTrue(validar_puntos(100, "agregar"))
    
    def test_puntos_invalidos_agregar_negativos(self):
        """Verifica que puntos negativos para agregar lancen excepción."""
        with self.assertRaises(PuntosInvalidosError):
            validar_puntos(-10, "agregar")
    
    def test_puntos_invalidos_agregar_cero(self):
        """Verifica que cero puntos para agregar lancen excepción."""
        with self.assertRaises(PuntosInvalidosError):
            validar_puntos(0, "agregar")
    
    def test_puntos_validos_canjear(self):
        """Verifica que puntos válidos para canjear pasen."""
        self.assertTrue(validar_puntos(50, "canjear", 100))
    
    def test_puntos_invalidos_canjear_excede_disponibles(self):
        """Verifica que puntos que exceden disponibles lancen excepción."""
        with self.assertRaises(PuntosInvalidosError):
            validar_puntos(150, "canjear", 100)
    
    # --- Tests de validación completa de cliente ---
    def test_validar_datos_cliente_correctos(self):
        """Verifica validación completa de datos de cliente."""
        datos = validar_datos_cliente(
            "Juan Pérez",
            "juan@mail.com",
            "912345678",
            "Av. Principal 123"
        )
        self.assertEqual(datos['nombre'], "Juan Pérez")
        self.assertEqual(datos['email'], "juan@mail.com")
        self.assertEqual(datos['telefono'], "912345678")
        self.assertEqual(datos['direccion'], "Av. Principal 123")
    
    def test_validar_datos_cliente_email_normalizado(self):
        """Verifica que el email se normalice a minúsculas."""
        datos = validar_datos_cliente(
            "Test User",
            "TEST@MAIL.COM",
            "912345678",
            "Calle Test 123"
        )
        self.assertEqual(datos['email'], "test@mail.com")


# ============================================================================
# SECCIÓN 3: TESTS DE LA CLASE CLIENTE (BASE)
# ============================================================================
class TestCliente(unittest.TestCase):
    """Tests para la clase base Cliente."""
    
    def setUp(self):
        """Configuración inicial para cada test."""
        self.cliente = Cliente(
            "Juan Pérez",
            "juan@mail.com",
            "912345678",
            "Av. Principal 123"
        )
    
    def test_crear_cliente_exitoso(self):
        """Verifica que se puede crear un cliente con datos válidos."""
        self.assertEqual(self.cliente.nombre, "Juan Pérez")
        self.assertEqual(self.cliente.email, "juan@mail.com")
        self.assertEqual(self.cliente.telefono, "912345678")
        self.assertEqual(self.cliente.direccion, "Av. Principal 123")
    
    def test_cliente_email_normalizado(self):
        """Verifica que el email se guarda en minúsculas."""
        cliente = Cliente("Test", "TEST@MAIL.COM", "912345678", "Calle Test 123")
        self.assertEqual(cliente.email, "test@mail.com")
    
    def test_cliente_datos_con_espacios(self):
        """Verifica que se eliminan espacios extras."""
        cliente = Cliente("  Juan Pérez  ", "  juan@mail.com  ", "  912345678  ", "  Calle 123  ")
        self.assertEqual(cliente.nombre, "Juan Pérez")
        self.assertEqual(cliente.email, "juan@mail.com")
        self.assertEqual(cliente.telefono, "912345678")
        self.assertEqual(cliente.direccion, "Calle 123")
    
    def test_cliente_str(self):
        """Verifica la representación en cadena del cliente."""
        resultado = str(self.cliente)
        self.assertIn("Juan Pérez", resultado)
        self.assertIn("juan@mail.com", resultado)
    
    def test_cliente_obtener_tipo(self):
        """Verifica que obtener_tipo retorna 'Cliente'."""
        self.assertEqual(self.cliente.obtener_tipo(), "Cliente")
    
    def test_cliente_obtener_datos(self):
        """Verifica que obtener_datos retorna diccionario correcto."""
        datos = self.cliente.obtener_datos()
        self.assertEqual(datos['tipo'], "Cliente")
        self.assertEqual(datos['nombre'], "Juan Pérez")
        self.assertEqual(datos['email'], "juan@mail.com")
        self.assertEqual(datos['telefono'], "912345678")
        self.assertEqual(datos['direccion'], "Av. Principal 123")
    
    def test_cliente_setters(self):
        """Verifica que los setters funcionan correctamente."""
        self.cliente.nombre = "Pedro González"
        self.cliente.telefono = "987654321"
        self.cliente.direccion = "Nueva Dirección 456"
        
        self.assertEqual(self.cliente.nombre, "Pedro González")
        self.assertEqual(self.cliente.telefono, "987654321")
        self.assertEqual(self.cliente.direccion, "Nueva Dirección 456")
    
    def test_cliente_validacion_email_invalido(self):
        """Verifica que no se puede crear cliente con email inválido."""
        with self.assertRaises(EmailInvalidoError):
            Cliente("Test", "emailinvalido", "912345678", "Calle 123")
    
    def test_cliente_validacion_telefono_invalido(self):
        """Verifica que no se puede crear cliente con teléfono inválido."""
        with self.assertRaises(TelefonoInvalidoError):
            Cliente("Test", "test@mail.com", "123", "Calle 123")
    
    def test_cliente_validacion_nombre_invalido(self):
        """Verifica que no se puede crear cliente con nombre inválido."""
        with self.assertRaises(NombreInvalidoError):
            Cliente("X", "test@mail.com", "912345678", "Calle 123")
    
    def test_cliente_validacion_direccion_invalida(self):
        """Verifica que no se puede crear cliente con dirección inválida."""
        with self.assertRaises(DireccionInvalidaError):
            Cliente("Test", "test@mail.com", "912345678", "Dir")


# ============================================================================
# SECCIÓN 4: TESTS DE CLIENTE REGULAR
# ============================================================================
class TestClienteRegular(unittest.TestCase):
    """Tests para la clase ClienteRegular."""
    
    def setUp(self):
        """Configuración inicial para cada test."""
        self.cliente = ClienteRegular(
            "Ana García",
            "ana@mail.com",
            "912345678",
            "Calle Norte 789"
        )
    
    def test_crear_cliente_regular(self):
        """Verifica que se puede crear un cliente regular."""
        self.assertEqual(self.cliente.nombre, "Ana García")
        self.assertEqual(self.cliente.email, "ana@mail.com")
    
    def test_herencia_de_cliente(self):
        """Verifica que ClienteRegular hereda de Cliente."""
        self.assertIsInstance(self.cliente, Cliente)
    
    def test_obtener_tipo(self):
        """Verifica que obtener_tipo retorna 'Regular'."""
        self.assertEqual(self.cliente.obtener_tipo(), "Regular")
    
    def test_constante_tipo_cliente(self):
        """Verifica la constante TIPO_CLIENTE."""
        self.assertEqual(ClienteRegular.TIPO_CLIENTE, "Regular")
    
    def test_constante_descuento(self):
        """Verifica la constante DESCUENTO."""
        self.assertEqual(ClienteRegular.DESCUENTO, 0.0)
    
    def test_calcular_descuento_cero(self):
        """Verifica que calcular_descuento retorna 0 para cliente regular."""
        descuento = self.cliente.calcular_descuento(1000)
        self.assertEqual(descuento, 0.0)
    
    def test_calcular_descuento_sin_monto(self):
        """Verifica calcular_descuento sin argumento."""
        descuento = self.cliente.calcular_descuento()
        self.assertEqual(descuento, 0.0)
    
    def test_beneficio_exclusivo(self):
        """Verifica el método beneficio_exclusivo."""
        beneficio = self.cliente.beneficio_exclusivo()
        self.assertIsInstance(beneficio, str)
        self.assertTrue(len(beneficio) > 0)
    
    def test_str_incluye_tipo(self):
        """Verifica que __str__ incluye el tipo."""
        resultado = str(self.cliente)
        self.assertIn("[Regular]", resultado)
        self.assertIn("Ana García", resultado)
    
    def test_repr(self):
        """Verifica la representación __repr__."""
        resultado = repr(self.cliente)
        self.assertIn("ClienteRegular", resultado)
        self.assertIn("Ana García", resultado)
    
    def test_obtener_datos_incluye_descuento(self):
        """Verifica que obtener_datos incluye el descuento."""
        datos = self.cliente.obtener_datos()
        self.assertEqual(datos['tipo'], "Regular")
        self.assertEqual(datos['descuento'], 0.0)


# ============================================================================
# SECCIÓN 5: TESTS DE CLIENTE PREMIUM
# ============================================================================
class TestClientePremium(unittest.TestCase):
    """Tests para la clase ClientePremium."""
    
    def setUp(self):
        """Configuración inicial para cada test."""
        self.cliente = ClientePremium(
            "Carlos López",
            "carlos@mail.com",
            "912345678",
            "Av. Sur 456",
            100  # puntos iniciales
        )
    
    def test_crear_cliente_premium(self):
        """Verifica que se puede crear un cliente premium."""
        self.assertEqual(self.cliente.nombre, "Carlos López")
        self.assertEqual(self.cliente.email, "carlos@mail.com")
    
    def test_herencia_de_cliente(self):
        """Verifica que ClientePremium hereda de Cliente."""
        self.assertIsInstance(self.cliente, Cliente)
    
    def test_obtener_tipo(self):
        """Verifica que obtener_tipo retorna 'Premium'."""
        self.assertEqual(self.cliente.obtener_tipo(), "Premium")
    
    def test_constante_tipo_cliente(self):
        """Verifica la constante TIPO_CLIENTE."""
        self.assertEqual(ClientePremium.TIPO_CLIENTE, "Premium")
    
    def test_constante_descuento(self):
        """Verifica la constante DESCUENTO (15%)."""
        self.assertEqual(ClientePremium.DESCUENTO, 0.15)
    
    def test_puntos_iniciales(self):
        """Verifica que los puntos iniciales se asignan correctamente."""
        self.assertEqual(self.cliente.puntos_acumulados, 100)
    
    def test_puntos_iniciales_por_defecto(self):
        """Verifica que los puntos por defecto son 0."""
        cliente = ClientePremium("Test", "test@mail.com", "912345678", "Calle 123")
        self.assertEqual(cliente.puntos_acumulados, 0)
    
    def test_calcular_descuento(self):
        """Verifica que calcular_descuento retorna 15%."""
        descuento = self.cliente.calcular_descuento(1000)
        self.assertEqual(descuento, 150.0)  # 15% de 1000
    
    def test_calcular_descuento_varios_montos(self):
        """Verifica descuento con varios montos."""
        self.assertEqual(self.cliente.calcular_descuento(100), 15.0)
        self.assertEqual(self.cliente.calcular_descuento(500), 75.0)
        self.assertEqual(self.cliente.calcular_descuento(0), 0.0)
    
    def test_agregar_puntos(self):
        """Verifica que se pueden agregar puntos."""
        puntos_iniciales = self.cliente.puntos_acumulados
        self.cliente.agregar_puntos(50)
        self.assertEqual(self.cliente.puntos_acumulados, puntos_iniciales + 50)
    
    def test_agregar_puntos_negativos_no_suma(self):
        """Verifica que puntos negativos no se agregan."""
        puntos_iniciales = self.cliente.puntos_acumulados
        self.cliente.agregar_puntos(-10)
        self.assertEqual(self.cliente.puntos_acumulados, puntos_iniciales)
    
    def test_canjear_puntos_exitoso(self):
        """Verifica canje exitoso de puntos."""
        self.cliente.agregar_puntos(100)  # Total: 200
        resultado = self.cliente.canjear_puntos(50)
        self.assertTrue(resultado)
        self.assertEqual(self.cliente.puntos_acumulados, 150)
    
    def test_canjear_puntos_insuficientes(self):
        """Verifica que no se pueden canjear más puntos de los disponibles."""
        resultado = self.cliente.canjear_puntos(500)  # Solo tiene 100
        self.assertFalse(resultado)
        self.assertEqual(self.cliente.puntos_acumulados, 100)
    
    def test_beneficio_exclusivo(self):
        """Verifica el método beneficio_exclusivo."""
        beneficio = self.cliente.beneficio_exclusivo()
        self.assertIn("15%", beneficio)
        self.assertIn("100", beneficio)  # puntos
    
    def test_str_incluye_puntos(self):
        """Verifica que __str__ incluye los puntos."""
        resultado = str(self.cliente)
        self.assertIn("[Premium]", resultado)
        self.assertIn("100 pts", resultado)
    
    def test_obtener_datos_incluye_puntos(self):
        """Verifica que obtener_datos incluye puntos acumulados."""
        datos = self.cliente.obtener_datos()
        self.assertEqual(datos['tipo'], "Premium")
        self.assertEqual(datos['puntos_acumulados'], 100)
        self.assertEqual(datos['descuento'], 0.15)


# ============================================================================
# SECCIÓN 6: TESTS DE CLIENTE CORPORATIVO
# ============================================================================
class TestClienteCorporativo(unittest.TestCase):
    """Tests para la clase ClienteCorporativo."""
    
    def setUp(self):
        """Configuración inicial para cada test."""
        self.cliente = ClienteCorporativo(
            "María Fernández",
            "maria@empresa.com",
            "912345678",
            "Av. Industrial 1000",
            "TechCorp S.A.",
            "76.543.210-K"
        )
    
    def test_crear_cliente_corporativo(self):
        """Verifica que se puede crear un cliente corporativo."""
        self.assertEqual(self.cliente.nombre, "María Fernández")
        self.assertEqual(self.cliente.email, "maria@empresa.com")
    
    def test_herencia_de_cliente(self):
        """Verifica que ClienteCorporativo hereda de Cliente."""
        self.assertIsInstance(self.cliente, Cliente)
    
    def test_obtener_tipo(self):
        """Verifica que obtener_tipo retorna 'Corporativo'."""
        self.assertEqual(self.cliente.obtener_tipo(), "Corporativo")
    
    def test_constante_tipo_cliente(self):
        """Verifica la constante TIPO_CLIENTE."""
        self.assertEqual(ClienteCorporativo.TIPO_CLIENTE, "Corporativo")
    
    def test_constante_descuento(self):
        """Verifica la constante DESCUENTO (25%)."""
        self.assertEqual(ClienteCorporativo.DESCUENTO, 0.25)
    
    def test_datos_empresa(self):
        """Verifica que los datos de empresa se asignan correctamente."""
        self.assertEqual(self.cliente.nombre_empresa, "TechCorp S.A.")
        self.assertEqual(self.cliente.rut_empresa, "76.543.210-K")
    
    def test_datos_empresa_por_defecto(self):
        """Verifica valores por defecto de datos de empresa."""
        cliente = ClienteCorporativo("Test", "test@mail.com", "912345678", "Calle 123")
        self.assertEqual(cliente.nombre_empresa, "")
        self.assertEqual(cliente.rut_empresa, "")
    
    def test_calcular_descuento(self):
        """Verifica que calcular_descuento retorna 25%."""
        descuento = self.cliente.calcular_descuento(1000)
        self.assertEqual(descuento, 250.0)  # 25% de 1000
    
    def test_calcular_descuento_varios_montos(self):
        """Verifica descuento con varios montos."""
        self.assertEqual(self.cliente.calcular_descuento(100), 25.0)
        self.assertEqual(self.cliente.calcular_descuento(400), 100.0)
        self.assertEqual(self.cliente.calcular_descuento(0), 0.0)
    
    def test_setters_empresa(self):
        """Verifica que los setters de empresa funcionan."""
        self.cliente.nombre_empresa = "NuevaCorp"
        self.cliente.rut_empresa = "12.345.678-9"
        
        self.assertEqual(self.cliente.nombre_empresa, "NuevaCorp")
        self.assertEqual(self.cliente.rut_empresa, "12.345.678-9")
    
    def test_generar_factura_info(self):
        """Verifica que generar_factura_info retorna datos correctos."""
        factura = self.cliente.generar_factura_info()
        
        self.assertEqual(factura['nombre_empresa'], "TechCorp S.A.")
        self.assertEqual(factura['rut_empresa'], "76.543.210-K")
        self.assertEqual(factura['direccion'], "Av. Industrial 1000")
        self.assertEqual(factura['contacto'], "María Fernández")
        self.assertEqual(factura['email'], "maria@empresa.com")
    
    def test_beneficio_exclusivo(self):
        """Verifica el método beneficio_exclusivo."""
        beneficio = self.cliente.beneficio_exclusivo()
        self.assertIn("25%", beneficio)
        self.assertIn("TechCorp S.A.", beneficio)
    
    def test_str_incluye_empresa(self):
        """Verifica que __str__ incluye la empresa."""
        resultado = str(self.cliente)
        self.assertIn("[Corporativo]", resultado)
        self.assertIn("TechCorp S.A.", resultado)
    
    def test_obtener_datos_incluye_empresa(self):
        """Verifica que obtener_datos incluye datos de empresa."""
        datos = self.cliente.obtener_datos()
        self.assertEqual(datos['tipo'], "Corporativo")
        self.assertEqual(datos['nombre_empresa'], "TechCorp S.A.")
        self.assertEqual(datos['rut_empresa'], "76.543.210-K")
        self.assertEqual(datos['descuento'], 0.25)


# ============================================================================
# SECCIÓN 7: TESTS DEL GESTOR DE CLIENTES
# ============================================================================
class TestGestorClientes(unittest.TestCase):
    """Tests para la clase GestorClientes."""
    
    def setUp(self):
        """Configuración inicial para cada test."""
        self.gestor = GestorClientes()
        self.cliente_regular = ClienteRegular(
            "Juan Pérez", "juan@mail.com", "912345678", "Calle Norte 123"
        )
        self.cliente_premium = ClientePremium(
            "Ana García", "ana@mail.com", "987654321", "Av. Sur 456", 50
        )
        self.cliente_corporativo = ClienteCorporativo(
            "Pedro López", "pedro@empresa.com", "955555555", "Av. Industrial 789",
            "MiEmpresa S.A.", "12.345.678-9"
        )
    
    def test_gestor_vacio_inicial(self):
        """Verifica que el gestor inicia vacío."""
        self.assertEqual(self.gestor.total_clientes, 0)
        self.assertEqual(len(self.gestor.clientes), 0)
    
    def test_propiedad_clientes_es_copia(self):
        """Verifica que la propiedad clientes retorna una copia."""
        self.gestor.agregar_cliente(self.cliente_regular, silencioso=True)
        clientes = self.gestor.clientes
        clientes.append(self.cliente_premium)  # Modificar la copia
        self.assertEqual(self.gestor.total_clientes, 1)  # Original sin cambios
    
    # --- Tests CRUD: CREATE ---
    def test_agregar_cliente_exitoso(self):
        """Verifica que se puede agregar un cliente."""
        resultado = self.gestor.agregar_cliente(self.cliente_regular, silencioso=True)
        self.assertTrue(resultado)
        self.assertEqual(self.gestor.total_clientes, 1)
    
    def test_agregar_cliente_duplicado(self):
        """Verifica que no se puede agregar cliente con email duplicado."""
        self.gestor.agregar_cliente(self.cliente_regular, silencioso=True)
        
        cliente_duplicado = ClienteRegular(
            "Otro Nombre", "juan@mail.com", "999999999", "Otra Dirección 456"
        )
        resultado = self.gestor.agregar_cliente(cliente_duplicado, silencioso=True)
        
        self.assertFalse(resultado)
        self.assertEqual(self.gestor.total_clientes, 1)
    
    def test_agregar_multiples_clientes(self):
        """Verifica que se pueden agregar múltiples clientes."""
        self.gestor.agregar_cliente(self.cliente_regular, silencioso=True)
        self.gestor.agregar_cliente(self.cliente_premium, silencioso=True)
        self.gestor.agregar_cliente(self.cliente_corporativo, silencioso=True)
        
        self.assertEqual(self.gestor.total_clientes, 3)
    
    # --- Tests CRUD: READ ---
    def test_buscar_cliente_existente(self):
        """Verifica búsqueda de cliente existente."""
        self.gestor.agregar_cliente(self.cliente_regular, silencioso=True)
        
        encontrado = self.gestor.buscar_cliente("juan@mail.com")
        self.assertIsNotNone(encontrado)
        self.assertEqual(encontrado.nombre, "Juan Pérez")
    
    def test_buscar_cliente_inexistente(self):
        """Verifica búsqueda de cliente que no existe."""
        encontrado = self.gestor.buscar_cliente("noexiste@mail.com")
        self.assertIsNone(encontrado)
    
    def test_buscar_cliente_case_insensitive(self):
        """Verifica que la búsqueda es case-insensitive."""
        self.gestor.agregar_cliente(self.cliente_regular, silencioso=True)
        
        encontrado = self.gestor.buscar_cliente("JUAN@MAIL.COM")
        self.assertIsNotNone(encontrado)
    
    def test_mostrar_cliente_existente(self):
        """Verifica mostrar_cliente para cliente existente."""
        self.gestor.agregar_cliente(self.cliente_regular, silencioso=True)
        resultado = self.gestor.mostrar_cliente("juan@mail.com")
        self.assertTrue(resultado)
    
    def test_mostrar_cliente_inexistente(self):
        """Verifica mostrar_cliente para cliente inexistente."""
        resultado = self.gestor.mostrar_cliente("noexiste@mail.com")
        self.assertFalse(resultado)
    
    # --- Tests CRUD: UPDATE ---
    def test_actualizar_cliente_exitoso(self):
        """Verifica actualización exitosa de cliente."""
        self.gestor.agregar_cliente(self.cliente_regular, silencioso=True)
        
        resultado = self.gestor.actualizar_cliente(
            "juan@mail.com",
            "Juan Pérez Modificado",
            "999888777",
            "Nueva Dirección 789"
        )
        
        self.assertTrue(resultado)
        cliente = self.gestor.buscar_cliente("juan@mail.com")
        self.assertEqual(cliente.nombre, "Juan Pérez Modificado")
        self.assertEqual(cliente.telefono, "999888777")
        self.assertEqual(cliente.direccion, "Nueva Dirección 789")
    
    def test_actualizar_cliente_parcial(self):
        """Verifica actualización parcial de cliente."""
        self.gestor.agregar_cliente(self.cliente_regular, silencioso=True)
        
        resultado = self.gestor.actualizar_cliente(
            "juan@mail.com",
            "Nuevo Nombre",
            "",  # No actualizar teléfono
            ""   # No actualizar dirección
        )
        
        self.assertTrue(resultado)
        cliente = self.gestor.buscar_cliente("juan@mail.com")
        self.assertEqual(cliente.nombre, "Nuevo Nombre")
        self.assertEqual(cliente.telefono, "912345678")  # Sin cambios
    
    def test_actualizar_cliente_inexistente(self):
        """Verifica actualización de cliente que no existe."""
        resultado = self.gestor.actualizar_cliente(
            "noexiste@mail.com", "Nombre", "123456789", "Dirección"
        )
        self.assertFalse(resultado)
    
    # --- Tests CRUD: DELETE ---
    def test_eliminar_cliente_exitoso(self):
        """Verifica eliminación exitosa de cliente."""
        self.gestor.agregar_cliente(self.cliente_regular, silencioso=True)
        
        resultado = self.gestor.eliminar_cliente("juan@mail.com")
        
        self.assertTrue(resultado)
        self.assertEqual(self.gestor.total_clientes, 0)
        self.assertIsNone(self.gestor.buscar_cliente("juan@mail.com"))
    
    def test_eliminar_cliente_inexistente(self):
        """Verifica eliminación de cliente que no existe."""
        resultado = self.gestor.eliminar_cliente("noexiste@mail.com")
        self.assertFalse(resultado)
    
    def test_limpiar_lista(self):
        """Verifica que limpiar_lista elimina todos los clientes."""
        self.gestor.agregar_cliente(self.cliente_regular, silencioso=True)
        self.gestor.agregar_cliente(self.cliente_premium, silencioso=True)
        
        self.gestor.limpiar_lista()
        
        self.assertEqual(self.gestor.total_clientes, 0)
    
    # --- Tests de filtrado y estadísticas ---
    def test_obtener_clientes_por_tipo(self):
        """Verifica filtrado de clientes por tipo."""
        self.gestor.agregar_cliente(self.cliente_regular, silencioso=True)
        self.gestor.agregar_cliente(self.cliente_premium, silencioso=True)
        self.gestor.agregar_cliente(self.cliente_corporativo, silencioso=True)
        
        regulares = self.gestor.obtener_clientes_por_tipo("Regular")
        premium = self.gestor.obtener_clientes_por_tipo("Premium")
        corporativos = self.gestor.obtener_clientes_por_tipo("Corporativo")
        
        self.assertEqual(len(regulares), 1)
        self.assertEqual(len(premium), 1)
        self.assertEqual(len(corporativos), 1)
    
    def test_obtener_clientes_por_tipo_vacio(self):
        """Verifica filtrado cuando no hay clientes del tipo."""
        self.gestor.agregar_cliente(self.cliente_regular, silencioso=True)
        
        premium = self.gestor.obtener_clientes_por_tipo("Premium")
        self.assertEqual(len(premium), 0)
    
    def test_obtener_total_clientes(self):
        """Verifica método obtener_total_clientes."""
        self.gestor.agregar_cliente(self.cliente_regular, silencioso=True)
        self.gestor.agregar_cliente(self.cliente_premium, silencioso=True)
        
        self.assertEqual(self.gestor.obtener_total_clientes(), 2)


# ============================================================================
# SECCIÓN 8: TESTS DE ARCHIVOS
# ============================================================================
class TestArchivos(unittest.TestCase):
    """Tests para el módulo de archivos."""
    
    def setUp(self):
        """Configuración inicial: crear directorio temporal."""
        self.temp_dir = tempfile.mkdtemp()
        self.archivo_csv = os.path.join(self.temp_dir, "clientes_test.csv")
        self.archivo_reporte = os.path.join(self.temp_dir, "reporte_test.txt")
        self.archivo_log = os.path.join(self.temp_dir, "test.log")
        
        # Crear clientes de prueba
        self.clientes = [
            ClienteRegular("Juan Pérez", "juan@mail.com", "912345678", "Calle Norte 123"),
            ClientePremium("Ana García", "ana@mail.com", "987654321", "Av. Sur 456", 100),
            ClienteCorporativo("Pedro López", "pedro@empresa.com", "955555555", 
                            "Av. Industrial 789", "MiEmpresa S.A.", "12.345.678-9")
        ]
    
    def tearDown(self):
        """Limpieza: eliminar directorio temporal."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    # --- Tests de exportación CSV ---
    def test_exportar_csv_exitoso(self):
        """Verifica exportación exitosa a CSV."""
        resultado = exportar_clientes_csv(self.clientes, self.archivo_csv)
        
        self.assertTrue(resultado)
        self.assertTrue(os.path.exists(self.archivo_csv))
    
    def test_exportar_csv_contenido(self):
        """Verifica el contenido del CSV exportado."""
        exportar_clientes_csv(self.clientes, self.archivo_csv)
        
        with open(self.archivo_csv, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            filas = list(reader)
        
        self.assertEqual(len(filas), 3)
        self.assertEqual(filas[0]['tipo'], 'Regular')
        self.assertEqual(filas[1]['tipo'], 'Premium')
        self.assertEqual(filas[2]['tipo'], 'Corporativo')
    
    def test_exportar_csv_lista_vacia(self):
        """Verifica exportación con lista vacía."""
        resultado = exportar_clientes_csv([], self.archivo_csv)
        self.assertTrue(resultado)
    
    def test_exportar_csv_columnas_correctas(self):
        """Verifica que el CSV tiene las columnas correctas."""
        exportar_clientes_csv(self.clientes, self.archivo_csv)
        
        with open(self.archivo_csv, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            columnas = reader.fieldnames
        
        columnas_esperadas = ['tipo', 'nombre', 'email', 'telefono', 'direccion', 
                            'puntos', 'empresa', 'rut']
        self.assertEqual(columnas, columnas_esperadas)
    
    # --- Tests de importación CSV ---
    def test_importar_csv_exitoso(self):
        """Verifica importación exitosa desde CSV."""
        # Primero exportar
        exportar_clientes_csv(self.clientes, self.archivo_csv)
        
        # Luego importar
        importados = importar_clientes_csv(self.archivo_csv)
        
        self.assertEqual(len(importados), 3)
    
    def test_importar_csv_tipos_correctos(self):
        """Verifica que los tipos de cliente se importan correctamente."""
        exportar_clientes_csv(self.clientes, self.archivo_csv)
        importados = importar_clientes_csv(self.archivo_csv)
        
        tipos = [c.obtener_tipo() for c in importados]
        self.assertIn('Regular', tipos)
        self.assertIn('Premium', tipos)
        self.assertIn('Corporativo', tipos)
    
    def test_importar_csv_datos_premium(self):
        """Verifica que los datos de cliente Premium se importan correctamente."""
        exportar_clientes_csv(self.clientes, self.archivo_csv)
        importados = importar_clientes_csv(self.archivo_csv)
        
        premium = next((c for c in importados if c.obtener_tipo() == 'Premium'), None)
        self.assertIsNotNone(premium)
        self.assertEqual(premium.puntos_acumulados, 100)
    
    def test_importar_csv_datos_corporativo(self):
        """Verifica que los datos de cliente Corporativo se importan correctamente."""
        exportar_clientes_csv(self.clientes, self.archivo_csv)
        importados = importar_clientes_csv(self.archivo_csv)
        
        corp = next((c for c in importados if c.obtener_tipo() == 'Corporativo'), None)
        self.assertIsNotNone(corp)
        self.assertEqual(corp.nombre_empresa, "MiEmpresa S.A.")
        self.assertEqual(corp.rut_empresa, "12.345.678-9")
    
    def test_importar_csv_archivo_no_existe(self):
        """Verifica que se lanza excepción si archivo no existe."""
        with self.assertRaises(ArchivoNoEncontradoError):
            importar_clientes_csv("/ruta/inexistente/archivo.csv")
    
    def test_importar_csv_formato_invalido(self):
        """Verifica que se detecta formato inválido."""
        # Crear archivo con formato incorrecto
        with open(self.archivo_csv, 'w', encoding='utf-8') as f:
            f.write("columna1,columna2\nvalor1,valor2\n")
        
        with self.assertRaises(FormatoArchivoError):
            importar_clientes_csv(self.archivo_csv)
    
    # --- Tests de crear_cliente_desde_fila ---
    def test_crear_cliente_desde_fila_regular(self):
        """Verifica creación de cliente Regular desde fila."""
        fila = {
            'tipo': 'Regular',
            'nombre': 'Test User',
            'email': 'test@mail.com',
            'telefono': '912345678',
            'direccion': 'Calle Test 123'
        }
        cliente = crear_cliente_desde_fila(fila)
        
        self.assertIsInstance(cliente, ClienteRegular)
        self.assertEqual(cliente.nombre, 'Test User')
    
    def test_crear_cliente_desde_fila_premium(self):
        """Verifica creación de cliente Premium desde fila."""
        fila = {
            'tipo': 'Premium',
            'nombre': 'Test Premium',
            'email': 'premium@mail.com',
            'telefono': '912345678',
            'direccion': 'Calle Premium 456',
            'puntos': '200'
        }
        cliente = crear_cliente_desde_fila(fila)
        
        self.assertIsInstance(cliente, ClientePremium)
        self.assertEqual(cliente.puntos_acumulados, 200)
    
    def test_crear_cliente_desde_fila_corporativo(self):
        """Verifica creación de cliente Corporativo desde fila."""
        fila = {
            'tipo': 'Corporativo',
            'nombre': 'Test Corp',
            'email': 'corp@empresa.com',
            'telefono': '912345678',
            'direccion': 'Av. Corporativa 789',
            'empresa': 'TestCorp S.A.',
            'rut': '12.345.678-9'
        }
        cliente = crear_cliente_desde_fila(fila)
        
        self.assertIsInstance(cliente, ClienteCorporativo)
        self.assertEqual(cliente.nombre_empresa, 'TestCorp S.A.')
    
    def test_crear_cliente_desde_fila_tipo_desconocido(self):
        """Verifica que tipo desconocido lanza excepción."""
        fila = {
            'tipo': 'TipoInvalido',
            'nombre': 'Test',
            'email': 'test@mail.com',
            'telefono': '912345678',
            'direccion': 'Calle 123'
        }
        with self.assertRaises(FormatoArchivoError):
            crear_cliente_desde_fila(fila)
    
    # --- Tests de generación de reporte ---
    def test_generar_reporte_exitoso(self):
        """Verifica generación exitosa de reporte."""
        resultado = generar_reporte(self.clientes, self.archivo_reporte)
        
        self.assertTrue(resultado)
        self.assertTrue(os.path.exists(self.archivo_reporte))
    
    def test_generar_reporte_contenido(self):
        """Verifica el contenido del reporte."""
        generar_reporte(self.clientes, self.archivo_reporte)
        
        with open(self.archivo_reporte, 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        self.assertIn("REPORTE DE CLIENTES", contenido)
        self.assertIn("Total de clientes: 3", contenido)
        self.assertIn("Juan Pérez", contenido)
        self.assertIn("Ana García", contenido)
        self.assertIn("Pedro López", contenido)
    
    def test_generar_reporte_lista_vacia(self):
        """Verifica reporte con lista vacía."""
        resultado = generar_reporte([], self.archivo_reporte)
        
        self.assertTrue(resultado)
        with open(self.archivo_reporte, 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        self.assertIn("No hay clientes registrados", contenido)
    
    # --- Tests de logging ---
    def test_registrar_log(self):
        """Verifica que registrar_log funciona correctamente."""
        # Este test usa el archivo de log por defecto del sistema
        resultado = registrar_log("Mensaje de prueba", "INFO")
        self.assertTrue(resultado)
    
    def test_leer_log(self):
        """Verifica que leer_log retorna contenido."""
        registrar_log("Mensaje para leer", "TEST")
        contenido = leer_log(10)
        # El contenido puede ser vacío si no existe el archivo, pero no debe fallar
        self.assertIsInstance(contenido, str)


# ============================================================================
# SECCIÓN 9: TESTS DE INTEGRACIÓN
# ============================================================================
class TestIntegracion(unittest.TestCase):
    """Tests de integración que verifican el funcionamiento conjunto del sistema."""
    
    def setUp(self):
        """Configuración inicial."""
        self.gestor = GestorClientes()
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Limpieza."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_ciclo_completo_cliente_regular(self):
        """Test de ciclo completo: crear, buscar, actualizar, eliminar cliente regular."""
        # Crear
        cliente = ClienteRegular("Test User", "test@mail.com", "912345678", "Calle Test 123")
        self.gestor.agregar_cliente(cliente, silencioso=True)
        
        # Buscar
        encontrado = self.gestor.buscar_cliente("test@mail.com")
        self.assertIsNotNone(encontrado)
        
        # Actualizar
        self.gestor.actualizar_cliente("test@mail.com", "Test User Modificado", "", "")
        actualizado = self.gestor.buscar_cliente("test@mail.com")
        self.assertEqual(actualizado.nombre, "Test User Modificado")
        
        # Eliminar
        self.gestor.eliminar_cliente("test@mail.com")
        self.assertEqual(self.gestor.total_clientes, 0)
    
    def test_ciclo_completo_exportar_importar(self):
        """Test de ciclo completo: agregar clientes, exportar e importar."""
        archivo_csv = os.path.join(self.temp_dir, "integracion_test.csv")
        
        # Agregar clientes
        clientes = [
            ClienteRegular("Regular User", "regular@mail.com", "912345678", "Calle Regular 123"),
            ClientePremium("Premium User", "premium@mail.com", "987654321", "Av. Premium 456", 150),
            ClienteCorporativo("Corp User", "corp@empresa.com", "955555555", 
                            "Av. Corp 789", "TestCorp", "12.345.678-9")
        ]
        
        for c in clientes:
            self.gestor.agregar_cliente(c, silencioso=True)
        
        # Exportar
        self.gestor.exportar_csv(archivo_csv)
        self.assertTrue(os.path.exists(archivo_csv))
        
        # Crear nuevo gestor e importar
        nuevo_gestor = GestorClientes()
        nuevo_gestor.importar_csv(archivo_csv)
        
        self.assertEqual(nuevo_gestor.total_clientes, 3)
    
    def test_polimorfismo_calcular_descuento(self):
        """Test de polimorfismo: calcular descuento en diferentes tipos de cliente."""
        clientes = [
            ClienteRegular("Regular", "regular@mail.com", "912345678", "Calle 123"),
            ClientePremium("Premium", "premium@mail.com", "987654321", "Av. 456", 0),
            ClienteCorporativo("Corp", "corp@mail.com", "955555555", "Av. 789", "Corp", "12.345.678-9")
        ]
        
        monto = 1000
        descuentos = [c.calcular_descuento(monto) for c in clientes]
        
        self.assertEqual(descuentos[0], 0.0)     # Regular: 0%
        self.assertEqual(descuentos[1], 150.0)  # Premium: 15%
        self.assertEqual(descuentos[2], 250.0)  # Corporativo: 25%
    
    def test_polimorfismo_obtener_tipo(self):
        """Test de polimorfismo: obtener_tipo en diferentes clases."""
        clientes = [
            ClienteRegular("Regular", "regular@mail.com", "912345678", "Calle 123"),
            ClientePremium("Premium", "premium@mail.com", "987654321", "Av. 456", 0),
            ClienteCorporativo("Corp", "corp@mail.com", "955555555", "Av. 789", "Corp", "12.345.678-9")
        ]
        
        tipos = [c.obtener_tipo() for c in clientes]
        
        self.assertEqual(tipos[0], "Regular")
        self.assertEqual(tipos[1], "Premium")
        self.assertEqual(tipos[2], "Corporativo")
    
    def test_gestor_con_lista_heterogenea(self):
        """Test del gestor manejando lista heterogénea de clientes."""
        self.gestor.agregar_cliente(
            ClienteRegular("Regular", "regular@mail.com", "912345678", "Calle 123"),
            silencioso=True
        )
        self.gestor.agregar_cliente(
            ClientePremium("Premium", "premium@mail.com", "987654321", "Av. 456", 100),
            silencioso=True
        )
        self.gestor.agregar_cliente(
            ClienteCorporativo("Corp", "corp@mail.com", "955555555", "Av. 789", "Corp", "12.345.678-9"),
            silencioso=True
        )
        
        # Verificar filtrado por tipo
        regulares = self.gestor.obtener_clientes_por_tipo("Regular")
        premium = self.gestor.obtener_clientes_por_tipo("Premium")
        corp = self.gestor.obtener_clientes_por_tipo("Corporativo")
        
        self.assertEqual(len(regulares), 1)
        self.assertEqual(len(premium), 1)
        self.assertEqual(len(corp), 1)
    
    def test_validaciones_en_creacion_de_clientes(self):
        """Test que verifica que las validaciones funcionan en la creación de clientes."""
        # Email inválido
        with self.assertRaises(EmailInvalidoError):
            ClienteRegular("Test", "emailinvalido", "912345678", "Calle 123")
        
        # Teléfono inválido
        with self.assertRaises(TelefonoInvalidoError):
            ClientePremium("Test", "test@mail.com", "123", "Calle 123", 0)
        
        # Nombre inválido
        with self.assertRaises(NombreInvalidoError):
            ClienteCorporativo("X", "test@mail.com", "912345678", "Calle 123", "Corp", "12.345.678-9")
        
        # Dirección inválida
        with self.assertRaises(DireccionInvalidaError):
            ClienteRegular("Test", "test@mail.com", "912345678", "Dir")
    
    def test_cliente_premium_programa_puntos(self):
        """Test completo del programa de puntos de cliente Premium."""
        cliente = ClientePremium("Premium User", "premium@mail.com", "912345678", "Av. Premium 123", 0)
        
        # Agregar puntos
        cliente.agregar_puntos(100)
        self.assertEqual(cliente.puntos_acumulados, 100)
        
        cliente.agregar_puntos(50)
        self.assertEqual(cliente.puntos_acumulados, 150)
        
        # Canjear puntos
        resultado = cliente.canjear_puntos(75)
        self.assertTrue(resultado)
        self.assertEqual(cliente.puntos_acumulados, 75)
        
        # Intento de canjear más de lo disponible
        resultado = cliente.canjear_puntos(100)
        self.assertFalse(resultado)
        self.assertEqual(cliente.puntos_acumulados, 75)
    
    def test_cliente_corporativo_facturacion(self):
        """Test de información de facturación de cliente corporativo."""
        cliente = ClienteCorporativo(
            "María Fernández",
            "maria@empresa.com",
            "912345678",
            "Av. Industrial 1000",
            "TechCorp S.A.",
            "76.543.210-K"
        )
        
        factura = cliente.generar_factura_info()
        
        # Verificar todos los campos de facturación
        self.assertEqual(factura['nombre_empresa'], "TechCorp S.A.")
        self.assertEqual(factura['rut_empresa'], "76.543.210-K")
        self.assertEqual(factura['direccion'], "Av. Industrial 1000")
        self.assertEqual(factura['contacto'], "María Fernández")
        self.assertEqual(factura['email'], "maria@empresa.com")


# ============================================================================
# SECCIÓN 10: TESTS DE CASOS LÍMITE Y ERRORES
# ============================================================================
class TestCasosLimite(unittest.TestCase):
    """Tests para casos límite y situaciones de error."""
    
    def test_nombre_minimo_caracteres(self):
        """Test con nombre de exactamente 2 caracteres (mínimo válido)."""
        cliente = ClienteRegular("Jo", "jo@mail.com", "912345678", "Calle 123 Norte")
        self.assertEqual(cliente.nombre, "Jo")
    
    def test_direccion_minimo_caracteres(self):
        """Test con dirección de exactamente 5 caracteres (mínimo válido)."""
        cliente = ClienteRegular("Test", "test@mail.com", "912345678", "Cal12")
        self.assertEqual(cliente.direccion, "Cal12")
    
    def test_telefono_minimo_digitos(self):
        """Test con teléfono de exactamente 8 dígitos (mínimo válido)."""
        cliente = ClienteRegular("Test", "test@mail.com", "12345678", "Calle Test 123")
        self.assertEqual(cliente.telefono, "12345678")
    
    def test_email_con_caracteres_especiales(self):
        """Test con email con caracteres especiales permitidos."""
        cliente = ClienteRegular("Test", "test.user+tag@mail.com", "912345678", "Calle 123")
        self.assertEqual(cliente.email, "test.user+tag@mail.com")
    
    def test_nombre_con_acentos(self):
        """Test con nombre con caracteres acentuados."""
        cliente = ClienteRegular("José María Álvarez", "jose@mail.com", "912345678", "Calle 123")
        self.assertEqual(cliente.nombre, "José María Álvarez")
    
    def test_puntos_premium_cero(self):
        """Test de cliente Premium con cero puntos."""
        cliente = ClientePremium("Test", "test@mail.com", "912345678", "Calle 123", 0)
        self.assertEqual(cliente.puntos_acumulados, 0)
        
        # Intentar canjear con cero puntos
        resultado = cliente.canjear_puntos(10)
        self.assertFalse(resultado)
    
    def test_gestor_operaciones_con_lista_vacia(self):
        """Test de operaciones del gestor con lista vacía."""
        gestor = GestorClientes()
        
        # Buscar en lista vacía
        resultado = gestor.buscar_cliente("test@mail.com")
        self.assertIsNone(resultado)
        
        # Actualizar en lista vacía
        resultado = gestor.actualizar_cliente("test@mail.com", "Nombre", "123456789", "Dir")
        self.assertFalse(resultado)
        
        # Eliminar en lista vacía
        resultado = gestor.eliminar_cliente("test@mail.com")
        self.assertFalse(resultado)
    
    def test_herencia_jerarquica(self):
        """Test de la jerarquía de herencia de excepciones."""
        # Verificar que todas las excepciones heredan correctamente
        self.assertTrue(issubclass(ValidacionError, GICError))
        self.assertTrue(issubclass(EmailInvalidoError, ValidacionError))
        self.assertTrue(issubclass(TelefonoInvalidoError, ValidacionError))
        self.assertTrue(issubclass(NombreInvalidoError, ValidacionError))
        self.assertTrue(issubclass(DireccionInvalidaError, ValidacionError))
        
        self.assertTrue(issubclass(ClienteError, GICError))
        self.assertTrue(issubclass(ClienteExistenteError, ClienteError))
        self.assertTrue(issubclass(ClienteNoEncontradoError, ClienteError))
        
        self.assertTrue(issubclass(ArchivoError, GICError))
        self.assertTrue(issubclass(ArchivoNoEncontradoError, ArchivoError))
        self.assertTrue(issubclass(FormatoArchivoError, ArchivoError))


# ============================================================================
# EJECUTOR DE TESTS
# ============================================================================
if __name__ == "__main__":
    # Configurar el nivel de verbosidad
    verbosity = 2
    
    # Crear suite de tests
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Agregar todas las clases de test
    suite.addTests(loader.loadTestsFromTestCase(TestExcepciones))
    suite.addTests(loader.loadTestsFromTestCase(TestValidaciones))
    suite.addTests(loader.loadTestsFromTestCase(TestCliente))
    suite.addTests(loader.loadTestsFromTestCase(TestClienteRegular))
    suite.addTests(loader.loadTestsFromTestCase(TestClientePremium))
    suite.addTests(loader.loadTestsFromTestCase(TestClienteCorporativo))
    suite.addTests(loader.loadTestsFromTestCase(TestGestorClientes))
    suite.addTests(loader.loadTestsFromTestCase(TestArchivos))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegracion))
    suite.addTests(loader.loadTestsFromTestCase(TestCasosLimite))
    
    # Ejecutar tests
    runner = unittest.TextTestRunner(verbosity=verbosity)
    resultado = runner.run(suite)
    
    # Mostrar resumen
    print("\n" + "=" * 70)
    print("RESUMEN DE TESTS")
    print("=" * 70)
    print(f"Tests ejecutados: {resultado.testsRun}")
    print(f"Tests exitosos: {resultado.testsRun - len(resultado.failures) - len(resultado.errors)}")
    print(f"Fallos: {len(resultado.failures)}")
    print(f"Errores: {len(resultado.errors)}")
    
    if resultado.failures:
        print("\n" + "-" * 70)
        print("DETALLES DE FALLOS:")
        print("-" * 70)
        for test, trace in resultado.failures:
            print(f"\n {test}")
            print(trace)
    
    if resultado.errors:
        print("\n" + "-" * 70)
        print("DETALLES DE ERRORES:")
        print("-" * 70)
        for test, trace in resultado.errors:
            print(f"\n {test}")
            print(trace)
    
    print("=" * 70)
