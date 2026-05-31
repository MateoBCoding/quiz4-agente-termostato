"""Captura un pantallazo reproducible de la GUI multi-habitacion.

Configura la casa con cinco estados representativos para que el plano
muestre simultaneamente las distintas acciones del agente:
- Sala: enfriando, Cocina: calentando, Hab. Principal: ahorro,
  Hab. Secundaria: manteniendo, Bano: apagado/ventilando.
"""

import os
import sys

from PIL import ImageGrab

sys.path.insert(0, os.path.dirname(__file__))

from gui import HouseGUI
from house import House

OUT_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "assets", "screenshot.png"
)


def configurar_estado(interfaz: HouseGUI) -> None:
    setup = {
        "Sala":            {"encendido": True,  "presencia": True,  "temp": 28.0, "humedad": 55.0},
        "Cocina":          {"encendido": True,  "presencia": True,  "temp": 16.0, "humedad": 60.0},
        "Hab. Principal":  {"encendido": True,  "presencia": False, "temp": 22.0, "humedad": 50.0},
        "Hab. Secundaria": {"encendido": True,  "presencia": True,  "temp": 22.0, "humedad": 45.0},
        "Bano":            {"encendido": True,  "presencia": True,  "temp": 23.0, "humedad": 85.0},
    }
    for nombre, valores in setup.items():
        v = interfaz.room_vars[nombre]
        v["encendido"].set(valores["encendido"])
        v["presencia"].set(valores["presencia"])
        v["temp"].set(valores["temp"])
        v["humedad"].set(valores["humedad"])

    # Primer ciclo encendido genera "Bienvenido"; segundo ya muestra accion operativa.
    interfaz._actualizar()
    interfaz._actualizar()


def main() -> None:
    casa = House()
    interfaz = HouseGUI(casa)

    configurar_estado(interfaz)

    interfaz.root.geometry("1180x820+120+80")
    interfaz.root.attributes("-topmost", True)
    interfaz.root.lift()
    interfaz.root.focus_force()

    def capturar_y_salir():
        interfaz.root.update_idletasks()
        interfaz.root.update()
        interfaz.root.lift()
        interfaz.root.update()
        x = interfaz.root.winfo_rootx()
        y = interfaz.root.winfo_rooty()
        w = interfaz.root.winfo_width()
        h = interfaz.root.winfo_height()
        bbox = (x, y, x + w, y + h)
        print(f"Capturando bbox={bbox}")
        img = ImageGrab.grab(bbox=bbox, all_screens=True)
        os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
        img.save(OUT_PATH)
        print(f"Screenshot guardado en: {OUT_PATH}")
        interfaz.root.destroy()

    interfaz.root.after(2000, capturar_y_salir)
    interfaz.root.mainloop()


if __name__ == "__main__":
    main()
