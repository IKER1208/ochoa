from grupo import Grupo
from menu_alumnos import MenuAlumnos
from menu_maestros import MenuMaestros
import os
import json
from config_mongo import is_connected, get_collection

PENDIENTES_FILE = "pendientes_grupos.json"

class MenuGrupos:
    def __init__(self, grupos=None):
        if grupos is None:
            self.grupos = Grupo()
            self.menu_alumnos = MenuAlumnos()
            self.menu_maestros = MenuMaestros()
            self.isJson = True
            self.cargar_datos()
        else:
            self.grupos = grupos
            self.menu_alumnos = MenuAlumnos()
            self.menu_maestros = MenuMaestros()
            self.isJson = False
        self.sincronizar_pendientes()

    def cargar_datos(self):
        if not self.isJson:
            return
        try:
            if os.path.exists("grupos.json"):
                loaded = Grupo().read_json()
                if loaded and hasattr(loaded, 'items'):
                    self.grupos = loaded
        except Exception as e:
            print(f"Error al cargar datos: {str(e)}")

    def guardar_datos(self, operacion=None, datos=None):
        if not self.isJson:
            return
        try:
            if is_connected():
                col = get_collection("grupos")
                if operacion == "insertar":
                    col.insert_one(datos)
                elif operacion == "editar":
                    col.update_one({"nombre": datos["nombre"]}, {"$set": datos})
                elif operacion == "eliminar":
                    col.delete_one({"nombre": datos["nombre"]})
                print("Datos guardados en MongoDB correctamente.")
                self.sincronizar_pendientes()
            else:
                if hasattr(self.grupos, 'to_json'):
                    self.grupos.to_json()
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
            col = get_collection("grupos")
            for p in pendientes:
                op = p["operacion"]
                datos = p["datos"]
                if op == "insertar":
                    col.insert_one(datos)
                elif op == "editar":
                    col.update_one({"nombre": datos["nombre"]}, {"$set": datos})
                elif op == "eliminar":
                    col.delete_one({"nombre": datos["nombre"]})
            os.remove(PENDIENTES_FILE)
            print("Operaciones pendientes sincronizadas con MongoDB.")
        except Exception as e:
            print(f"Error al sincronizar pendientes: {str(e)}")

    def mostrar_menu(self):
        while True:
            print("\n--- GESTIÓN DE GRUPOS ---")
            print("1. Listar grupos")
            print("2. Agregar grupo")
            print("3. Editar grupo")
            print("4. Eliminar grupo")
            print("5. Asignar maestro a grupo")
            print("6. Agregar alumno a grupo")
            print("7. Eliminar alumno de grupo")
            print("8. Eliminar maestro de grupo")
            print("9. Salir")
            
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
                self.eliminar_alumno_grupo()
            elif opcion == "8":
                self.eliminar_maestro_grupo()
            elif opcion == "9":
                print("Saliendo del sistema...")
                if self.isJson:
                    self.guardar_datos()
                break
            else:
                print("Opción no válida. Intente nuevamente.")

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
        print("\n--- NUEVO GRUPO ---")
        try:
            nombre = input("Nombre del grupo: ")
            nuevo_grupo = Grupo(nombre=nombre)
            print("\n--- Asignando un maestro al grupo ---")
            self.menu_maestros.agregar_maestro()
            if hasattr(self.menu_maestros.maestros, 'items') and self.menu_maestros.maestros.items:
                maestro = self.menu_maestros.maestros.items[-1]
                nuevo_grupo.maestro = maestro
            else:
                print("No se pudo asignar el maestro.")
                return
            agregar_alumnos = input("¿Deseas agregar alumnos? (s/n): ").lower()
            if agregar_alumnos == "s":
                print("\n--- Agregando alumnos al grupo ---")
                while True:
                    self.menu_alumnos.agregar_alumno()
                    if hasattr(self.menu_alumnos.alumnos, 'items') and self.menu_alumnos.alumnos.items:
                        alumno = self.menu_alumnos.alumnos.items[-1]
                        if not hasattr(nuevo_grupo, 'alumnos'):
                            nuevo_grupo.alumnos = self.menu_alumnos.alumnos.__class__()
                        nuevo_grupo.alumnos.agregar(alumno)
                    continuar = input("¿Deseas agregar otro alumno? (s/n): ").lower()
                    if continuar != "s":
                        break
            if not hasattr(self.grupos, 'agregar'):
                self.grupos = Grupo()
            self.grupos.agregar(nuevo_grupo)
            if self.isJson:
                self.guardar_datos("insertar", self.grupo_to_dict(nuevo_grupo))
                print("Grupo agregado y guardado en archivo.")
            else:
                print("Grupo agregado (modo objeto).")
        except Exception as e:
            print(f"Error: {str(e)}")

    def editar_grupo(self):
        self.listar_grupos()
        if not hasattr(self.grupos, 'items') or not self.grupos.items:
            return
        try:
            indice = int(input("\nNúmero del grupo a editar: ")) - 1
            grupo = self.grupos.items[indice]
            print("\n--- EDITAR GRUPO ---")
            print("Deje en blanco los campos que no desea modificar")
            nombre = input(f"Nombre ({grupo.nombre}): ") or grupo.nombre
            grupo.nombre = nombre
            actualizar_maestro = input("¿Deseas actualizar al maestro? (s/n): ").lower()
            if actualizar_maestro == "s":
                print("\n--- Actualizando maestro ---")
                self.menu_maestros.agregar_maestro()
                if hasattr(self.menu_maestros.maestros, 'items') and self.menu_maestros.maestros.items:
                    grupo.maestro = self.menu_maestros.maestros.items[-1]
                else:
                    print("No se pudo actualizar el maestro, manteniendo el original.")
            actualizar_alumnos = input("¿Deseas gestionar los alumnos del grupo? (s/n): ").lower()
            if actualizar_alumnos == "s":
                print("\n--- Gestionando alumnos del grupo ---")
                while True:
                    self.menu_alumnos.agregar_alumno()
                    if hasattr(self.menu_alumnos.alumnos, 'items') and self.menu_alumnos.alumnos.items:
                        alumno = self.menu_alumnos.alumnos.items[-1]
                        if not hasattr(grupo, 'alumnos'):
                            grupo.alumnos = self.menu_alumnos.alumnos.__class__()
                        grupo.alumnos.agregar(alumno)
                    continuar = input("¿Deseas agregar otro alumno? (s/n): ").lower()
                    if continuar != "s":
                        break
            if self.isJson:
                self.guardar_datos("editar", self.grupo_to_dict(grupo))
            print("Grupo actualizado correctamente.")
        except (IndexError, ValueError) as e:
            print(f"Error: {str(e)}")

    def eliminar_grupo(self):
        self.listar_grupos()
        if not hasattr(self.grupos, 'items') or not self.grupos.items:
            return
        try:
            indice = int(input("\nNúmero del grupo a eliminar: ")) - 1
            confirmacion = input(f"¿Eliminar grupo {self.grupos.items[indice].nombre}? (s/n): ")
            if confirmacion.lower() == 's':
                grupo = self.grupos.items[indice]
                self.grupos.eliminar(indice=indice)
                if self.isJson:
                    self.guardar_datos("eliminar", self.grupo_to_dict(grupo))
                print("Grupo eliminado correctamente.")
        except (IndexError, ValueError) as e:
            print(f"Error: {str(e)}")

    def grupo_to_dict(self, grupo):
        # Convierte el grupo y sus relaciones a un dict serializable
        d = {
            "nombre": grupo.nombre,
            "maestro": grupo.maestro.__dict__ if grupo.maestro else None,
            "alumnos": [a.__dict__ for a in grupo.alumnos.items] if hasattr(grupo, 'alumnos') and grupo.alumnos and hasattr(grupo.alumnos, 'items') else []
        }
        return d

    def asignar_maestro_grupo(self):
        self.listar_grupos()
        if not hasattr(self.grupos, 'items') or not self.grupos.items:
            return
            
        try:
            grupo_indice = int(input("\nNúmero del grupo: ")) - 1
            grupo = self.grupos.items[grupo_indice]
            
            print("\n--- MAESTROS ---")
            self.menu_maestros.listar_maestros()
            
            maestro_indice = int(input("\nNúmero del maestro: ")) - 1
            maestro = self.menu_maestros.maestros.items[maestro_indice]
            
            grupo.maestro = maestro
            print(f"Maestro {maestro.nombre} asignado")
            if self.isJson:
                self.guardar_datos("editar", self.grupo_to_dict(grupo))
        except (IndexError, ValueError) as e:
            print(f"Error: {str(e)}")

    def agregar_alumno_grupo(self):
        self.listar_grupos()
        if not hasattr(self.grupos, 'items') or not self.grupos.items:
            return
            
        try:
            grupo_indice = int(input("\nNúmero del grupo: ")) - 1
            grupo = self.grupos.items[grupo_indice]
            
            print("\n--- ALUMNOS ---")
            self.menu_alumnos.listar_alumnos()
            
            alumno_indice = int(input("\nNúmero del alumno: ")) - 1
            alumno = self.menu_alumnos.alumnos.items[alumno_indice]
            
            if not hasattr(grupo, 'alumnos'):
                grupo.alumnos = self.menu_alumnos.alumnos.__class__()
            
            grupo.alumnos.agregar(alumno)
            print(f"Alumno {alumno.nombre} agregado")
            if self.isJson:
                self.guardar_datos("editar", self.grupo_to_dict(grupo))
        except (IndexError, ValueError) as e:
            print(f"Error: {str(e)}")

    def eliminar_alumno_grupo(self):
        self.listar_grupos()
        if not hasattr(self.grupos, 'items') or not self.grupos.items:
            return
            
        try:
            grupo_indice = int(input("\nNúmero del grupo: ")) - 1
            grupo = self.grupos.items[grupo_indice]
            
            if not hasattr(grupo, 'alumnos') or not grupo.alumnos or not hasattr(grupo.alumnos, 'items') or not grupo.alumnos.items:
                print("No hay alumnos")
                return
            
            print("\nAlumnos en el grupo:")
            for i, alumno in enumerate(grupo.alumnos.items):
                print(f"{i+1}. {alumno.nombre} {alumno.apellido} ({alumno.matricula})")
            
            alumno_indice = int(input("\nNúmero del alumno: ")) - 1
            confirmacion = input(f"¿Eliminar a {grupo.alumnos.items[alumno_indice].nombre}? (s/n): ")
            
            if confirmacion.lower() == 's':
                grupo.alumnos.eliminar(indice=alumno_indice)
                print("Alumno eliminado")
                if self.isJson:
                    self.guardar_datos("editar", self.grupo_to_dict(grupo))
        except (IndexError, ValueError) as e:
            print(f"Error: {str(e)}")

    def eliminar_maestro_grupo(self):
        self.listar_grupos()
        if not hasattr(self.grupos, 'items') or not self.grupos.items:
            return
            
        try:
            grupo_indice = int(input("\nNúmero del grupo: ")) - 1
            grupo = self.grupos.items[grupo_indice]
            
            if not grupo.maestro:
                print("No hay maestro")
                return
            
            confirmacion = input(f"¿Eliminar maestro {grupo.maestro.nombre}? (s/n): ")
            
            if confirmacion.lower() == 's':
                grupo.maestro = None
                print("Maestro eliminado")
                if self.isJson:
                    self.guardar_datos("editar", self.grupo_to_dict(grupo))
        except (IndexError, ValueError) as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    app = MenuGrupos()
    app.mostrar_menu() 