"""Casa: coleccion ordenada de Rooms con sus agentes termostato.

La House orquesta las percepciones de todas las habitaciones en cada
ciclo y devuelve un dict con la accion seleccionada por cada zona.
"""

from typing import Dict, List

from room import Room

NOMBRES_DEFAULT = [
    "Sala",
    "Cocina",
    "Hab. Principal",
    "Hab. Secundaria",
    "Bano",
]


class House:
    def __init__(self, nombres: List[str] = None) -> None:
        nombres = nombres if nombres is not None else NOMBRES_DEFAULT
        self.rooms: List[Room] = [Room(n) for n in nombres]

    def percibir_todas(self) -> Dict[str, str]:
        return {r.nombre: r.percibir() for r in self.rooms}
