import os


def abrirArchivo(carpeta, archivo, modo):
    ruta = os.path.join(carpeta, archivo)
    crearSiNoExiste(carpeta)
    # abre el archivo en segun el modo
    return open(ruta, modo)


def listarArchivos(carpeta):
    crearSiNoExiste(carpeta)
    return os.listdir(carpeta)


def eliminarArchivo(ruta):
    os.remove(ruta)


def crearSiNoExiste(ruta):
    # si no existe, crea la carpeta
    if ruta != "" and not os.path.exists(ruta):
        os.mkdir(ruta)
