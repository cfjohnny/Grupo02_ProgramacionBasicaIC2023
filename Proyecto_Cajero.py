

#----------------------------Menu principal------------------------------

while True:
    # menu principal
    print("1.Registrar nuevo usuario")
    intentos_1 = int(0)
    print("2.Usuario registrado")
    print("3.Configuración avanzada")
    print("4.Salir")
    opcion = int(input())
    if opcion == 1: # opcion para registrase como nuevo usuario
        #registrarUsuario(intentos_1)
        import os 
        while intentos_1 < 3: # numero de intentos para ingresar cedula correcta
            cedula = input("Ingrese su cedula\nLa cedula debe constar de 9 numeros\n")#solicitud de cedula
            if len(cedula) == 9: #cedula correcta
                intentos_1 = 3
                print("Cedula aceptada")
                if os.path.isfile(cedula):
                    print(f"Ya existe una cuenta asociada a la cédula {cedula}.")
                    break
                else:
                    nombre = str(input("Ingrese primer nombre\n"))
                    apellido1 = str(input("Ingrese primer apellido\n"))
                    apellido2 = str(input("Ingrese segundo apellido\n"))
                    while True:
                        import getpass
                        pin = getpass.getpass("Ingrese un PIN de 4 caracteres")
                        if pin.__len__() == 4:
                            print("Pin aceptado")
                            while True:
                                pinConfirmacion = getpass.getpass("Confirme su PIN")
                                if pin==pinConfirmacion:
                                    print(f"El usuario {cedula} ha sido creado con éxito.")
                                    # abre el archivo en modo escritura y lo guarda en la variable "archivo"
                                    with open(cedula, "w") as archivo:
                                        # escribe cada variable en una línea separada
                                        archivo.write("Cedula: " +cedula + "\n")
                                        archivo.write("Nombre: " + nombre + "\n")
                                        archivo.write("Primer apellido: " + apellido1 + "\n")
                                        archivo.write("Segundo apellido: " + apellido2 + "\n")
                                        archivo.write("Pin: " + pin + "\n")
                                    break
                                        
                                else:
                                    pin != pinConfirmacion
                                    print("PIN no coincide")
                            break
                        else:
                            print("Error")
                            print("El PIN debe constar de 4 numeros")
                            

            else: # no se cumple con requerimientos de cedula
                print("Error, no se digitaron la cantidad de caracteres requeridos")
                intentos_1 = intentos_1 + 1
                if intentos_1 == 3:
                    print("""Se excedió el máximo de intentos
para ingresar un numero de cedula valido, 
volviendo al menú principal""")
    elif opcion == 2: # opcion para usuario registrado
        print()
    elif opcion == 3: # opcion para realizar la configuracion avanzada
        print()
    elif opcion == 4: # opcion para salir del sistema
        break
    else: 
        print("Seleccione una opción valida")
