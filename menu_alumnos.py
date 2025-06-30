from alumno import Alumno
import os
from config_mongo import is_connected, get_collection

class MenuAlumnos:
    def __init__(self, alumnos=None):
        if alumnos is None:
            self.alumnos = Alumno()
            self.isJson = True
            self.cargar_datos()
        else:
            self.alumnos = alumnos
            self.isJson = False

    def cargar_datos(self):
        if not self.isJson:
            return
        try:
            if os.path.exists("alumnos.json"):
                loaded = Alumno().read_json()
                if loaded and hasattr(loaded, 'items'):
                    self.alumnos = loaded
        except Exception as e:
            print(f"Error al cargar datos: {str(e)}")

    def guardar_datos(self):
        if not self.isJson:
            return
        try:
            self.alumnos.to_json()
            print("Datos guardados correctamente en JSON.")
            if is_connected():
                col = get_collection("alumnos")
                col.delete_many({})
                for alumno in self.alumnos.items:
                    col.insert_one(alumno.__dict__)
                print("Datos guardados correctamente en MongoDB.")
            else:
                print("No hay conexión a MongoDB. Solo se guardó en JSON.")
        except Exception as e:
            print(f"Error al guardar datos: {str(e)}")

    def mostrar_menu(self):
        while True:
            print("\n=== MENU ALUMNOS ===")
            print("1. Ver alumnos")
            print("2. Nuevo alumno")
            print("3. Editar alumno")
            print("4. Borrar alumno")
            print("5. Salir")
            opcion = input("Opción: ")
            if opcion == "1":
                self.listar_alumnos()
            elif opcion == "2":
                self.agregar_alumno()
            elif opcion == "3":
                self.editar_alumno()
            elif opcion == "4":
                self.eliminar_alumno()
            elif opcion == "5":
                print("Adiós")
                break
            else:
                print("Opción inválida")

    def listar_alumnos(self):
        print("\n=== ALUMNOS ===")
        if not hasattr(self.alumnos, 'items') or not self.alumnos.items:
            print("No hay alumnos")
            return
        for i, alumno in enumerate(self.alumnos.items):
            print(f"{i+1}. {alumno.nombre} {alumno.apellido} - {alumno.matricula} - Promedio: {alumno.promedio}")

    def agregar_alumno(self):
        print("\n=== NUEVO ALUMNO ===")
        try:
            nombre = input("Nombre: ")
            apellido = input("Apellido: ")
            edad = int(input("Edad: "))
            matricula = input("Matrícula: ")
            promedio = float(input("Promedio (0-10): "))
            nuevo_alumno = Alumno(nombre=nombre, apellido=apellido, edad=edad, matricula=matricula, promedio=promedio)
            if not hasattr(self.alumnos, 'agregar'):
                self.alumnos = Alumno()
            self.alumnos.agregar(nuevo_alumno)
            self.guardar_datos()
            print("Alumno agregado correctamente.")
        except Exception as e:
            print(f"Error al agregar alumno: {str(e)}")

    def editar_alumno(self):
        self.listar_alumnos()
        if not hasattr(self.alumnos, 'items') or not self.alumnos.items:
            return
        try:
            indice = int(input("Número del alumno: ")) - 1
            alumno = self.alumnos.items[indice]
            print("\n=== EDITAR ALUMNO ===")
            nombre = input(f"Nombre ({alumno.nombre}): ") or alumno.nombre
            apellido = input(f"Apellido ({alumno.apellido}): ") or alumno.apellido
            edad = input(f"Edad ({alumno.edad}): ")
            edad = int(edad) if edad else alumno.edad
            matricula = input(f"Matrícula ({alumno.matricula}): ") or alumno.matricula
            promedio = input(f"Promedio ({alumno.promedio}): ")
            promedio = float(promedio) if promedio else alumno.promedio
            alumno.nombre = nombre
            alumno.apellido = apellido
            alumno.edad = edad
            alumno.matricula = matricula
            alumno.promedio = promedio
            self.guardar_datos()
            print("Alumno actualizado correctamente.")
        except Exception as e:
            print(f"Error al editar alumno: {str(e)}")

    def eliminar_alumno(self):
        self.listar_alumnos()
        if not hasattr(self.alumnos, 'items') or not self.alumnos.items:
            return
        try:
            indice = int(input("Número del alumno: ")) - 1
            confirmacion = input(f"¿Borrar alumno {self.alumnos.items[indice].nombre}? (s/n): ")
            if confirmacion.lower() == 's':
                if not self.alumnos.eliminar(indice=indice):
                    print("No se pudo borrar")
                else:
                    print("Alumno borrado")
            self.guardar_datos()
        except Exception as e:
            print(f"Error al eliminar alumno: {str(e)}")

if __name__ == "__main__":
    app = MenuAlumnos()
    app.mostrar_menu() 