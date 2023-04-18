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


def modificarTipoCambio():
    raise NotImplementedError()


def flujoModificarTipoCambio():
    opciones = [
        const.modificarCompraColones,
        const.modificarVentaColones,
        const.modificarCompraDolares,
        const.modificarVentaDolares,
        const.modificarCompraBitcoin,
        const.modificarVentaBitcoin,
    ]
    factores = [
        [
            const.modificarCompraColones,
            'de colones a bitcoin: ',
            'de colones a dólares: '
        ],
        [
            const.modificarVentaColones,
            'de colones a bitcoin: ',
            'de colones a dólares: '
        ],
        [
            const.modificarCompraDolares,
            'de dólares a colones: ',
            'de dólares a bitcoin: '
        ],
        [
            const.modificarVentaDolares,
            'de dólares a colones: ',
            'de dólares a bitcoin: '
        ],
        [
            const.modificarCompraBitcoin,
            'de bitcoin a colones: ',
            'de bitcoin a dólares: '
        ],
        [
            const.modificarVentaBitcoin,
            'de bitcoin a colones: ',
            'de bitcoin a dólares: '
        ],
    ]
    while True:
        configuracion = cargarConfiguracion()

        menuModificarTipoCambio()

        opcion = input("Seleccione una opcion: ")
        opcionInt = int(opcion)
        valorFloat = 0.0

        try:
            if opcion in opciones:
                for i in range(2):
                    compraOVenta = "Compra"
                    if (opcionInt % 2) == 0:
                        compraOVenta = "Venta"
                    indice = (opcionInt * 2) - 1 + i
                    msjInput = input(
                        f"{compraOVenta} {factores[opcionInt - 1][i+1]}")
                    valorFloat = float(msjInput)
                    configuracion[indice] = str(valorFloat)
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

        if opcion == const.eliminarUsuario:
            cedula = input("Ingrese la cedula del usuario: ")
            eliminarUsuario(cedula)
        elif opcion == const.modificarTipoDeCambio:
            flujoModificarTipoCambio()
        elif opcion == const.salirConfiguracion:
            break
        else:
            print('Opcion invalida. Intente de nuevo...')
