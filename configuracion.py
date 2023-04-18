from getpass import getpass
import os
import archivos
import constantes as const


def solicitarPin():
    return getpass("Ingrese su PIN de Administrador: ")


def esAdmin(pinIngresado):
    pinEncontrado = ""
    with archivos.abrirArchivo('', const.archivoConfig, 'r') as archivo:
        pinEncontrado = archivo.readline().rstrip('\n')
    return pinEncontrado == pinIngresado


def mostrarSubmenu():
    print("\n+========= CONFIGURACION AVANZADA =========+")
    print("| 1. Eliminar usuario                      |")
    print("| 2. Modificar tipos de cambio             |")
    print("| 3. Salir                                 |")
    print('+==========================================+')


def eliminarUsuario(cedula):
    ruta = f"{const.carpetaUsuarios}/{cedula}"
    if os.path.exists(ruta):
        archivos.eliminarArchivo(ruta)
        print(f"El usuario con la cédula {cedula} ha sido eliminado.")
    else:
        print(f"El usuario con la cédula {cedula} no existe.")


def cargarConfiguracion():
    configuracion = []
    with archivos.abrirArchivo('', const.archivoConfig, 'r') as archivo:
        configuracion = [linea.rstrip('\n') for linea in archivo.readlines()]
    return configuracion


def menuModificarTipoCambio():
    print("\n+========== MODIFICAR TIPO DE CAMBIO ==========+")
    print("| ¿Qué tipo de cambio desea modificar?         |")
    print("| 1. Compra de colones                         |")
    print("| 2. Venta de colones                          |")
    print("| 3. Compra de dólares                         |")
    print("| 4. Venta de dólares                          |")
    print("| 5. Compra de bitcoin                         |")
    print("| 6. Venta de bitcoin                          |")
    print("| 7. Salir                                     |")
    print("+==============================================+")


def guardarConfiguracion(configuracion):
    with archivos.abrirArchivo('', const.archivoConfig, 'w') as archivo:
        lineas = [linea + '\n' for linea in configuracion]
        archivo.writelines(lineas)


def modificarTipoCambio(opcion):
    nuevaConfiguracion = cargarConfiguracion()
    factores = [
        ['de colones a bitcoin: ', 'de colones a dólares: '],
        ['de colones a bitcoin: ', 'de colones a dólares: '],
        ['de dólares a colones: ', 'de dólares a bitcoin: '],
        ['de dólares a colones: ', 'de dólares a bitcoin: '],
        ['de bitcoin a colones: ', 'de bitcoin a dólares: '],
        ['de bitcoin a colones: ', 'de bitcoin a dólares: '],
    ]
    compraOVenta = "Compra"

    if (opcion % 2) == 0:
        compraOVenta = "Venta"

    for i in range(2):
        indice = (opcion * 2) - 1 + i
        msjInput = input(f"{compraOVenta} {factores[opcion - 1][i]}")
        valorFloat = float(msjInput)
        nuevaConfiguracion[indice] = str(valorFloat)

    return nuevaConfiguracion


def flujoModificarTipoCambio():
    while True:
        configuracion = []
        opciones = [
            const.modificarCompraColones,
            const.modificarVentaColones,
            const.modificarCompraDolares,
            const.modificarVentaDolares,
            const.modificarCompraBitcoin,
            const.modificarVentaBitcoin,
        ]

        menuModificarTipoCambio()
        opcion = input("Seleccione una opcion: ")

        try:
            if opcion in opciones:
                configuracion = modificarTipoCambio(int(opcion))
            elif opcion == const.salirModificar:
                break
            else:
                print('Opcion invalida. Intente de nuevo...')
        except ValueError:
            print('Opcion invalida. Intente de nuevo...')

        guardarConfiguracion(configuracion)


def flujoPrincipal():
    while True:
        mostrarSubmenu()
        opcion = input("Seleccione una opcion: ")

        if opcion == const.configEliminarUsuario:
            cedula = input("Ingrese la cedula del usuario: ")
            eliminarUsuario(cedula)
        elif opcion == const.modificarTipoDeCambio:
            flujoModificarTipoCambio()
        elif opcion == const.salirConfiguracion:
            break
        else:
            print('Opcion invalida. Intente de nuevo...')
