from pathlib import Path
import importlib

from PIL import Image



import streamlit as st
from ultralytics import YOLO


st.set_page_config(
    page_title="Detección PPE",
    page_icon="🦺",
    layout="wide",
)

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "runs" / "detect" / "train-3" / "weights" / "best.pt"


@st.cache_resource(show_spinner="Cargando modelo...")
def load_model():
    return YOLO(str(MODEL_PATH))


def load_image(uploaded_file) -> Image.Image:
    return Image.open(uploaded_file).convert("RGB")


def detect(image: Image.Image):
    model = load_model()
    results = model.predict(image, imgsz=640, conf=0.25, verbose=False)
    return results[0]


def get_detected_items(result) -> list[dict]:
    items = []
    boxes = result.boxes
    if boxes is None or len(boxes) == 0:
        return items

    names = result.names
    for cls_id, conf in zip(boxes.cls.tolist(), boxes.conf.tolist()):
        items.append(
            {
                "clase": names[int(cls_id)],
                "confianza": float(conf),
            }
        )
    return items




st.markdown("# Detección de elementos de protección personal (PPE)")
st.markdown("**Por: Juan Escobar**")
st.divider()

st.subheader("1. Selector o capturador de imagen")
option = st.radio(
    "Elige cómo quieres ingresar la imagen:",
    ("Cargar imagen", "Tomar foto"),
    horizontal=True,
)

uploaded_image = None
if option == "Cargar imagen":
    uploaded_file = st.file_uploader(
        "Sube una imagen",
        type=["jpg", "jpeg", "png", "webp"],
        accept_multiple_files=False,
    )
    if uploaded_file is not None:
        uploaded_image = load_image(uploaded_file)
else:
    camera_file = st.camera_input("Toma una foto")
    if camera_file is not None:
        uploaded_image = load_image(camera_file)

st.divider()
st.subheader("2. Elementos identificados junto con el recuadro")

if uploaded_image is None:
    st.info("Carga una imagen o toma una foto para ver las detecciones del modelo.")
else:
    with st.spinner("Analizando imagen..."):
        result = detect(uploaded_image)
        detected_items = get_detected_items(result)
        annotated = result.plot()  # Imagen con cajas y etiquetas detectadas

    col1, col2 = st.columns([1.2, 0.8], gap="large")

    with col1:
        st.image(annotated, caption="Resultado de detección", channels="BGR", use_container_width=True)

    with col2:
        if detected_items:
            st.success(f"Se detectaron {len(detected_items)} elementos en la imagen.")
            unique_classes = []
            for item in detected_items:
                if item["clase"] not in unique_classes:
                    unique_classes.append(item["clase"])

            st.write("**Clases identificadas:**")
            st.write(", ".join(unique_classes))

        else:
            st.warning("No se identificaron elementos en la imagen.")





