import os
import getpass as gp
import archivos
from constantes import \
    cedula, \
    pin, \
    retirarDinero, \
    depositarDinero, \
    verSaldoActual, \
    salirUsuario, \
    carpetaUsuarios, \
    maximoIntentos


def cargarUsuarios():
    todosLosArchivos = archivos.listarArchivos(carpetaUsuarios)
    usuarios = []

    for archivo in todosLosArchivos:
        infoUsuario = None

        with archivos.abrirArchivo(carpetaUsuarios, archivo, "r") as archivoUsuario:
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
    cedula = solicitarCedula()

    while not existeLaCedula(cedula, usuarios) and intentos < maximoIntentos:
        intentosRestantes = maximoIntentos - intentos
        print(f'Cedula incorrecta. Intente de nuevo, intentos restantes: {intentosRestantes}')
        intentos += 1
        cedula = solicitarCedula()

    if intentos == maximoIntentos:
        print('Ha alcanzado el maximo de intentos.\n')
        return False
    # ---------------------------------------------------------------------------

    # Solicitar y validar el PIN ------------------------------------------------
    intentos = 1
    pin = solicitarPIN()

    while not esValidoElPIN(cedula, pin, usuarios) and intentos < maximoIntentos:
        intentosRestantes = maximoIntentos - intentos
        print(f'PIN incorrecto. Intente de nuevo, intentos restantes: {intentosRestantes}')
        intentos += 1
        pin = solicitarPIN()

    if intentos == maximoIntentos:
        print('Ha alcanzado el maximo de intentos.\n')
        return False
    # ---------------------------------------------------------------------------

    return True


def menuRetirarDinero():
    print("\n========= RETIRAR DINERO =========")
    print("Cuentas disponibles:")
    print("1. Colones")
    print("2. Dólares")
    print("3. Bitcoin\n")


def menuDepositarDinero():
    print("\n========= DEPOSITAR DINERO =========")
    print("Cuentas disponibles:")
    print("1. Colones")
    print("2. Dólares")
    print("3. Bitcoin\n")


def mostrarSubmenu():
    print("\n========= USUARIO REGISTRADO =========")
    print("1. Retirar dinero")
    print("2. Depositar dinero")
    print("3. Ver saldo actual")
    print("4. Pagar servicios")
    print("5. Compra/Venta de Divisas")
    print("6. Eliminar usuario")
    print("7. Salir\n")


def iniciarFlujo():
    while True:
        mostrarSubmenu()
        opcionUsuario = input('Seleccione una opcion: ')

        if opcionUsuario == retirarDinero:
            print()
            menuRetirarDinero()
            opcionRetirarDinero = input('¿De cual cuenta desea retirar dinero?\n')
            # TODO: Implementar logica de retiro de dinero

        elif opcionUsuario == depositarDinero:
            print()
            menuDepositarDinero()
            opcionDepositarDinero = input('¿A cuál cuenta desea acreditar el depósito de dinero?\n')
            # TODO: Implementar logica de deposito de dinero

        elif opcionUsuario == verSaldoActual:
            print()
            # TODO: Logica de ver saldos

        elif opcionUsuario == salirUsuario:
            break
        else:
            print('Opcion invalida. Intente de nuevo...')