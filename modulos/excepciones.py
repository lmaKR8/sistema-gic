"""
==================
Modulo Excepciones
==================
Jerarquia de Excepciones:
    Exception
        |
        +-- GICError (clase base del sistema)
                |
                +-- ValidacionError (errores de validacion)
                |       |
                |       +-- EmailInvalidoError
                |       +-- TelefonoInvalidoError
                |       +-- NombreInvalidoError
                |       +-- DireccionInvalidaError
                |
                +-- ClienteError (errores de gestion de clientes)
                        |
                        +-- ClienteExistenteError
                        +-- ClienteNoEncontradoError
"""

class GICError(Exception):
    """
    Todas las excepciones personalizadas del sistema heredan de esta clase.
    
    Attributes:
        mensaje (str): Mensaje descriptivo del error
        codigo (str): Codigo identificador del error (opcional)
    """
    
    def __init__(self, mensaje: str = "Error en el sistema GIC", codigo: str = "GIC000"):
        self.mensaje = mensaje
        self.codigo = codigo
        super().__init__(self.mensaje)
    
    def __str__(self) -> str:
        """Representacion en cadena del error."""
        return f"[{self.codigo}] {self.mensaje}"



"""
EXCEPCIONES DE VALIDACION DE DATOS
"""
class ValidacionError(GICError):
    """
    Clase base para errores de validacion de datos
    """
    
    def __init__(self, mensaje: str = "Error de validacion", codigo: str = "VAL000"):
        super().__init__(mensaje, codigo)


class EmailInvalidoError(ValidacionError):
    """
    Excepcion para emails con formato invalido
    """
    def __init__(self, email: str = ""):
        self.email = email
        mensaje = f"Email invalido: '{email}'. Debe tener formato usuario@dominio.com"
        super().__init__(mensaje, "VAL001")


class TelefonoInvalidoError(ValidacionError):
    """
    Excepcion para telefonos con formato invalido
    """
    def __init__(self, telefono: str = ""):
        self.telefono = telefono
        mensaje = f"Telefono invalido: '{telefono}'. Debe contener entre 8 y 15 digitos"
        super().__init__(mensaje, "VAL002")


class NombreInvalidoError(ValidacionError):
    """
    Excepcion para nombres con formato invalido
    """
    def __init__(self, nombre: str = ""):
        self.nombre = nombre
        mensaje = f"Nombre invalido: '{nombre}'. Debe tener al menos 2 caracteres alfabeticos"
        super().__init__(mensaje, "VAL003")


class DireccionInvalidaError(ValidacionError):
    """
    Excepcion para direcciones con formato invalido
    """
    
    def __init__(self, direccion: str = ""):
        self.direccion = direccion
        mensaje = f"Direccion invalida: '{direccion}'. Debe tener al menos 5 caracteres"
        super().__init__(mensaje, "VAL004")


class RutInvalidoError(ValidacionError):
    """
    Excepcion para RUT empresarial con formato invalido
    """
    
    def __init__(self, rut: str = ""):
        self.rut = rut
        mensaje = f"RUT invalido: '{rut}'. Formato esperado: XX.XXX.XXX-X"
        super().__init__(mensaje, "VAL005")


class PuntosInvalidosError(ValidacionError):
    """
    Excepcion para operaciones invalidas con puntos de fidelidad
    """
    
    def __init__(self, puntos: int = 0, disponibles: int = 0, operacion: str = ""):
        self.puntos = puntos
        self.disponibles = disponibles
        if operacion == "canjear":
            mensaje = f"No se pueden canjear {puntos} puntos. Disponibles: {disponibles}"
        elif operacion == "agregar":
            mensaje = f"No se pueden agregar {puntos} puntos. Los puntos deben ser positivos"
        else:
            mensaje = f"Operacion invalida con puntos: {puntos}"
        super().__init__(mensaje, "VAL006")



"""
EXCEPCIONES DE GESTION DE CLIENTES
"""
class ClienteError(GICError):
    """
    Se utiliza cuando ocurre un error en operaciones CRUD de clientes
    """
    def __init__(self, mensaje: str = "Error de cliente", codigo: str = "CLI000"):
        super().__init__(mensaje, codigo)


class ClienteExistenteError(ClienteError):
    """
    Excepcion cuando se intenta registrar un cliente duplicado
    """
    def __init__(self, email: str = ""):
        self.email = email
        mensaje = f"Ya existe un cliente registrado con el email: '{email}'"
        super().__init__(mensaje, "CLI001")


class ClienteNoEncontradoError(ClienteError):
    """
    Excepcion cuando no se encuentra un cliente buscado
    """
    def __init__(self, email: str = ""):
        self.email = email
        mensaje = f"No se encontro ningun cliente con el email: '{email}'"
        super().__init__(mensaje, "CLI002")


class ListaVaciaError(ClienteError):
    """
    Excepcion cuando se intenta operar sobre una lista vacia.
    """
    def __init__(self):
        mensaje = "No hay clientes registrados en el sistema"
        super().__init__(mensaje, "CLI003")



"""
PROPIEDADES DE ARCHIVOS
"""
class ArchivoError(GICError):
    """
    Clase base para errores relacionados con archivos.
    """
    def __init__(self, mensaje: str = "Error de archivo", codigo: str = "ARC000"):
        super().__init__(mensaje, codigo)


class ArchivoNoEncontradoError(ArchivoError):
    """
    Excepcion cuando no se encuentra un archivo
    """
    def __init__(self, ruta: str = ""):
        self.ruta = ruta
        mensaje = f"Archivo no encontrado: '{ruta}'"
        super().__init__(mensaje, "ARC001")


class ErrorEscrituraError(ArchivoError):
    """
    Excepcion cuando falla la escritura de un archivo
    """
    def __init__(self, ruta: str = "", detalle: str = ""):
        self.ruta = ruta
        mensaje = f"Error al escribir archivo '{ruta}': {detalle}"
        super().__init__(mensaje, "ARC002")
