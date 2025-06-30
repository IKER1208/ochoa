from alumno import Alumno
import os
<<<<<<< HEAD
import json
from config_mongo import is_connected, get_collection

PENDIENTES_FILE = "pendientes_alumnos.json"
=======
>>>>>>> 43f61c1d815adea1547a3ea0b26d18203555a5c5

class MenuAlumnos:
    def __init__(self, alumnos=None):
        if alumnos is None:
            self.alumnos = Alumno()
            self.isJson = True
            self.cargar_datos()
        else:
            self.alumnos = alumnos
            self.isJson = False
<<<<<<< HEAD
        self.sincronizar_pendientes()
=======
>>>>>>> 43f61c1d815adea1547a3ea0b26d18203555a5c5

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

<<<<<<< HEAD
    def guardar_datos(self, operacion=None, datos=None):
        if not self.isJson:
            return
        try:
            if is_connected():
                col = get_collection("alumnos")
                if operacion == "insertar":
                    col.insert_one(datos)
                elif operacion == "editar":
                    col.update_one({"matricula": datos["matricula"]}, {"$set": datos})
                elif operacion == "eliminar":
                    col.delete_one({"matricula": datos["matricula"]})
                print("Datos guardados en MongoDB correctamente.")
                self.sincronizar_pendientes()
            else:
                if hasattr(self.alumnos, 'to_json'):
                    self.alumnos.to_json()
                if operacion:
                    self.registrar_pendiente(operacion, datos)
                print("No hay conexión a MongoDB. Datos guardados en JSON y operación pendiente registrada.")
        except Exception as e:
            print(f"Error al guardar datos: {str(e)}")

    def registrar_pendiente(self, operacion, datos):
        pendientes = []
        if os.path.exists(PENDIENTES_FILE):
            with open(PENDIENTES_FILE, "r") as f:
                pendientes = json.load(f)
        pendientes.append({"operacion": operacion, "datos": datos})
        with open(PENDIENTES_FILE, "w") as f:
            json.dump(pendientes, f)

    def sincronizar_pendientes(self):
        if not is_connected():
            return
        if not os.path.exists(PENDIENTES_FILE):
            return
        try:
            with open(PENDIENTES_FILE, "r") as f:
                pendientes = json.load(f)
            col = get_collection("alumnos")
            for p in pendientes:
                op = p["operacion"]
                datos = p["datos"]
                if op == "insertar":
                    col.insert_one(datos)
                elif op == "editar":
                    col.update_one({"matricula": datos["matricula"]}, {"$set": datos})
                elif op == "eliminar":
                    col.delete_one({"matricula": datos["matricula"]})
            os.remove(PENDIENTES_FILE)
            print("Operaciones pendientes sincronizadas con MongoDB.")
        except Exception as e:
            print(f"Error al sincronizar pendientes: {str(e)}")

=======
    def guardar_datos(self):
        if not self.isJson:
            return
        try:
           
                self.alumnos.to_json()
                print("Datos guardados correctamente.")
        except Exception as e:
            print(f"Error al guardar datos: {str(e)}")

>>>>>>> 43f61c1d815adea1547a3ea0b26d18203555a5c5
    def mostrar_menu(self):
        while True:
            print("\n--- GESTIÓN DE ALUMNOS ---")
            print("1. Listar alumnos")
            print("2. Agregar alumno")
            print("3. Editar alumno")
            print("4. Eliminar alumno")
            print("5. Salir")
            
            opcion = input("Seleccione una opción: ")
            
            if opcion == "1":
                self.listar_alumnos()
            elif opcion == "2":
                self.agregar_alumno()
            elif opcion == "3":
                self.editar_alumno()
            elif opcion == "4":
                self.eliminar_alumno()
            elif opcion == "5":
                print("Saliendo del sistema...")
                break
            else:
                print("Opción no válida. Intente nuevamente.")

    def listar_alumnos(self):
        print("\n--- LISTA DE ALUMNOS ---")
        if not hasattr(self.alumnos, 'items') or not self.alumnos.items:
            print("No hay alumnos registrados.")
            return
            
        for i, alumno in enumerate(self.alumnos.items):
            print(f"{i+1}. {alumno.nombre} {alumno.apellido} - {alumno.matricula} - Promedio: {alumno.promedio}")

    def agregar_alumno(self):
        print("\n--- AGREGAR ALUMNO ---")
        try:
            nombre = input("Nombre: ")
            apellido = input("Apellido: ")
            edad = int(input("Edad: "))
            matricula = input("Matrícula: ")
            promedio = float(input("Promedio (0-10): "))
            
            nuevo_alumno = Alumno(
                nombre=nombre,
                apellido=apellido,
                edad=edad,
                matricula=matricula,
                promedio=promedio
            )
<<<<<<< HEAD
=======
            
>>>>>>> 43f61c1d815adea1547a3ea0b26d18203555a5c5
            if not hasattr(self.alumnos, 'agregar'):
                self.alumnos = Alumno()
            self.alumnos.agregar(nuevo_alumno)
            print("Alumno agregado correctamente.")
<<<<<<< HEAD
            if self.isJson:
                self.guardar_datos("insertar", nuevo_alumno.__dict__)
=======
            
            if self.isJson:
                self.guardar_datos()
>>>>>>> 43f61c1d815adea1547a3ea0b26d18203555a5c5
        except ValueError as e:
            print(f"Error en los datos ingresados: {str(e)}")
        except Exception as e:
            print(f"Error al agregar alumno: {str(e)}")

    def editar_alumno(self):
        self.listar_alumnos()
        if not hasattr(self.alumnos, 'items') or not self.alumnos.items:
            return
            
        try:
            indice = int(input("Seleccione el número del alumno a editar: ")) - 1
            alumno = self.alumnos.items[indice]
<<<<<<< HEAD
            print("\n--- EDITAR ALUMNO ---")
            print("Deje en blanco los campos que no desea modificar")
=======
            
            print("\n--- EDITAR ALUMNO ---")
            print("Deje en blanco los campos que no desea modificar")
            
>>>>>>> 43f61c1d815adea1547a3ea0b26d18203555a5c5
            nombre = input(f"Nombre ({alumno.nombre}): ") or alumno.nombre
            apellido = input(f"Apellido ({alumno.apellido}): ") or alumno.apellido
            edad = input(f"Edad ({alumno.edad}): ")
            edad = int(edad) if edad else alumno.edad
            matricula = input(f"Matrícula ({alumno.matricula}): ") or alumno.matricula
            promedio = input(f"Promedio ({alumno.promedio}): ")
            promedio = float(promedio) if promedio else alumno.promedio
<<<<<<< HEAD
=======
            
>>>>>>> 43f61c1d815adea1547a3ea0b26d18203555a5c5
            alumno.nombre = nombre
            alumno.apellido = apellido
            alumno.edad = edad
            alumno.matricula = matricula
            alumno.promedio = promedio
<<<<<<< HEAD
            print("Alumno actualizado correctamente.")
            if self.isJson:
                self.guardar_datos("editar", alumno.__dict__)
=======
            
            print("Alumno actualizado correctamente.")
            if self.isJson:
                self.guardar_datos()
>>>>>>> 43f61c1d815adea1547a3ea0b26d18203555a5c5
        except (IndexError, ValueError) as e:
            print(f"Selección no válida: {str(e)}")

    def eliminar_alumno(self):
        self.listar_alumnos()
        if not hasattr(self.alumnos, 'items') or not self.alumnos.items:
            return
            
        try:
            indice = int(input("Seleccione el número del alumno a eliminar: ")) - 1
            confirmacion = input(f"¿Está seguro de eliminar a {self.alumnos.items[indice].nombre}? (s/n): ")
            if confirmacion.lower() == 's':
<<<<<<< HEAD
                alumno = self.alumnos.items[indice]
=======
>>>>>>> 43f61c1d815adea1547a3ea0b26d18203555a5c5
                if not self.alumnos.eliminar(indice=indice):
                    print("No se pudo eliminar el alumno.")
                else:
                    print("Alumno eliminado correctamente.")
                    if self.isJson:
<<<<<<< HEAD
                        self.guardar_datos("eliminar", alumno.__dict__)
=======
                        self.guardar_datos()
>>>>>>> 43f61c1d815adea1547a3ea0b26d18203555a5c5
        except (IndexError, ValueError) as e:
            print(f"Selección no válida: {str(e)}")

if __name__ == "__main__":
    alumno1 = Alumno(nombre="Juan", apellido="Pérez", edad=22, matricula="222222222", promedio=9.5)
    alumno2 = Alumno(nombre="Jose", apellido="Garcíaa", edad=21, matricula="1222222222", promedio=8.7)
    alumnos = Alumno()
    alumnos.agregar(alumno1)
    alumnos.agregar(alumno2)
    app = MenuAlumnos(alumnos=alumnos)
    app.mostrar_menu() 