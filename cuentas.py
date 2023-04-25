import constantes as const
import os
import archivos
from constantes import \
    archivoSaldos, \
    maximoIntentos, \
    saldoColones, \
    saldoDolares, \
    saldoBitcoin \


def cargarSaldos(carpetaUsuario):
    saldos = []
    with archivos.abrirArchivo(carpetaUsuario, archivoSaldos, "r") as archivo:
        saldos = [float(saldo.rstrip('\n')) for saldo in archivo.readlines()]
    return saldos


def guardarSaldos(carpeta, saldos):
    with archivos.abrirArchivo(carpeta, archivoSaldos, "w") as archivo:
        lineas = [str(linea) + '\n' for linea in saldos]
        archivo.writelines(lineas)


def menuDepositoDeDinero():
    print("\n+=========== DEPOSITO DINERO ===========+")
    print("| Cuentas disponibles:                  |")
    print("| 1. Colones                            |")
    print("| 2. Dólares                            |")
    print("| 3. Bitcoin                            |")
    print("+=======================================+")
    return ['1', '2', '3']


def menuRetiroDeDinero():
    print("\n+========== RETIRAR DINERO ==========+")
    print("| Cuentas disponibles:               |")
    print("| 1. Colones                         |")
    print("| 2. Dólares                         |")
    print("| 3. Bitcoin                         |")
    print("+====================================+")
    return ['1', '2', '3']


def retiroDeDinero(carpeta, saldos):
    opcionesRetiro = menuRetiroDeDinero()
    opcionRetirarDinero = input('¿De cual cuenta desea retirar dinero?\n')
    intentos = 1

    while intentos <= maximoIntentos:
        try:
            intentosRestantes = maximoIntentos - intentos
            if opcionRetirarDinero in opcionesRetiro:
                indice = int(opcionRetirarDinero) - 1
                montoRetiro = float(input('¿Cuánto desea retirar?\n'))
                if montoRetiro > 0 and saldos[indice] >= montoRetiro:
                    saldos[indice] -= montoRetiro
                    guardarSaldos(carpeta, saldos)
                    print(f'\nTransaccion exitosa. Saldo actual: {saldos[indice]}')
                    break
                elif montoRetiro <= 0:
                    intentos += 1
                    print(f'El monto a retirar debe ser mayor que cero. Intentos restantes: {intentosRestantes}')
                else:
                    intentos += 1
                    print(f'\nNo cuenta con fondos suficientes. Intentos restantes: {intentosRestantes}')
            else:
                print('Opcion invalida. Intente de nuevo...')
                break
        except ValueError:
            print('Valor invalido. Solamente se permiten valores numericos.')
    else:
        print('Ha alcanzado el maximo de intentos.')
        return False
    
    return True


def depositoDeDinero(carpeta, saldos):
    opcionesCuentas = menuDepositoDeDinero()
    opcion = input('¿A cuál cuenta desea acreditar el depósito de dinero?\n')

    try:
        if opcion in opcionesCuentas:
            indice = int(opcion) - 1
            montoDeposito = float(input('¿Cuánto desea acreditar?\n'))
            if montoDeposito > 0:
                confirmacion = input('¿Está seguro/a que desea proceder con la transacción?\n(S/N): ').upper()
                if confirmacion in ['S','N']:
                    if confirmacion == 'S':
                        saldos[indice] += montoDeposito
                        guardarSaldos(carpeta, saldos)
                        print(f'\nTransaccion exitosa. Saldo actual: {saldos[indice]}')
                    else:
                        print('Transaccion cancelada...')
                else:
                    print('Opcion invalida. Cancelando transaccion...')
            else:
                print('El monto a depositar debe ser mayor que cero. Cancelando transaccion...')

        else:
            print('Opcion invalida. Intente de nuevo...')
    except ValueError:
        print('Valor invalido. Solamente se permiten valores numericos.')


def verSaldos(saldos):
    print()
    print(f'Colones: {saldos[saldoColones]} CRC')
    print(f'Dolares: {saldos[saldoDolares]} USD')
    print(f'Bitcoin: {saldos[saldoBitcoin]} BTC')

    with open("config", 'r') as f:
        divisas = []
        for linea in f:
            fila = linea.strip().strip(',')
            divisas.append(fila)
    return divisas


def compraVentaDivisas(cedula):
    saldosUsuario = [0, 0, 0]
    #cedula = input("Por favor ingresar cedula: ")
    rutaCarpeta = './usuarios/' + cedula
    rutaSaldos =  './usuarios/{}/saldos'.format(cedula)
    with open("config", 'r') as f:
        divisas = []
        for linea in f:
            fila = linea.strip().strip(',')
            divisas.append(fila)
    with open(rutaSaldos, 'r') as f:
        saldoCuentas = []
        for linea in f:
            fila = linea.strip().strip(',')
            saldoCuentas.append(fila)
    if os.path.exists(rutaCarpeta):
        with open(rutaSaldos, 'r') as archivo:
            saldos = archivo.read()
            print("Los saldos de la cuenta {} son:".format(cedula))
            print("CRC USD BTC\nRespectivamente:")
            print(saldos)
        while True:
            opcion = int(input("""¿Qué operación desea realizar?\n1. Compra de colones\n2. Venta de colones\n3. Compra de dólares\n4. Venta de dólares\n5. Compra de bitcoin\n6. Venta de bitcoin\n7. Salir\n"""))
            if opcion == 1:
                cuenta = int(input("Seleccione la cuenta de origen\n1. Dolares\n2. Bitcoin\n"))
                if cuenta == 1: 
                    print("El equivalente en colones del dolar es: ")
                    print(divisas[const.compraColonesADolares])
                    saldoDecimal = float(saldoCuentas[1])
                    cantidad=int(input(("Cuantos Colones desea comprar?\n")))
                    conversion = cantidad/float(divisas[const.compraColonesADolares])
                    if conversion <= saldoDecimal:
                        nuevaSuma = float(saldoCuentas[0])+cantidad
                        nuevaResta = float(saldoCuentas[1])- conversion
                        saldosUsuario[0]=nuevaSuma
                        saldosUsuario[1]=nuevaResta
                        saldosUsuario[2]= saldoCuentas[2]
                        guardarSaldos(rutaCarpeta, saldosUsuario)
                        with open(rutaSaldos, 'r') as archivo:
                            saldos = archivo.read()
                            print("Los saldos de la cuenta {} son:".format(cedula))
                            print("CRC USD BTC\nRespectivamente:")
                            print(saldos)
                        break 
                    else:
                        print("Monto insuficiente")
                        break
                elif cuenta == 2:
                    print("El equivalente en colones del bitcoin es: ")
                    print(divisas[const.compraColonesABitcoin])
                    saldoDecimal = float(saldoCuentas[2])
                    cantidad=int(input(("Cuantos Colones desea comprar?\n")))
                    conversion = cantidad/float(divisas[const.compraColonesABitcoin])
                    if conversion <= saldoDecimal:
                        nuevaSuma = float(saldoCuentas[0])+cantidad
                        nuevaResta = float(saldoCuentas[2])- conversion
                        saldosUsuario[0]=nuevaSuma
                        saldosUsuario[2]=nuevaResta
                        saldosUsuario[1]= saldoCuentas[1]
                        guardarSaldos(rutaCarpeta, saldosUsuario)
                        with open(rutaSaldos, 'r') as archivo:
                            saldos = archivo.read()
                            print("Los saldos de la cuenta {} son:".format(cedula))
                            print("CRC USD BTC\nRespectivamente:")
                            print(saldos)
                        break
                    else:
                        print("Monto insuficiente")
                        break 
                else: 
                    print("Escoja una opcion valida")
            elif opcion == 2: 
                cuenta = int(input("Seleccione la cuenta de destino\n1. Dolares\n2. Bitcoin\n "))
                if cuenta == 1: 
                    print("El equivalente en colones del dolar es: ")
                    print(divisas[const.ventaColonesADolares])
                    saldoDecimal = float(saldoCuentas[0])
                    cantidad=int(input(("Cuantos Colones desea vender?\n")))
                    conversion = cantidad/float(divisas[const.ventaColonesADolares])
                    if cantidad <= saldoDecimal:
                        nuevaResta = float(saldoCuentas[0])-cantidad
                        nuevaSuma = float(saldoCuentas[1])+ conversion
                        saldosUsuario[1]=nuevaSuma
                        saldosUsuario[0]=nuevaResta
                        saldosUsuario[2]= saldoCuentas[2]
                        guardarSaldos(rutaCarpeta, saldosUsuario)
                        with open(rutaSaldos, 'r') as archivo:
                            saldos = archivo.read()
                            print("Los saldos de la cuenta {} son:".format(cedula))
                            print("CRC USD BTC\nRespectivamente:")
                            print(saldos)
                        break
                    else:
                        print("Monto insuficiente")
                        break
                elif cuenta == 2:
                    print("El equivalente en colones del bitcoin es: ")
                    print(divisas[const.ventaColonesABitcoin])
                    saldoDecimal = float(saldoCuentas[0])
                    cantidad=int(input(("Cuantos Colones desea vender?\n")))
                    conversion = cantidad/float(divisas[const.ventaColonesABitcoin])
                    if cantidad <= saldoDecimal:
                        nuevaResta = float(saldoCuentas[0])-cantidad
                        nuevaSuma = float(saldoCuentas[2])+ conversion
                        saldosUsuario[2]=nuevaSuma
                        saldosUsuario[0]=nuevaResta
                        saldosUsuario[1]= saldoCuentas[1]
                        guardarSaldos(rutaCarpeta, saldosUsuario)
                        with open(rutaSaldos, 'r') as archivo:
                            saldos = archivo.read()
                            print("Los saldos de la cuenta {} son:".format(cedula))
                            print("CRC USD BTC\nRespectivamente:")
                            print(saldos)
                        break
                    else:
                        print("Monto insuficiente")
                        break 
                else: 
                    print("Escoja una opcion valida")
            elif opcion == 3:
                cuenta = int(input("Seleccione la cuenta de origen\n1. Colones\n2. Bitcoin\n "))
                if cuenta == 1:  
                    print("El equivalente en dolares del colon es: ")
                    print(divisas[const.compraDolaresAColones])
                    saldoDecimal = float(saldoCuentas[0])
                    cantidad=int(input(("Cuantos Dolares desea comprar?\n")))
                    conversion = cantidad/float(divisas[const.compraDolaresAColones])
                    if conversion <= saldoDecimal:
                        nuevaSuma = float(saldoCuentas[1])+cantidad
                        nuevaResta = float(saldoCuentas[0])- conversion
                        saldosUsuario[1]=nuevaSuma
                        saldosUsuario[0]=nuevaResta
                        saldosUsuario[2]= saldoCuentas[2]
                        guardarSaldos(rutaCarpeta, saldosUsuario)
                        with open(rutaSaldos, 'r') as archivo:
                            saldos = archivo.read()
                            print("Los saldos de la cuenta {} son:".format(cedula))
                            print("CRC USD BTC\nRespectivamente:")
                            print(saldos)
                        break 
                    else:
                        print("Monto insuficiente")
                        break
                elif cuenta == 2:
                    print("El equivalente en dolares del bitcoin es: ")
                    print(divisas[const.compraDolaresABitcoin])
                    saldoDecimal = float(saldoCuentas[2])
                    cantidad=int(input(("Cuantos Dolares desea comprar?\n")))
                    conversion = cantidad/float(divisas[const.compraDolaresABitcoin])
                    if conversion <= saldoDecimal:
                        nuevaSuma = float(saldoCuentas[1])+cantidad
                        nuevaResta = float(saldoCuentas[2])- conversion
                        saldosUsuario[1]=nuevaSuma
                        saldosUsuario[2]=nuevaResta
                        saldosUsuario[0]= saldoCuentas[0]
                        guardarSaldos(rutaCarpeta, saldosUsuario)
                        with open(rutaSaldos, 'r') as archivo:
                            saldos = archivo.read()
                            print("Los saldos de la cuenta {} son:".format(cedula))
                            print("CRC USD BTC\nRespectivamente:")
                            print(saldos)
                        break 
                    else:
                        print("Monto insuficiente")
                        break 
                else: 
                    print("Escoja una opcion valida")
            elif opcion == 4:
                cuenta = int(input("Seleccione la cuenta de destino\n1. Colones\n2. Bitcoin\n "))
                if cuenta == 1: 
                    print("El equivalente en dolares del colon es: ")
                    print(divisas[const.ventaDolaresAColones])
                    saldoDecimal = float(saldoCuentas[1])
                    cantidad=int(input(("Cuantos Dolares desea vender?\n")))
                    conversion = cantidad/float(divisas[const.ventaDolaresAColones])
                    if cantidad <= saldoDecimal:
                        nuevaResta = float(saldoCuentas[1])-cantidad
                        nuevaSuma = float(saldoCuentas[0])+ conversion
                        saldosUsuario[0]=nuevaSuma
                        saldosUsuario[1]=nuevaResta
                        saldosUsuario[2]= saldoCuentas[2]
                        guardarSaldos(rutaCarpeta, saldosUsuario)
                        with open(rutaSaldos, 'r') as archivo:
                            saldos = archivo.read()
                            print("Los saldos de la cuenta {} son:".format(cedula))
                            print("CRC USD BTC\nRespectivamente:")
                            print(saldos)
                        break
                    else:
                        print("Monto insuficiente")
                        break
                elif cuenta == 2:
                    print("El equivalente en dolares del bitcoin es: ")
                    print(divisas[const.ventaDolaresABitcoin])
                    saldoDecimal = float(saldoCuentas[1])
                    cantidad=int(input(("Cuantos Dolares desea vender?\n")))
                    conversion = cantidad/float(divisas[const.ventaDolaresABitcoin])
                    if cantidad <= saldoDecimal:
                        nuevaResta = float(saldoCuentas[1])-cantidad
                        nuevaSuma = float(saldoCuentas[2])+ conversion
                        saldosUsuario[2]=nuevaSuma
                        saldosUsuario[0]=nuevaResta
                        saldosUsuario[1]= saldoCuentas[1]
                        guardarSaldos(rutaCarpeta, saldosUsuario)
                        with open(rutaSaldos, 'r') as archivo:
                            saldos = archivo.read()
                            print("Los saldos de la cuenta {} son:".format(cedula))
                            print("CRC USD BTC\nRespectivamente:")
                            print(saldos)
                        break
                    else:
                        print("Monto insuficiente")
                        break 
                else: 
                    print("Escoja una opcion valida")
            elif opcion == 5:
                cuenta = int(input("Seleccione la cuenta de origen\n1. Colones\n2. Dolares\n "))
                if cuenta == 1:  
                    print("El equivalente en bitcoins del colon es: ")
                    print(divisas[const.compraBitcoinAColones])
                    saldoDecimal = float(saldoCuentas[0])
                    cantidad=int(input(("Cuantos Bitcoins desea comprar?\n")))
                    conversion = cantidad/float(divisas[const.compraBitcoinAColones])
                    if conversion <= saldoDecimal:
                        nuevaSuma = float(saldoCuentas[2])+cantidad
                        nuevaResta = float(saldoCuentas[0])- conversion
                        saldosUsuario[2]=nuevaSuma
                        saldosUsuario[0]=nuevaResta
                        saldosUsuario[1]= saldoCuentas[1]
                        guardarSaldos(rutaCarpeta, saldosUsuario)
                        with open(rutaSaldos, 'r') as archivo:
                            saldos = archivo.read()
                            print("Los saldos de la cuenta {} son:".format(cedula))
                            print("CRC USD BTC\nRespectivamente:")
                            print(saldos)
                        break 
                    else:
                        print("Monto insuficiente")
                        break
                elif cuenta == 2:
                    print("El equivalente en bitcoins del dolar es: ")
                    print(divisas[const.compraBitcoinADolares])
                    saldoDecimal = float(saldoCuentas[1])
                    cantidad=int(input(("Cuantos Bitcoins desea comprar?\n")))
                    conversion = cantidad/float(divisas[const.compraBitcoinADolares])
                    if conversion <= saldoDecimal:
                        nuevaSuma = float(saldoCuentas[2])+cantidad
                        nuevaResta = float(saldoCuentas[1])- conversion
                        saldosUsuario[2]=nuevaSuma
                        saldosUsuario[1]=nuevaResta
                        saldosUsuario[0]= saldoCuentas[0]
                        guardarSaldos(rutaCarpeta, saldosUsuario)
                        with open(rutaSaldos, 'r') as archivo:
                            saldos = archivo.read()
                            print("Los saldos de la cuenta {} son:".format(cedula))
                            print("CRC USD BTC\nRespectivamente:")
                            print(saldos)
                        break 
                    else:
                        print("Monto insuficiente")
                        break 
                else: 
                    print("Escoja una opcion valida")
            elif opcion == 6:
                cuenta = int(input("Seleccione la cuenta de destino\n1. Colones\n2. Dolares\n"))
                if cuenta == 1: 
                    print("El equivalente en bitcoins del colon es: ")
                    print(divisas[const.ventaBitcoinAColones])
                    saldoDecimal = float(saldoCuentas[2])
                    cantidad=int(input(("Cuantos Bitcoins desea vender?\n")))
                    conversion = cantidad/float(divisas[const.ventaBitcoinAColones])
                    if cantidad <= saldoDecimal:
                        nuevaResta = float(saldoCuentas[2])-cantidad
                        nuevaSuma = float(saldoCuentas[0])+ conversion
                        saldosUsuario[0]=nuevaSuma
                        saldosUsuario[2]=nuevaResta
                        saldosUsuario[1]= saldoCuentas[1]
                        guardarSaldos(rutaCarpeta, saldosUsuario)
                        with open(rutaSaldos, 'r') as archivo:
                            saldos = archivo.read()
                            print("Los saldos de la cuenta {} son:".format(cedula))
                            print("CRC USD BTC\nRespectivamente:")
                            print(saldos)
                        break
                    else:
                        print("Monto insuficiente")
                        break
                elif cuenta == 2:
                    print("El equivalente en bitcoins del dolar es: ")
                    print(divisas[const.ventaBitcoinADolares])
                    saldoDecimal = float(saldoCuentas[2])
                    cantidad=int(input(("Cuantos Bitcoins desea vender?\n")))
                    conversion = cantidad/float(divisas[const.ventaBitcoinADolares])
                    if cantidad <= saldoDecimal:
                        nuevaResta = float(saldoCuentas[2])-cantidad
                        nuevaSuma = float(saldoCuentas[1])+ conversion
                        saldosUsuario[1]=nuevaSuma
                        saldosUsuario[2]=nuevaResta
                        saldosUsuario[0]= saldoCuentas[0]
                        guardarSaldos(rutaCarpeta, saldosUsuario)
                        with open(rutaSaldos, 'r') as archivo:
                            saldos = archivo.read()
                            print("Los saldos de la cuenta {} son:".format(cedula))
                            print("CRC USD BTC\nRespectivamente:")
                            print(saldos)
                        break
                    else:
                        print("Monto insuficiente")
                        break 
                else: 
                    print("Escoja una opcion valida")
            elif opcion == 7:
                print("Volviendo al menu principal...")
                break
            else: 
                print("Escoja una opcion valida")
