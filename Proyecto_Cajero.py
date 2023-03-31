import os 
import getpass
import archivos
import usuarios
import constantes as const

# ----------------------------Menu principal------------------------------

while True:
    # menu principal
    print("\n+========= MENU PRINCIPAL ==========+")
    print("| 1.Registrar nuevo usuario         |")
    print("| 2.Usuario registrado              |")
    print("| 3.Configuración avanzada          |")
    print("| 4.Salir                           |")
    print("+===================================+")
    opcion = input('Seleccione una opcion: ')
    intentos = 0

    if opcion == const.registrarUsuario: # opcion para registrase como nuevo usuario
        #registrarUsuario(intentos_1)
        while intentos < const.maximoIntentos: # numero de intentos para ingresar cedula correcta
            cedula = input("Ingrese su cedula\nLa cedula debe constar de 9 numeros\n")#solicitud de cedula
            if len(cedula) == 9: #cedula correcta
                intentos = 3
                ruta = f"{const.carpetaUsuarios}/{cedula}"
                print("Cedula aceptada")
                if os.path.isfile(ruta):
                    print(f"Ya existe una cuenta asociada a la cédula {cedula}.")
                    break
                else:
                    nombre = input("Ingrese primer nombre\n")
                    apellido1 = input("Ingrese primer apellido\n")
                    apellido2 = input("Ingrese segundo apellido\n")
                    while True:
                        pin = getpass.getpass("Ingrese un PIN de 4 caracteres")
                        if len(pin) == 4:
                            print("Pin aceptado")
                            while True:
                                pinConfirmacion = getpass.getpass("Confirme su PIN")
                                if pin == pinConfirmacion:
                                    rutaArchivos = ruta
                                    print(f"El usuario {cedula} ha sido creado con éxito.")

                                    # abre el archivo en modo escritura y lo guarda en la variable "archivo"
                                    with archivos.abrirArchivo(const.carpetaUsuarios, cedula, "w") as archivo:
                                        # escribe cada variable en una línea separada
                                        archivo.writelines([
                                            f"{cedula}\n",
                                            f"{nombre}\n",
                                            f"{apellido1}\n",
                                            f"{apellido2}\n",
                                            f"{pin}\n"
                                        ])
                                    break
                                        
                                elif pin != pinConfirmacion:
                                    print("PIN no coincide")
                                else:
                                    pass
                            break
                        else:
                            print("Error")
                            print("El PIN debe constar de 4 numeros")
                            

            else: # no se cumple con requerimientos de cedula
                print("Error, no se digitaron la cantidad de caracteres requeridos")
                intentos = intentos + 1
                if intentos == 3:
                    print(
                        """Se excedió el máximo de intentos
                        para ingresar un numero de cedula valido, 
                        volviendo al menú principal"""
                    )
    elif opcion == const.usuarioRegistrado:  # opcion para usuario registrado
        listaUsuarios = usuarios.cargarUsuarios()
        
        if usuarios.existenUsuarios(listaUsuarios):
            estaAutenticado = usuarios.autenticarUsuario(listaUsuarios)
            
            if estaAutenticado:
                usuarios.iniciarFlujo()
        else:
            print("No existen usuarios registrados.\n")
            input('Presione ENTER para continuar...')
    elif opcion == const.configuracionAvanzada:  # opcion para realizar la configuracion avanzada
        print()
    elif opcion == const.salirPrincipal:  # opcion para salir del sistema
        break
    else:
        print("Seleccione una opción valida")
