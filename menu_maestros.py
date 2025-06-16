from maestro import Maestro
import os

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
            if hasattr(self.maestros, 'to_json'):
                self.maestros.to_json()
                print("Datos guardados correctamente.")
        except Exception as e:
            print(f"Error al guardar datos: {str(e)}")

    def mostrar_menu(self):
        while True:
            print("\n--- GESTIÓN DE MAESTROS ---")
            print("1. Listar maestros")
            print("2. Agregar maestro")
            print("3. Editar maestro")
            print("4. Eliminar maestro")
            print("5. Salir")
            
            opcion = input("Seleccione una opción: ")
            
            if opcion == "1":
                self.listar_maestros()
            elif opcion == "2":
                self.agregar_maestro()
            elif opcion == "3":
                self.editar_maestro()
            elif opcion == "4":
                self.eliminar_maestro()
            elif opcion == "5":
                print("Saliendo del sistema...")
                break
            else:
                print("Opción no válida. Intente nuevamente.")

    def listar_maestros(self):
        print("\n--- LISTA DE MAESTROS ---")
        if not hasattr(self.maestros, 'items') or not self.maestros.items:
            print("No hay maestros registrados.")
            return
            
        for i, maestro in enumerate(self.maestros.items):
            print(f"{i+1}. {maestro.nombre} {maestro.apellido} - {maestro.matricula} - {maestro.especialidad}")

    def agregar_maestro(self):
        print("\n--- AGREGAR MAESTRO ---")
        try:
            nombre = input("Nombre: ")
            apellido = input("Apellido: ")
            edad = int(input("Edad: "))
            matricula = input("Matrícula: ")
            especialidad = input("Especialidad: ")
            
            nuevo_maestro = Maestro(
                nombre=nombre,
                apellido=apellido,
                edad=edad,
                matricula=matricula,
                especialidad=especialidad
            )
            
            if not hasattr(self.maestros, 'agregar'):
                self.maestros = Maestro()
            self.maestros.agregar(nuevo_maestro)
            print("Maestro agregado correctamente.")
            
            if self.isJson:
                self.guardar_datos()
        except ValueError as e:
            print(f"Error en los datos ingresados: {str(e)}")
        except Exception as e:
            print(f"Error al agregar maestro: {str(e)}")

    def editar_maestro(self):
        self.listar_maestros()
        if not hasattr(self.maestros, 'items') or not self.maestros.items:
            return
            
        try:
            indice = int(input("Seleccione el número del maestro a editar: ")) - 1
            maestro = self.maestros.items[indice]
            
            print("\n--- EDITAR MAESTRO ---")
            print("Deje en blanco los campos que no desea modificar")
            
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
            
            print("Maestro actualizado correctamente.")
            if self.isJson:
                self.guardar_datos()
        except (IndexError, ValueError) as e:
            print(f"Selección no válida: {str(e)}")

    def eliminar_maestro(self):
        self.listar_maestros()
        if not hasattr(self.maestros, 'items') or not self.maestros.items:
            return
            
        try:
            indice = int(input("Seleccione el número del maestro a eliminar: ")) - 1
            confirmacion = input(f"¿Está seguro de eliminar a {self.maestros.items[indice].nombre}? (s/n): ")
            if confirmacion.lower() == 's':
                if not self.maestros.eliminar(indice=indice):
                    print("No se pudo eliminar el maestro.")
                else:
                    print("Maestro eliminado correctamente.")
                    if self.isJson:
                        self.guardar_datos()
        except (IndexError, ValueError) as e:
            print(f"Selección no válida: {str(e)}")

if __name__ == "__main__":
    maestro1 = Maestro(nombre="Juan", apellido="Pérez", edad=35, matricula="333333333", especialidad="Matemáticas")
    maestro2 = Maestro(nombre="María", apellido="García", edad=40, matricula="444444444", especialidad="Física")
    maestros = Maestro()
    maestros.agregar(maestro1)
    maestros.agregar(maestro2)
    app = MenuMaestros(maestros=maestros)
    app.mostrar_menu() 