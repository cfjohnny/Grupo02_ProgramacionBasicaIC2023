import os
import getpass
import archivos
import usuarios
import configuracion as config
import constantes as const
import DepositoObligatorioParaRegistrarUsuario as depositoObligatorioDelRegistro

#----------------------------Menu principal------------------------------
while True:
    print("\n+========= MENU PRINCIPAL ==========+")
    print("| 1.Registrar nuevo usuario         |")
    print("| 2.Usuario registrado              |")
    print("| 3.Configuración avanzada          |")
    print("| 4.Salir                           |")
    print("+===================================+")
    opcion = input('Seleccione una opcion: ')
    intentos = 0

    if opcion == const.registrarUsuario:  # opcion para registrase como nuevo usuario
        # registrarUsuario(intentos_1)
        while intentos < const.maximoIntentos:  # numero de intentos para ingresar cedula correcta
            # solicitud de cedula
            cedula = input("Ingrese su cedula\nLa cedula debe constar de 9 numeros.\n") #solicitud de cedula
            if len(cedula) == 9:  # cedula correcta
                intentos = 3
                ruta = f"{const.carpetaUsuarios}/{cedula}"
                print("Cedula aceptada")
                if os.path.isdir(ruta):
                    #Usuario digita una cedula que ya se encontraba en el sistema
                    print(f"Ya existe una cuenta asociada a la cédula: {cedula}.") 
                    break
                else: #Solicitarle el nombre y apellidos al usuario
                    nombre = input("Ingrese primer nombre\n")
                    apellido1 = input("Ingrese primer apellido\n")
                    apellido2 = input("Ingrese segundo apellido\n")
                    while True:
                        pinIngresado = getpass.getpass("Ingrese un PIN de 4 caracteres.") #Solicitud del PIN
                        if len(pinIngresado) == 4:
                            print("Pin aceptado.")
                            while True:
                                pinConfirmacion = getpass.getpass("Confirme su PIN.") #Confirmacion del PIN
                                if pinIngresado == pinConfirmacion:
                                    exito = depositoObligatorioDelRegistro.depositoObligatorio(cedula)
                                    if exito:
                                        archivos.crearEstructuraArchivos([
                                            cedula,
                                            nombre,
                                            apellido1,
                                            apellido2,
                                            pinIngresado,
                                        ])
                                        usuarios.generarServiciosAleatorios(cedula)
                                        print(f"El usuario {cedula} ha sido creado con éxito.")
                                    else:
                                        pass

                                    break
                                elif pinIngresado != pinConfirmacion:
                                    print("PIN no coincide.")
                                else:
                                    pass
                            break
                        else:
                            print("Error.")
                            print("El PIN debe constar de 4 numeros.")
    
            else:  # no se cumple con requerimientos de cedula
                intentos += 1
                if len(cedula) > 9: # Cedula mayor de 9 digitos
                    print("Los digitos de la cedula no pueden exceder 9 digitos, intentalo nuevamente.\n")
                elif len(cedula) < 9: # Cedula menor de 9 digitos
                    print("Los digitos de la cedula no pueden ser menores de 9 digitos, intentalo nuevamente.\n")
                else:
                    break
                intentos = intentos + 1
                if intentos == 3:
                    print(
                        """Se excedió el máximo de intentos
                        para ingresar un numero de cedula valido, 
                        volviendo al menú principal..."""
                    )
 
    elif opcion == const.usuarioRegistrado:  # opcion para usuario registrado
        listaUsuarios = usuarios.cargarUsuarios()

        if usuarios.existenUsuarios(listaUsuarios):
            estaAutenticado, cedula = usuarios.autenticarUsuario(listaUsuarios)
            if estaAutenticado:
                usuarios.flujoPrincipal(cedula)
        else:
            print("No existen usuarios registrados.\n")
            input('Presione ENTER para continuar...')
    elif opcion == const.configuracionAvanzada:  # opcion para realizar la configuracion avanzada
        pinAdmin = config.solicitarPin()
        if config.esAdmin(pinAdmin):
            config.flujoPrincipal()
        else:
            print("El PIN ingresado es incorrecto.")
            input('Presione ENTER para continuar...')
    elif opcion == const.salirPrincipal:  # opcion para salir del sistema
        break
    else:
        print("Seleccione una opción valida.")
