import os
import getpass as gp
import archivos
import cuentas
import constantes as const
import configuracion 
import random
# from DepositoObligatorioParaRegistrarUsuario import tasaDeCambio 
from constantes import \
    cedula, \
    pin, \
    retirarDinero, \
    depositarDinero, \
    verSaldoActual, \
    pagarServicios, \
    compraVentaDivisas, \
    eliminarUsuario ,\
    salirUsuario, \
    carpetaUsuarios, \
    maximoIntentos \

#----------------------------GENERADOR DE SERVICIOS ALEATOREOS PARA EL USUARIO -------------------------------
def generarServiciosAleatorios(cedula): # Se define una función llamada "generarServiciosAleatorios()" que se encargará de seleccionar aleatoriamente tres servicios activos.
    listaServiciosTotales = ["Electricidad", "Agua", "Telefonia", "Internet", "Impuestos", "Colegios Profesionales", "Tarjeta de credito"] #Se define una lista que contiene todos los servicios disponibles.
    serviciosAleatorios = random.sample([servicio for servicio in listaServiciosTotales if not isinstance(servicio, (int, float))], k=3) #Se crea una lista de tres elementos que contiene una selección aleatoria de servicios activos. Los servicios aleatorios se seleccionan de la listaServiciosTotales utilizando la función "random.sample()" y se filtran los elementos que no son cadenas.
    serviciosActivos = {} #Se crea un diccionario vacío que contendrá los servicios activos seleccionados junto con el monto aleatorio generado para cada uno de ellos.
    monto = 0
    for servicio in serviciosAleatorios: #Se repite a través de cada servicio en la lista de servicios aleatorios.
        if servicio == "Electricidad":
            monto = const.electricidad
        elif servicio == "Agua":
            monto = const.agua
        elif servicio == "Telefonia":
            monto = const.telefonia, 
        elif servicio == "Internet":
            monto = const.internet
        elif servicio == "Impuestos":
            monto = const.impuestos
        elif servicio == "Colegios Profesionales":
            monto = const.colegiosProfesionales
        elif servicio == "Tarjeta de crédito":
            monto = const.tarjetaDeCredito
        serviciosActivos[servicio] = {"monto": monto, "activo": True}
    rutaServiciosActivos = f"{const.carpetaUsuarios}/{cedula}/ServiciosActivos.txt"
    with open(rutaServiciosActivos, "w") as archivoServiciosActivos: #Se abre el archivo "ServiciosActivos.txt" en modo escritura.
        for servicio, info in serviciosActivos.items(): #Se repite a través del diccionario serviciosActivos y se desempaqueta el servicio y su información.
            archivoServiciosActivos.write(f"{servicio}: Monto a pagar: {info['monto']}, Servicio activo: {info['activo']}\n") #Se agrega al diccionario serviciosActivos el servicio y sus detalles, incluido el monto y el valor del servicio activo.

    rutaServiciosNoActivos = f"{const.carpetaUsuarios}/{cedula}/ServiciosNoActivos.txt"
    serviciosNoActivos = [servicio for servicio in listaServiciosTotales if servicio not in serviciosActivos] # Crea una lista de los servicios que no estan activos que contiene los servicios totales que no están en los servicios activos.
    with open(rutaServiciosNoActivos, "w") as archivoServiciosNoActivos: # Abre un archivo llamado Servicios No Activos en modo escritura.
        for servicio in serviciosNoActivos: # Se repite sobre la lista serviciosNoActivos.
            archivoServiciosNoActivos.write(servicio + "\n") #Escribe cada servicio en el archivo ServiciosNoActivos
            
def leerServiciosActivos(): #Define una función leerServiciosActivos 
    with open("serviciosActivos.txt", "r") as archivoServiciosActivos: #Abre el archivo serviciosActivos en modo lectura y lo asocia con el nombre de variable archivoServiciosActivos.
        for linea in archivoServiciosActivos: # Se repite sobre las líneas del archivo archivoServiciosActivos.
            print(linea)#Imprime cada línea en la consola.
            
def leerServiciosNoActivos():#Define una función leerServiciosNoActivos que no toma argumentos.
    with open("ServiciosNoActivos.txt", "r") as archivoServiciosNoActivos: #Abre el archivo ServiciosNoActivos en modo lectura y lo asocia con el nombre de variable 
        for linea in archivoServiciosNoActivos: #  Se repite sobre las líneas del archivo archivoServiciosNoActivos.
            print(linea) #Imprime cada línea en la consola.

#----------------------------FIN DEL GENERADOR DE SERVICIOS ALEATOREOS PARA EL USUARIO -------------------------------

def cargarUsuarios():
    todosLosDirectorios = archivos.listarDirectorios(carpetaUsuarios)
    usuarios = []

    for directorio in todosLosDirectorios:
        infoUsuario = []

        with archivos.abrirArchivo(f"{carpetaUsuarios}/{directorio}", "info", "r") as archivoUsuario:
            infoUsuario = archivoUsuario.readlines()

        usuarios.append([info.rstrip('\n') for info in infoUsuario])

    return usuarios

def existenUsuarios(usuarios):
    return len(usuarios) > 0


def existeLaCedula(cedulaInput, usuarios):
    for usuario in usuarios:
        if usuario[cedula] == cedulaInput:
            return True
    return False


def esValidoElPIN(cedulaInput, pinInput, usuarios):
    for usuario in usuarios:
        if usuario[cedula] == cedulaInput and usuario[pin] == pinInput:
            return True
    return False


def solicitarCedula():
    return input("Ingrese su cédula: ")


def solicitarPIN():
    return gp.getpass("Ingrese su PIN: ")


def autenticarUsuario(usuarios):
    # Solicitar y validar la cedula --------------------------------------------
    intentos = 1

    while True:
        cedula = solicitarCedula()
        intentosRestantes = maximoIntentos - intentos
        if existeLaCedula(cedula, usuarios):
            break
        elif intentosRestantes > 0:
            print(f'Cedula incorrecta. Intente de nuevo... (intentos restantes: {intentosRestantes})')
            intentos += 1
        else:
            print('Ha alcanzado el maximo de intentos.')
            return [False, None]
    # ---------------------------------------------------------------------------

    # Solicitar y validar el PIN ------------------------------------------------
    intentos = 1

    while True:
        pin = solicitarPIN()
        intentosRestantes = maximoIntentos - intentos
        if esValidoElPIN(cedula, pin, usuarios):
            break
        elif intentosRestantes > 0:
            print(f'PIN incorrecto. Intente de nuevo... (intentos restantes: {intentosRestantes})')
            intentos += 1
        else:
            print('Ha alcanzado el maximo de intentos.')
            return [False, None]
    # ---------------------------------------------------------------------------

    return [True, cedula]


def mostrarSubmenu():
    print("\n+========== USUARIO REGISTRADO ==========+")
    print("| 1. Retirar dinero                      |")
    print("| 2. Depositar dinero                    |")
    print("| 3. Ver saldo actual                    |")
    print("| 4. Pagar servicios                     |")
    print("| 5. Compra/Venta de Divisas             |")
    print("| 6. Eliminar usuario                    |")
    print("| 7. Salir                               |")
    print("+========================================+")


def pagarServicio(servicio, costo, tasaDeCambio, cedula):
    # Verificar si tiene el servicio activo
    print("Saldo a pagar: {}".format(costo))
    carpeta = f"{carpetaUsuarios}/{cedula}"
    monedas = ["colones", "dolares", "bitcoins"]
    moneda = int(input("Con cual cuenta deseas hacer el deposito?\n1-Colones\n2-Dolares\n3-Bitcoins\n")) -1
    saldos = cuentas.cargarSaldos(carpeta)
    # Calcular el monto a pagar
    pago = costo/tasaDeCambio[moneda]
    # Verificar si el usuario tiene suficiente dinero en la cuenta seleccionada
    if saldos[moneda] >= pago:
        #Reducir pago de la cuenta
        saldos[moneda] -= pago
        cuentas.guardarSaldos(carpeta, saldos) #aqui se guarda en la carpeta de saldos, el nuevo saldo con el monto ya debitado,
        # Mostrar confirmación de pago
        print("El saldo de la cuenta en {} es de {}. Se ha realizado un pago de {} {} por el servicio de {}.".format(monedas[moneda], saldos[moneda], pago, monedas[moneda], servicio))
    else:
        # Mostrar mensaje de error
        print("No hay suficiente saldo en la cuenta en {} para realizar el pago.".format(monedas[moneda]))


def menuPagarServicios(cedula):
    # Opción de pagar servicios
    while True:
        print("\n+=========== PAGAR SERVICIOS ============+")
        print("| 1. Electricidad                        |")
        print("| 2. Agua                                |")
        print("| 3. Telefonia                           |")
        print("| 4. Internet                            |")
        print("| 5. Impuestos                           |")
        print("| 6. Colegios profesionales              |")
        print("| 7. Tarjeta de credito                  |")
        print("| 8. Salir                               |")
        print("+========================================+")

        opcion = int(input())
        config = configuracion.cargarConfiguracion()
        tasaDeCambio = [
            1, 
            float(config[const.ventaDolaresAColones]), 
            float(config[const.ventaBitcoinAColones]), 
        ]
        servicios = [
            "Electricidad",
            "Agua",
            "Telefonia",
            "Internet",
            "Impuestos",
            "Colegios profesionales",
            "Tarjeta de credito",
        ]
        serviciosNoActivos = []
        with archivos.abrirArchivo(f"{const.carpetaUsuarios}/{cedula}", "ServiciosNoActivos.txt", "r") as archivo:
            serviciosNoActivos = [s.rstrip('\n') for s in archivo.readlines()]

        #VERIFICAR SI EL SERVICIO ESTA ACTIVO

        if servicios[opcion] in serviciosNoActivos:
            print('Este servicio no esta activo.')
            break

        elif opcion == const.pagoElectricidad:
            pagarServicio("electricidad", const.electricidad, tasaDeCambio, cedula)
        elif opcion == const.pagoAgua:
            pagarServicio("agua", const.agua, tasaDeCambio, cedula)
        elif opcion == const.pagoTelefonia:
            pagarServicio("telefonía", const.telefonia, tasaDeCambio, cedula)
        elif opcion == const.pagoInternet:
            pagarServicio("internet", const.internet, tasaDeCambio, cedula)
        elif opcion == const.pagoImpuestos:
            pagarServicio("impuestos", const.impuestos, tasaDeCambio, cedula)
        elif opcion == const.pagoColegiosProfesionales:
            pagarServicio("colegios profesionales", const.colegiosProfesionales, tasaDeCambio, cedula)
        elif opcion == const.pagoTarjetaDeCredito:
            pagarServicio("tarjeta de credito", const.tarjetaDeCredito, tasaDeCambio, cedula)
        elif opcion == const.pagoServicioSalir:
            break
        else:
            print('Opcion no valida, intentalo nuevamente.')
        


def flujoPrincipal(cedula):
    carpeta = f"{carpetaUsuarios}/{cedula}"
    while True:
        mostrarSubmenu()
        opcionUsuario = input('Seleccione una opcion: ')
        saldos = cuentas.cargarSaldos(carpeta)

        if opcionUsuario == retirarDinero:
            retiroValido = cuentas.retiroDeDinero(carpeta, saldos)
            if not retiroValido:
                break

        elif opcionUsuario == depositarDinero:
            cuentas.depositoDeDinero(carpeta, saldos)

        elif opcionUsuario == verSaldoActual:
            cuentas.verSaldos(saldos)

        elif opcionUsuario == pagarServicios:
            menuPagarServicios(cedula)

        elif opcionUsuario == compraVentaDivisas:
            raise NotImplementedError()

        elif opcionUsuario == eliminarUsuario:
            raise NotImplementedError()

        elif opcionUsuario == pagarServicios:
            menuPagarServicios()
            
        elif opcionUsuario == salirUsuario:
            break
        else:
            print('Opcion invalida. Intente de nuevo...')

