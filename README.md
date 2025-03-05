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
  - [PropietarioDB](#propietarioDB)
  - [VehiculoDB](#vehiculoDB)
  - [ParqueaderoDB](#parqueaderoDB)
- [Resultados Parciales](#resultados-parciales)
- 
## Introducción
El tráfico en las grandes ciudades es un problema creciente que afecta la movilidad y calidad de vida de millones de personas. La saturación vehicular no solo genera largas demoras, sino que también incrementa la contaminación ambiental y el estrés en los conductores. Un factor clave que contribuye a este problema es la dificultad para encontrar estacionamiento, lo que provoca que muchos conductores den vueltas innecesarias dentro de los parqueaderos o incluso en las calles, aumentando el tráfico y el consumo de combustible. Estudios han demostrado que la exposición prolongada a situaciones de congestión vehicular eleva los niveles de cortisol, la hormona del estrés, lo que puede derivar en problemas de salud como hipertensión y fatiga crónica. Para mitigar estos efectos, es esencial contar con soluciones que optimicen la búsqueda de estacionamiento y reduzcan el tiempo que los conductores permanecen innecesariamente en circulación.

## Problema
Uno de los mayores problemas en los parqueaderos es la falta de información en tiempo real sobre la disponibilidad de espacios, lo que obliga a los conductores a recorrer el estacionamiento sin una guía clara. En promedio, una persona puede tardar hasta 8 minutos buscando un lugar para estacionar, lo que no solo genera frustración y estrés, sino que también contribuye al tráfico dentro del parqueadero y al desperdicio de tiempo y combustible. Esta situación impacta negativamente la experiencia del usuario, especialmente en lugares concurridos como centros comerciales, donde el flujo constante de vehículos dificulta aún más el proceso. Para abordar este problema, es fundamental contar con un sistema eficiente que optimice la asignación de espacios y brinde información actualizada a los conductores.

## Solución
Desarrollar un sistema inteligente de gestión de parqueaderos que permita monitorear en tiempo real la disponibilidad de espacios, informando a los usuarios sobre los lugares libres y registrando automáticamente la entrada y salida de los vehículos. La información será procesada y mostrada en una interfaz accesible para los usuarios, facilitando la búsqueda de estacionamiento. Además, el sistema llevará un registro detallado de los vehículos que ingresan y salen, optimizando la administración del parqueadero.




## Diagramas de Clase
``` mermaid

classDiagram

 class ConnectorDB {
        - str host
        - str user
        - str password
        - str database
        - connection
        - cursor
        + ConnectorDB(host, user, password, database)
        + connect()
    }
    
    class PropietarioDB {
        - int _id_propietario
        - str _nombre
        - str _telefono
        - str _correo
        + PropietarioDB(identificacion, nombre, telefono, correo, host, user, password, database)
        + id_propietario: int
        + nombre: str
        + telefono: str
        + correo: str
        + agregar_propietario()
        + obtener_propietario_por_id()
        + actualizar_propietario()
        + eliminar_propietario(id_propietario)
        + obtener_propietarios()
        + cerrar_conexion()
    }
    
    class ConnectorDB {
        + connect()
    }


    class VehiculoDB {
        - str _placa
        - str _tipo
        - int _propietario
        + VehiculoDB(placa, tipo, propietario, host, user, password, database)
        + placa: str
        + tipo: str
        + propietario: int
        + agregar_vehiculo()
        + obtener_vehiculo_por_placa()
        + actualizar_vehiculo()
        + eliminar_vehiculo()
        + obtener_vehiculos()
        + cerrar_conexion()
    }
    
    class ConnectorDB {
        + connect()
    }

    class PropietarioDB {
        + id_propietario: int
    }

    class ParqueaderoDB {
        - int _id_espacio
        - str _tipo
        - str _placa
        - str _estado
        + ParqueaderoDB(id_espacio, tipo, placa, estado, host, user, password, database)
        + id_espacio: int
        + tipo: str
        + placa: str
        + estado: str
        + crear_espacios(cantidad, tipo)
        + ocupar_espacio()
        + desocupar_espacio()
        + obtener_espacios()
        + obtener_espacio_por_placa()
        + obtener_espacios_libres()
        + cerrar_conexion()
    }

    class ConnectorDB {
        + connect()
    }

    class VehiculoDB {
        + placa: str
    }

    class HistorialDB {
        - str _placa
        - int _id_espacio
        - str _hora_entrada
        - str _hora_salida
        - float _tarifa
        + HistorialDB(placa, id_espacio, hora_entrada, hora_salida, tarifa, host, user, password, database)
        + placa: str
        + id_espacio: int
        + hora_entrada: str
        + hora_salida: str
        + tarifa: float
        + agregar_historial()
        + obtener_historial_por_placa()
        + obtener_todo_el_historial()
        + actualizar_historial_salida(hora_salida, tarifa)
        + cerrar_conexion()
    }

    class ConnectorDB {
        + connect()
    }

    class ParqueaderoDB {
        + id_espacio: int
    }

    class VehiculoDB {
        + placa: str
    }

    

    HistorialDB --|> ConnectorDB
    HistorialDB o-- ParqueaderoDB : id_espacio
    HistorialDB o-- VehiculoDB : placa
    ParqueaderoDB --|> ConnectorDB
    VehiculoDB --|> ConnectorDB
    VehiculoDB o-- PropietarioDB : Tienen un
    PropietarioDB --|> ConnectorDB
```


### `PropietarioDB`
Esta clase se usa para instanciar diferentes datos del propietario, ademas de contar con sus diferentes setters and getters, ademas de una funcion que nos devuelve todos estos datos recopilados en un diccionario
``` mermaid
classDiagram
class PropietarioDB {
        - int _id_propietario
        - str _nombre
        - str _telefono
        - str _correo
        + PropietarioDB(identificacion, nombre, telefono, correo, host, user, password, database)
        + id_propietario: int
        + nombre: str
        + telefono: str
        + correo: str
        + agregar_propietario()
        + obtener_propietario_por_id()
        + actualizar_propietario()
        + eliminar_propietario(id_propietario)
        + obtener_propietarios()
        + cerrar_conexion()
    }
```
### `VehiculoDB`
Esta clase se utiliza para crear diferentes vehículos, aprovechando las características que los diferencian, como su placa o su propietario. Además, incluye métodos para acceder a información privada, como los datos del usuario.

``` mermaid
classDiagram
class VehiculoDB {
        - str _placa
        - str _tipo
        - int _propietario
        + VehiculoDB(placa, tipo, propietario, host, user, password, database)
        + placa: str
        + tipo: str
        + propietario: int
        + agregar_vehiculo()
        + obtener_vehiculo_por_placa()
        + actualizar_vehiculo()
        + eliminar_vehiculo()
        + obtener_vehiculos()
        + cerrar_conexion()
    }


    VehiculoDB  <|-- Bicicleta
    VehiculoDB <|-- Moto
    VehiculoDB <|-- Carro
```
### `ConectorDB`
Esta clase calcula el tiempo que estuvo el vehiculo en el parqueadero.
``` mermaid
classDiagram
class ConnectorDB {
        - str host
        - str user
        - str password
        - str database
        - connection
        - cursor
        + ConnectorDB(host, user, password, database)
        + connect()
    }
```
### `HistorialDB`
Esta clase utiliza datetime para calcular el tiempo que un vehículo permanece en el parqueadero. Posteriormente, multiplica el tiempo, dado en segundos, por la tarifa correspondiente a cada clase de vehículo.
``` mermaid
classDiagram
class HistorialDB {
        - str _placa
        - int _id_espacio
        - str _hora_entrada
        - str _hora_salida
        - float _tarifa
        + HistorialDB(placa, id_espacio, hora_entrada, hora_salida, tarifa, host, user, password, database)
        + placa: str
        + id_espacio: int
        + hora_entrada: str
        + hora_salida: str
        + tarifa: float
        + agregar_historial()
        + obtener_historial_por_placa()
        + obtener_todo_el_historial()
        + actualizar_historial_salida(hora_salida, tarifa)
        + cerrar_conexion()
    }

```
### `ParqueaderoDB`
Esta clase genera atributos que contiene información sobre el estado de cada espacio.
``` mermaid
classDiagram
class ParqueaderoDB {
        - int _id_espacio
        - str _tipo
        - str _placa
        - str _estado
        + ParqueaderoDB(id_espacio, tipo, placa, estado, host, user, password, database)
        + id_espacio: int
        + tipo: str
        + placa: str
        + estado: str
        + crear_espacios(cantidad, tipo)
        + ocupar_espacio()
        + desocupar_espacio()
        + obtener_espacios()
        + obtener_espacio_por_placa()
        + obtener_espacios_libres()
        + cerrar_conexion()
    }
```
# CONTROLLER

``` mermaid
classDiagram
    class HomeController {
        +Flask app
        +home() : render_template
    }

    class PropietarioController {
        +Flask app
        +registrar_propietario() : render_template
    }

    class VehiculoController {
        +Flask app
        +registrar_vehiculo() : render_template
    }

    class ParqueaderoController {
        +Flask app
        +mostrar_espacios() : render_template
        +obtener_espacios() : jsonify
        +ocupar_espacio() : jsonify
        +liberar_espacio() : jsonify
        +calcular_tarifa(hora_entrada, hora_salida) : float
    }

    class ExportarHistorialCSV {
        +HistorialDB historial_db
        +generar_csv(nombre_archivo) : void
    }

    class PropietarioDB {
        +identificacion: str
        +nombre: str
        +telefono: str
        +correo: str
        +agregar_propietario() : void
        +obtener_propietario_por_id() : PropietarioDB
        +cerrar_conexion() : void
    }

    class VehiculoDB {
        +placa: str
        +tipo: str
        +propietario_id: str
        +agregar_vehiculo() : void
        +obtener_vehiculo_por_placa() : VehiculoDB
        +cerrar_conexion() : void
    }

    class ParqueaderoDB {
        +id_espacio: int
        +tipo: str
        +placa: str
        +estado: str
        +obtener_espacios() : list
        +ocupar_espacio() : void
        +desocupar_espacio() : void
        +cerrar_conexion() : void
    }

    class HistorialDB {
        +placa: str
        +id_espacio: int
        +hora_entrada: datetime
        +hora_salida: datetime
        +tarifa: float
        +agregar_historial() : void
        +obtener_historial_por_placa() : list
        +actualizar_historial_salida(hora_salida, tarifa) : void
        +obtener_todo_el_historial() : list
        +cerrar_conexion() : void
    }

    HomeController --> Flask
    PropietarioController --> Flask
    VehiculoController --> Flask
    ParqueaderoController --> Flask
    ExportarHistorialCSV --> HistorialDB
    PropietarioController --> PropietarioDB
    VehiculoController --> VehiculoDB
    ParqueaderoController --> ParqueaderoDB
    ParqueaderoController --> HistorialDB
    HistorialDB --> ParqueaderoDB
    HistorialDB --> VehiculoDB
    VehiculoDB --> PropietarioDB
``` 

## Resultado

El desarrollo del sistema de gestión de parqueaderos dio como resultado una aplicación web funcional que permite la administración eficiente de los espacios de estacionamiento. Se implementaron diversas interfaces que facilitan la interacción del usuario, incluyendo pantallas para el registro de propietarios y vehículos, la visualización de espacios disponibles y el control del historial de uso del parqueadero.

En cuanto al almacenamiento de datos, se lograron registrar propietarios con información detallada (nombre, identificación, contacto), así como vehículos asociados a cada usuario. Además, el sistema almacena el historial de entradas y salidas de los vehículos, calculando automáticamente la tarifa correspondiente en función del tiempo de uso.

Para la gestión del parqueadero, se desarrollaron funcionalidades clave, como la ocupación y liberación de espacios en tiempo real, con respuestas inmediatas a través de la API. Asimismo, se implementó la opción de exportar el historial en formato CSV, facilitando la consulta y análisis de datos.

Finalmente, el modelo relacional y el diagrama de clases reflejan la estructura del sistema, evidenciando la correcta integración entre los distintos módulos y garantizando su escalabilidad y mantenimiento a futuro.

# View

![Home](https://github.com/Fabian0611/Project_POO/blob/main/Interfaz_home.jpg?raw=true)

![Página registro de vehículo](https://github.com/Fabian0611/Project_POO/blob/main/Registro_de_veh%C3%ADculo.jpg?raw=true)

# RECURSOS USADOS

### Flask
Es un framework web en Python que usamos para desarrollar la API del sistema de gestión de parqueaderos. Nos permitió manejar solicitudes HTTP, conectar la base de datos y facilitar la comunicación entre la interfaz y la lógica del sistema.
### MySQL 
Fue utilizado como el sistema de gestión de bases de datos para almacenar y administrar la información del parqueadero. Su uso permitió manejar grandes volúmenes de datos de manera estructurada y eficiente.
### CVS
El formato CSV se utilizó para exportar y almacenar registros históricos de manera simple y accesible.
Funciones clave:
Generación de reportes: Permitió exportar el historial de parqueo en un formato compatible con herramientas externas como Excel.






