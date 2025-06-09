import os
from alumno import Alumno
from maestro import Maestro
from grupo import Grupo

class Main:
    def __init__(self):
        self.alumnos = Alumno()
        self.maestros = Maestro()
        self.grupos = Grupo()
        
        self.cargar_datos()

    def cargar_datos(self):
        try:
            if os.path.exists("alumnos.json"):
                loaded = Alumno().read_json()
                if loaded and hasattr(loaded, 'items'):
                    self.alumnos = loaded
            
            if os.path.exists("maestros.json"):
                loaded = Maestro().read_json()
                if loaded and hasattr(loaded, 'items'):
                    self.maestros = loaded
            
            if os.path.exists("grupos.json"):
                loaded = Grupo().read_json()
                if loaded and hasattr(loaded, 'items'):
                    self.grupos = loaded
        except Exception as e:
            print(f"Error al cargar datos: {str(e)}")

    def guardar_datos(self):
        try:
            if hasattr(self.alumnos, 'to_json'):
                self.alumnos.to_json()
            if hasattr(self.maestros, 'to_json'):
                self.maestros.to_json()
            if hasattr(self.grupos, 'to_json'):
                self.grupos.to_json()
        except Exception as e:
            print(f"Error al guardar datos: {str(e)}")

    def mostrar_menu_principal(self):
        while True:
            print("\n--- SISTEMA DE GESTIÓN ESCOLAR ---")
            print("1. Gestión de Alumnos")
            print("2. Gestión de Maestros")
            print("3. Gestión de Grupos")
            print("4. Salir")
            
            opcion = input("Seleccione una opción: ")
            
            if opcion == "1":
                self.mostrar_menu_alumnos()
            elif opcion == "2":
                self.mostrar_menu_maestros()
            elif opcion == "3":
                self.mostrar_menu_grupos()
            elif opcion == "4":
                self.guardar_datos()
                print("¡Datos guardados correctamente!")
                print("Saliendo del sistema...")
                break
            else:
                print("Opción no válida. Intente nuevamente.")

    def mostrar_menu_alumnos(self):
        while True:
            print("\n--- GESTIÓN DE ALUMNOS ---")
            print("1. Listar alumnos")
            print("2. Agregar alumno")
            print("3. Editar alumno")
            print("4. Eliminar alumno")
            print("5. Volver al menú principal")
            
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
                break
            else:
                print("Opción no válida. Intente nuevamente.")

    def mostrar_menu_maestros(self):
        while True:
            print("\n--- GESTIÓN DE MAESTROS ---")
            print("1. Listar maestros")
            print("2. Agregar maestro")
            print("3. Editar maestro")
            print("4. Eliminar maestro")
            print("5. Volver al menú principal")
            
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
                break
            else:
                print("Opción no válida. Intente nuevamente.")

    def mostrar_menu_grupos(self):
        while True:
            print("\n--- GESTIÓN DE GRUPOS ---")
            print("1. Listar grupos")
            print("2. Agregar grupo")
            print("3. Editar grupo")
            print("4. Eliminar grupo")
            print("5. Asignar maestro a grupo")
            print("6. Agregar alumno a grupo")
            print("7. Volver al menú principal")
            
            opcion = input("Seleccione una opción: ")
            
            if opcion == "1":
                self.listar_grupos()
            elif opcion == "2":
                self.agregar_grupo()
            elif opcion == "3":
                self.editar_grupo()
            elif opcion == "4":
                self.eliminar_grupo()
            elif opcion == "5":
                self.asignar_maestro_grupo()
            elif opcion == "6":
                self.agregar_alumno_grupo()
            elif opcion == "7":
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
            promedio = float(input("Promedio: "))
            
            nuevo_alumno = Alumno(
                nombre=nombre,
                apellido=apellido,
                edad=edad,
                matricula=matricula,
                promedio=promedio
            )
            
            if not hasattr(self.alumnos, 'agregar'):
                self.alumnos = Alumno()
            self.alumnos.agregar(nuevo_alumno)
            print("Alumno agregado correctamente.")
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
            
            print("\n--- EDITAR ALUMNO ---")
            print("Deje en blanco los campos que no desea modificar")
            
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
            
            print("Alumno actualizado correctamente.")
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
                self.alumnos.eliminar(indice=indice)
                print("Alumno eliminado correctamente.")
        except (IndexError, ValueError) as e:
            print(f"Selección no válida: {str(e)}")

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
                self.maestros.eliminar(indice=indice)
                print("Maestro eliminado correctamente.")
        except (IndexError, ValueError) as e:
            print(f"Selección no válida: {str(e)}")

    def listar_grupos(self):
        print("\n--- LISTA DE GRUPOS ---")
        if not hasattr(self.grupos, 'items') or not self.grupos.items:
            print("No hay grupos registrados.")
            return
            
        for i, grupo in enumerate(self.grupos.items):
            print(f"\n{i+1}. Grupo: {grupo.nombre}")
            if grupo.maestro:
                print(f"   Maestro: {grupo.maestro.nombre} {grupo.maestro.apellido}")
            else:
                print("   Maestro: No asignado")
            
            if hasattr(grupo, 'alumnos') and grupo.alumnos and hasattr(grupo.alumnos, 'items') and grupo.alumnos.items:
                print("   Alumnos inscritos:")
                for alumno in grupo.alumnos.items:
                    print(f"   - {alumno.nombre} {alumno.apellido} ({alumno.matricula})")
            else:
                print("   No hay alumnos inscritos")

    def agregar_grupo(self):
        print("\n--- AGREGAR GRUPO ---")
        try:
            nombre = input("Nombre del grupo: ")
            
            nuevo_grupo = Grupo(nombre=nombre)
            
            if not hasattr(self.grupos, 'agregar'):
                self.grupos = Grupo()
            self.grupos.agregar(nuevo_grupo)
            print("Grupo creado correctamente.")
        except Exception as e:
            print(f"Error al crear grupo: {str(e)}")

    def editar_grupo(self):
        self.listar_grupos()
        if not hasattr(self.grupos, 'items') or not self.grupos.items:
            return
            
        try:
            indice = int(input("Seleccione el número del grupo a editar: ")) - 1
            grupo = self.grupos.items[indice]
            
            print("\n--- EDITAR GRUPO ---")
            nuevo_nombre = input(f"Nuevo nombre del grupo ({grupo.nombre}): ") or grupo.nombre
            grupo.nombre = nuevo_nombre
            print("Grupo actualizado correctamente.")
        except (IndexError, ValueError) as e:
            print(f"Selección no válida: {str(e)}")

    def eliminar_grupo(self):
        self.listar_grupos()
        if not hasattr(self.grupos, 'items') or not self.grupos.items:
            return
            
        try:
            indice = int(input("Seleccione el número del grupo a eliminar: ")) - 1
            confirmacion = input(f"¿Está seguro de eliminar el grupo {self.grupos.items[indice].nombre}? (s/n): ")
            if confirmacion.lower() == 's':
                self.grupos.eliminar(indice=indice)
                print("Grupo eliminado correctamente.")
        except (IndexError, ValueError) as e:
            print(f"Selección no válida: {str(e)}")

    def asignar_maestro_grupo(self):
        self.listar_grupos()
        if not hasattr(self.grupos, 'items') or not self.grupos.items:
            return
            
        try:
            grupo_indice = int(input("Seleccione el número del grupo: ")) - 1
            grupo = self.grupos.items[grupo_indice]
            
            self.listar_maestros()
            if not hasattr(self.maestros, 'items') or not self.maestros.items:
                return
                
            maestro_indice = int(input("Seleccione el número del maestro a asignar: ")) - 1
            maestro = self.maestros.items[maestro_indice]
            
            grupo.maestro = maestro
            print(f"Maestro {maestro.nombre} asignado al grupo {grupo.nombre} correctamente.")
        except (IndexError, ValueError) as e:
            print(f"Selección no válida: {str(e)}")

    def agregar_alumno_grupo(self):
        self.listar_grupos()
        if not hasattr(self.grupos, 'items') or not self.grupos.items:
            return
            
        try:
            grupo_indice = int(input("Seleccione el número del grupo: ")) - 1
            grupo = self.grupos.items[grupo_indice]
            
            self.listar_alumnos()
            if not hasattr(self.alumnos, 'items') or not self.alumnos.items:
                return
                
            alumno_indice = int(input("Seleccione el número del alumno a agregar: ")) - 1
            alumno = self.alumnos.items[alumno_indice]
            
            if not hasattr(grupo, 'alumnos'):
                grupo.alumnos = Alumno()
            
            grupo.alumnos.agregar(alumno)
            print(f"Alumno {alumno.nombre} agregado al grupo {grupo.nombre} correctamente.")
        except (IndexError, ValueError) as e:
            print(f"Selección no válida: {str(e)}")

if __name__ == "__main__":
    app = Main()
    app.mostrar_menu_principal() 