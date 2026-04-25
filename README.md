# Detección de Elementos de Protección Personal (PPE)

Aplicación web construida con **Streamlit** y **YOLOv8** para detectar elementos de protección personal (EPP/PPE) en imágenes de sitios de construcción.

**Autor:** Juan Escobar

---

## Descripción

La aplicación permite cargar una imagen o tomar una foto directamente desde la cámara, y luego utiliza un modelo YOLO entrenado para identificar y clasificar los elementos de protección personal y otros objetos presentes en la escena. Los resultados se muestran con recuadros anotados y una lista de las clases detectadas.

## Clases detectadas

El dataset cuenta con 25 clases en total, pero **solo algunas son relevantes para la detección de EPP**. Las clases realmente utilizadas en el contexto de seguridad personal son:

| Clase | Descripción |
|---|---|
| Hardhat | Casco de seguridad presente |
| NO-Hardhat | Persona sin casco |
| Safety Vest | Chaleco reflectante presente |
| NO-Safety Vest | Persona sin chaleco |
| Mask | Mascarilla presente |
| NO-Mask | Persona sin mascarilla |
| Gloves | Guantes de protección |
| Safety Cone | Cono de seguridad |
| Worker | Trabajador identificado |

Las demás clases del dataset corresponden a vehículos y maquinaria (excavadoras, camiones, buses, etc.) que no son el foco principal de la aplicación.

### ⚠️ Limitación conocida

El modelo **no detecta gafas de seguridad (safety glasses/goggles)**, ya que esta clase no fue incluida en el dataset de entrenamiento. Se reconoce como una mejora pendiente para futuras versiones.

## Requisitos

- Python 3.10+
- Dependencias del sistema (ver `packages.txt`):
  ```
  libgl1
  ```
- Dependencias Python (ver `requirements.txt`):
  ```
  streamlit
  opencv-python-headless>=4.8.0
  lap
  ultralytics==8.4.41
  ```

## Instalación

```bash
# 1. Clonar el repositorio
git clone https://github.com/jgesc-05/epp-st-exercise.git
cd epp-st-exercise

# 2. (Opcional) Crear y activar entorno virtual
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# 3. Instalar dependencias del sistema (Linux)
sudo apt-get install -y libgl1

# 4. Instalar dependencias Python
pip install -r requirements.txt
```

## Uso

```bash
streamlit run app.py
```

La aplicación abrirá en el navegador en `http://localhost:8501`.

1. Selecciona **"Cargar imagen"** para subir un archivo (JPG, PNG, WEBP) o **"Tomar foto"** para usar la cámara.
2. La aplicación analizará la imagen automáticamente con el modelo YOLO.
3. Se mostrará la imagen con los recuadros de detección y un resumen de las clases identificadas.

## Estructura del proyecto

```
epp-st-exercise/
├── app.py                  # Aplicación Streamlit principal
├── requirements.txt        # Dependencias Python
├── packages.txt            # Dependencias del sistema
├── EPP.ipynb               # Notebook de entrenamiento/exploración
├── epp3-1/                 # Dataset (Roboflow, CC BY 4.0)
│   ├── data.yaml
│   ├── train/
│   ├── valid/
│   └── test/
└── runs/                   # Resultados del entrenamiento YOLO
    └── detect/
        └── train-3/
            └── weights/
                └── best.pt # Modelo entrenado
```

## Dataset

Dataset provisto por [Roboflow Universe](https://universe.roboflow.com/juans-workspace-agc9e/epp3).  
Licencia: **CC BY 4.0**

## Tecnologías

- [Streamlit](https://streamlit.io/) — Interfaz web interactiva
- [Ultralytics YOLOv8](https://docs.ultralytics.com/) — Detección de objetos
- [Pillow](https://pillow.readthedocs.io/) — Procesamiento de imágenes
- [OpenCV](https://opencv.org/) — Visión por computadora
