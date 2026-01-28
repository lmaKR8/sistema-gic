"""
===================
Módulo validaciones
===================
"""
import re
from modulos.excepciones import (
    EmailInvalidoError,
    TelefonoInvalidoError,
    NombreInvalidoError,
    DireccionInvalidaError,
    RutInvalidoError,
    PuntosInvalidosError
)


"""
PATRONES REGEX
"""

# Patron para email: usuario@dominio.extension
# Permite: letras, numeros, puntos, guiones y guiones bajos
PATRON_EMAIL = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

# Patron para telefono: 8-15 digitos, permite espacios, guiones y parentesis
# Ejemplos validos: +56912345678, (09) 1234-5678, 912345678
PATRON_TELEFONO = r'^[\d\s\-\(\)\+]{8,20}$'

# Patron para nombre: al menos 2 caracteres alfabeticos
# Permite: letras (incluyendo acentos), espacios y guiones
PATRON_NOMBRE = r'^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s\-]{2,100}$'

# Patron para direccion: al menos 5 caracteres
# Permite: letras, numeros, espacios y caracteres comunes de direcciones
PATRON_DIRECCION = r'^[\w\sáéíóúÁÉÍÓÚñÑüÜ\.\,\#\-\°]{5,200}$'

# Patron para RUT chileno: XX.XXX.XXX-X o XXXXXXXX-X
# El digito verificador puede ser numero o K
PATRON_RUT = r'^(\d{1,2}\.?\d{3}\.?\d{3}-[\dkK])$'



"""
FUNCIONES DE VALIDACION
"""
def validar_email(email: str) -> bool:
    """
    Reglas de validacion:
    - No puede estar vacio
    - Debe contener exactamente un @
    - Debe tener un dominio con al menos un punto
    - Solo caracteres permitidos antes y despues del @
    
    Args:
        email (str): Correo electronico a validar
    Returns:
        bool: True si el email es valido
    Raises:
        EmailInvalidoError: Si el email no cumple el formato
    """
    if not email or not isinstance(email, str):
        raise EmailInvalidoError(str(email))
    
    email = email.strip()
    
    if not re.match(PATRON_EMAIL, email):
        raise EmailInvalidoError(email)
    
    return True


def validar_telefono(telefono: str) -> bool:
    """
    Reglas de validacion:
    - No puede estar vacio
    - Debe contener entre 8 y 15 digitos
    - Permite espacios, guiones, parentesis y signo +
    
    Args:
        telefono (str): Numero de telefono a validar
    Returns:
        bool: True si el telefono es valido
    Raises:
        TelefonoInvalidoError: Si el telefono no cumple el formato
    """
    if not telefono or not isinstance(telefono, str):
        raise TelefonoInvalidoError(str(telefono))
    
    telefono = telefono.strip()
    
    # Verifica patron general
    if not re.match(PATRON_TELEFONO, telefono):
        raise TelefonoInvalidoError(telefono)
    
    # Contar solo digitos (debe tener entre 8 y 15)
    solo_digitos = re.sub(r'\D', '', telefono)
    if len(solo_digitos) < 8 or len(solo_digitos) > 15:
        raise TelefonoInvalidoError(telefono)
    
    return True


def validar_nombre(nombre: str) -> bool:
    """
    Reglas de validacion:
    - No puede estar vacio
    - Debe tener al menos 2 caracteres
    - Solo permite letras, espacios y guiones
    - No puede ser solo numeros
    
    Args:
        nombre (str): Nombre a validar
    Returns:
        bool: True si el nombre es valido
    Raises:
        NombreInvalidoError: Si el nombre no cumple el formato
    """
    if not nombre or not isinstance(nombre, str):
        raise NombreInvalidoError(str(nombre))
    
    nombre = nombre.strip()
    
    if len(nombre) < 2:
        raise NombreInvalidoError(nombre)
    
    if not re.match(PATRON_NOMBRE, nombre):
        raise NombreInvalidoError(nombre)
    
    # Verifica que no sea solo numeros
    if nombre.isdigit():
        raise NombreInvalidoError(nombre)
    
    return True


def validar_direccion(direccion: str) -> bool:
    """
    Reglas de validacion:
    - No puede estar vacia
    - Debe tener al menos 5 caracteres
    - Permite letras, numeros, espacios y caracteres comunes
    
    Args:
        direccion (str): Direccion a validar
    Returns:
        bool: True si la direccion es valida
    Raises:
        DireccionInvalidaError: Si la direccion no cumple el formato
    """
    if not direccion or not isinstance(direccion, str):
        raise DireccionInvalidaError(str(direccion))
    
    direccion = direccion.strip()
    
    if len(direccion) < 5:
        raise DireccionInvalidaError(direccion)
    
    if not re.match(PATRON_DIRECCION, direccion):
        raise DireccionInvalidaError(direccion)
    
    return True


def validar_rut(rut: str) -> bool:
    """
    Reglas de validacion:
    - Formato: XX.XXX.XXX-X o XXXXXXXX-X
    - El digito verificador puede ser numero (0-9) o K
    
    Args:
        rut (str): RUT a validar
    Returns:
        bool: True si el RUT es valido
    Raises:
        RutInvalidoError: Si el RUT no cumple el formato
    """
    if not rut or not isinstance(rut, str):
        raise RutInvalidoError(str(rut))
    
    rut = rut.strip().upper()
    
    if not re.match(PATRON_RUT, rut):
        raise RutInvalidoError(rut)
    
    return True


def validar_puntos(puntos: int, operacion: str = "agregar", disponibles: int = 0) -> bool:
    """
    Reglas de validacion:
    - Los puntos deben ser un numero entero
    - Para agregar: deben ser positivos
    - Para canjear: no pueden superar los disponibles
    
    Args:
        puntos (int): Cantidad de puntos a validar
        operacion (str): Tipo de operacion ("agregar" o "canjear")
        disponibles (int): Puntos disponibles (para canje)
    Returns:
        bool: True si los puntos son validos
    Raises:
        PuntosInvalidosError: Si la operacion no es valida
    """
    if not isinstance(puntos, int):
        try:
            puntos = int(puntos)
        except (ValueError, TypeError):
            raise PuntosInvalidosError(0, 0, operacion)
    
    if operacion == "agregar":
        if puntos <= 0:
            raise PuntosInvalidosError(puntos, 0, "agregar")
    
    elif operacion == "canjear":
        if puntos <= 0:
            raise PuntosInvalidosError(puntos, disponibles, "canjear")
        if puntos > disponibles:
            raise PuntosInvalidosError(puntos, disponibles, "canjear")
    
    return True



"""
FUNCIONES DE VALIDACION COMPLETA
"""
def validar_datos_cliente(nombre: str, email: str, telefono: str, direccion: str) -> dict:
    """
    Ejecuta todas las validaciones necesarias para crear un cliente.
    
    Args:
        nombre (str): Nombre del cliente
        email (str): Email del cliente
        telefono (str): Telefono del cliente
        direccion (str): Direccion del cliente
    Returns:
        dict: Diccionario con los datos validados y limpios
    Raises:
        NombreInvalidoError: Si el nombre es invalido
        EmailInvalidoError: Si el email es invalido
        TelefonoInvalidoError: Si el telefono es invalido
        DireccionInvalidaError: Si la direccion es invalida
    """
    # Valida cada campo (lanza excepcion si falla)
    validar_nombre(nombre)
    validar_email(email)
    validar_telefono(telefono)
    validar_direccion(direccion)
    
    # Retorna datos limpios
    return {
        'nombre': nombre.strip(),
        'email': email.strip().lower(),
        'telefono': telefono.strip(),
        'direccion': direccion.strip()
    }


def validar_datos_corporativo(nombre_empresa: str, rut_empresa: str) -> dict:
    """
    Valida los datos adicionales de un cliente corporativo.
    
    Args:
        nombre_empresa (str): Nombre de la empresa
        rut_empresa (str): RUT de la empresa
    Returns:
        dict: Diccionario con los datos validados
    Raises:
        NombreInvalidoError: Si el nombre de empresa es invalido
        RutInvalidoError: Si el RUT es invalido
    """
    validar_nombre(nombre_empresa)
    validar_rut(rut_empresa)
    
    return {
        'nombre_empresa': nombre_empresa.strip(),
        'rut_empresa': rut_empresa.strip().upper()
    }
