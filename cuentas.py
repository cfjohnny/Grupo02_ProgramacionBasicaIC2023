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
