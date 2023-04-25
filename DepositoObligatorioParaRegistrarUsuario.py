import archivos
import cuentas
import constantes as const
import configuracion as config 
#PARTE DEL DEPOSITO

def depositoObligatorio(cedula):
    tasaDeCambio = [1, 0, 0]
    with archivos.abrirArchivo('', const.archivoConfig, 'r') as config:
        lineas = [linea.rstrip('\n') for linea in config.readlines()]
        tasaDeCambio[const.saldoDolares] = float(lineas[const.compraColonesADolares])
        tasaDeCambio[const.saldoBitcoin] = float(lineas[const.compraColonesABitcoin])

    intentos = 3 #El usuario solo tendra 3 intentos para digitar el monto minimo correcto
    while intentos > 0:
        print("Para poder ser un usuario de Global Bank Inc, debe realizar un depósito mínimo de 100,000 colones o equivalente en otra moneda.") #Imprimir un mensaje educando al usuario con el monto minimo
        print("Ingrese el tipo de moneda a utilizar:\n1-Colones\n2-Dólares\n3-Bitcoins\n") #Desplegar el menu de las opciones 

        monedas = ["colones", "dolares", "bitcoin"] #opciones de moneda disponibles.
        indiceMoneda = -1
        moneda = None

        while True: #Se inicia un bucle while que se ejecutará mientras la variable monedaValida sea falsa.
            try:
                indiceMoneda = int(input()) - 1
                moneda = monedas[indiceMoneda] # Se intenta obtener la opción de moneda seleccionada por el usuario a través de la entrada por teclado. Si se ingresa un valor no válido (que no sea 1, 2 o 3), se captura la excepción y se muestra un mensaje de error.
                break #Si se obtiene una opción de moneda válida, se cambia el valor de la variable monedaValida a True para salir del bucle.
            except (ValueError, IndexError): #En caso de obtener un error, para hacerlo facil de entender al usuario, se le educara imprimiendo un mensaje.
                print("Moneda inválida, por favor intente de nuevo.")

        #Se calcula el monto mínimo requerido para el depósito en la moneda seleccionada por el usuario.
        montoMinimo = const.montoMinimo / tasaDeCambio[indiceMoneda]
        # if moneda == "bitcoin": #Si la opción de moneda seleccionada es bitcoin, se cambia el valor del monto mínimo requerido a 0.0062.
        #   montoMinimo = 1000 

        #Se solicita al usuario que ingrese el monto que desea depositar. Se muestra en pantalla el monto mínimo requerido para el depósito en la moneda seleccionada.
        montoADepositar = float(input(f"Ingrese el monto que desea depositar (el monto mínimo es {montoMinimo} {moneda}):"))
        if montoADepositar < montoMinimo: #Si el monto ingresado por el usuario es menor que el monto mínimo requerido, se muestra un mensaje de error y se reduce el número de intentos en 1.
            intentos -= 1
            print(f"Debe depositar al menos {montoMinimo:.1f} {moneda}, por favor intente de nuevo. Le quedan {intentos} intentos.")
            if intentos == 0:
                print("Ha superado el número máximo de intentos permitidos. Volviendo al menu principal")
                return False
                #VOLVER AL PROGRAMA PRINCIPAL
        else:
            # Mostrar el monto a depositar y preguntar al usuario si desea continuar
            print("¿Desea continuar con el depósito?")
            print(f"- Monto depositado en {moneda}: {montoADepositar}")
            continuarDeposito = input("¿Desea continuar con el depósito?\n1-Si\n2-No\n")
            # Si el usuario no desea continuar, salir del bucle principal
            if continuarDeposito == "1":
                carpeta = f"{const.carpetaUsuarios}/{cedula}"
                saldos = [0, 0, 0]
                saldos[indiceMoneda] = montoADepositar
                cuentas.guardarSaldos(carpeta, saldos)
                print(f"El monto {montoADepositar:.1f} {moneda} ha sido depositado con éxito. ¡Gracias por confiar en Global Bank Inc!")
                return True
            elif continuarDeposito == "2":
                print("El usuario no ha realizado el depósito.")
                return False
                #VOLVER AL PROGRAMA PRINCIPAL
