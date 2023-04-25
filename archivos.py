import os
from constantes import \
    carpetaUsuarios, \
    cedula, \
    nombre, \
    apellido1, \
    apellido2, \
    pin

def abrirArchivo(carpeta, archivo, modo):
    crearSiNoExiste(carpeta)
    ruta = os.path.join(carpeta, archivo)
    # abre el archivo en segun el modo
    return open(ruta, modo)


def listarDirectorios(carpeta):
    crearSiNoExiste(carpeta)
    return os.listdir(carpeta)


def eliminarArchivo(ruta):
    os.remove(ruta)


def crearSiNoExiste(ruta):
    # si no existe, crea la carpeta
    if ruta != "" and not os.path.exists(ruta):
        os.makedirs(ruta, exist_ok=True)


def crearEstructuraArchivos(usuario):
    carpeta = f"{carpetaUsuarios}/{usuario[cedula]}"
    # abre el archivo en modo escritura y lo guarda en la variable "archivo"
    with abrirArchivo(carpeta, "info", "w") as archivo:
        # escribe cada variable en una línea separada
        archivo.writelines([
            f"{usuario[cedula]}\n",
            f"{usuario[nombre]}\n",
            f"{usuario[apellido1]}\n",
            f"{usuario[apellido2]}\n",
            f"{usuario[pin]}\n"
        ])