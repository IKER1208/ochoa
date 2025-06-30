from maestro import Maestro
import os
from config_mongo import is_connected, get_collection

class MenuMaestros:
    def __init__(self, maestros=None):
        if maestros is None:
            self.maestros = Maestro()
            self.isJson = True
            self.cargar_datos()
        else:
            self.maestros = maestros
            self.isJson = False

    def cargar_datos(self):
        if not self.isJson:
            return
        try:
            if os.path.exists("maestros.json"):
                loaded = Maestro().read_json()
                if loaded and hasattr(loaded, 'items'):
                    self.maestros = loaded
        except Exception as e:
            print(f"Error al cargar datos: {str(e)}")

    def guardar_datos(self):
        if not self.isJson:
            return
        try:
            self.maestros.to_json()
            print("Datos guardados correctamente en JSON.")
            if is_connected():
                col = get_collection("maestros")
                col.delete_many({})
                for maestro in self.maestros.items:
                    col.insert_one(maestro.__dict__)
                print("Datos guardados correctamente en MongoDB.")
            else:
                print("No hay conexión a MongoDB. Solo se guardó en JSON.")
        except Exception as e:
            print(f"Error al guardar datos: {str(e)}")

    def mostrar_menu(self):
        while True:
            print("\n=== MENU MAESTROS ===")
            print("1. Ver maestros")
            print("2. Nuevo maestro")
            print("3. Editar maestro")
            print("4. Borrar maestro")
            print("5. Salir")
            opcion = input("Opción: ")
            if opcion == "1":
                self.listar_maestros()
            elif opcion == "2":
                self.agregar_maestro()
            elif opcion == "3":
                self.editar_maestro()
            elif opcion == "4":
                self.eliminar_maestro()
            elif opcion == "5":
                print("Adiós")
                break
            else:
                print("Opción inválida")

    def listar_maestros(self):
        print("\n=== MAESTROS ===")
        if not hasattr(self.maestros, 'items') or not self.maestros.items:
            print("No hay maestros")
            return
        for i, maestro in enumerate(self.maestros.items):
            print(f"{i+1}. {maestro.nombre} {maestro.apellido} - {maestro.matricula} - {maestro.especialidad}")

    def agregar_maestro(self):
        print("\n=== NUEVO MAESTRO ===")
        try:
            nombre = input("Nombre: ")
            apellido = input("Apellido: ")
            edad = int(input("Edad: "))
            matricula = input("Matrícula: ")
            especialidad = input("Especialidad: ")
            nuevo_maestro = Maestro(nombre=nombre, apellido=apellido, edad=edad, matricula=matricula, especialidad=especialidad)
            if not hasattr(self.maestros, 'agregar'):
                self.maestros = Maestro()
            self.maestros.agregar(nuevo_maestro)
            self.guardar_datos()
            print("Maestro agregado correctamente.")
        except Exception as e:
            print(f"Error al agregar maestro: {str(e)}")

    def editar_maestro(self):
        self.listar_maestros()
        if not hasattr(self.maestros, 'items') or not self.maestros.items:
            return
        try:
            indice = int(input("Número del maestro: ")) - 1
            maestro = self.maestros.items[indice]
            print("\n=== EDITAR MAESTRO ===")
            nombre = input(f"Nombre ({maestro.nombre}): ") or maestro.nombre
            apellido = input(f"Apellido ({maestro.apellido}): ") or maestro.apellido
            edad = input(f"Edad ({maestro.edad}): ")
            edad = int(edad) if edad else maestro.edad
            matricula = input(f"Matrícula ({maestro.matricula}): ") or maestro.matricula
            especialidad = input(f"Especialidad ({maestro.especialidad}): ") or maestro.especialidad
            maestro.nombre = nombre
            maestro.apellido = apellido
            maestro.edad = edad
            maestro.matricula = matricula
            maestro.especialidad = especialidad
            self.guardar_datos()
            print("Maestro actualizado correctamente.")
        except Exception as e:
            print(f"Error al editar maestro: {str(e)}")

    def eliminar_maestro(self):
        self.listar_maestros()
        if not hasattr(self.maestros, 'items') or not self.maestros.items:
            return
        try:
            indice = int(input("Número del maestro: ")) - 1
            confirmacion = input(f"¿Borrar maestro {self.maestros.items[indice].nombre}? (s/n): ")
            if confirmacion.lower() == 's':
                if not self.maestros.eliminar(indice=indice):
                    print("No se pudo borrar")
                else:
                    print("Maestro borrado")
            self.guardar_datos()
        except Exception as e:
            print(f"Error al eliminar maestro: {str(e)}")

if __name__ == "__main__":
    app = MenuMaestros()
    app.mostrar_menu() 