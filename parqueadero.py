import json
import datetime
import csv

# Clase que representa a un propietario de un vehiculo
class Propietario:
    def __init__(self, identificacion, nombre, telefono, correo):
        self.__id_propietario = identificacion
        self.__nombre = nombre
        self.__telefono = telefono
        self.__correo = correo

    # Metodos para obtener y establecer los atributos del propietario
    def get_id_propietario(self):
        return self.__id_propietario

    def get_nombre(self):
        return self.__nombre

    def set_nombre(self, nuevo_nombre):
        self.__nombre = nuevo_nombre

    def get_telefono(self):
        return self.__telefono

    def set_telefono(self, nuevo_telefono):
        self.__telefono = nuevo_telefono

    def get_correo(self):
        return self.__correo

    def set_correo(self, nuevo_correo):
        self.__correo = nuevo_correo

    # Metodo para obtener la información de contacto del propietario
    def obtener_contacto(self):
        return {
            "ID Propietario": self.__id_propietario,
            "Nombre": self.__nombre,
            "Telefono": self.__telefono,
            "Correo": self.__correo,
        }


# Clase que representa un vehiculo
class Vehiculo:
    def __init__(self, placa, tipo, propietario):
        self.__placa = placa
        self.__tipo = tipo
        self.__propietario = propietario

    # Metodos para obtener y establecer los atributos del vehículo
    def get_placa(self):
        return self.__placa

    def set_placa(self, nueva_placa):
        self.__placa = nueva_placa

    def get_tipo(self):
        return self.__tipo

    def set_tipo(self, nuevo_tipo):
        self.__tipo = nuevo_tipo

    def get_propietario(self):
        return self.__propietario

    def set_propietario(self, nuevo_propietario):
        self.__propietario = nuevo_propietario

    # Metodo para obtener la informacion del vehiculo
    def obtener_informacion(self):
        return {
            "Placa": self.__placa,
            "Tipo": self.__tipo,
            "Propietario ID": self.__propietario.get_id_propietario(),
        }


# Clases que representan tipos especificos de vehiculos
class Carro(Vehiculo):
    def __init__(self, placa, propietario):
        super().__init__(placa, "Carro", propietario)


class Moto(Vehiculo):
    def __init__(self, placa, propietario):
        super().__init__(placa, "Moto", propietario)


class Bici(Vehiculo):
    def __init__(self, placa, propietario):
        super().__init__(placa, "Bici", propietario)


# Clase que maneja la base de datos de propietarios y vehiculos
class BaseDatos:
    def __init__(self, archivo):
        self.archivo = archivo
        self.__propietarios = {}
        self.__vehiculos = []
        self.__historial = []
        self.__cargar_datos()

    # Metodo para cargar datos desde un archivo JSON
    def __cargar_datos(self):
        try:
            with open(self.archivo, "r") as file:
                datos = json.load(file)
                for propietario in datos.get("Propietarios", []):
                    self.__propietarios[propietario["ID Propietario"]] = Propietario(
                        propietario["ID Propietario"],
                        propietario["Nombre"],
                        propietario["Telefono"],
                        propietario["Correo"],
                    )
                for vehiculo in datos.get("Vehiculos", []):
                    propietario_id = vehiculo["Propietario ID"]
                    if propietario_id in self.__propietarios:
                        propietario = self.__propietarios[propietario_id]
                        if vehiculo["Tipo"] == "Carro":
                            vehiculo_obj = Carro(vehiculo["Placa"], propietario)
                        elif vehiculo["Tipo"] == "Moto":
                            vehiculo_obj = Moto(vehiculo["Placa"], propietario)
                        elif vehiculo["Tipo"] == "Bici":
                            vehiculo_obj = Bici(vehiculo["Placa"], propietario)
                        else:
                            continue
                        self.__vehiculos.append(vehiculo_obj)
                self.__historial = datos.get("Historial", [])
        except FileNotFoundError:
            print(f"Archivo '{self.archivo}' no encontrado. Se creará uno nuevo.")
        except Exception as e:
            print(f"Error al cargar datos: {e}")

    # Metodos para agregar propietarios, vehículos e historial a la base de datos
    def agregar_propietario(self, propietario):
        self.__propietarios[propietario.get_id_propietario()] = propietario

    def agregar_vehiculo(self, vehiculo):
        if all(v.get_placa() != vehiculo.get_placa() for v in self.__vehiculos):
            self.__vehiculos.append(vehiculo)

    def agregar_historial(self, placa, hora_entrada, hora_salida, tarifa):
        historial = {
            "Placa": placa,
            "Hora de entrada": hora_entrada,
            "Hora de salida": hora_salida,
            "Tarifa": tarifa,
        }
        self.__historial.append(historial)

    # Metodo para guardar los datos en un archivo JSON
    def generar_json(self):
        datos = {
            "Propietarios": [p.obtener_contacto() for p in self.__propietarios.values()],
            "Vehiculos": [v.obtener_informacion() for v in self.__vehiculos],
            "Historial": self.__historial,
        }
        try:
            with open(self.archivo, "w") as file:
                json.dump(datos, file, indent=4)
            print("Datos guardados correctamente.")
        except IOError as e:
            print(f"Error al escribir el archivo JSON: {e}")


# Clase que calcula el tiempo que un vehículo ha estado en el parqueadero
class HorasEnElParqueadero:
    def __init__(self, fecha_hora_entrada, fecha_hora_salida):
        self.fecha_hora_entrada = fecha_hora_entrada
        self.fecha_hora_salida = fecha_hora_salida

    # Metodo para calcular el tiempo en segundos entre la entrada y la salida
    def calcular_tiempo_en_segundos(self):
        formato = "%Y-%m-%d %H:%M"
        entrada_dt = datetime.datetime.strptime(self.fecha_hora_entrada, formato)
        salida_dt = datetime.datetime.strptime(self.fecha_hora_salida, formato)

        diferencia = (salida_dt - entrada_dt).total_seconds()

        if diferencia < 0:
            raise ValueError("La fecha y hora de salida no pueden ser anteriores a la entrada.")

        return diferencia


# Clase que calcula la tarifa a pagar segun el tiempo y tipo de vehículo
class Tarifa:
    def __init__(self, segundos):
        self.segundos = segundos

    # Metodo para calcular la tarifa basada en el tipo de vehiculo y el tiempo en segundos
    def calcular_tarifa(self, tipo_vehiculo):
        tipo_vehiculo = tipo_vehiculo.get_tipo()

        tarifas = {
            "Carro": 4000, 
            "Moto": 3000,
            "Bici": 400,
        }
        tarifa_base = tarifas.get(tipo_vehiculo, 0)
        if tarifa_base == 0:
            return "Tipo de vehículo no válido"

        horas = self.segundos / 3600
        return tarifa_base * horas

# Clase que maneja el parqueadero y sus espacios
class Parqueadero:
    def __init__(self, filas_carros, columnas_carros, filas_motos, columnas_motos, filas_bicis, columnas_bicis):
        self.espacios_carros = [[{"placa": "", "hora": ""} for _ in range(columnas_carros)] for _ in range(filas_carros)]
        self.espacios_motos = [[{"placa": "", "hora": ""} for _ in range(columnas_motos)] for _ in range(filas_motos)]
        self.espacios_bicis = [[{"placa": "", "hora": ""} for _ in range(columnas_bicis)] for _ in range(filas_bicis)]

    # Metodo para ocupar un espacio en el parqueadero
    def ocupar_espacio(self, fila, columna, vehiculo, hora):
        tipo_vehiculo = vehiculo.get_tipo()
        
        if tipo_vehiculo == "Carro":
            matriz = self.espacios_carros
        elif tipo_vehiculo == "Moto":
            matriz = self.espacios_motos
        elif tipo_vehiculo == "Bici":
            matriz = self.espacios_bicis
        else:
            raise ValueError("Tipo de vehículo no válido. Use 'Carro', 'Moto' o 'Bici'.")

        fila -= 1  # Ajuste a base 0
        columna -= 1  # Ajuste a base 0

        if matriz[fila][columna]["placa"]:
            raise ValueError("El espacio ya está ocupado.")
        
        matriz[fila][columna] = {"placa": vehiculo.get_placa(), "hora": hora}

    # Metodo para liberar un espacio en el parqueadero
    def liberar_espacio(self, fila, columna, vehiculo, hora_salida):
        tipo_vehiculo = vehiculo.get_tipo() 

        if tipo_vehiculo == "Carro":
            matriz = self.espacios_carros
        elif tipo_vehiculo == "Moto":
            matriz = self.espacios_motos  
        elif tipo_vehiculo == "Bici":
            matriz = self.espacios_bicis
        else:
            raise ValueError("Tipo de vehículo no válido. Use 'Carro', 'Moto' o 'Bici'.")

        fila -= 1 
        columna -= 1  

        if not matriz[fila][columna]["placa"]:
            raise ValueError("El espacio ya está vacío.")

        placa = matriz[fila][columna]["placa"]
        hora_entrada = matriz[fila][columna]["hora"]
        matriz[fila][columna] = {"placa": "", "hora": ""}

        return {"placa": placa, "hora_entrada": hora_entrada, "hora_salida": hora_salida}

    # Metodo para mostrar el estado del parqueadero
    def mostrar_parqueadero(self):
        print("Estado del Parqueadero:")
        print("\nEspacios para Carros:")
        self._mostrar_matriz(self.espacios_carros)
        print("\nEspacios para Motos:")
        self._mostrar_matriz(self.espacios_motos)
        print("\nEspacios para Bicis:")
        self._mostrar_matriz(self.espacios_bicis)

    # Metodo auxiliar para mostrar una matriz de espacios
    def _mostrar_matriz(self, matriz):
        for i, fila in enumerate(matriz):
            fila_str = [f"[{espacio['placa']}]" if espacio["placa"] else "[LIBRE]" for espacio in fila]
            print(f"Fila {i + 1}: " + " ".join(fila_str))


# Clase que maneja los datos de los vehiculos y genera reportes
class ManejadorDatosVehiculos:
    def __init__(self, archivo_json):
        with open(archivo_json, 'r') as archivo:
            self.datos = json.load(archivo)

    # Metodo para generar un archivo CSV con los datos de los vehiculos
    def generar_csv(self, archivo_salida):
        with open(archivo_salida, mode='w', newline='', encoding='utf-8') as archivo_csv:
            escritor = csv.writer(archivo_csv)
            escritor.writerow(["Placa", "Tipo", "ID Propietario", "Nombre", "Telefono", "Correo", "Hora de entrada", "Hora de salida", "Tarifa"])
            
            for vehiculo in self.datos["Vehiculos"]:
                for registro in self.datos["Historial"]:
                    if vehiculo["Placa"] == registro["Placa"]:
                        propietario = next((p for p in self.datos["Propietarios"] if p["ID Propietario"] == vehiculo["Propietario ID"]), None)
                        if propietario:
                            escritor.writerow([
                                vehiculo["Placa"],
                                vehiculo["Tipo"],
                                propietario["ID Propietario"],
                                propietario["Nombre"],
                                propietario["Telefono"],
                                propietario["Correo"],
                                registro["Hora de entrada"],
                                registro["Hora de salida"],
                                registro["Tarifa"]
                            ])

    # Metodo para generar una cadena con los datos de los vehiculos
    def generar_cadena(self):
        resultado = []
        for vehiculo in self.datos["Vehiculos"]:
            for registro in self.datos["Historial"]:
                if vehiculo["Placa"] == registro["Placa"]:
                    propietario = next((p for p in self.datos["Propietarios"] if p["ID Propietario"] == vehiculo["Propietario ID"]), None)
                    if propietario:
                        resultado.append(f"Placa: {vehiculo['Placa']}, Tipo: {vehiculo['Tipo']}, Propietario: {propietario['Nombre']}, Telefono: {propietario['Telefono']}, Correo: {propietario['Correo']}, Hora de entrada: {registro['Hora de entrada']}, Hora de salida: {registro['Hora de salida']}, Tarifa: {registro['Tarifa']}\n")
        return "".join(resultado)


# Codigo principal para probar las clases y metodos
if __name__ == "__main__":
    filas_carros = int(input("Ingrese el numero de filas para carros: "))
    columnas_carros = int(input("Ingrese el numero de columnas para carros: "))
    filas_motos = int(input("Ingrese el numero de filas para motos: "))
    columnas_motos = int(input("Ingrese el numero de columnas para motos: "))
    filas_bicis = int(input("Ingrese el numero de filas para bicicletas: "))
    columnas_bicis = int(input("Ingrese el numero de columnas para bicicletas: "))
    
    parqueadero = Parqueadero(filas_carros, columnas_carros, filas_motos, columnas_motos, filas_bicis, columnas_bicis)

    num_vehiculos = int(input("Ingrese el numero de vehiculos a registrar: "))
    vehiculos = []

    for _ in range(num_vehiculos):
        cedula = input("Ingrese la cedula del propietario: ")
        nombre = input("Ingrese el nombre del propietario: ")
        telefono = input("Ingrese el Telefono del propietario: ")
        correo = input("Ingrese el correo del propietario: ")
        propietario = Propietario(cedula, nombre, telefono, correo)

        tipo_vehiculo = input("Ingrese el tipo de vehículo (bici/carro/moto): ").strip().lower()
        placa = input("Ingrese la placa del vehículo: ") 
        
        if tipo_vehiculo == "bici":
            vehiculo = Bici(placa, propietario)
        elif tipo_vehiculo == "moto":
            vehiculo = Moto(placa, propietario)
        elif tipo_vehiculo == "carro":
            vehiculo = Carro(placa, propietario)
        else:
            print("Tipo de vehículo no válido.")
            exit()

        vehiculos.append((vehiculo, propietario))

    for vehiculo, propietario in vehiculos:
        print("\n OCUPAR ESPACIO ")
        fila_ocupar = int(input("Ingrese la fila donde estacionara: "))
        columna_ocupar = int(input("Ingrese la columna donde estacionara: "))
        hora_actual = input("Ingrese la hora actual (YYYY-MM-DD HH:MM): ")
        parqueadero.ocupar_espacio(fila_ocupar, columna_ocupar, vehiculo, hora_actual)
        parqueadero.mostrar_parqueadero()
    
    for vehiculo, propietario in vehiculos:
        print("\n LIBERAR ESPACIO ")
        fila_ocupar = int(input("Ingrese la fila donde estaba estacionado: "))
        columna_ocupar = int(input("Ingrese la columna donde estaba estacionado: "))
        hora_salida = input("Ingrese la hora de salida (YYYY-MM-DD HH:MM): ")
        informe = parqueadero.liberar_espacio(fila_ocupar, columna_ocupar, vehiculo, hora_salida)
        print(f"Placa: {informe['placa']}, Hora entrada: {informe['hora_entrada']}, Hora salida: {informe['hora_salida']}")

        horas = HorasEnElParqueadero(informe["hora_entrada"], informe["hora_salida"])
        tiempo_segundos = horas.calcular_tiempo_en_segundos()
        tarifa = Tarifa(tiempo_segundos).calcular_tarifa(vehiculo)

        base_datos = BaseDatos("base_datos.json")
        base_datos.agregar_propietario(propietario)
        base_datos.agregar_vehiculo(vehiculo)
        base_datos.agregar_historial(informe["placa"], informe["hora_entrada"], informe["hora_salida"], tarifa)
        base_datos.generar_json()

        print(f"Tarifa calculada: ${tarifa:.2f}")

    print("\n ESTADO FINAL DEL PARQUEADERO ")
    parqueadero.mostrar_parqueadero()

    manejador = ManejadorDatosVehiculos('base_datos.json')
    manejador.generar_csv('salida.csv')
    print(manejador.generar_cadena())