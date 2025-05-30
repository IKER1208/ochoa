from alumno import Alumno
from arreglo import Arreglo
from maestro import Maestro
import os
import json

class Grupo(Arreglo):
    def __init__(self, nombre=None, maestro=None):
        if nombre is None and maestro is None: 
            Arreglo.__init__(self)
            self.es_arreglo = True
        else:
            self.nombre = nombre
            self.maestro = maestro
            self.alumnos = Alumno()
            self.es_arreglo = False

    def to_json(self):
        with open("grupos.json", 'w') as file:
         json.dump(self.to_dict(), file, indent=4)

    def to_dict(self):
        if self.es_arreglo:
                return  [item.to_dict() for item in self.items] if self.items else []
        return {
            'tipo': 'grupo','nombre': self.nombre,
            'maestro': self.maestro.to_dict()if self.maestro 
              else None,'alumnos': self.alumnos.to_dict()
        }

    def asignar_maestro(self, maestro):
        self.maestro = maestro

    def cambiarNombre(self, nombre):
        self.nombre = nombre

    def __str__(self):
        if self.es_arreglo:
            return f"Total de grupos: {len(self.items)}"

        maestro_info = f"{self.maestro.nombre} {self.maestro.apellido}" if self.maestro else "Falta asignar"

        return (
            f"Grupo: {self.nombre}\n"
            f"Maestro: {maestro_info}\n"
            f"Total de alumnos: {str(self.alumnos)}\n"
        )


if __name__ == "__main__":
    ALUMNO = Alumno("Iker", "Flores", 18, "23170032", 10)
    ALUMNO2 = Alumno("Jesus", "De la rosa", 19, "23170119", 10)
    MAESTRO = Maestro("Ramiro", "Esquivel", 40, "1", "Android")
    ALUMNO3 = Alumno("Juan", "Perez", 20, "23170120", 10)
    ''''''
    '''
        print("=== Alumno individual ===")
    print(ALUMNO.to_dict())
    print("\n=== Maestro individual ===")
    print(MAESTRO.to_dict())
    '''
    GRUPO = Grupo("Desarrollo Móvil", MAESTRO)
    GRUPO.alumnos.agregar(ALUMNO, ALUMNO2, ALUMNO3)
    #GRUPO.alumnos.eliminar(ALUMNO2)
    
    ''' print("\n=== Grupo completo ===")
    print(GRUPO.to_dict())'''

    print("\n=== Lista de Grupos ===")
    grupos = Grupo()
    grupos.agregar(GRUPO)
    print(grupos.to_dict())
    grupos.to_json()