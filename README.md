# ⚪⚫ Aprendiendo a jugar a Otelo: Agente Inteligente con Búsqueda Adversaria y Deep Learning

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-orange.svg)
![Keras](https://img.shields.io/badge/Keras-2.x-red.svg)
![PyGame](https://img.shields.io/badge/PyGame-2.x-green.svg)
![License](https://img.shields.io/badge/License-MIT-lightgrey.svg)

Este repositorio contiene el código fuente y la memoria del Trabajo de Fin de Asignatura de **Inteligencia Aritificial** para el desarrollo de un agente inteligente capaz de jugar al clásico juego de mesa **Otelo (Reversi)**.

El proyecto explora la hibridación de algoritmos clásicos deterministas (**Minimax con Poda Alfa-Beta**) con modelos paramétricos modernos basados en **Deep Learning**, sustituyendo las funciones de evaluación manuales por una Red Neuronal entrenada mediante autojuego.

##  Características Principales

* **Motor de Juego Aislado:** Implementación de las reglas completas de Otelo (mecánica de flanqueo, turnos nulos, condiciones de victoria) utilizando `NumPy` de forma altamente eficiente, separando la lógica de la interfaz.
* **Agente Minimax Clásico:** Algoritmo de búsqueda adversaria con poda alfa-beta, límite de profundidad dinámico y heurística basada en el recuento del diferencial de fichas.
* **Agente Híbrido (Deep Learning):** Sustitución de la heurística clásica por un Perceptrón Multicapa (MLP) entrenado con Keras/TensorFlow para deducir patrones estratégicos (control de esquinas, bordes, etc.).
* **Autojuego y Generación de Datos:** Módulo automatizado para simular miles de partidas entre agentes en segundo plano y retroalimentar a la IA con nuevos tableros etiquetados.
* **Interfaz Gráfica (FSM):** Interfaz interactiva desarrollada con `PyGame`, regida por una Máquina de Estados Finita (Menú, Configuración de IA, Juego en curso, Resolución). Permite inyectar parámetros como el tipo de IA y su profundidad antes de jugar.

---


## 📂 Estructura del Proyecto

```text
├── datasets/                 # Tensores NumPy (.npy) con tableros y etiquetas generados por autojuego.
├── docs/                     # Memoria académica del proyecto (PDF y código fuente LaTeX).
│   └── images/               # Capturas de pantalla e imágenes de la memoria.
├── modelos/                  # Modelos de redes neuronales compilados (.keras).
├── src/                      # Código fuente principal del proyecto.
│   ├── entrenamiento_red.py  # Script de diseño, entrenamiento y evaluación de modelos en Keras.
│   ├── generar_datos.py      # Script de generación de datasets mediante autojuego.
│   ├── main.py               # Orquestador gráfico (PyGame) y Máquina de Estados.
│   ├── minimax.py            # Inteligencia Artificial (Clásica e Híbrida).
│   ├── otelo.py              # Motor lógico del juego (tablero, reglas y validaciones).
│   ├── test_minimax.py       # Suite de pruebas unitarias para escenarios críticos (ej. turnos nulos).
│   └── torneo.py             # Entorno de simulación de torneos automatizados IA vs IA.
├── README.md                 # Documentación del repositorio.
└── requirements.txt          # Dependencias del proyecto.
```
## 🚀 Instalación y ejecución

### 1. Clona este repositorio
```bash
git clone <URL_DE_TU_REPOSITORIO>
cd <NOMBRE_CARPETA>
```

### 2. Crea un entorno virtual (recomendado) e instala las dependencias
Dependiendo de tu sistema operativo, los comandos para activar el entorno virtual varían ligeramente:

* **Usuarios de Windows:**
  ```bash
  python -m venv venv
  venv\Scripts\activate
  pip install -r requirements.txt
  ```

* **Usuarios de macOS y Linux:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  pip3 install -r requirements.txt
  ```

### 3. Ejecuta el juego base
Para lanzar el juego y enfrentarte a la IA (o jugar Jugador vs Jugador), asegúrate de tener la terminal abierta en el directorio raíz del proyecto y ejecuta el orquestador principal como módulo. 

* **Usuarios de Windows:**
  ```bash
  python -m src.main
  ```

* **Usuarios de macOS y Linux:**
  ```bash
  python3 -m src.main



### 4. Herramientas de Desarrollo y Entrenamiento

Si deseas generar nuevos datos, reentrenar los modelos desde cero, o simular torneos analíticos sin interfaz gráfica, puedes ejecutar los módulos correspondientes desde la raíz del proyecto:

* Generar nuevos tableros de autojuego: 
    ```bash 
    python -m src.generar_datos
* Entrenar redes neuronales: 
    ```bash
    python -m src.entrenamiento_red
* Ejecutar torneo de validación: 
    ```bash
    python -m src.torneo
### 5. Ejecución de Pruebas Unitarias

Para verificar la estabilidad del motor y el control de turnos nulos del algoritmo Minimax, puedes lanzar la suite de pruebas automatizada:

* Usuarios de Windows: 
    ```bash
    python -m unittest src.test_minimax
* Usuarios de macOS/Linux: 
    ```bash
    python3 -m unittest src.test_minimax
