# Programa gestor de concesionario.

## PROPÓSITO

El propósito principal del programa es organizar y gestionar los alquileres **de coches** de un concesionario, gestionados con ficheros **XML** para almacenar los datos de manera local y poder acceder de manera sencilla desde el programa principal a los datos.

---

## REQUISITOS

- [PyCharm 3.13](https://github.com/Jockpls/Concesionario/wiki/Uso-de-Python-e-instalación-de-Pycharm.) para la programación en Python.

- [VSCode](https://github.com/Jockpls/Concesionario/wiki/Instalación-VS-Code) para la gestión de JSON y XML con las extensiones: 
  1. XML,
  2. XML Tools
  3. JSON Tools

En los enlaces se encuentra la guía de instalación de dichos IDEs.

---

## INSTALACIÓN DEL PROGRAMA
Para la instalación del programa debemos seguir los siguientes pasos:

1. Clonar repositorio desde GitHub en la carpeta seleccionada.
   > Es importante que en esa carpeta se encuentren únicamente los elementos que componen el repositorio, en caso contrario podría originar errores en la ejecución o corrupción de datos.
2. Ejecutar concesionario.py

Encontraremos la guía del programa en su página de la [wiki](https://github.com/Jockpls/Concesionario/wiki/Descripción-del-programa).

---

## ITEMS
- JSON:
<div align: "center">

### GESTIÓN DE ALQUILER
| **DATO** | **DESCRIPCIÓN** |
| :----------: | :----------: |
| **DNI** | Identificador del coche  |
| **MATRÍCULA** | Identificador del cliente |
| **EXTRAS** | Extras y valor de estos |
| **FECHA_INICIO** | Fecha de inicio del alquiler |
| **FECHA_FIN** | Fecha de finalización del alquiler |
| **PRECIO_FINAL** | Precio final al cliente |
</div>

- XML:

<div align: "center">

### GESTIÓN DE CLIENTES
| **DATO** | **DESCRIPCIÓN** |
| :----------: | :----------: |
| **DNI** | Documento de identidad, se usa cómo identificador del cliente |
| **NOMBRE_COMPLETO** | Nombre y Apellidos del cliente |
| **EDAD** | Edad del cliente |
</div>
<div align: "center">

### GESTIÓN DE COCHES
|**DATO** | **DESCRIPCIÓN** |
| :----------: | :----------: |
| **MATRÍCULA** | Identificador del vehículo |
| **MARCA** | Marca del coche |
| **PRECIO_POR_DÍA** | Precio de alquiler diario |
</div>

El uso de estos ficheros nos codifica y ordena la gestión de la base de datos. 
Para los datos de los **clientes** utilizamos *XML* para poder definir y manejar los datos de los clientes con mayor facilidad.</br>
Para los datos de los **alquileres** utilizamos *JSON* para definirlos cómo diccionarios y poder acceder a ellos de una manera simple y rápida.

---

<h1>Base de Datos</h1>
Las relaciones de las clases en la base de datos se organizan cómo podemos observar en el diagrama. Partiendo del alquiler las otras dos clases.
No es una relación de herencia dentro del código, pero sí que se relacionan directamente, recogiendo todos los datos del cliente y del vehículo la clase Renting.

```mermaid
classDiagram
    class Cliente {
        +String dni
        +String nombre
        +Date fecha_nacimiento
        +int edad
        +calcular_edad() int
    }

    class Vehiculo {
        +String matricula
        +String marca
        +float precio_base_dia
        +__str__() String
    }

    class Renting {
        +Cliente cliente
        +Vehiculo vehiculo
        +Date fecha_inicio
        +Date fecha_fin
        +Dict extras
        +float precio_final
        +calcular_precio(int dias_alquiler) float
        +to_dict() Dict
    }

    class PrecioInvalidoError {
        <<exception>>
    }

    class ObjectError {
        <<exception>>
        Utilizado para poder generar mensajes de error personalizados
    }

    %% Relaciones
    Renting --> Cliente : tiene un
    Renting --> Vehiculo : alquila un
    Vehiculo ..> PrecioInvalidoError : lanza si precio < 0
    Cliente ..> ValueError : lanza si DNI inválido

    %% Funciones globales (fuera de clases)
    namespace Persistencia_y_Logica {
        class Funciones_Globales {
            +insertar_cliente(Cliente c)
            +insertar_vehiculo_xml(Vehiculo v)
            +buscar_cliente_xml(String dni)
            +buscar_vehiculo_xml(String matricula)
            +menu()
            +main()
        }
    }
```
