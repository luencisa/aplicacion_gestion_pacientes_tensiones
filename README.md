# Sistema de Gestión de Consultas y Tomas de Tensión (E1 + E2)

Esta aplicación de escritorio permite gestionar el flujo completo de pacientes, agendas de citas y tomas de tensión arterial en el contexto de un centro de atención sanitaria. El proyecto está diseñado bajo una arquitectura limpia de 3 capas con un punto de entrada independiente mediante inyección de dependencias.

## 🛠️ Tecnologías y Principios
* **Lenguaje:** Python 3.x
* **Interfaz Gráfica (Presentación):** Tkinter (Arquitectura MVC)
* **Base de Datos (Datos):** MongoDB (vía PyMongo)
* **Principios de Diseño:** YAGNI, KISS, DRY e Inyección de Dependencias para el desacoplamiento de tecnologías.

---

## 🚀 Cómo Ejecutar el Proyecto

### 1. Prerrequisitos
Asegúrate de tener **MongoDB** ejecutándose de forma local (o configurar tu cadena de conexión en el `.env`) y Python instalado.

### 2. Instalación y Ejecución
Clona el repositorio, instala las dependencias del proyecto y lanza la aplicación:

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar la aplicación
python main.py