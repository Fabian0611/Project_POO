from flask import Flask, render_template, request, jsonify, send_file
import os
from models.modelos import PropietarioDB, VehiculoDB, ParqueaderoDB, HistorialDB  # Asegúrate de que este archivo y clase existen correctamente
from datetime import datetime
import csv

class HomeController:
    def __init__(self, app: Flask):
        """
        Constructor de la clase HomeController.
        Se encarga de configurar las rutas para la aplicación Flask.
        """
        self.app = app
        self.setup_routes()  # Configura las rutas de la aplicación.

    def setup_routes(self):
        """
        Define las rutas de la aplicación Flask.
        En este caso, se configura la ruta principal ('/') para mostrar la página de inicio.
        """
        self.app.add_url_rule('/', 'home', self.home)  # Ruta principal de la aplicación.

    def home(self):
        """
        Maneja la solicitud a la ruta principal ('/').
        Renderiza y devuelve la plantilla HTML de la página de inicio.
        """
        return render_template('home.html')



class PropietarioController:
    def __init__(self, app: Flask):
        """
        Constructor de la clase PropietarioController.
        Se encarga de configurar las rutas para la gestión de propietarios.
        """
        self.app = app
        self.setup_routes()  # Configura las rutas de la aplicación.

    def setup_routes(self):
        """
        Define las rutas de la aplicación Flask relacionadas con propietarios.
        En este caso, se configura la ruta para registrar un propietario.
        """
        self.app.add_url_rule('/registrar_propietario', 'registrar_propietario', 
                              self.registrar_propietario, methods=['GET', 'POST'])

    def registrar_propietario(self):
        """
        Maneja la visualización del formulario y el registro de propietarios.
        - Si la solicitud es GET, muestra el formulario de registro.
        - Si la solicitud es POST, obtiene los datos del formulario y registra al propietario.
        """
        if request.method == 'POST':
            # Obtener datos del formulario
            identificacion = request.form['identificacion']
            nombre = request.form['nombre']
            telefono = request.form['telefono']
            correo = request.form['correo']

            # Crear una instancia de PropietarioDB con los datos ingresados
            propietario = PropietarioDB(identificacion, nombre, telefono, correo)

            # Verificar si el propietario ya está registrado en la base de datos
            if propietario.obtener_propietario_por_id():
                # Si ya existe, renderizar la página con un mensaje de error
                return render_template('registro_propietario.html', registrado=False)

            # Si no existe, proceder con el registro
            propietario.agregar_propietario()
            propietario.cerrar_conexion()  # Cerrar la conexión a la base de datos

            # Mostrar mensaje de éxito en la plantilla
            return render_template('registro_propietario.html', registrado=True)

        # Si la solicitud es GET, mostrar el formulario sin estado de registro
        return render_template('registro_propietario.html', registrado=None)


class VehiculoController:
    def __init__(self, app: Flask):
        """
        Constructor de la clase VehiculoController.
        Se encarga de configurar las rutas para la gestión de vehículos.
        """
        self.app = app
        self.setup_routes()  # Configura las rutas de la aplicación.

    def setup_routes(self):
        """
        Define las rutas de la aplicación Flask relacionadas con vehículos.
        En este caso, se configura la ruta para registrar un vehículo.
        """
        self.app.add_url_rule('/registrar_vehiculo', endpoint='registrar_vehiculo', 
                              view_func=self.registrar_vehiculo, methods=['GET', 'POST'])

    def registrar_vehiculo(self):
        """
        Maneja la visualización del formulario y el registro de vehículos.
        - Si la solicitud es GET, muestra el formulario de registro.
        - Si la solicitud es POST, obtiene los datos del formulario y registra el vehículo.
        """
        if request.method == 'POST':
            # Obtener datos del formulario
            placa = request.form['placa']
            tipo = request.form['tipo']
            propietario_id = request.form['propietario']

            # Crear instancias de VehiculoDB y PropietarioDB para validar los datos
            vehiculo = VehiculoDB(placa, tipo, propietario_id)
            propietario = PropietarioDB(propietario_id, None, None, None)

            # Verificar si el vehículo ya está registrado en la base de datos
            if vehiculo.obtener_vehiculo_por_placa():
                return render_template('registro_vehiculo.html', registrado=False, 
                                       mensaje="El vehículo ya está registrado.")
            
            # Verificar si el propietario existe antes de registrar el vehículo
            if not propietario.obtener_propietario_por_id():
                return render_template('registro_vehiculo.html', propietario_existente=False, mensaje="El propietario no está registrado.")

            # Si el propietario existe y el vehículo no está registrado, proceder con el registro
            vehiculo.agregar_vehiculo()
            
            # Cerrar conexiones a la base de datos
            vehiculo.cerrar_conexion()
            propietario.cerrar_conexion()
            
            return render_template('registro_vehiculo.html', registrado=True, propietario_existente=True, mensaje="Vehículo registrado exitosamente.")

        # Si la solicitud es GET, mostrar el formulario sin estado de registro
        return render_template('registro_vehiculo.html', registrado=None, propietario_existente=None, mensaje=None)


class ParqueaderoController:
    def __init__(self, app: Flask):
        """
        Constructor de la clase ParqueaderoController.
        Se encarga de configurar las rutas para la gestión del parqueadero.
        """
        self.app = app
        self.setup_routes()  # Configuración de las rutas de la aplicación.

    def setup_routes(self):
        """
        Define las rutas de la aplicación Flask relacionadas con el parqueadero.
        """
        self.app.add_url_rule('/mostrar_espacios', 'mostrar_espacios', self.mostrar_espacios)
        self.app.add_url_rule('/espacios', 'obtener_espacios', self.obtener_espacios, methods=['GET'])
        self.app.add_url_rule('/ocupar_espacio', 'ocupar_espacio', self.ocupar_espacio, methods=['POST'])
        self.app.add_url_rule('/liberar_espacio', 'liberar_espacio', self.liberar_espacio, methods=['POST'])
        self.app.add_url_rule('/exportar_historial', 'exportar_historial', self.exportar_historial, methods=['GET'])

    def mostrar_espacios(self):
        """
        Muestra la página principal del parqueadero.
        """
        return render_template('parqueadero.html')

    def obtener_espacios(self):
        """
        Obtiene todos los espacios del parqueadero y los retorna en formato JSON.
        """
        db = ParqueaderoDB(None, None, None, None)
        espacios = db.obtener_espacios()
        db.cerrar_conexion()
        
        espacios_json = [{
            "id_espacio": esp[0], 
            "tipo": esp[1], 
            "placa": esp[2], 
            "estado": esp[3]
        } for esp in espacios]

        return jsonify({"espacios": espacios_json})

    def ocupar_espacio(self):
        """
        Ocupa un espacio en el parqueadero, validando la existencia del vehículo y su compatibilidad con el espacio.
        """
        data = request.get_json()
        id_espacio = data.get('id_espacio')
        placa = data.get('placa')
        hora_entrada = datetime.now()

        # Validación de datos
        if not id_espacio or not placa:
            return jsonify({'success': False, 'error': 'Datos inválidos'}), 400

        try:
            # Verificar si el vehículo está registrado
            vehiculo_db = VehiculoDB(placa, None, None)
            vehiculo = vehiculo_db.obtener_vehiculo_por_placa()
            vehiculo_db.cerrar_conexion()

            if not vehiculo:
                return jsonify({'success': False, 'error': 'Vehículo no registrado'}), 404

            _, tipo_vehiculo, _ = vehiculo  # Extraer el tipo de vehículo

            # Consultar el estado y tipo del espacio
            db = ParqueaderoDB(id_espacio, None, None, None)
            query = "SELECT tipo, estado FROM Parqueadero WHERE id_espacio = %s"
            db.cursor.execute(query, (id_espacio,))
            resultado = db.cursor.fetchone()

            if not resultado:
                db.cerrar_conexion()
                return jsonify({'success': False, 'error': 'El espacio no existe'}), 404

            tipo_espacio, estado_actual = resultado

            # Validar si el espacio está libre
            if estado_actual != 'libre':
                db.cerrar_conexion()
                return jsonify({'success': False, 'error': 'El espacio ya está ocupado'}), 400

            # Validar si el tipo de vehículo coincide con el tipo de espacio
            if tipo_vehiculo.lower() != tipo_espacio.lower():
                db.cerrar_conexion()
                return jsonify({'success': False, 'error': f'El espacio es para {tipo_espacio}, no para {tipo_vehiculo}'}), 400

            # Registrar la ocupación del espacio
            db.placa = placa
            db.estado = 'ocupado'
            db.ocupar_espacio()

            # Registrar la entrada en el historial
            historial_db = HistorialDB(placa, id_espacio, hora_entrada, None, None)
            historial_db.agregar_historial()

            db.cerrar_conexion()
            historial_db.cerrar_conexion()

            return jsonify({'success': True})

        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500

    def liberar_espacio(self):
        """
        Libera un espacio del parqueadero y calcula la tarifa a pagar.
        """
        data = request.get_json()
        id_espacio = data.get('id_espacio')
        placa = data.get('placa')

        if not id_espacio or not placa:
            return jsonify({'success': False, 'error': 'Datos inválidos'}), 400

        try:
            db_espacio = ParqueaderoDB(id_espacio, None, None, None)
            estado_espacio = db_espacio.obtener_estado_espacio()

            if estado_espacio[0] != 'ocupado':
                return jsonify({'success': False, 'error': 'El espacio no está ocupado'}), 400

            placa_ocupante = db_espacio.obtener_placa_ocupante()

            if placa_ocupante[0] != placa:
                return jsonify({'error': f'La placa {placa} no coincide con el vehículo en el espacio'}), 400

            hora_salida = datetime.now()
            historial_db = HistorialDB(placa, id_espacio, None, None, None)
            historial = historial_db.ultimo_historial_por_placa()

            if historial:
                hora_entrada = historial[2]
                tarifa = self.calcular_tarifa(hora_entrada, hora_salida)

                historial_db.actualizar_historial_salida(hora_salida, tarifa)
                db_espacio.desocupar_espacio()

                db_espacio.cerrar_conexion()
                historial_db.cerrar_conexion()

                return jsonify({
                    'success': True, 
                    'placa': placa, 
                    'tarifa': tarifa
                })

            return jsonify({'success': False, 'error': 'No se encontró historial de entrada'}), 404

        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500

    def calcular_tarifa(self, hora_entrada, hora_salida):
        """
        Calcula la tarifa según el tiempo de uso del espacio.
        """
        diferencia = (hora_salida - hora_entrada).total_seconds() / 3600  
        tarifa_por_hora = 5000  # Tarifa estándar (puede ajustarse según el tipo de vehículo)
        return round(diferencia * tarifa_por_hora, 2)

    def exportar_historial(self):
        """
        Exporta el historial de parqueo en un archivo CSV y lo envía como descarga.
        """
        exportador = ExportarHistorialCSV()
        nombre_archivo = "historial.csv"
        exportador.generar_csv(nombre_archivo)

        if os.path.exists(nombre_archivo):
            return send_file(nombre_archivo, as_attachment=True, mimetype='text/csv')
        else:
            return jsonify({'success': False, 'error': 'No se pudo generar el archivo CSV'}), 500
        
    
class ExportarHistorialCSV:
    """
    Clase encargada de exportar el historial de parqueo en formato CSV.
    """

    def __init__(self):
        """
        Constructor de la clase. Inicializa la conexión con la base de datos del historial.
        """
        self.historial_db = HistorialDB(None, None, None, None, None)

    def generar_csv(self, nombre_archivo="historial.csv"):
        """
        Genera un archivo CSV con el historial de parqueo.
        """
        # Obtener todos los registros del historial desde la base de datos
        datos = self.historial_db.obtener_todo_el_historial()

        # Validar si hay datos en el historial
        if not datos:
            print("No hay datos en el historial para exportar.")
            return

        # Crear y escribir en el archivo CSV
        with open(nombre_archivo, mode="w", newline="", encoding="utf-8") as archivo_csv:
            escritor_csv = csv.writer(archivo_csv)

            # Escribir la fila de encabezados
            escritor_csv.writerow(["Placa", "ID Espacio", "Hora Entrada", "Hora Salida", "Tarifa"])

            # Escribir los datos obtenidos de la base de datos
            escritor_csv.writerows(datos)

        print(f"El archivo '{nombre_archivo}', tu historial, está listo ;)")