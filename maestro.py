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

    def read_json(self):
        with open("maestros.json", 'r') as file:
            data = json.load(file)
            return self._dict_to_object(data)

    def _dict_to_object(self, data):
        if not data:
            return None

        if isinstance(data, list):
            maestro_arreglo = Maestro()
            for item in data:
                maestro = maestro_arreglo._dict_to_object(item)                
                maestro_arreglo.agregar(maestro)
            return maestro_arreglo
        else:
            return Maestro(
                data['nombre'],
                data['apellido'],
                data['edad'],
                data['matricula'],
                data['especialidad']
            )

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
    MAESTRO3 = Maestro("Juan", "Perez", 20, "23170120", "Web")

    print("\n=== Lista de Maestros ===")
    maestros = Maestro()
    maestros.agregar(MAESTRO, MAESTRO2, MAESTRO3)
    print(maestros.to_dict())
    maestros.to_json()

    print("\n=== Maestros Recuperados ===")
    maestro_recuperado = Maestro().read_json()
    if maestro_recuperado.es_arreglo:
        for maestro in maestro_recuperado.items:
            print(f"\nNombre: {maestro.nombre} {maestro.apellido}")
            print(f"Edad: {maestro.edad}")
            print(f"Matrícula: {maestro.matricula}")
            print(f"Especialidad: {maestro.especialidad}")
    else:
        print(f"\nNombre: {maestro_recuperado.nombre} {maestro_recuperado.apellido}")
        print(f"Edad: {maestro_recuperado.edad}")
        print(f"Matrícula: {maestro_recuperado.matricula}")
        print(f"Especialidad: {maestro_recuperado.especialidad}")

    maestro = Maestro()
    maestro_recuperado = maestro.read_json()
    maestro = maestro_recuperado
    maestro.to_json()