# Termostato Inteligente Multi-Habitación

Aplicación de escritorio que simula un agente reactivo simple controlando la climatización de una casa con cinco habitaciones (Sala, Cocina, Habitación Principal, Habitación Secundaria, Baño). Cada habitación tiene su propio agente termostato independiente con la misma tabla de siete reglas condición-acción.

Quiz 4 — Inteligencia Artificial. Politécnico Colombiano Jaime Isaza Cadavid.
Autor: **Mateo Betancur** — mateo.betancur@s4ds.com

---

## Tabla de contenidos
1. [Prerrequisitos del sistema](#1-prerrequisitos-del-sistema)
2. [Instalación](#2-instalación)
3. [Cómo abrir la aplicación](#3-cómo-abrir-la-aplicación)
4. [Funcionalidades](#4-funcionalidades)
5. [Guía de uso paso a paso](#5-guía-de-uso-paso-a-paso)
6. [Tabla percepción → acción del agente](#6-tabla-percepción--acción-del-agente)
7. [Regenerar pantallazo y documento entregable](#7-regenerar-pantallazo-y-documento-entregable)
8. [Estructura del proyecto](#8-estructura-del-proyecto)
9. [Solución de problemas](#9-solución-de-problemas)

---

## 1. Prerrequisitos del sistema

| Requisito | Versión recomendada | Notas |
|---|---|---|
| Sistema operativo | Windows 10/11, macOS o Linux | Probado en Windows 10. La captura de pantalla automática (`capture_screenshot.py`) usa `PIL.ImageGrab`, que funciona en Windows y macOS sin configuración extra; en Linux requiere `scrot` o `xdotool`. |
| Python | 3.7 o superior | Verifica con `python --version`. |
| Tkinter | Incluido en la mayoría de instalaciones de Python | En Linux puede requerir `sudo apt install python3-tk`. |
| pip | Cualquier versión reciente | Para instalar las dependencias del documento. |
| Microsoft Word (opcional) | 2016 o superior | Solo necesario para abrir el documento `.docx` entregable. |

**Dependencias de Python** (solo necesarias para regenerar el documento y el pantallazo):
- `python-docx` ≥ 0.8.11
- `Pillow` ≥ 9.0.0

La aplicación principal (`main.py`) usa exclusivamente la biblioteca estándar y **no requiere instalar nada** si Tkinter ya está disponible.

---

## 2. Instalación

1. Clona o descarga el proyecto a una carpeta local.
2. Abre una terminal en la raíz del proyecto.
3. (Opcional, recomendado) Crea un entorno virtual:
   ```bash
   python -m venv venv
   # En Windows:
   venv\Scripts\activate
   # En macOS/Linux:
   source venv/bin/activate
   ```
4. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

---

## 3. Cómo abrir la aplicación

Desde la raíz del proyecto:

```bash
python src/main.py
```

Se abrirá una ventana titulada **"Termostato Multi-Habitacion - Agente Reactivo"** (~1180×820 px) con dos secciones:

- **Arriba**: plano visual de la casa con las cinco habitaciones representadas como rectángulos coloreados.
- **Abajo**: cinco tarjetas de control, una por habitación.

> Cierra la ventana normalmente (botón X) para terminar la aplicación.

---

## 4. Funcionalidades

### 4.1 Plano interactivo de la casa
- Las cinco habitaciones se dibujan como rectángulos en un Canvas, con una disposición tipo plano arquitectónico.
- Cada rectángulo muestra:
  - **Nombre** de la habitación.
  - **Temperatura** actual en °C y **humedad** en %.
  - **Acción** que el agente decidió ejecutar.
  - Una **estrella ★ amarilla** en la esquina superior derecha si hay presencia y la habitación está encendida.
- El **color de fondo** del rectángulo cambia automáticamente según la acción del agente:

  | Color | Significado |
  |---|---|
  | 🔵 Azul | Enfriando habitación |
  | 🔴 Rojo | Calentando habitación |
  | 🟦 Cyan | Ventilando para reducir humedad |
  | 🟢 Verde | Manteniendo temperatura óptima |
  | 🟡 Amarillo | Modo ahorro de energía (sin presencia) |
  | ⬛ Gris | Apagado / en espera |

### 4.2 Leyenda de colores
Debajo del plano hay una barra con los seis colores y sus etiquetas para facilitar la interpretación visual.

### 4.3 Tarjetas de control por habitación
Cada habitación tiene una tarjeta independiente con:
- **Casilla "Encendido"**: enciende o apaga el termostato de esa zona.
- **Casilla "Presencia"**: simula si hay personas en la habitación.
- **Slider "Temp (C)"**: rango 10 °C a 35 °C.
- **Slider "Humedad (%)"**: rango 0 % a 100 %.
- **Etiqueta "Acción del agente"**: muestra en texto la acción actual (espejo del plano).

### 4.4 Reactividad en tiempo real
Cada vez que cambias **cualquier control** (mover un slider, marcar/desmarcar una casilla), el agente correspondiente se ejecuta inmediatamente y tanto la tarjeta como el rectángulo del plano se actualizan al instante.

### 4.5 Independencia entre habitaciones
Cada habitación tiene su propia instancia del agente. Puedes tener simultáneamente, por ejemplo, la Sala enfriando, la Cocina calentando, el Baño ventilando y la Habitación Principal en modo ahorro — todo en el mismo instante.

### 4.6 Umbrales de decisión (fijos en código)
Los umbrales que dispara cada acción están definidos en `src/room.py`:
- **Temperatura alta**: > 25 °C
- **Temperatura baja**: < 18 °C
- **Temperatura óptima**: entre 18 °C y 25 °C
- **Humedad alta**: > 70 %

---

## 5. Guía de uso paso a paso

1. **Inicia la aplicación** con `python src/main.py`. Al arrancar, todas las habitaciones están apagadas (gris).
2. **Enciende una habitación** marcando su casilla "Encendido" — el rectángulo cambia de color según el estado por defecto (22 °C, 50 % humedad, con presencia → verde "Manteniendo temperatura óptima").
3. **Sube la temperatura** de la Sala por encima de 25 °C arrastrando su slider → el rectángulo se vuelve **azul** y la acción cambia a "Enfriando habitación".
4. **Baja la temperatura** de la Cocina por debajo de 18 °C → rectángulo **rojo**, "Calentando habitación".
5. **Sube la humedad** del Baño por encima de 70 % manteniendo temperatura óptima → rectángulo **cyan**, "Ventilando para reducir humedad".
6. **Desmarca "Presencia"** en la Hab. Principal → rectángulo **amarillo**, "Activando modo ahorro de energía" (independiente de la temperatura).
7. **Desmarca "Encendido"** en cualquier zona → vuelve a **gris**, "Termostato apagado".

Cada acción es instantánea y completamente independiente entre habitaciones.

---

## 6. Tabla percepción → acción del agente

La misma tabla se aplica de forma independiente en cada habitación. El agente recorre las reglas en orden y ejecuta la primera cuyo conjunto de percepciones requeridas esté contenido en las percepciones actuales.

| Percepción | Acción | Color |
|---|---|---|
| `apagar` | Termostato apagado. Hasta pronto | Gris |
| `encender` (primer ciclo) | Termostato activado. Bienvenido | Verde |
| `ausencia` | Activando modo ahorro de energía | Amarillo |
| `temperatura_alta, presencia` | Enfriando habitación | Azul |
| `temperatura_baja, presencia` | Calentando habitación | Rojo |
| `temperatura_optima, humedad_alta, presencia` | Ventilando para reducir humedad | Cyan |
| `temperatura_optima, presencia` | Manteniendo temperatura óptima | Verde |

---

## 7. Regenerar pantallazo y documento entregable

### Pantallazo (Figura 1 del documento)
```bash
python src/capture_screenshot.py
```
Configura la casa en un estado representativo donde las cinco habitaciones muestran cinco acciones diferentes simultáneamente y guarda la imagen en `assets/screenshot.png`. La ventana se abre, se captura y se cierra automáticamente.

### Documento Word entregable
```bash
python docs/generar_documento.py
```
Toma el template original (`C:\Users\user\Downloads\Taller_Agentes.docx`), lo rellena con el contenido del proyecto (resumen, PEAS, tabla percepción-acción, sección de aplicación construida con la Figura 1 incrustada, conclusiones y bibliografía) y guarda el resultado en `docs/Taller_Agentes_Lleno.docx`.

> **Importante:** cierra el documento en Word antes de regenerarlo, de lo contrario falla con un error de permisos por bloqueo de escritura.

---

## 8. Estructura del proyecto

```
.
├── src/
│   ├── agent.py              # ThermostatAgent: tabla reactiva de 7 reglas
│   ├── room.py               # Room: estado del entorno + agente por habitación
│   ├── house.py              # House: orquesta las 5 habitaciones
│   ├── gui.py                # HouseGUI: plano (Canvas) + 5 tarjetas (Tkinter)
│   ├── main.py               # Entrypoint principal
│   └── capture_screenshot.py # Helper para regenerar la Figura 1
├── docs/
│   ├── generar_documento.py  # Llenado automático del template .docx
│   └── Taller_Agentes_Lleno.docx
├── assets/
│   └── screenshot.png        # Figura 1 (pantallazo del plano)
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 9. Solución de problemas

| Problema | Causa probable | Solución |
|---|---|---|
| `ModuleNotFoundError: No module named 'tkinter'` | Tkinter no está instalado | Linux: `sudo apt install python3-tk`. Windows/macOS: reinstalar Python marcando la opción de Tcl/Tk. |
| `PermissionError` al regenerar el .docx | El archivo está abierto en Word | Cierra Word y vuelve a ejecutar el script. |
| El pantallazo captura otra ventana | Otra aplicación se interpuso al frente | Cierra ventanas que se superpongan y vuelve a correr `capture_screenshot.py`. |
| La ventana se ve cortada o desordenada | Resolución de pantalla muy baja | Reduce el escalado del sistema o aumenta el tamaño de la ventana editando `geometry("1180x820")` en `src/gui.py`. |
| Cambios en el slider no se reflejan | Bug raro de Tkinter en la sesión | Cierra y vuelve a abrir la aplicación. |
