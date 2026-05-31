"""Interfaz Tkinter multi-habitacion para el agente termostato.

Muestra una casa con 5 habitaciones representadas como rectangulos en un
plano. Cada habitacion cambia de color segun la accion seleccionada por
su agente reactivo. Debajo del plano, una tarjeta por habitacion expone
controles individuales (encendido, temperatura, humedad, presencia).
"""

import tkinter as tk
from tkinter import ttk

from house import House

COLOR_FONDO = "#0f172a"
COLOR_TARJETA = "#1e293b"
COLOR_BORDE = "#334155"
COLOR_TEXTO = "#f1f5f9"
COLOR_TENUE = "#94a3b8"
COLOR_ACENTO = "#38bdf8"

COLORES_ACCION = {
    "Enfriando habitacion": "#3b82f6",
    "Calentando habitacion": "#ef4444",
    "Ventilando para reducir humedad": "#06b6d4",
    "Manteniendo temperatura optima": "#22c55e",
    "Activando modo ahorro de energia": "#eab308",
    "Termostato apagado. Hasta pronto": "#475569",
    "Termostato en espera (apagado)": "#475569",
    "Termostato activado. Bienvenido": "#22c55e",
}

GEOMETRIA_PLANO = {
    "Sala":             (10, 10,  340, 130),
    "Cocina":           (340, 10, 670, 130),
    "Bano":             (10, 130, 210, 230),
    "Hab. Principal":   (210, 130, 670, 230),
    "Hab. Secundaria":  (10, 230, 670, 330),
}

CANVAS_W = 680
CANVAS_H = 340


class HouseGUI:
    def __init__(self, house: House) -> None:
        self.house = house

        self.root = tk.Tk()
        self.root.title("Termostato Multi-Habitacion - Agente Reactivo")
        self.root.geometry("1180x820")
        self.root.configure(bg=COLOR_FONDO)

        self.room_vars = {}
        for room in self.house.rooms:
            self.room_vars[room.nombre] = {
                "encendido": tk.BooleanVar(value=room.encendido_solicitado),
                "presencia": tk.BooleanVar(value=room.presencia),
                "temp": tk.DoubleVar(value=room.temperatura),
                "humedad": tk.DoubleVar(value=room.humedad),
                "accion": tk.StringVar(value=room.ultima_accion),
            }

        self._construir_ui()
        self._actualizar()

    def _construir_ui(self) -> None:
        tk.Label(
            self.root,
            text="Termostato Inteligente Multi-Habitacion",
            font=("Segoe UI", 20, "bold"),
            fg=COLOR_TEXTO,
            bg=COLOR_FONDO,
        ).pack(pady=(16, 2))

        tk.Label(
            self.root,
            text="Agente reactivo simple - una instancia por zona",
            font=("Segoe UI", 10, "italic"),
            fg=COLOR_TENUE,
            bg=COLOR_FONDO,
        ).pack(pady=(0, 12))

        canvas_frame = tk.Frame(self.root, bg=COLOR_FONDO)
        canvas_frame.pack(pady=(0, 12))

        self.canvas = tk.Canvas(
            canvas_frame,
            width=CANVAS_W,
            height=CANVAS_H,
            bg=COLOR_TARJETA,
            highlightthickness=2,
            highlightbackground=COLOR_BORDE,
        )
        self.canvas.pack()

        self._construir_leyenda()
        self._construir_tarjetas()

    def _construir_leyenda(self) -> None:
        frame = tk.Frame(self.root, bg=COLOR_FONDO)
        frame.pack(pady=(0, 6))

        leyenda_items = [
            ("Enfriando", "#3b82f6"),
            ("Calentando", "#ef4444"),
            ("Ventilando", "#06b6d4"),
            ("Optimo", "#22c55e"),
            ("Ahorro", "#eab308"),
            ("Apagado", "#475569"),
        ]
        for texto, color in leyenda_items:
            chip = tk.Frame(frame, bg=color, width=14, height=14)
            chip.pack(side="left", padx=(10, 4))
            chip.pack_propagate(False)
            tk.Label(
                frame,
                text=texto,
                bg=COLOR_FONDO,
                fg=COLOR_TENUE,
                font=("Segoe UI", 9),
            ).pack(side="left")

    def _construir_tarjetas(self) -> None:
        tarjetas_frame = tk.Frame(self.root, bg=COLOR_FONDO)
        tarjetas_frame.pack(pady=(8, 16), padx=10, fill="x")

        for col, room in enumerate(self.house.rooms):
            self._construir_tarjeta(tarjetas_frame, room, col)

        for col in range(len(self.house.rooms)):
            tarjetas_frame.columnconfigure(col, weight=1, uniform="card")

    def _construir_tarjeta(self, parent, room, col) -> None:
        nombre = room.nombre
        v = self.room_vars[nombre]

        card = tk.Frame(
            parent,
            bg=COLOR_TARJETA,
            highlightthickness=1,
            highlightbackground=COLOR_BORDE,
        )
        card.grid(row=0, column=col, padx=5, pady=4, sticky="nsew")

        tk.Label(
            card,
            text=nombre,
            font=("Segoe UI", 12, "bold"),
            fg=COLOR_TEXTO,
            bg=COLOR_TARJETA,
        ).pack(anchor="w", padx=10, pady=(8, 4))

        tk.Checkbutton(
            card,
            text="Encendido",
            variable=v["encendido"],
            command=self._actualizar,
            bg=COLOR_TARJETA,
            fg=COLOR_TEXTO,
            activebackground=COLOR_TARJETA,
            activeforeground=COLOR_TEXTO,
            selectcolor=COLOR_FONDO,
            font=("Segoe UI", 9),
        ).pack(anchor="w", padx=8)

        tk.Checkbutton(
            card,
            text="Presencia",
            variable=v["presencia"],
            command=self._actualizar,
            bg=COLOR_TARJETA,
            fg=COLOR_TEXTO,
            activebackground=COLOR_TARJETA,
            activeforeground=COLOR_TEXTO,
            selectcolor=COLOR_FONDO,
            font=("Segoe UI", 9),
        ).pack(anchor="w", padx=8)

        temp_row = tk.Frame(card, bg=COLOR_TARJETA)
        temp_row.pack(fill="x", padx=8, pady=(6, 0))
        tk.Label(
            temp_row,
            text="Temp (C):",
            bg=COLOR_TARJETA,
            fg=COLOR_TENUE,
            font=("Segoe UI", 9),
        ).pack(side="left")
        temp_label = tk.Label(
            temp_row,
            text=f"{v['temp'].get():.1f}",
            bg=COLOR_TARJETA,
            fg=COLOR_ACENTO,
            font=("Segoe UI", 9, "bold"),
            width=5,
        )
        temp_label.pack(side="right")
        v["temp_label"] = temp_label

        ttk.Scale(
            card,
            from_=10,
            to=35,
            orient="horizontal",
            variable=v["temp"],
            command=lambda _e: self._actualizar(),
        ).pack(fill="x", padx=8, pady=(0, 4))

        hum_row = tk.Frame(card, bg=COLOR_TARJETA)
        hum_row.pack(fill="x", padx=8, pady=(2, 0))
        tk.Label(
            hum_row,
            text="Humedad (%):",
            bg=COLOR_TARJETA,
            fg=COLOR_TENUE,
            font=("Segoe UI", 9),
        ).pack(side="left")
        hum_label = tk.Label(
            hum_row,
            text=f"{v['humedad'].get():.1f}",
            bg=COLOR_TARJETA,
            fg=COLOR_ACENTO,
            font=("Segoe UI", 9, "bold"),
            width=5,
        )
        hum_label.pack(side="right")
        v["hum_label"] = hum_label

        ttk.Scale(
            card,
            from_=0,
            to=100,
            orient="horizontal",
            variable=v["humedad"],
            command=lambda _e: self._actualizar(),
        ).pack(fill="x", padx=8, pady=(0, 6))

        sep = tk.Frame(card, bg=COLOR_BORDE, height=1)
        sep.pack(fill="x", padx=8, pady=4)

        tk.Label(
            card,
            text="Accion del agente:",
            bg=COLOR_TARJETA,
            fg=COLOR_TENUE,
            font=("Segoe UI", 8),
        ).pack(anchor="w", padx=8)
        tk.Label(
            card,
            textvariable=v["accion"],
            bg=COLOR_TARJETA,
            fg="#4ade80",
            font=("Segoe UI", 10, "bold"),
            wraplength=200,
            justify="left",
        ).pack(anchor="w", padx=8, pady=(0, 10))

    def _aplicar_vars_a_rooms(self) -> None:
        for room in self.house.rooms:
            v = self.room_vars[room.nombre]
            room.encendido_solicitado = v["encendido"].get()
            room.presencia = v["presencia"].get()
            room.temperatura = v["temp"].get()
            room.humedad = v["humedad"].get()

    def _redibujar_plano(self) -> None:
        self.canvas.delete("all")
        for room in self.house.rooms:
            x0, y0, x1, y1 = GEOMETRIA_PLANO[room.nombre]
            color = COLORES_ACCION.get(room.ultima_accion, "#475569")

            self.canvas.create_rectangle(
                x0, y0, x1, y1,
                fill=color,
                outline=COLOR_BORDE,
                width=2,
            )

            cx = (x0 + x1) // 2
            cy = (y0 + y1) // 2

            self.canvas.create_text(
                cx, y0 + 18,
                text=room.nombre,
                fill="#ffffff",
                font=("Segoe UI", 12, "bold"),
            )
            self.canvas.create_text(
                cx, cy,
                text=f"{room.temperatura:.1f} C   |   {room.humedad:.0f}%",
                fill="#ffffff",
                font=("Segoe UI", 10),
            )
            self.canvas.create_text(
                cx, y1 - 16,
                text=room.ultima_accion,
                fill="#ffffff",
                font=("Segoe UI", 9, "italic"),
                width=(x1 - x0) - 14,
            )
            if room.presencia and room.encendido_solicitado:
                self.canvas.create_text(
                    x1 - 14, y0 + 14,
                    text="★",
                    fill="#fde047",
                    font=("Segoe UI", 13, "bold"),
                )

    def _actualizar(self) -> None:
        self._aplicar_vars_a_rooms()
        self.house.percibir_todas()

        for room in self.house.rooms:
            v = self.room_vars[room.nombre]
            v["temp_label"].config(text=f"{v['temp'].get():.1f}")
            v["hum_label"].config(text=f"{v['humedad'].get():.1f}")
            v["accion"].set(room.ultima_accion)

        self._redibujar_plano()

    def run(self) -> None:
        self.root.mainloop()
