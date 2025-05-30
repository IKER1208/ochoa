from arreglo import Arreglo

import os
import json

class Maestro(Arreglo):
    def __init__(self, nombre=None, apellido=None, edad=None, matricula=None, especialidad=None):
        if nombre is None and apellido is None and edad is None and matricula is None and especialidad is None:
            Arreglo.__init__(self)
            self.es_arreglo = True
        else:
            self.nombre = nombre
            self.apellido = apellido
            self.edad = edad
            self.matricula = matricula
            self.especialidad = especialidad
            self.es_arreglo = False
    def to_json(self):
        with open("maestros.json", 'w') as file:
         json.dump(self.to_dict(), file, indent=4)

    def to_dict(self):
        if self.es_arreglo:
            return [item.to_dict() for item in self.items] if self.items else []
        return {
            'tipo': 'maestro','nombre': self.nombre,'apellido': self.apellido,'edad': self.edad,'matricula': self.matricula,'especialidad': self.especialidad
        }

    def __str__(self):
        if self.es_arreglo:
            return Arreglo.__str__(self)
        return (f"Maestro: {self.nombre} {self.apellido}, {self.edad} años, "
                f"Matricual: {self.matricula}, Especialidad: {self.especialidad}")

    def cambiarEspecialidad(self, especialidad):
        self.especialidad = especialidad


if __name__ == "__main__":
    MAESTRO = Maestro("Ramiro", "Esquivel", 40, "1", "Android")
    MAESTRO2 = Maestro("Jesus", "Burciaga", 40, "2", "iOS")
    MAESTRO3 = Maestro("Juan", "Perez", 20, "23170120", 10)
    '''print("=== Maestro individual ===")
    print(MAESTRO.to_dict())
    print("\n=== Maestro individual 2 ===")
    print(MAESTRO2.to_dict())
    '''
    print("\n=== Lista de Maestros ===")
    maestros = Maestro()
    maestros.agregar(MAESTRO)
    maestros.agregar(MAESTRO2)
    maestros.agregar(MAESTRO3)
    #maestros.eliminar(MAESTRO2)
    print(maestros.to_dict())
    maestros.to_json()