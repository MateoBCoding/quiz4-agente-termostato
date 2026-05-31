"""Habitacion: encapsula el estado del entorno y su agente termostato.

Cada Room mantiene sus propias percepciones (temperatura, humedad,
presencia, encendido solicitado) e instancia su propio ThermostatAgent.
Esto permite que cada habitacion decida de forma totalmente independiente,
simulando un sistema HVAC zonificado.
"""

from agent import ThermostatAgent

TEMP_ALTA_UMBRAL = 25.0
TEMP_BAJA_UMBRAL = 18.0
HUMEDAD_ALTA_UMBRAL = 70.0


class Room:
    def __init__(
        self,
        nombre: str,
        temperatura: float = 22.0,
        humedad: float = 50.0,
        presencia: bool = True,
        encendido: bool = False,
    ) -> None:
        self.nombre = nombre
        self.temperatura = temperatura
        self.humedad = humedad
        self.presencia = presencia
        self.encendido_solicitado = encendido
        self.agente = ThermostatAgent()
        self.ultima_accion: str = "Termostato en espera (apagado)"
        self.ultimas_percepciones: list = []

    def _construir_percepciones(self) -> list:
        percepciones = []

        if self.encendido_solicitado:
            if not self.agente.encendido:
                percepciones.append("encender")
        else:
            if self.agente.encendido:
                percepciones.append("apagar")
            else:
                return ["apagar"]

        if not self.presencia:
            percepciones.append("ausencia")
        else:
            percepciones.append("presencia")

        if self.temperatura > TEMP_ALTA_UMBRAL:
            percepciones.append("temperatura_alta")
        elif self.temperatura < TEMP_BAJA_UMBRAL:
            percepciones.append("temperatura_baja")
        else:
            percepciones.append("temperatura_optima")

        if self.humedad > HUMEDAD_ALTA_UMBRAL:
            percepciones.append("humedad_alta")

        return percepciones

    def percibir(self) -> str:
        self.ultimas_percepciones = self._construir_percepciones()
        self.ultima_accion = self.agente.percibir(self.ultimas_percepciones)
        return self.ultima_accion
