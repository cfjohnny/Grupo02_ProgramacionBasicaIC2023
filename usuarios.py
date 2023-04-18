import os
import getpass as gp
import archivos
import cuentas
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
    maximoIntentos


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
            raise NotImplementedError()

        elif opcionUsuario == compraVentaDivisas:
            raise NotImplementedError()

        elif opcionUsuario == eliminarUsuario:
            raise NotImplementedError()

        elif opcionUsuario == salirUsuario:
            break
        else:
            print('Opcion invalida. Intente de nuevo...')
