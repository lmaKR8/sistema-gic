# DIAGRAMA UML - SISTEMA GIC - SOLUTIONTECH

---
## Índice
- [Instrucciones de Exportación](#instrucciones-de-exportación)
- [Diagrama UML](#diagrama-uml)
- [Leyenda de Símbolos UML](#leyenda-de-símbolos-uml)
- [Cliente Regular](#cliente-regular)
- [Cliente Premium](#cliente-premium)
- [Cliente Corporativo](#cliente-corporativo)

---
## Instrucciones de Exportación
### 1. Usando PlantUML Online

1. Ir a: [https://www.plantuml.com/plantuml/uml](https://www.plantuml.com/plantuml/uml)
2. Copiar el código entre `@startuml` y `@enduml` del archivo `diagrama_clases_gic.puml`
3. Descargar como PNG o SVG -> Ver archivo `diagrama-clases.png`

---
## Diagrama UML
### Clase Base y Subclases
```
                            ┌─────────────────────────┐
                            │       <<abstract>>      │
                            │         Cliente         │
                            ├─────────────────────────┤
                            │ - __nombre: str         │
                            │ - __email: str          │
                            │ - __telefono: str       │
                            │ - __direccion: str      │
                            ├─────────────────────────┤
                            │ + nombre: str           │
                            │ + email: str            │
                            │ + telefono: str         │
                            │ + direccion: str        │
                            ├─────────────────────────┤
                            │ + __init__()            │
                            │ + __str__(): str        │
                            │ + mostrar_info()        │
                            │ + obtener_datos(): dict │
                            │ + obtener_tipo(): str   │
                            └───────────┬─────────────┘
                                        │
                                        │ herencia
                    ┌───────────────────┼───────────────────┐
                    │                   │                   │
                    ▼                   ▼                   ▼
    ┌───────────────────────┐ ┌───────────────────────┐ ┌───────────────────────┐
    │   ClienteRegular      │ │   ClientePremium      │ │  ClienteCorporativo   │
    ├───────────────────────┤ ├───────────────────────┤ ├───────────────────────┤
    │ - __descuento: 0.0    │ │ - __descuento: 0.15   │ │ - __descuento: 0.25   │
    │                       │ │ - __puntos: int       │ │ - __empresa: str      │
    │                       │ │                       │ │ - __rut: str          │
    ├───────────────────────┤ ├───────────────────────┤ ├───────────────────────┤
    │ + mostrar_info()      │ │ + mostrar_info()      │ │ + mostrar_info()      │
    │ + obtener_tipo()      │ │ + obtener_tipo()      │ │ + obtener_tipo()      │
    │ + beneficio_exclusivo │ │ + beneficio_exclusivo │ │ + beneficio_exclusivo │
    │ + calcular_descuento  │ │ + calcular_descuento  │ │ + calcular_descuento  │
    │                       │ │ + agregar_puntos()    │ │ + nombre_empresa      │
    │                       │ │ + puntos_acumulados   │ │ + rut_empresa         │
    └───────────────────────┘ └───────────────────────┘ └───────────────────────┘
```

### Gestor de Clientes (Composición)
```
    ┌───────────────────────────────────────┐
    │          GestorClientes               │
    ├───────────────────────────────────────┤
    │ - __clientes: list[Cliente]           │
    ├───────────────────────────────────────┤
    │ + clientes: list <<property>>         │
    │ + total_clientes: int <<property>>    │
    ├───────────────────────────────────────┤
    │ + agregar_cliente(cliente): bool      │
    │ + listar_clientes()         │
    │ + buscar_cliente(email): Cliente|None │
    │ + mostrar_cliente(email): bool        │
    │ + actualizar_cliente(...): bool       │
    │ + eliminar_cliente(email): bool       │
    │ + obtener_clientes_por_tipo(): list   │
    └───────────────────────────────────────┘
                    ◆
                    │ composición (1 a muchos)
                    │
                    ▼
            ┌───────────────┐
            │   Cliente     │
            │   (0..*)      │
            └───────────────┘
```

---
## Leyenda de Símbolos UML
### Visibilidad
```
| Símbolo | Significado |
| ------- | ----------- |
| `+`     | Público     |
| `-`     | Privado     |
| `#`     | Protegido   |
```

### Relaciones
```
| Símbolo | Significado                                           |
| ------- | ----------------------------------------------------- |
| `──▷`   | Herencia (extends)                                    |
| `◆──`   | Composición (el contenedor es dueño de los objetos)   |
| `◇──`   | Agregación (el contenedor NO es dueño de los objetos) |
| `───`   | Asociación simple                                     |

```

### Multiplicidad
```
| Símbolo | Significado     |
| ------- | --------------- |
| `1`     | Exactamente uno |
| `0..1`  | Cero o uno      |
| `*`     | Cero o más      |
| `0..*`  | Cero o más      |
| `1..*`  | Uno o más       |
```

---
## Cliente Regular

### Descripción
La clase `ClienteRegular` representa un cliente estándar del sistema sin beneficios especiales. Es el tipo de cliente más básico, sin descuentos ni programa de puntos.

### Relación UML
```
ClienteRegular ──▷ Cliente (Herencia)
```

### Diagrama UML
```
    ┌─────────────────────────┐
    │    ClienteRegular       │
    ├─────────────────────────┤
    │ - __descuento_base: 0.0 │
    ├─────────────────────────┤
    │ + mostrar_info()        │
    │ + obtener_tipo(): str   │
    │ + beneficio_exclusivo() │
    │ + calcular_descuento()  │
    └─────────────────────────┘
                ▲
                │ hereda
                │
    ┌─────────────────────────┐
    │        Cliente          │
    └─────────────────────────┘
```

### Atributos Propios
```
| Atributo           | Tipo    | Visibilidad | Descripción                                 |
| ------------------ | ------- | ----------- | ------------------------------------------- |
| `__descuento_base` | `float` | Privado     | Porcentaje de descuento (0% para regulares) |
```

### Atributos Heredados
```
| Atributo      | Tipo  | Visibilidad | Descripción           |
| ------------- | ----- | ----------- | --------------------- |
| `__nombre`    | `str` | Privado     | Nombre del cliente    |
| `__email`     | `str` | Privado     | Email del cliente     |
| `__telefono`  | `str` | Privado     | Teléfono del cliente  |
| `__direccion` | `str` | Privado     | Dirección del cliente |
```

### Constantes de Clase
```
| Constante      | Valor       | Descripción                       |
| -------------- | ----------- | --------------------------------- |
| `TIPO_CLIENTE` | `"Regular"` | Identificador del tipo de cliente |
```

---
## Cliente Premium

### Descripción
La clase `ClientePremium` representa un cliente con programa de puntos y descuentos especiales del 15%. Este tipo de cliente tiene acceso a beneficios exclusivos como acumulación de puntos y acceso prioritario.

### Relación UML
```
ClientePremium ──▷ Cliente (Herencia)
```

### Diagrama UML
```
    ┌───────────────────────────┐
    │     ClientePremium        │
    ├───────────────────────────┤
    │ - __descuento_base: 0.15  │
    │ - __puntos_acumulados: int│
    ├───────────────────────────┤
    │ + mostrar_info()          │
    │ + obtener_tipo(): str     │
    │ + beneficio_exclusivo()   │
    │ + calcular_descuento()    │
    │ + agregar_puntos()        │
    │ + canjear_puntos()        │
    │ + puntos_acumulados       │
    └───────────────────────────┘
            ▲
            │ hereda
            │
    ┌───────────────────────────┐
    │         Cliente           │
    └───────────────────────────┘
```

### Atributos Propios
```
| Atributo              | Tipo    | Visibilidad | Descripción                                |
| --------------------- | ------- | ----------- | ------------------------------------------ |
| `__descuento_base`    | `float` | Privado     | Porcentaje de descuento (15% para premium) |
| `__puntos_acumulados` | `int`   | Privado     | Puntos del programa de fidelidad           |
```

### Atributos Heredados
```
| Atributo      | Tipo  | Visibilidad | Descripción           |
| ------------- | ----- | ----------- | --------------------- |
| `__nombre`    | `str` | Privado     | Nombre del cliente    |
| `__email`     | `str` | Privado     | Email del cliente     |
| `__telefono`  | `str` | Privado     | Teléfono del cliente  |
| `__direccion` | `str` | Privado     | Dirección del cliente |
```

### Constantes de Clase
```
| Constante      | Valor       | Descripción                       |
| -------------- | ----------- | --------------------------------- |
| `TIPO_CLIENTE` | `"Premium"` | Identificador del tipo de cliente |
```

---
## Cliente Corporativo

### Descripción
La clase `ClienteCorporativo` representa un cliente empresarial del sistema con datos de empresa y los mayores descuentos (25%). Este tipo de cliente tiene acceso a beneficios exclusivos como facturación empresarial, línea de crédito y ejecutivo de cuenta dedicado.

### Relación UML
```
ClienteCorporativo ──▷ Cliente (Herencia)
```

### Diagrama UML
```
    ┌─────────────────────────────┐
    │    ClienteCorporativo       │
    ├─────────────────────────────┤
    │ - __descuento_base: 0.25    │
    │ - __nombre_empresa: str     │
    │ - __rut_empresa: str        │
    ├─────────────────────────────┤
    │ + mostrar_info()            │
    │ + obtener_tipo(): str       │
    │ + beneficio_exclusivo()     │
    │ + calcular_descuento()      │
    │ + generar_factura_info()    │
    │ + nombre_empresa <<prop>>   │
    │ + rut_empresa <<prop>>      │
    └─────────────────────────────┘
            ▲
            │ hereda
            │
    ┌─────────────────────────────┐
    │          Cliente            │
    └─────────────────────────────┘
```

### Atributos Propios
```
| Atributo           | Tipo    | Visibilidad | Descripción                                     |
| ------------------ | ------- | ----------- | ----------------------------------------------- |
| `__descuento_base` | `float` | Privado     | Porcentaje de descuento (25% para corporativos) |
| `__nombre_empresa` | `str`   | Privado     | Nombre de la empresa                            |
| `__rut_empresa`    | `str`   | Privado     | RUT de la empresa                               |
```

### Atributos Heredados
```
| Atributo      | Tipo  | Visibilidad | Descripción           |
| ------------- | ----- | ----------- | --------------------- |
| `__nombre`    | `str` | Privado     | Nombre del cliente    |
| `__email`     | `str` | Privado     | Email del cliente     |
| `__telefono`  | `str` | Privado     | Teléfono del cliente  |
| `__direccion` | `str` | Privado     | Dirección del cliente |
```

### Constantes de Clase
```
| Constante      | Valor           | Descripción                       |
| -------------- | --------------- | --------------------------------- |
| `TIPO_CLIENTE` | `"Corporativo"` | Identificador del tipo de cliente |
```
