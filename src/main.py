"""Punto de entrada del agente termostato multi-habitacion."""

from gui import HouseGUI
from house import House


def main() -> None:
    casa = House()
    interfaz = HouseGUI(casa)
    interfaz.run()


if __name__ == "__main__":
    main()
