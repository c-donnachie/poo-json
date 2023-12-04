from clase import Banco, CuentaBancaria
from conn import conectar_mysql, cerrar_conexion
from config import db_config
from termcolor import colored
import os

opciones = {
    1: " 1.- Agregar cuentas",
    2: " 2.- Eliminar cuenta",
    3: " 3.- Modificar cuenta",
    4: " 4.- Listar cuentas",
    5: " 5.- Mostrar JSON del banco",
    6: " 6.- Subir datos a MySQL",
    7: " 7.- Salir",
}


def limpiar_consola():
    sistema_operativo = os.name
    if sistema_operativo == "posix":
        os.system("clear")
    elif sistema_operativo == "nt":
        os.system("cls")
    else:
        print("No se pudo determinar el sistema operativo.")


def mostrar_menu():
    print(
        colored(
            "╔════════════════ ** MENÚ PRINCIPAL ** ════════════════╗",
            "light_magenta",
            attrs=["bold"],
        )
    )
    for opcion in opciones.values():
        print(colored("║", "light_magenta") + colored(opcion, "green"))
    print(
        colored(
            "╚══════════════════════════════════════════════════════╝",
            "light_magenta",
        )
    )


def main():
    banco = Banco()
    conexion_mysql = conectar_mysql(db_config)
    banco.borrar_datos_mysql(conexion_mysql)

    banco.cargar_desde_json("datos.json")

    while True:
        limpiar_consola()
        banco.listar_cuentas()
        mostrar_menu()
        opcion = input("Ingrese el número de la opción deseada: ")

        if opcion == "1":
            # Agregar cuenta
            titular = input("Ingrese el titular de la cuenta: ")
            tipo = input("Ingrese el tipo de cuenta: ")
            saldo = float(input("Ingrese el saldo inicial: "))
            nueva_cuenta = CuentaBancaria(titular, tipo, saldo)
            banco.agregar_cuenta(nueva_cuenta)
            print("Cuenta agregada exitosamente.")
        elif opcion == "2":
            # Eliminar cuenta
            numero_cuenta = int(input("Ingrese el número de la cuenta a eliminar: "))
            banco.eliminar_cuenta(numero_cuenta)
        elif opcion == "3":
            # Modificar cuenta
            numero_cuenta = int(input("Ingrese el número de la cuenta a modificar: "))
            banco.modificar_cuenta(numero_cuenta)
        elif opcion == "4":
            # Listar cuentas
            banco.listar_cuentas()
        elif opcion == "5":
            # Mostrar JSON
            banco.json_rep()
        elif opcion == "6":
            # Subir datos a MySQL
            banco.guardar_en_mysql(conexion_mysql)
        elif opcion == "7":
            # Salir
            cerrar_conexion(conexion_mysql)
            print("¡Gracias por utilizar el sistema bancario!")
            break
        else:
            print("Opción no válida. Por favor, ingrese un número del 1 al 6.")


if __name__ == "__main__":
    main()
