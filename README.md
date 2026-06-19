# ♟️ Aprendiendo a jugar a Otelo (IA)

Proyecto para la asignatura de **Inteligencia Artificial** del Grado en Ingeniería Informática - Ingeniería del Software (Universidad de Sevilla).

## 🎯 Objetivo del Proyecto

El objetivo principal es construir un agente inteligente capaz de jugar al clásico juego de Otelo (Reversi) utilizando una combinación de algoritmos de búsqueda clásica y Deep Learning. 

Concretamente, esta implementación corresponde a la **Variante 2 (Convocatoria de Julio)**, que incluye:
* Un motor de juego completo para Otelo interactivo.
* Un agente basado en el algoritmo **Minimax con poda Alfa-Beta** (con profundidad limitada).
* Una **Red Neuronal** entrenada para proporcionar una heurística de evaluación de las posiciones intermedias, reemplazando la evaluación manual.

## 🛠️ Tecnologías utilizadas

* **Python 3**
* **NumPy:** Representación matricial del tablero y cálculos eficientes.
* **PyGame:** Interfaz gráfica para la visualización del tablero y la interacción humana.
* **TensorFlow / Keras:** (Próximamente) Diseño, entrenamiento y predicción del modelo de Deep Learning.

## 🚀 Instalación y ejecución

1. Clona este repositorio:
   ```bash
   git clone <URL_DE_TU_REPOSITORIO>
   cd <NOMBRE_CARPETA>

2. Crea un entorno virtual (recomendado) e instala las dependencias
    ```bash
        python -m venv venv
        source venv/bin/activate
        pip3 install -r requirements.txt
    ```

3. Ejecuta el juego base
    ```bash
        python3 main.py
    ```