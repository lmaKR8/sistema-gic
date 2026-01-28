"""
===============
Módulo archivos
===============
"""
import os
import csv
from datetime import datetime
from modulos.cliente_regular import ClienteRegular
from modulos.cliente_premium import ClientePremium
from modulos.cliente_corporativo import ClienteCorporativo
from modulos.excepciones import (
    ArchivoError,
    ArchivoNoEncontradoError,
    PermisoArchivoError,
    FormatoArchivoError
)


"""
CONFIGURACION DE RUTAS
"""
# Obtener la ruta base del proyecto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Rutas de los directorios
DATOS_DIR = os.path.join(BASE_DIR, "datos")
REPORTES_DIR = os.path.join(BASE_DIR, "reportes")
LOGS_DIR = os.path.join(BASE_DIR, "logs")

# Archivos por defecto
ARCHIVO_CLIENTES = os.path.join(DATOS_DIR, "clientes.csv")
ARCHIVO_ENTRADA = os.path.join(DATOS_DIR, "clientes_entrada.csv")
ARCHIVO_REPORTE = os.path.join(REPORTES_DIR, "resumen.txt")
ARCHIVO_LOG = os.path.join(LOGS_DIR, "app.log")


"""
FUNCIONES AUXILIARES
"""
def crear_directorios():
    """
    Crea los directorios datos/, reportes/, logs/ si no existen.
    """
    for directorio in [DATOS_DIR, REPORTES_DIR, LOGS_DIR]:
        if not os.path.exists(directorio):
            os.makedirs(directorio)


def obtener_timestamp() -> str:
    """
    Obtiene la fecha y hora actual formateada.
    
    Returns:
        str: Timestamp en formato 'YYYY-MM-DD HH:MM:SS'
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")



"""
EXPORTACION DE CLIENTES A CSV
"""
def exportar_clientes_csv(clientes, archivo=None) -> bool:
    """
    Exporta la lista de clientes a un archivo CSV.

    Args:
        clientes (list): Lista de objetos Cliente a exportar
        archivo (str, optional): Ruta del archivo. Por defecto usa ARCHIVO_CLIENTES
    Returns:
        bool: True si la exportacion fue exitosa
    Raises:
        ArchivoError: Si ocurre un error al escribir el archivo
        PermisoArchivoError: Si no hay permisos de escritura
    """
    if archivo is None:
        archivo = ARCHIVO_CLIENTES
    
    try:
        crear_directorios()
        with open(archivo, 'w', newline='', encoding='utf-8') as file:
            campos = ['tipo', 'nombre', 'email', 'telefono', 'direccion', 
                    'puntos', 'empresa', 'rut']
            
            writer = csv.DictWriter(file, fieldnames=campos)
            writer.writeheader()
            
            for cliente in clientes:
                fila = {
                    'tipo': cliente.obtener_tipo(),
                    'nombre': cliente.nombre,
                    'email': cliente.email,
                    'telefono': cliente.telefono,
                    'direccion': cliente.direccion,
                    'puntos': '',
                    'empresa': '',
                    'rut': ''
                }
                
                # Agrega campos especificos segun el tipo
                if cliente.obtener_tipo() == "Premium":
                    fila['puntos'] = cliente.puntos_acumulados
                elif cliente.obtener_tipo() == "Corporativo":
                    fila['empresa'] = cliente.nombre_empresa
                    fila['rut'] = cliente.rut_empresa
                
                writer.writerow(fila)
        
        # Registra en el log
        registrar_log(f"EXPORTACION: {len(clientes)} clientes exportados a {archivo}")
        return True
    
    # Manejo de excepciones
    except PermissionError:
        raise PermisoArchivoError(archivo, "escritura")
    except Exception as e:
        raise ArchivoError(f"Error al exportar clientes: {str(e)}")



"""
IMPORTACION DE CLIENTES DESDE CSV
"""
def importar_clientes_csv(archivo=None) -> list:
    """
    Lee el archivo CSV y crea objetos Cliente segun el tipo especificado.
    
    Args:
        archivo (str, optional): Ruta del archivo CSV. Por defecto usa ARCHIVO_ENTRADA
    Returns:
        list: Lista de objetos Cliente creados
    Raises:
        ArchivoNoEncontradoError: Si el archivo no existe
        PermisoArchivoError: Si no hay permisos de lectura
        FormatoArchivoError: Si el formato del CSV es invalido
    """
    if archivo is None:
        archivo = ARCHIVO_ENTRADA
    
    # Verifica que el archivo existe
    if not os.path.exists(archivo):
        raise ArchivoNoEncontradoError(archivo)
    
    clientes_importados = []
    errores = []
    
    try:
        with open(archivo, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            columnas_requeridas = {'tipo', 'nombre', 'email', 'telefono', 'direccion'}
            if not columnas_requeridas.issubset(set(reader.fieldnames or [])):
                raise FormatoArchivoError(
                    archivo, 
                    f"Faltan columnas requeridas: {columnas_requeridas}"
                )
            
            for num_fila, fila in enumerate(reader, start=2):
                try:
                    cliente = crear_cliente_desde_fila(fila)
                    if cliente:
                        clientes_importados.append(cliente)
                except Exception as e:
                    errores.append(f"Fila {num_fila}: {str(e)}")
        
        # Registra en el log
        registrar_log(f"IMPORTACION: {len(clientes_importados)} clientes importados desde {archivo}")
        
        if errores:
            registrar_log(f"IMPORTACION: {len(errores)} errores durante la importacion")
        return clientes_importados
    
    # Manejo de excepciones
    except PermissionError:
        raise PermisoArchivoError(archivo, "lectura")
    except FormatoArchivoError:
        raise
    except ArchivoNoEncontradoError:
        raise
    except Exception as e:
        raise ArchivoError(f"Error al importar clientes: {str(e)}")


def crear_cliente_desde_fila(fila) -> object:
    """
    Crea un objeto Cliente a partir de una fila del CSV.
    
    Args:
        fila (dict): Diccionario con los datos de la fila
    Returns:
        Cliente: Objeto del tipo correspondiente (Regular, Premium, Corporativo)
    Raises:
        FormatoArchivoError: Si el tipo de cliente es desconocido
    """
    tipo = fila.get('tipo', '').strip()
    nombre = fila.get('nombre', '').strip()
    email = fila.get('email', '').strip()
    telefono = fila.get('telefono', '').strip()
    direccion = fila.get('direccion', '').strip()
    
    if tipo == "Regular":
        return ClienteRegular(nombre, email, telefono, direccion)
    
    elif tipo == "Premium":
        puntos_str = fila.get('puntos', '0').strip()
        puntos = int(puntos_str) if puntos_str else 0
        return ClientePremium(nombre, email, telefono, direccion, puntos)
    
    elif tipo == "Corporativo":
        empresa = fila.get('empresa', '').strip()
        rut = fila.get('rut', '').strip()
        return ClienteCorporativo(nombre, email, telefono, direccion, empresa, rut)
    
    else:
        raise FormatoArchivoError("", f"Tipo de cliente desconocido: {tipo}")


"""
GENERACION DE REPORTES
"""
def generar_reporte(clientes, archivo=None) -> bool:
    """
    Genera un reporte de resumen en formato TXT. El reporte incluye:
    - Fecha y hora de generacion
    - Total de clientes
    - Cantidad por tipo de cliente
    - Lista resumida de clientes
    
    Args:
        clientes (list): Lista de objetos Cliente
        archivo (str, optional): Ruta del archivo. Por defecto usa ARCHIVO_REPORTE
    Returns:
        bool: True si el reporte fue generado exitosamente
    Raises:
        ArchivoError: Si ocurre un error al escribir el archivo
        PermisoArchivoError: Si no hay permisos de escritura
    """
    if archivo is None:
        archivo = ARCHIVO_REPORTE
    
    try:
        crear_directorios()
        
        # Cuenta clientes por tipo
        conteo = {"Regular": 0, "Premium": 0, "Corporativo": 0}
        for cliente in clientes:
            tipo = cliente.obtener_tipo()
            if tipo in conteo:
                conteo[tipo] += 1
        
        # Escribe el reporte
        with open(archivo, 'w', encoding='utf-8') as file:
            # Encabezado
            file.write("=" * 60 + "\n")
            file.write(" " * 10 + "REPORTE DE CLIENTES - SISTEMA GIC\n")
            file.write(" " * 15 + "SolutionTech S.A.\n")
            file.write("=" * 60 + "\n\n")
            
            # Fecha de generacion
            file.write(f"Fecha de generacion: {obtener_timestamp()}\n")
            file.write("-" * 60 + "\n\n")
            
            # Resumen estadistico
            file.write("RESUMEN ESTADISTICO\n")
            file.write("-" * 30 + "\n")
            file.write(f"Total de clientes: {len(clientes)}\n\n")
            file.write("Distribucion por tipo:\n")
            file.write(f"  - Clientes Regular:     {conteo['Regular']}\n")
            file.write(f"  - Clientes Premium:     {conteo['Premium']}\n")
            file.write(f"  - Clientes Corporativo: {conteo['Corporativo']}\n")
            file.write("-" * 30 + "\n\n")
            
            # Lista de clientes
            file.write("LISTA DE CLIENTES\n")
            file.write("-" * 60 + "\n")
            
            if clientes:
                for i, cliente in enumerate(clientes, 1):
                    file.write(f"\n{i}. {cliente.nombre}\n")
                    file.write(f"   Tipo: {cliente.obtener_tipo()}\n")
                    file.write(f"   Email: {cliente.email}\n")
                    file.write(f"   Telefono: {cliente.telefono}\n")
                    file.write(f"   Direccion: {cliente.direccion}\n")
                    
                    # Datos adicionales segun tipo
                    if cliente.obtener_tipo() == "Premium":
                        file.write(f"   Puntos: {cliente.puntos_acumulados}\n")
                    elif cliente.obtener_tipo() == "Corporativo":
                        file.write(f"   Empresa: {cliente.nombre_empresa}\n")
                        file.write(f"   RUT: {cliente.rut_empresa}\n")
            else:
                file.write("No hay clientes registrados.\n")
            
            # Pie del reporte
            file.write("\n" + "-" * 60 + "\n")
            file.write("Fin del reporte\n")
            file.write("=" * 60 + "\n")
        
        # Registra en el log
        registrar_log(f"REPORTE: Reporte generado en {archivo}")
        return True
    
    # Manejo de excepciones
    except PermissionError:
        raise PermisoArchivoError(archivo, "escritura")
    except Exception as e:
        raise ArchivoError(f"Error al generar reporte: {str(e)}")


"""
SISTEMA DE LOGGING
"""
def registrar_log(mensaje, nivel="INFO") -> bool:
    """
    Registra cada entrada en formato [YYYY-MM-DD HH:MM:SS] [NIVEL] Mensaje
    
    Args:
        mensaje (str): Mensaje a registrar
        nivel (str): Nivel del log (INFO, WARNING, ERROR, etc.)
    Returns:
        bool: True si se registro correctamente
    """
    try:
        # Crea directorios si no existen
        crear_directorios()
        
        # Formatea la entrada del log
        timestamp = obtener_timestamp()
        entrada = f"[{timestamp}] [{nivel}] {mensaje}\n"
        
        # Escribe al archivo (modo append)
        with open(ARCHIVO_LOG, 'a', encoding='utf-8') as file:
            file.write(entrada)
        
        return True
    
    # Manejo de excepciones
    except Exception:
        # Silencia errores de logging para no interrumpir el flujo
        return False


def registrar_alta_cliente(cliente):
    """
    Registra el alta de un nuevo cliente en el log.
    
    Args:
        cliente: Objeto Cliente que fue agregado
    """
    mensaje = f"ALTA: Nuevo cliente '{cliente.nombre}' ({cliente.obtener_tipo()}) - Email: {cliente.email}"
    registrar_log(mensaje, "INFO")


def registrar_baja_cliente(cliente):
    """
    Registra la baja de un cliente en el log.
    
    Args:
        cliente: Objeto Cliente que fue eliminado
    """
    mensaje = f"BAJA: Cliente eliminado '{cliente.nombre}' ({cliente.obtener_tipo()}) - Email: {cliente.email}"
    registrar_log(mensaje, "INFO")


def registrar_modificacion_cliente(cliente, campos_modificados):
    """
    Registra la modificacion de un cliente en el log.
    
    Args:
        cliente: Objeto Cliente que fue modificado
        campos_modificados (list): Lista de campos que fueron modificados
    """
    campos = ", ".join(campos_modificados)
    mensaje = f"MODIFICACION: Cliente '{cliente.nombre}' - Campos: {campos}"
    registrar_log(mensaje, "INFO")


def registrar_error(error, contexto=""):
    """
    Registra un error en el log.
    
    Args:
        error: Objeto de excepcion o mensaje de error
        contexto (str): Contexto donde ocurrio el error
    """
    if contexto:
        mensaje = f"ERROR en {contexto}: {str(error)}"
    else:
        mensaje = f"ERROR: {str(error)}"
    registrar_log(mensaje, "ERROR")


def leer_log(lineas=50) -> str:
    """
    Lee las ultimas lineas del archivo de log.
    
    Args:
        lineas (int): Numero de lineas a leer
    Returns:
        str: Contenido del log
    """
    try:
        if not os.path.exists(ARCHIVO_LOG):
            return "No hay registros de log disponibles."
        
        with open(ARCHIVO_LOG, 'r', encoding='utf-8') as file:
            todas_lineas = file.readlines()
            ultimas = todas_lineas[-lineas:] if len(todas_lineas) > lineas else todas_lineas
            return "".join(ultimas)
    
    # Manejo de excepciones
    except Exception as e:
        return f"Error al leer el log: {str(e)}"
