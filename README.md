# Sistema GIC - Gestor Inteligente de Clientes

## Índice

- [Autor](#autor)
- [Descripción del Proyecto](#descripción-del-proyecto)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Conceptos de POO Aplicados](#conceptos-de-poo-aplicados)
- [Funcionalidades Implementadas](#funcionalidades-implementadas)
- [Uso del Sistema](#uso-del-sistema)
- [Testing](#testing)
- [Documentación Adicional](#documentación-adicional)

---

## Autor
**Desarrollado por**: Leandro Marchant A.  
**Tipo**: Proyecto Educativo - Evaluación Final  
**Módulo**: Programación Orientada a Objetos con Python  
**Programa**: Fullstack Python - Talento Digital  
**Año**: 2026

---
## Descripción del Proyecto
El **Sistema GIC (Gestor Inteligente de Clientes)** es una aplicación de escritorio desarrollada como proyecto final del módulo de Programación Orientada a Objetos con Python del programa **Fullstack Python - Talento Digital 2026**.

Implementa un sistema completo de gestión de clientes utilizando los pilares fundamentales de la Programación Orientada a Objetos: **Encapsulamiento**, **Herencia**, **Polimorfismo** y **Abstracción**.

### El Desafío
Desarrollar para **SolutionTech**, una empresa de servicios tecnológicos, un sistema que permita:

- Gestionar tres tipos diferentes de clientes: **Regular**, **Premium** y **Corporativo**
- Aplicar descuentos diferenciados según el tipo de cliente
- Implementar un programa de puntos para clientes Premium
- Gestionar datos empresariales para clientes Corporativos
- Mantener persistencia de datos mediante archivos CSV
- Generar reportes y mantener logs de actividad
- Validar robustamente todos los datos de entrada

### Solución Implementada
Sistema modular con arquitectura orientada a objetos que implementa:

- **3 clases de cliente** con herencia jerárquica
- **Sistema de validaciones** con expresiones regulares
- **Excepciones personalizadas** con jerarquía propia
- **Operaciones CRUD** completas sobre clientes
- **Persistencia de datos** en CSV con importación/exportación
- **Sistema de logging** para auditoría
- **Suite de tests** con 153 casos de prueba

---
## Estructura del Proyecto
El proyecto está organizado siguiendo principios de modularización y separación de responsabilidades:

```
sistema-gic/
│
├── main.py                          # Punto de entrada del programa
│
├── modulos/                         # Paquete principal de módulos
│   ├── __init__.py                  # Inicializador del paquete
│   ├── cliente.py                   # Clase base Cliente
│   ├── cliente_regular.py           # Subclase ClienteRegular (0% descuento)
│   ├── cliente_premium.py           # Subclase ClientePremium (15% + puntos)
│   ├── cliente_corporativo.py       # Subclase ClienteCorporativo (25% + empresa)
│   ├── gestor_clientes.py           # Gestor CRUD de clientes
│   ├── validaciones.py              # Funciones de validación con REGEX
│   ├── excepciones.py               # Excepciones personalizadas
│   └── archivos.py                  # Gestión de CSV, reportes y logs
│
├── datos/                           # Directorio de datos
│   ├── clientes.csv                 # Exportación de clientes
│   └── clientes_entrada.csv         # Archivo de importación
│
├── reportes/                        # Directorio de reportes
│   └── resumen.txt                  # Reporte de resumen
│
├── logs/                            # Directorio de logs
│   └── app.log                      # Log de actividad del sistema
│
├── test/                            # Suite de tests
│   ├── __init__.py
│   └── test_proyecto.py             # 153 tests unitarios e integración
│
├── docs/                            # Documentación
│   ├── diagrama_clases_gic.puml     # Diagrama UML PlantUML
│   ├── diagrama_clases_gic.md       # Documentación del diagrama
│   ├── diagrama-clases.png          # Imagen PNG del diagrama           
│   └── informe_test.md              # Informe completo de testing
│
└── README.md                        # Este archivo
```

---
## Conceptos de POO Aplicados

### 1. **Encapsulamiento**
- Atributos privados con prefijo `__` (ej: `__nombre`, `__email`)
- Acceso controlado mediante propiedades (`@property`)
- Validación en setters antes de modificar datos

**Ejemplo:**
```python
class Cliente:
    def __init__(self, nombre: str, email: str, ...):
        self.__nombre = nombre.strip()
        self.__email = email.strip().lower()

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str):
        validar_nombre(valor)
        self.__nombre = valor
```

### 2. **Herencia**
- Clase base `Cliente` con atributos y métodos comunes
- Tres subclases especializadas:
  - `ClienteRegular`: Sin descuento
  - `ClientePremium`: 15% descuento + puntos de fidelidad
  - `ClienteCorporativo`: 25% descuento + datos empresariales

**Jerarquía:**
```
Cliente (clase base)
    │
    ├── ClienteRegular
    ├── ClientePremium
    └── ClienteCorporativo
```

### 3. **Polimorfismo**
- Método `obtener_tipo()` sobrescrito en cada subclase
- Método `calcular_descuento()` con diferente implementación por tipo
- Método `mostrar_info()` personalizado para cada tipo
- `GestorClientes` maneja lista heterogénea de clientes de forma uniforme

**Ejemplo:**
```python
# Mismo método, diferentes comportamientos
cliente_regular.calcular_descuento(1000)     # → 0.0 (0%)
cliente_premium.calcular_descuento(1000)     # → 150.0 (15%)
cliente_corporativo.calcular_descuento(1000) # → 250.0 (25%)
```

### 4. **Abstracción**
- Interfaz simplificada en `GestorClientes`
- Métodos de alto nivel que ocultan complejidad interna
- Excepciones personalizadas con jerarquía clara
- Separación de responsabilidades en módulos

### 5. **Validaciones Robustas** 
- Expresiones regulares (REGEX) para validar formatos
- Validación de emails, teléfonos, nombres, direcciones y RUT
- Excepciones específicas para cada tipo de error
- Mensajes descriptivos de error

### 6. **Manejo de Excepciones**
Jerarquía de excepciones personalizadas:

```
Exception
    └── GICError (base)
            ├── ValidacionError
            │       ├── EmailInvalidoError
            │       ├── TelefonoInvalidoError
            │       ├── NombreInvalidoError
            │       ├── DireccionInvalidaError
            │       ├── RutInvalidoError
            │       └── PuntosInvalidosError
            ├── ClienteError
            │       ├── ClienteExistenteError
            │       ├── ClienteNoEncontradoError
            │       └── ListaVaciaError
            └── ArchivoError
                    ├── ArchivoNoEncontradoError
                    ├── PermisoArchivoError
                    └── FormatoArchivoError
```

---
## Funcionalidades Implementadas

### 1. Agregar Cliente

- Selección del tipo de cliente (Regular, Premium o Corporativo)
- Validación completa de datos básicos: nombre, email, teléfono y dirección
- Solicitud de datos adicionales según el tipo:
  - **Premium**: Puntos iniciales
  - **Corporativo**: Nombre de empresa y RUT
- Verificación de email único (no permite duplicados)
- Registro automático en el log de actividad

### 2. Listar Clientes
Opciones de visualización:

- **Todos los clientes**: Lista completa con tipo identificado
- **Por tipo**: Filtrado de clientes Regular, Premium o Corporativo
- Muestra información resumida de cada cliente
- Contador total de clientes

### 3. Buscar Cliente
- Búsqueda por email (identificador único)
- Insensible a mayúsculas/minúsculas
- Muestra información detallada completa del cliente
- Incluye beneficios específicos según el tipo

### 4. Actualizar Cliente
- Búsqueda del cliente por email
- Muestra datos actuales antes de actualizar
- Permite actualización parcial (solo los campos que se deseen)
- Validación de nuevos datos antes de guardar
- Registro de modificaciones en el log

### 5. Eliminar Cliente
- Búsqueda del cliente por email
- Solicita confirmación antes de eliminar
- Eliminación segura con registro en log
- Actualización automática de estadísticas

### 6. Ver Estadísticas
- Distribución de clientes por tipo
- Representación visual con barras de progreso
- Porcentajes calculados automáticamente
- Total general de clientes

### 7. Gestión de Archivos

#### Exportar a CSV
- Exporta todos los clientes a `datos/clientes.csv`
- Formato estándar con 8 columnas: tipo, nombre, email, teléfono, dirección, puntos, empresa, rut
- Codificación UTF-8 para caracteres especiales
- Campos adicionales vacíos según corresponda

#### Importar desde CSV
- Lee archivo CSV y crea objetos Cliente según el tipo
- Detecta automáticamente el tipo de cada cliente
- Omite duplicados (clientes con email existente)
- Maneja errores de formato y archivos no encontrados
- Registra cantidad importada y duplicados ignorados

#### Generar Reporte TXT
- Crea reporte completo en `reportes/resumen.txt`
- Incluye:
  - Fecha y hora de generación
  - Resumen estadístico por tipo
  - Lista detallada de todos los clientes
  - Datos específicos según el tipo de cliente

#### Ver Log de Actividad
- Muestra las últimas 30 entradas del log
- Formato: `[YYYY-MM-DD HH:MM:SS] [NIVEL] Mensaje`
- Registra:
  - Altas de clientes
  - Bajas de clientes
  - Modificaciones con campos actualizados
  - Operaciones de importación/exportación
  - Errores del sistema

### 8. Cálculo de Descuentos (Polimorfismo)
Cada tipo de cliente calcula su descuento de forma diferente:

- **Regular**: 0% de descuento
- **Premium**: 15% de descuento
- **Corporativo**: 25% de descuento

### 9. Programa de Puntos (Solo Premium)
- **Agregar puntos**: Acumula puntos por compras
- **Canjear puntos**: Usa puntos para beneficios
- Validación de puntos disponibles antes de canjear
- No permite puntos negativos

### 10. Datos Empresariales (Solo Corporativo)
- Almacenamiento de nombre de empresa y RUT
- Método `generar_factura_info()` con datos de facturación
- Validación de formato RUT chileno (XX.XXX.XXX-X)

---
## Uso del Sistema

### Requisitos
- **Python**: 3.6 o superior
- **Módulos**: Solo módulos estándar de Python
  - `re` (expresiones regulares)
  - `csv` (manejo de CSV)
  - `os` (operaciones del sistema)
  - `datetime` (manejo de fechas)
  - `unittest` / `pytest` (para ejecutar tests)

### Instalación
```bash
# Clonar o descargar el proyecto
cd sistema-gic

# No requiere instalación de dependencias adicionales
```

### Ejecución
```bash
# Ejecutar el programa principal
python main.py
```

### Flujo de Uso
1. **Inicio del sistema**
   - Muestra encabezado de bienvenida
   - Pregunta si desea cargar datos de prueba (6 clientes de ejemplo)

2. **Menú principal**
   ```
   ============================================================
           SISTEMA GIC - GESTOR INTELIGENTE DE CLIENTES
                          SolutionTech
   ============================================================

   ----------------------------------------
              MENÚ PRINCIPAL
   ----------------------------------------
     1. Agregar cliente
     2. Listar clientes
     3. Buscar cliente
     4. Actualizar cliente
     5. Eliminar cliente
     6. Ver estadísticas
     7. Gestión de archivos
     8. Salir
   ----------------------------------------
   ```

3. **Selección de opciones**
   - Ingresar número del 1 al 8
   - Seguir instrucciones en pantalla
   - Mensajes claros de éxito `[OK]` o error `[X]`

4. **Salir**
   - Opción 8 para finalizar
   - Los cambios en memoria se pierden si no se exportan

### Ejemplo de Uso: Agregar Cliente Premium
```
  Seleccione una opción (1-8): 1

--- Seleccione el tipo de cliente ---
  1. Cliente Regular (sin descuento)
  2. Cliente Premium (15% descuento + puntos)
  3. Cliente Corporativo (25% descuento)
  4. Cancelar
  Opción: 2

--- Ingreso de datos del cliente ---
  Nombre completo: Juan Pérez García
  Email: juan.perez@email.com
  Teléfono: +56912345678
  Dirección: Av. Principal 1234, Santiago

--- Datos adicionales (Premium) ---
  Puntos iniciales (0 si es nuevo): 500

[OK] Cliente 'Juan Pérez García' agregado exitosamente.
```

### Datos de Prueba
Al iniciar, el sistema puede cargar 6 clientes de ejemplo:

- 2 **Clientes Regular**
- 2 **Clientes Premium** (con 1500 y 3200 puntos)
- 2 **Clientes Corporativo** (TechCorp S.A. e InnovaTech SpA)

### Formato de Datos CSV
**Estructura de `datos/clientes.csv`:**

```csv
tipo,nombre,email,telefono,direccion,puntos,empresa,rut
Regular,Juan Perez,juan@email.com,912345678,Av. Principal 123,,,
Premium,Ana Garcia,ana@email.com,987654321,Calle Norte 456,1500,,
Corporativo,Carlos Lopez,carlos@corp.com,955555555,Av. Sur 789,,TechCorp S.A.,76.543.210-K
```

**Campos:**
- `tipo`: Regular | Premium | Corporativo
- `nombre`: Nombre completo (mínimo 2 caracteres)
- `email`: Formato válido (usuario@dominio.com)
- `telefono`: 8-15 dígitos (permite +, espacios, guiones)
- `direccion`: Mínimo 5 caracteres
- `puntos`: Solo para Premium (entero)
- `empresa`: Solo para Corporativo (nombre empresa)
- `rut`: Solo para Corporativo (formato XX.XXX.XXX-X)

---
## Testing

### Suite de Tests
El proyecto incluye una suite completa de 153 tests unitarios y de integración.

**Archivo:** `test/test_proyecto.py`

### Organización de Tests
```
| Sección                | Tests | Cobertura               |
| ---------------------- | ----- | ----------------------- |
| TestExcepciones        | 16    | Sistema de excepciones  |
| TestValidaciones       | 30+   | Validaciones REGEX      |
| TestCliente            | 11    | Clase base              |
| TestClienteRegular     | 11    | Herencia y polimorfismo |
| TestClientePremium     | 16    | Programa de puntos      |
| TestClienteCorporativo | 14    | Datos empresariales     |
| TestGestorClientes     | 18    | Operaciones CRUD        |
| TestArchivos           | 18    | CSV, reportes, logs     |
| TestIntegracion        | 8     | Flujos completos        |
| TestCasosLimite        | 8     | Casos borde             |
```

### Ejecutar Tests
**Con pytest (recomendado):**

```bash
# Instalar pytest (si no está instalado)
pip install pytest

# Ejecutar todos los tests
python -m pytest test/test_proyecto.py -v

# Ejecutar con resumen corto
python -m pytest test/test_proyecto.py -v --tb=short

# Ejecutar una sección específica
python -m pytest test/test_proyecto.py::TestClientePremium -v
```

**Con unittest:**

```bash
# Ejecutar todos los tests
python -m unittest test.test_proyecto -v

# Ejecutar el archivo directamente
python test/test_proyecto.py
```

### Resultados de Tests
```
=================== 153 passed, 32 subtests passed in 0.22s ===================

--Todos los tests pasan exitosamente--
```

### Cobertura Estimada
- **Módulos principales**: ~95-100%
- **Funciones de validación**: 100%
- **Excepciones**: 100%
- **Operaciones CRUD**: 100%
- **Archivos CSV/Reportes**: ~90%

---
## Documentación Adicional

### Diagramas UML
**Diagrama de Clases**: `docs/diagrama_clases_gic.puml`

- Diagrama completo en formato PlantUML
- Muestra relaciones de herencia
- Incluye atributos y métodos de cada clase

### Informes
**Informe de Testing**: `docs/informe_test.md`

- Resumen ejecutivo de tests
- Detalle por sección
- Problemas detectados y soluciones
- Métricas de calidad

### Patrones de Diseño Aplicados
1. **Patrón Strategy (Implícito)**
   - Diferentes estrategias de descuento por tipo de cliente
   - Método `calcular_descuento()` polimórfico

2. **Patrón Template Method**
   - Método `obtener_datos()` en clase base
   - Subclases extienden con datos específicos

3. **Patrón Factory (Implícito)**
   - Función `crear_cliente_desde_fila()` en archivos.py
   - Crea diferentes tipos de cliente según datos

---
## Validaciones Implementadas

### Patrones REGEX
```
| Campo         | Patrón                                             | Descripción                        |
| ------------- | -------------------------------------------------- | ---------------------------------- |
| **Email**     | `^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$` | Formato estándar de email          |
| **Teléfono**  | `^[\d\s\-\(\)\+]{8,20}$`                           | 8-15 dígitos con formato flexible  |
| **Nombre**    | `^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s\-]{2,100}$`              | Letras, espacios, guiones, acentos |
| **Dirección** | `^[\w\sáéíóúÁÉÍÓÚñÑüÜ\.\,\#\-\°]{5,200}$`          | Alfanumérico con símbolos comunes  |
| **RUT**       | `^(\d{1,2}\.?\d{3}\.?\d{3}-[\dkK])$`               | Formato chileno XX.XXX.XXX-X       |
```

### Excepciones por Validación
Cada validación lanza una excepción específica con código único:

- `EmailInvalidoError` → VAL001
- `TelefonoInvalidoError` → VAL002
- `NombreInvalidoError` → VAL003
- `DireccionInvalidaError` → VAL004
- `RutInvalidoError` → VAL005
- `PuntosInvalidosError` → VAL006

---
## Características Técnicas

### Buenas Prácticas Implementadas

**Código limpio y legible**
- Nombres descriptivos de variables y funciones
- Comentarios y docstrings en español
- Separación lógica en módulos
- Constantes en mayúsculas

**Type hints**
- Anotaciones de tipos en parámetros y retornos
- Uso de `typing` para tipos complejos
- Mejora la documentación del código

**Documentación**
- Docstrings en todas las clases y métodos
- Comentarios explicativos en lógica compleja
- README completo con ejemplos

**Manejo de errores**
- Try-except en todas las operaciones críticas
- Excepciones específicas para cada caso
- Mensajes descriptivos de error

**Testing exhaustivo**
- 153 tests unitarios e integración
- Cobertura alta de código
- Tests de casos límite y errores

**Logs y auditoría**
- Registro de todas las operaciones CRUD
- Timestamps en cada entrada
- Niveles de log (INFO, ERROR)

---
## Problemas Conocidos y Limitaciones

### Bug Detectado: Validación de Dirección

**Descripción:** El patrón REGEX para direcciones no permite apóstrofes (`'`), causando rechazo de direcciones válidas como "Av. O'Higgins".

**Ubicación:** `modulos/validaciones.py`, línea 35

**Impacto:** Medio - Afecta direcciones con apóstrofes

**Solución:** Agregar `'` al patrón:

```python
PATRON_DIRECCION = r'^[\w\sáéíóúÁÉÍÓÚñÑüÜ\.\,\#\-\°\']{5,200}$'
```

**Estado:** Documentado en test `test_direccion_con_apostrofe_falla`

### Limitaciones Actuales
- Sin persistencia automática (requiere exportar manualmente)
- Sin interfaz gráfica (solo consola)
- Sin búsqueda por nombre (solo por email)
- Sin autenticación o control de acceso

---
## Licencia
Este proyecto es de uso educativo y no tiene licencia comercial.
