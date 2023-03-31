import os

def abrirArchivo(carpeta, archivo, modo):
    crearSiNoExiste(carpeta)
    # abre el archivo en segun el modo
    return open(f"{carpeta}/{archivo}", modo)

def listarArchivos(carpeta):
    crearSiNoExiste(carpeta)
    return os.listdir(carpeta)

def crearSiNoExiste(carpeta):
    # si no existe, crea la carpeta
    if not os.path.exists(carpeta):
        os.mkdir(carpeta)