import json
from conn import cerrar_conexion
from termcolor import colored
import os


class CuentaBancaria:
    contador_cuentas = 0

    def __init__(self, titular, tipo, saldo):
        CuentaBancaria.contador_cuentas += 1
        self.numero = CuentaBancaria.contador_cuentas
        self.titular = titular
        self.tipo = tipo
        self.saldo = saldo


class Banco:
    def __init__(self):
        self.cuentas_bancarias = []

    def cargar_desde_json(self, json_file):
        try:
            with open(json_file, "r") as file:
                data = json.load(file)
                cuentas_json = data.get("cuentas_bancarias", [])

                for cuenta_json in cuentas_json:
                    cuenta = CuentaBancaria(
                        titular=cuenta_json["titular"],
                        tipo=cuenta_json["tipo"],
                        saldo=cuenta_json["saldo"],
                    )
                    cuenta.numero = cuenta_json["numero"]
                    self.cuentas_bancarias.append(cuenta)

                print("Cuentas cargadas desde el archivo JSON.")
        except FileNotFoundError:
            print(f"No se encontró el archivo JSON: {json_file}")

    def agregar_cuenta(self, cuenta):
        self.cuentas_bancarias.append(cuenta)

    def eliminar_cuenta(self, numero_cuenta):
        for cuenta in self.cuentas_bancarias:
            if cuenta.numero == numero_cuenta:
                self.cuentas_bancarias.remove(cuenta)
                print(f"Cuenta bancaria con número {numero_cuenta} eliminada.")
                return
        print(f"No se encontró cuenta bancaria con número {numero_cuenta}.")

    def modificar_cuenta(self, numero_cuenta):
        for i, cuenta in enumerate(self.cuentas_bancarias):
            if cuenta.numero == numero_cuenta:
                nuevo_titular = input("Ingrese el nuevo titular: ")
                nuevo_tipo = input("Ingrese el nuevo tipo de cuenta: ")
                nuevo_saldo = float(input("Ingrese el nuevo saldo: "))

                self.cuentas_bancarias[i] = CuentaBancaria(
                    nuevo_titular, nuevo_tipo, nuevo_saldo
                )
                print(f"Cuenta bancaria con número {numero_cuenta} modificada.")
                return
        print(f"No se encontró cuenta bancaria con número {numero_cuenta}.")

    def listar_cuentas(self):
        print(
            colored(
                "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",
                "light_blue",
                attrs=["blink"],
            )
        )
        for cuenta in self.cuentas_bancarias:
            print(
                f"Número: {cuenta.numero}, Titular: {cuenta.titular}, Tipo: {cuenta.tipo}, Saldo: {cuenta.saldo}"
            )
        print(
            colored(
                "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",
                "light_blue",
                attrs=["blink"],
            )
        )

    def json_rep(self):
        print("Representación JSON del banco:")
        print(
            json.dumps([cuenta.__dict__ for cuenta in self.cuentas_bancarias], indent=2)
        )

    def guardar_en_mysql(self, conexion):
        if conexion.is_connected():
            try:
                cursor = conexion.cursor()
                cursor.execute("DROP TABLE IF EXISTS CuentasBancarias")
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS CuentasBancarias (
                        numero INT PRIMARY KEY,
                        titular VARCHAR(255) NOT NULL,
                        tipo VARCHAR(255) NOT NULL,
                        saldo DECIMAL(10, 2) NOT NULL
                    )
                """
                )

                for cuenta in self.cuentas_bancarias:
                    cursor.execute(
                        """
                        INSERT INTO CuentasBancarias (numero, titular, tipo, saldo)
                        VALUES (%s, %s, %s, %s)
                    """,
                        (cuenta.numero, cuenta.titular, cuenta.tipo, cuenta.saldo),
                    )

                conexion.commit()
                print("Datos guardados en MySQL.")
            except Exception as e:
                print(f"Error al guardar datos en MySQL: {e}")
                conexion.rollback()
        else:
            print("No hay conexión a MySQL.")

    def borrar_datos_mysql(self, conexion):
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("DELETE FROM CuentasBancarias")
                conexion.commit()
                print("Datos SQL previos borrados.")
            except Exception as e:
                print(f"Error al borrar datos en MySQL: {e}")
                conexion.rollback()
        else:
            print("No hay conexión a MySQL.")
