import xml.etree.ElementTree as ET
from xml.dom import minidom
import json
import re
import datetime

class PrecioInvalidoError(Exception): pass       #Control de errores

class ObjectError(Exception): pass

class Cliente:      #Client class
    def __init__(self, dni: str, nombre: str, fecha_nacimiento: datetime.date):
        if not re.fullmatch(r"\d{8}[A-HJ-NP-TV-Z]$", dni):
            raise ValueError('Dni invalido')
        self.dni = dni
        self.nombre = nombre
        self.fecha_nacimiento = fecha_nacimiento
        self.edad = self.calcular_edad()

    def calcular_edad(self):
        hoy = datetime.date.today()
        edad = hoy.year - self.fecha_nacimiento.year

        if (hoy.month, hoy.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day):
            edad -= 1
        return edad

class Vehiculo:       #Clase Madre
    def __init__(self, matricula: str, marca: str, precio_base_dia: float):
        if precio_base_dia < 0:     #Control de errores, el precio no puede ser negativo
            raise PrecioInvalidoError('El precio base de dia no puede ser negativo')
        self.precio_base_dia = float(precio_base_dia)
        self.matricula = matricula
        self.marca = marca

    def __str__(self):
        return f'{self.matricula}, {self.marca}'


class Renting:
    def __init__(self, cliente: Cliente, vehiculo: Vehiculo, fecha_fin: datetime.date):
        self.cliente = cliente
        self.vehiculo = vehiculo
        self.fecha_inicio = datetime.date.today()
        self.fecha_fin = fecha_fin
        diferencia = self.fecha_fin - datetime.date.today()
        dias_alquiler = diferencia.days
        self.extras = {}
        self.precio_final = self.calcular_precio(dias_alquiler)


    def calcular_precio(self, dias_alquiler): #Funcion para calcular el precio final
        ext = input('¿Qué extra desea? Intro para terminar. ')
        while ext != "":
            valor = float(input('Ingrese el precio del extra: '))
            self.extras[ext] = valor
            ext = input('Ingrese otro extra, Intro para terminar: ')

        self.precio_final = (self.vehiculo.precio_base_dia + sum(self.extras.values())) * dias_alquiler
        return self.precio_final

    def to_dict(self):
        return {
            "cliente": str(self.cliente.dni),  # Guardamos el DNI/Nombre
            "vehiculo": str(self.vehiculo.matricula),  # Guardamos la matrícula
            "fecha_inicio": self.fecha_inicio.isoformat(),  # "2024-05-20"
            "fecha_fin": self.fecha_fin.isoformat(),
            "precio_final": self.precio_final,
            "extras": self.extras
        }
def insertar_cliente(cliente):
    archivo = 'gestionclientes.xml'
    try:
        tree = ET.parse(archivo)
        root = tree.getroot()
    except (FileNotFoundError, ET.ParseError):
        root = ET.Element("clientes")
        tree = ET.ElementTree(root)

    nuevo = ET.SubElement(root, "cliente")
    ET.SubElement(nuevo, 'dni').text = cliente.dni
    ET.SubElement(nuevo, 'nombre').text = cliente.nombre
    # Convertimos fecha y edad a string, si no, dará error
    ET.SubElement(nuevo, 'fecha_nacimiento').text = str(cliente.fecha_nacimiento)
    ET.SubElement(nuevo, 'edad').text = str(cliente.edad)

    # Generamos el XML con formato "bonito"
    xml_bytes = ET.tostring(root, encoding='utf-8')
    xml_pretty = minidom.parseString(xml_bytes).toprettyxml(indent="  ")

    # Usamos 'w' para que el archivo siempre sea un XML válido y único
    with open(archivo, 'w', encoding='utf-8') as xml_file:
        xml_file.write(xml_pretty)
    print('Cliente creado con éxito')

def insertar_vehiculo_xml(vehiculo): #Función para añadir vehículos a XML
    archivo = 'gestioncoches.xml'
    try:
        tree = ET.parse(archivo)
        root = tree.getroot()
        for elem in root.iter():    #Se eliminan los saltos de lineas extra
            elem.tail = None
            if elem.text and not elem.text.strip(): elem.text = None
    except (FileNotFoundError, ET.ParseError):
        root = ET.Element("concesionario")
        tree = ET.ElementTree(root)

    nuevo = ET.SubElement(root, 'coche')
    ET.SubElement(nuevo, "matricula").text = vehiculo.matricula
    ET.SubElement(nuevo, "marca").text = vehiculo.marca
    ET.SubElement(nuevo, "precio").text = str(vehiculo.precio_base_dia) #Se convierte el precio a str para poder almacenarlo

    lineas = minidom.parseString(ET.tostring(root)).toprettyxml(indent="  ").splitlines()
    pretty_xml = "\n".join(l for l in lineas if l.strip())

    with open(archivo, 'w', encoding='utf-8') as f:
        f.write(pretty_xml)

    print('Vehiculo añadido con exito')


def buscar_cliente_xml(dni_buscado):
    try:
        tree = ET.parse('gestionclientes.xml')  # Asegúrate de que el nombre coincida
        root = tree.getroot()
        for node in root.findall('cliente'):
            if node.find('dni').text == dni_buscado:
                nombre = node.find('nombre').text
                fecha_str = node.find('fecha_nacimiento').text
                # Convertimos el texto "1996-11-12" de nuevo a objeto date
                fecha_obj = datetime.date.fromisoformat(fecha_str)
                return Cliente(dni_buscado, nombre, fecha_obj)
    except FileNotFoundError:
        return None
    return None


def buscar_vehiculo_xml(matricula_buscada):
    tree = ET.parse('gestioncoches.xml')
    root = tree.getroot()

    for coche_node in root.findall('coche'):
        if coche_node.find('matricula').text == matricula_buscada:
            precio = float(coche_node.find('precio').text)
            marca = coche_node.find('marca').text
            return Vehiculo(matricula = matricula_buscada,marca = marca, precio_base_dia = precio)
    return None

def menu(): #Creamos la función menú en el caso de querer traducirlo, que somos muy internacionales
    print('--- MENÚ ---')
    print('1. Añadir vehículos.')
    print('2. Añadir clientes.')
    print('3. Mostrar vehículos disponibles.')
    print('4. Alquilar.')
    print('5. Salir.')


def main():
    vehiculo_alquilado = {}
    while True: #Iniciamos el bucle del menú
        menu()     #imprimimos el menú
        opcion = input('Ingrese su opcion: ')
        match opcion:
            case '1':
                try:
                    matricula= input('Ingrese la matricula: ')
                    matriculamayus = matricula.upper()
                    marca = input('Ingrese la marca: ')
                    precio_base_dia = float(input('Ingrese el precio: '))
                    bicicleta = Vehiculo(matriculamayus, marca, precio_base_dia)
                        #Objeto creado, añadimos a xml
                except ValueError:
                    print(f'Valor incorrecto, inténtelo de nuevo.')
                except PrecioInvalidoError as e:        #Control de errores
                    print(e)
                else:
                    insertar_vehiculo_xml(bicicleta)
            case '2':
                try:
                    dni = input('Ingrese DNI: ')
                    dnimayus = dni.upper()
                    nombre = input('Ingrese el nombre completo: ')
                    dia = int(input('Ingrese su día de nacimiento: '))
                    mes = int(input('Ingrese su mes de nacimiento: '))
                    año = int(input('Ingrese su año de nacimiento: '))
                    nacimiento = datetime.date(año, mes, dia)
                    client1 = Cliente(dnimayus, nombre, nacimiento)

                except ValueError as e:
                    print(e)
                else:
                    insertar_cliente(client1) #Solo se añade el cliente en caso de que se cree la clase con éxito

            case '3': #Mostramos los vehículos disponibles
                try:
                    tree = ET.parse('gestioncoches.xml')
                    root = tree.getroot()
                    encontrados = False

                    print("\n--- VEHÍCULOS DISPONIBLES ---")
                    for vehiculo in root.findall('coche'):
                        matricula = vehiculo.find('matricula').text
                        # Solo mostramos si NO está en el diccionario de alquilados
                        if matricula not in vehiculo_alquilado:
                            marca = vehiculo.find('marca').text
                            precio = vehiculo.find('precio').text
                            print(f"Matrícula: {matricula} | Marca: {marca} | Precio/día: {precio}€")
                            encontrados = True

                    if not encontrados:
                        print("No hay vehículos disponibles en este momento.")

                except FileNotFoundError:
                    print("Error: No existe el archivo Vehiculos.xml")

            case '4':   #Código para alquilar
                try:
                    id_cliente = input("Ingrese el DNI del cliente: ")
                    id_clientemayus = id_cliente.upper()
                    cliente_real = buscar_cliente_xml(id_clientemayus)
                    if not cliente_real:
                        raise ObjectError('Cliente no encontrado')
                    id_coche = input("Ingrese la matrícula del coche: ")
                    id_cochemayus = id_coche.upper()
                    vehiculo_real = buscar_vehiculo_xml(id_cochemayus)
                    if not vehiculo_real:
                        raise ObjectError("Vehículo no encontrado")
                    fin_day = input("Día de finalizacion: ")
                    fin_month = input("Mes de finalizacion: ")
                    fin_year = input("Año de finalizacion: ")
                    fecha_fin = datetime.date(int(fin_year), int(fin_month), int(fin_day))
                    alquiler1 = Renting(cliente_real, vehiculo_real, fecha_fin)

                    with open('gestionalquiler.json', 'w') as f:
                        json.dump(alquiler1.to_dict(), f, indent=4)
                        f.write('\n')

                except ValueError as e: print(e)
                except ObjectError as e: print(e)
                else:
                    print(f'El precio total es {alquiler1.precio_final}')
                    vehiculo_alquilado[vehiculo_real.matricula] = datetime.date.today()
            case '5':     #Salida
                print('...Saliendo...')
                break
            case _:
                print('Error, intentelo de nuevo')



if __name__ == '__main__':
    main()