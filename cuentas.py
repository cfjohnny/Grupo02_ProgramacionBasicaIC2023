import archivos
from constantes import \
    archivoSaldos, \
    maximoIntentos


def cargarSaldos(carpetaUsuario):
    saldos = []
    with archivos.abrirArchivo(carpetaUsuario, archivoSaldos, "r") as archivo:
        saldos = [float(saldo.rstrip('\n')) for saldo in archivo.readlines()]
    return saldos


def guardarSaldos(carpeta, saldos):
    with archivos.abrirArchivo(carpeta, archivoSaldos, "w") as archivo:
        lineas = [str(linea) + '\n' for linea in saldos]
        archivo.writelines(lineas)


def menuRetirarDinero():
    print("\n+========== RETIRAR DINERO ==========+")
    print("| Cuentas disponibles:               |")
    print("| 1. Colones                         |")
    print("| 2. Dólares                         |")
    print("| 3. Bitcoin                         |")
    print("+====================================+")
    return ['1', '2', '3']


def retiroDeDinero(carpeta, saldos):
    opcionesRetiro = menuRetirarDinero()
    opcionRetirarDinero = input('¿De cual cuenta desea retirar dinero?\n')
    indice = int(opcionRetirarDinero) - 1
    intentos = 1

    while intentos <= maximoIntentos:
        intentosRestantes = maximoIntentos - intentos

        if opcionRetirarDinero in opcionesRetiro:
            montoRetiro = float(input('¿Cuánto desea retirar?\n'))
            if saldos[indice] >= montoRetiro:
                saldos[indice] = saldos[indice] - montoRetiro
                guardarSaldos(carpeta, saldos)
                print(f'\nRetiro exitoso. Saldo actual: {saldos[indice]}')
                break
            else:
                intentos += 1
                print(f'No cuenta con fondos suficientes. Intentos restantes: {intentosRestantes}')
        else:
            print('Opcion invalida. Intente de nuevo...')
            break
    else:
        print('Ha alcanzado el maximo de intentos.\n')