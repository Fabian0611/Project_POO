import mysql.connector  # Importa el módulo para conectarse a bases de datos MySQL

class ConnectorDB:
    def __init__(self, host="localhost", user="root", password="", database="parqueadero"):
        """
        Constructor de la clase ConnectorDB.
        Inicializa los parámetros de conexión a la base de datos.
        """
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None  # Almacena la conexión a la base de datos
        self.cursor = None  # Almacena el cursor para ejecutar consultas

    def connect(self):
        """
        Método para establecer la conexión con la base de datos.
        Si la conexión es exitosa, se crea un cursor para ejecutar consultas SQL.
        En caso de error, se captura la excepción y se muestra un mensaje de error.
        """
        try:
            # Intenta establecer la conexión con MySQL
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            self.cursor = self.connection.cursor()  # Crea un cursor para ejecutar consultas
            print("Conexión exitosa a la base de datos")
        except mysql.connector.Error as err:
            # Captura errores en la conexión y los muestra en consola
            print(f"Error de conexión: {err}")



class PropietarioDB(ConnectorDB):
    def __init__(self, identificacion, nombre, telefono, correo, host="localhost", user="root", password="12345678", database="parqueadero"):
        """
        Constructor de la clase PropietarioDB que hereda de ConnectorDB.
        Se encarga de inicializar los datos del propietario y establecer la conexión con la base de datos.
        """
        super().__init__(host, user, password, database)  # Llama al constructor de la clase padre
        self._id_propietario = identificacion
        self._nombre = nombre
        self._telefono = telefono
        self._correo = correo
        self.connect()  # Establece la conexión con la base de datos

    # Métodos getter y setter para los atributos privados del propietario
    @property
    def id_propietario(self):
        """Devuelve la identificación del propietario."""
        return self._id_propietario

    @property
    def nombre(self):
        """Devuelve el nombre del propietario."""
        return self._nombre

    @nombre.setter
    def nombre(self, nuevo_nombre):
        """Permite modificar el nombre del propietario."""
        self._nombre = nuevo_nombre

    @property
    def telefono(self):
        """Devuelve el número de teléfono del propietario."""
        return self._telefono

    @telefono.setter
    def telefono(self, nuevo_telefono):
        """Permite modificar el número de teléfono del propietario."""
        self._telefono = nuevo_telefono

    @property
    def correo(self):
        """Devuelve el correo electrónico del propietario."""
        return self._correo

    @correo.setter
    def correo(self, nuevo_correo):
        """Permite modificar el correo electrónico del propietario."""
        self._correo = nuevo_correo

    def agregar_propietario(self):
        """
        Inserta un nuevo propietario en la base de datos.
        """
        query = "INSERT INTO propietarios (id_propietario, nombre, telefono, correo) VALUES (%s, %s, %s, %s)"
        valores = (self.id_propietario, self.nombre, self.telefono, self.correo)  # Se corrigió un error: antes se repetía self.nombre en lugar de self.telefono
        self.cursor.execute(query, valores)
        self.connection.commit()  # Guarda los cambios en la base de datos

    def obtener_propietario_por_id(self):
        """
        Obtiene la información de un propietario por su identificación.
        """
        query = "SELECT id_propietario, nombre, telefono, correo FROM propietarios WHERE id_propietario = %s"
        self.cursor.execute(query, (self.id_propietario,))
        return self.cursor.fetchone()  # Devuelve una sola fila del resultado

    def actualizar_propietario(self):
        """
        Actualiza los datos de un propietario en la base de datos.
        """
        query = "UPDATE propietarios SET nombre = %s, telefono = %s, correo = %s WHERE id_propietario = %s"
        valores = (self.nombre, self.telefono, self.correo, self.id_propietario)
        self.cursor.execute(query, valores)
        self.connection.commit()  # Guarda los cambios en la base de datos

    def eliminar_propietario(self):
        """
        Elimina un propietario de la base de datos usando su identificación.
        """
        query = "DELETE FROM propietarios WHERE id_propietario = %s"
        self.cursor.execute(query, (self.id_propietario,))
        self.connection.commit()  # Guarda los cambios en la base de datos

    def obtener_propietarios(self):
        """
        Obtiene todos los propietarios registrados en la base de datos.
        """
        query = "SELECT id_propietario, nombre, telefono, correo FROM propietarios"
        self.cursor.execute(query)
        return self.cursor.fetchall()  # Devuelve todas las filas del resultado

    def cerrar_conexion(self):
        """
        Cierra la conexión con la base de datos y libera los recursos.
        """
        self.cursor.close()
        self.connection.close()


class VehiculoDB(ConnectorDB):
    def __init__(self, placa, tipo, propietario, host="localhost", user="root", password="12345678", database="parqueadero"):
        """
        Constructor de la clase VehiculoDB que hereda de ConnectorDB.
        Se encarga de inicializar los datos del vehículo y establecer la conexión con la base de datos.
        """
        super().__init__(host, user, password, database)  # Llama al constructor de la clase padre
        self._placa = placa
        self._tipo = tipo
        self._propietario = propietario
        self.connect()  # Establece la conexión con la base de datos

    # Métodos getter y setter para los atributos privados del vehículo
    @property
    def placa(self):
        """Devuelve la placa del vehículo."""
        return self._placa

    @placa.setter
    def placa(self, nueva_placa):
        """Permite modificar la placa del vehículo."""
        self._placa = nueva_placa

    @property
    def tipo(self):
        """Devuelve el tipo de vehículo."""
        return self._tipo

    @tipo.setter
    def tipo(self, nuevo_tipo):
        """Permite modificar el tipo de vehículo."""
        self._tipo = nuevo_tipo

    @property
    def propietario(self):
        """Devuelve el ID del propietario del vehículo."""
        return self._propietario

    @propietario.setter
    def propietario(self, nuevo_propietario):
        """Permite modificar el propietario del vehículo."""
        self._propietario = nuevo_propietario

    def agregar_vehiculo(self):
        """
        Inserta un nuevo vehículo en la base de datos.
        """
        query = "INSERT INTO vehiculos (placa, tipo, id_propietario) VALUES (%s, %s, %s)"
        valores = (self.placa, self.tipo, self.propietario)
        self.cursor.execute(query, valores)
        self.connection.commit()  # Guarda los cambios en la base de datos

    def obtener_vehiculo_por_placa(self):
        """
        Obtiene la información de un vehículo por su placa.
        """
        query = "SELECT placa, tipo, id_propietario FROM vehiculos WHERE placa = %s"
        valor = (self.placa,)
        self.cursor.execute(query, valor)
        return self.cursor.fetchone()  # Devuelve una sola fila del resultado

    def actualizar_vehiculo(self):
        """
        Actualiza los datos de un vehículo en la base de datos.
        """
        query = "UPDATE vehiculos SET tipo = %s, id_propietario = %s WHERE placa = %s"
        valores = (self.tipo, self.propietario, self.placa)
        self.cursor.execute(query, valores)
        self.connection.commit()  # Guarda los cambios en la base de datos

    def eliminar_vehiculo(self):
        """
        Elimina un vehículo de la base de datos usando su placa.
        """
        query = "DELETE FROM vehiculos WHERE placa = %s"
        self.cursor.execute(query, (self.placa,))
        self.connection.commit()  # Guarda los cambios en la base de datos

    def obtener_vehiculos(self):
        """
        Obtiene todos los vehículos registrados en la base de datos.
        """
        query = "SELECT placa, tipo, id_propietario FROM vehiculos"
        self.cursor.execute(query)
        return self.cursor.fetchall()  # Devuelve todas las filas del resultado

    def cerrar_conexion(self):
        """
        Cierra la conexión con la base de datos y libera los recursos.
        """
        self.cursor.close()
        self.connection.close()


class ParqueaderoDB(ConnectorDB):
    def __init__(self, id_espacio, tipo, placa, estado, host="localhost", user="root", password="12345678", database="parqueadero"):
        """
        Constructor de la clase ParqueaderoDB que hereda de ConnectorDB.
        Se encarga de inicializar los datos del espacio de parqueo y establecer la conexión con la base de datos.
        """
        super().__init__(host, user, password, database)  # Llama al constructor de la clase padre
        self._id_espacio = id_espacio
        self._tipo = tipo
        self._placa = placa
        self._estado = estado
        self.connect()  # Establece la conexión con la base de datos

    # Métodos getter y setter para los atributos privados del espacio de parqueo
    @property
    def id_espacio(self):
        """Devuelve el ID del espacio de parqueo."""
        return self._id_espacio

    @property
    def tipo(self):
        """Devuelve el tipo de espacio de parqueo."""
        return self._tipo

    @tipo.setter
    def tipo(self, tipo):
        """Permite modificar el tipo de espacio de parqueo."""
        self._tipo = tipo

    @property
    def placa(self):
        """Devuelve la placa del vehículo que ocupa el espacio (None si está libre)."""
        return self._placa

    @placa.setter
    def placa(self, placa):
        """Permite asignar o modificar la placa del vehículo en el espacio de parqueo."""
        self._placa = placa

    @property
    def estado(self):
        """Devuelve el estado del espacio de parqueo (libre u ocupado)."""
        return self._estado

    @estado.setter
    def estado(self, estado):
        """Permite modificar el estado del espacio de parqueo."""
        self._estado = estado

    def crear_espacios(self, cantidad, tipo):
        """
        Crea múltiples espacios de parqueo del mismo tipo y los marca como "libre".
        """
        query = "INSERT INTO Parqueadero (tipo, estado) VALUES (%s, 'libre')"
        valores = [(tipo,) for _ in range(cantidad)]  # Crea una lista de valores para insertar múltiples filas
        self.cursor.executemany(query, valores)
        self.connection.commit()  # Guarda los cambios en la base de datos

    def ocupar_espacio(self):
        """
        Asigna un vehículo a un espacio de parqueo, marcándolo como "ocupado".
        Solo ocupa el espacio si está libre.
        """
        query = "UPDATE Parqueadero SET placa = %s, estado = 'ocupado' WHERE id_espacio = %s AND estado = 'libre'"
        valores = (self.placa, self.id_espacio)
        self.cursor.execute(query, valores)
        self.connection.commit()  # Guarda los cambios en la base de datos

    def desocupar_espacio(self):
        """
        Libera un espacio de parqueo, eliminando la placa y marcándolo como "libre".
        """
        query = "UPDATE Parqueadero SET estado = 'libre', placa = NULL WHERE id_espacio = %s"
        valores = (self._id_espacio,)
        self.cursor.execute(query, valores)
        self.connection.commit()  # Guarda los cambios en la base de datos

    def obtener_espacios(self):
        """
        Obtiene todos los espacios de parqueo registrados en la base de datos.
        """
        query = "SELECT id_espacio, tipo, placa, estado FROM Parqueadero"
        self.cursor.execute(query)
        return self.cursor.fetchall()  # Devuelve todas las filas del resultado

    def obtener_espacio_por_placa(self):
        """
        Obtiene la información de un espacio de parqueo basado en la placa del vehículo.
        """
        query = "SELECT id_espacio, tipo, placa, estado FROM Parqueadero WHERE placa = %s"
        self.cursor.execute(query, (self.placa,))
        return self.cursor.fetchone()  # Devuelve una sola fila del resultado

    def obtener_espacios_libres(self):
        """
        Obtiene una lista de espacios de parqueo que están libres.
        """
        query = "SELECT id_espacio, tipo FROM Parqueadero WHERE estado = 'libre'"
        self.cursor.execute(query)
        return self.cursor.fetchall()  # Devuelve todas las filas del resultado

    def obtener_estado_espacio(self):
        """
        Obtiene el estado de un espacio de parqueo específico.
        """
        query = "SELECT estado FROM Parqueadero WHERE id_espacio = %s"
        self.cursor.execute(query, (self.id_espacio,))
        return self.cursor.fetchone()  # Devuelve una sola fila del resultado

    def obtener_placa_ocupante(self):
        """
        Obtiene la placa del vehículo que está ocupando un espacio de parqueo específico.
        """
        query = "SELECT placa FROM Parqueadero WHERE id_espacio = %s"
        self.cursor.execute(query, (self.id_espacio,))
        return self.cursor.fetchone()  # Devuelve una sola fila del resultado

    def cerrar_conexion(self):
        """
        Cierra la conexión con la base de datos y libera los recursos.
        """
        self.cursor.close()
        self.connection.close()



class HistorialDB(ConnectorDB):
    def __init__(self, placa, id_espacio, hora_entrada, hora_salida, tarifa, host="localhost", user="root", password="12345678", database="parqueadero"):
        """
        Constructor de la clase HistorialDB que hereda de ConnectorDB.
        Se encarga de inicializar los datos del historial de estacionamiento y establecer la conexión con la base de datos
        """
        super().__init__(host, user, password, database)  # Llama al constructor de la clase padre
        self._placa = placa
        self._id_espacio = id_espacio
        self._hora_entrada = hora_entrada
        self._hora_salida = hora_salida
        self._tarifa = tarifa
        self.connect()  # Establece la conexión con la base de datos

    # Métodos getter y setter para los atributos privados del historial
    @property
    def placa(self):
        """Devuelve la placa del vehículo asociado al historial."""
        return self._placa 

    @property
    def id_espacio(self):
        """Devuelve el ID del espacio de parqueo utilizado."""
        return self._id_espacio

    @property
    def hora_entrada(self):
        """Devuelve la fecha y hora de entrada del vehículo al parqueadero."""
        return self._hora_entrada

    @property
    def hora_salida(self):
        """Devuelve la fecha y hora de salida del vehículo del parqueadero."""
        return self._hora_salida

    @property
    def tarifa(self):
        """Devuelve la tarifa cobrada por el uso del parqueadero."""
        return self._tarifa

    @placa.setter
    def placa(self, placa):
        """Permite modificar la placa del vehículo en el historial."""
        self._placa = placa

    @id_espacio.setter
    def id_espacio(self, id_espacio):
        """Permite modificar el ID del espacio de parqueo en el historial."""
        self._id_espacio = id_espacio

    @hora_entrada.setter
    def hora_entrada(self, hora_entrada):
        """Permite modificar la hora de entrada en el historial."""
        self._hora_entrada = hora_entrada

    @hora_salida.setter
    def hora_salida(self, hora_salida):
        """Permite modificar la hora de salida en el historial."""
        self._hora_salida = hora_salida

    @tarifa.setter
    def tarifa(self, tarifa):
        """Permite modificar la tarifa en el historial."""
        self._tarifa = tarifa

    def agregar_historial(self):
        """
        Registra una nueva entrada en el historial de parqueo cuando un vehículo ingresa al parqueadero.
        """
        query = "INSERT INTO historial (placa, id_espacio, hora_entrada, hora_salida, tarifa) VALUES (%s, %s, %s, %s, %s)"
        valores = (self.placa, self.id_espacio, self.hora_entrada, self.hora_salida, self.tarifa)
        self.cursor.execute(query, valores)
        self.connection.commit()  # Guarda los cambios en la base de datos

    def obtener_historial_por_placa(self):
        """
        Obtiene todo el historial de un vehículo basado en su placa.
        """
        query = "SELECT placa, id_espacio, hora_entrada, hora_salida, tarifa FROM historial WHERE placa = %s"
        self.cursor.execute(query, (self.placa,))
        return self.cursor.fetchall()  # Devuelve todas las filas del resultado

    def actualizar_historial_salida(self, hora_salida, tarifa):
        """
        Actualiza la hora de salida y la tarifa de un registro en el historial cuando un vehículo sale del parqueadero.
        """
        query = "UPDATE historial SET hora_salida = %s, tarifa = %s WHERE placa = %s AND id_espacio = %s AND hora_salida IS NULL"
        valores = (hora_salida, tarifa, self._placa, self._id_espacio)
        self.cursor.execute(query, valores)
        self.connection.commit()  # Guarda los cambios en la base de datos

    def ultimo_historial_por_placa(self):
        """
        Obtiene el último registro en el historial de un vehículo basado en su placa.
        """
        query = "SELECT placa, id_espacio, hora_entrada, hora_salida, tarifa FROM historial WHERE placa = %s ORDER BY hora_entrada DESC LIMIT 1"
        self.cursor.execute(query, (self.placa,))
        return self.cursor.fetchone()  # Devuelve la última fila del resultado

    def obtener_todo_el_historial(self):
        """
        Obtiene todos los registros del historial del parqueadero.
        """
        query = "SELECT placa, id_espacio, hora_entrada, hora_salida, tarifa FROM historial"
        self.cursor.execute(query)
        return self.cursor.fetchall()  # Devuelve todas las filas del resultado

    def cerrar_conexion(self):
        """
        Cierra la conexión con la base de datos y libera los recursos.
        """
        self.cursor.close()
        self.connection.close()


'''db_parqueadero = ParqueaderoDB(1, "Carro", "ABC123", "libre")
db_parqueadero.crear_espacios(15, "Carro")
print(db_parqueadero.obtener_espacios())
db_parqueadero.cerrar_conexion()
'''


