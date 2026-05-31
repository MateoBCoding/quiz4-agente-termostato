"""Agente reactivo simple — Termostato inteligente.

Implementa un agente puramente reactivo basado en una tabla ordenada de
reglas condicion-accion. El agente NO mantiene un modelo del mundo: cada
ciclo consulta sus percepciones actuales y devuelve la primera accion
cuya precondicion se cumple.
"""

from typing import Iterable, List, Set, Tuple

Regla = Tuple[Set[str], str]


class ThermostatAgent:
    """Agente reactivo simple para control de climatizacion."""

    def __init__(self) -> None:
        self.encendido: bool = False
        self.reglas: List[Regla] = [
            ({"apagar"}, "Termostato apagado. Hasta pronto"),
            ({"encender"}, "Termostato activado. Bienvenido"),
            ({"ausencia"}, "Activando modo ahorro de energia"),
            ({"temperatura_alta", "presencia"}, "Enfriando habitacion"),
            ({"temperatura_baja", "presencia"}, "Calentando habitacion"),
            (
                {"temperatura_optima", "humedad_alta", "presencia"},
                "Ventilando para reducir humedad",
            ),
            ({"temperatura_optima", "presencia"}, "Manteniendo temperatura optima"),
        ]

    def percibir(self, percepciones: Iterable[str]) -> str:
        """Devuelve la accion correspondiente a las percepciones actuales."""
        percepciones_set = set(percepciones)

        if "encender" in percepciones_set:
            self.encendido = True
        if "apagar" in percepciones_set:
            self.encendido = False
            return "Termostato apagado. Hasta pronto"

        if not self.encendido:
            return "Termostato en espera (apagado)"

        for requeridas, accion in self.reglas:
            if requeridas.issubset(percepciones_set):
                return accion

        return "Sin accion: percepciones no reconocidas"
