from pathlib import Path
import importlib

from PIL import Image



import streamlit as st
from ultralytics import YOLO
import cv2 as cv
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
import av

st.set_page_config(
    page_title="Detección PPE",
    page_icon="🦺",
    layout="wide",
)

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "runs" / "detect" / "train-3" / "weights" / "best.pt"



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


class VideoProcessor(VideoTransformerBase):
    def __init__(self):
        self.model = get_model()

    def recv(self, frame):
        # 1. Convertir el frame de video a un array de numpy (BGR para OpenCV/YOLO)
        img = frame.to_ndarray(format="bgr24")

        # 2. Realizar la detección
        # Usamos stream=True para optimizar el uso de memoria en video
        results = self.model.predict(img, imgsz=640, conf=0.25, verbose=False)

        # 3. Dibujar las anotaciones en el frame
        annotated_frame = results[0].plot()

        # 4. Devolver el frame procesado al stream de video
        return av.VideoFrame.from_ndarray(annotated_frame, format="bgr24")



st.markdown("# Detección de elementos de protección personal (PPE)")
st.markdown("**Por: Juan Escobar**")
st.divider()

st.subheader("1. Selector o capturador de imagen")
option = st.radio(
    "Elige cómo quieres ingresar la imagen:",
    ("Cargar imagen", "Tomar foto", "En vivo"),
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
# ... (tu código anterior de carga de modelo y detección)

if option == "En vivo":
    st.subheader("Streaming de Cámara Web")
    st.write("El modelo está procesando el video fotograma a fotograma.")

    webrtc_streamer(
        key="yolo-live",
        video_processor_factory=VideoProcessor,
        # Configuración para que funcione en servidores externos (STUN servers)
        rtc_configuration={
            "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
        },
        # Esto asegura que el formato sea el correcto para el procesamiento
        media_stream_constraints={"video": True, "audio": False},
    )
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





