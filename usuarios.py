# esto es una prueba

import os
import getpass as gp

# Constantes
INTENTOS = 3
CARPETA_USUARIOS = 'usuarios'
ARCHIVO_PIN = 'pin.txt'


def cargarUsuarios():
    # todo: cargar archivos de texto
    todosLosArchivos = os.listdir(CARPETA_USUARIOS)
    usuarios = []
    for folderCedula in todosLosArchivos:
        pin = None
        ruta = os.path.join(CARPETA_USUARIOS, folderCedula, ARCHIVO_PIN)
        archivoPin = open(ruta)
        with archivoPin:
            pin = archivoPin.read()
        usuarios.append([folderCedula, pin])

    return usuarios


def existenUsuarios(usuarios):
    if usuarios.count() == 0:
        return False
    else:
        return True


def existeLaCedula(cedula, usuarios):
    for u in usuarios:
        if u[0] == cedula:
            return True
    return False


def esValidoElPIN(cedula, pin, usuarios):
    for u in usuarios:
        if u[0] == cedula and u[1] == pin:
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

    while not existeLaCedula(cedula, usuarios) and intentos < INTENTOS:
        intentos += 1
        cedula = solicitarCedula()

    if intentos == INTENTOS:
        return False
    # ---------------------------------------------------------------------------

    # Solicitar y validar el PIN ------------------------------------------------
    intentos = 1
    pin = solicitarPIN()

    while not esValidoElPIN(cedula, pin, usuarios) and intentos < INTENTOS:
        intentos += 1
        pin = solicitarPIN()

    if intentos == INTENTOS:
        return False
    # ---------------------------------------------------------------------------

    return True
