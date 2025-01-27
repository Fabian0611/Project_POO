# Project POO

## Nombre del Grupo: ***Puppet Masters***

## Integrantes
- Juan Manuel Berdugo Torres
- Valentina Carreño Granados
- Fabian Camilo Arciniegas Morales

## Tabla de Contenido
- [Introducción](#introducción)
- [Problema](#problema)
- [Solución](#solución)
- [Diagramas de Clase](#diagramas-de-clase)
  - [Propietario](#propietario)
  - [Vehiculo](#vehiculo)
  - [BaseDeDatos](#basededatos)
  - [HorasEnElParqueadero](#horasenelparqueadero)
  - [Tarifa](#tarifa)
  - [Parqueadero](#parqueadero)
  - [ManejadorDatosVehiculo](#manejadordatosvehiculo)
- [Resultados Parciales](#resultados-parciales)
## Introducción
Usualmente cada vez que vamos a un centro comercial nos podemos encontrar con el mismo problema todos los dias, ya que encontrar un espacio de parqueo se puede convertir en una aventura, 
ya que las indicaciones que nos brindan los sistemas en estos centros comerciales pueden ser minimas o inexistentes, por eso mismo nuestro equipo ***Puppet Masters*** propone una solucion el cual es un codigo en pyhton el cual asignara un espacio en especifico al `vehiculo` en cuestion.

## Problema
El principal problema que buscamos resolver con este proyecto es facilitar la busqueda de un espacio de parqueo, ya que en centros comerciales o en grandes tiendas esta es una actividad que puede tardar varios minutos e incluso horas en horarios pico, esto afecta ya que es una perdida de tiempo, combustible y paciencia, lo que deja con una mala experiencia al cliente.

## Solución
Nuestra solución propuesta es la creación de un sistema que asigne espacios de estacionamiento específicos a los vehículos. Este sistema proporciona información sobre los espacios disponibles, reduciendo significativamente el tiempo empleado en buscar un lugar. Al implementar esta tecnología, buscamos mejorar la experiencia general de estacionamiento para los compradores y fomentar el uso eficiente de los recursos.

## Diagramas de Clase
``` mermaid
classDiagram
    class ManejadorDatosVehiculos{
        +archivo_json
        +generar_csv(self, archivo_salida)
        +generar_cadena(self)
    }

    class Propietario{
    + str Identificación
    + str Nombre 
    + str Telefono
    + str Correo
    + Obeter_contacto(self): dict 
    + get_id_propietario(self): str
    + get_telefono(self):str 
    + get_correo (self):str
    + set_id_propietario(self): str
    + set_telefono(self):str 
    + set_correo (self):str
    }

        class Vehiculo {
        + Str placa
        + Str tipo
        + Propietario propietario
        + obtenerInformacion(self, propietario):dict 
        + get_placa(self) : str
        + get_tipo(self) : str
        + get_ propietario (self): propietario
        + set_ placa (self, placa : str): placa 
        + set_tipo (self, tipo: str): tipo
        + set_propietario (self. propietario:"Propietario"): propietario
        
    }

    class Moto {
        +  Str placa
        + Str tipo
        + Propietario propietario

    }

    class Carro {
        + Str placa
        + Str tipo
        + Propietario propietario

    }
    class Bicicleta{
        +  Str placa
        + Str tipo
        + Propietario propietario
    }

    class BaseDatos{
        +Str archivo
        +List __propietarios
        +List __vehiculos
        +List __historial
        +__cargar_datos(self)
        +agregar_propietario(self, propietario)
        +agregar_vehiculo(self, vehiculo)
        +agregar_historial(self, placa, hora_entrada, hora_salida, tarifa)
        +generar_json(self)
}

    class HorasEnElParqueadero{
        +Str hora_entrada
        +Str hora_salida
        +calcular_tiempo_en_segundos(self): float
    }

    class Tarifa{
        +Str tipo_vehiculo
        +Float segundos
        +calcular_tarifa(self): Float
    }

    class Parqueadero{
        +Int filas_carros
        +Int columnas_carros
        +Int filas_motos
        +Int columnas_motos
        +Int filas_bicis
        +Int columnas_bicis
        +ocupar_espacio(self, tipo, fila, columna, placa, hora)
        +liberar_espacio(self, tipo, columna, hora_salida): dict
        +mostar_parqueadero(self): Str
        +mostar_matriz(self, matriz): Str
    }

    class ManejadorDatosVehiculos{
        +archivo_json
        +generar_csv(self, archivo_salida)
        +generar_cadena(self): Cadena
    }

    Vehiculo  <|-- Bicicleta
    Vehiculo <|-- Moto
    Vehiculo <|-- Carro
    Propietario --> Vehiculo: tiene un/unos
    Propietario --> BaseDatos: Recibe info
    Vehiculo --> BaseDatos: Recibe Info
    HorasEnElParqueadero --> BaseDatos: Recibe Info
    Tarifa --> BaseDatos: Recibe Info
    BaseDatos --> ManejadorDatosVehiculos: Entrega Info
    Vehiculo --> Parqueadero: Ocupa
```
### `Propietario`
Esta clase se usa para instanciar diferentes datos del propietario, ademas de contar con sus diferentes setters and getters, ademas de una funcion que nos devuelve todos estos datos recopilados en un diccionario
``` mermaid
classDiagram
   class propietario{
    + str Identificación
    + str Nombre 
    + str Telefono
    + str Correo
    + Obeter_contacto(self): dict 
    + get_id_propietario(self): str
    + get_telefono(self):str 
    + get_correo (self):str
    + set_id_propietario(self): str
    + set_telefono(self):str 
    + set_correo (self):str
    }
```
### `Vehiculo`
Esta clase se utiliza para crear diferentes vehículos, aprovechando las características que los diferencian, como su placa o su propietario. Además, incluye métodos para acceder a información privada, como los datos del usuario
``` mermaid
classDiagram
    class Vehiculo {
        + Str placa
        + Str tipo
        + Propietario propietario
        + obtenerInformacion(self, propietario):dict 
        + get_placa(self) : str
        + get_tipo(self) : str
        + get_ propietario (self): propietario
        + set_ placa (self, placa : str): placa 
        + set_tipo (self, tipo: str): tipo
        + set_propietario (self. propietario:"Propietario"): propietario
        
    }

    class Moto {
        +  Str placa
        + Str tipo
        + Propietario propietario

    }

    class Carro {
        + Str placa
        + Str tipo
        + Propietario propietario

    }
    class Bicicleta{
        +  Str placa
        + Str tipo
        + Propietario propietario
    }



    Vehiculo  <|-- Bicicleta
    Vehiculo <|-- Moto
    Vehiculo <|-- Carro
```

### `BaseDeDatos`
La clase `BaseDeDatos` genera un archivo json donde se guardan la informacion de los propietarios, vehiculos y uso del parqueadero.
```mermaid
classDiagram
    class BaseDatos{
        +chain archivo
        +dict __propietarios
        +List __vehiculos
        +List __historial
        +
        +__cargar_datos(self)
        +agregar_propietario(self, propietario:"Propietario")
        +agregar_vehiculo(self, vehiculo)
        +agregar_historial(self, placa, hora_entrada, hora_salida, tarifa)
        +generar_json(self)
}
```
### `HorasEnElParqueadero`
Esta clase calcula el tiempo que estuvo el vehiculo en el parqueadero.
``` mermaid
classDiagram
    class HorasEnElParqueadero{
        +hora_entrada
        +hora_salida
        +calcular_tiempo_en_segundos(self)
    }
```
### `Tarifa`
Esta clase utiliza datetime para calcular el tiempo que un vehículo permanece en el parqueadero. Posteriormente, multiplica el tiempo, dado en segundos, por la tarifa correspondiente a cada clase de vehículo.
``` mermaid
classDiagram
    class Tarifa{
        +tipo_vehiculo
        +segundos
        +calcular_tarifa(self)
    }
```
### `Parqueadero`
Esta clase genera una matriz que contiene información sobre el estado de cada espacio.
``` mermaid
classDiagram
    class Parqueadero{
        +filas_carros
        +columnas_carros
        +filas_motos
        +columnas_motos
        +filas_bicis
        +columnas_bicis
        +ocupar_espacio(self, tipo, fila, columna, placa, hora)
        +liberar_espacio(self, tipo, columna, hora_salida): dict
        +mostar_parqueadero(self)
        +mostar_matriz(self, matriz)
    }
```
### `ManejadorDatosVehiculo`
Genera un csv con el reporte de todos ls movimientos que se han realizado en el parqueadero.
``` mermaid
classDiagram
    class ManejadorDatosVehiculos{
        +archivo_json
        +generar_csv(self, archivo_salida)
        +generar_cadena(self)
    }
```

## Resultados Parciales
El código es capaz de generar una matriz que simula un parqueadero, consultar el estado de cada celda y, con base en la ocupación, asignar un espacio a cada usuario. Además, calcula la tarifa de cada usuario en función del tiempo que estuvo en el parqueadero y el tipo de vehículo que utiliza.
