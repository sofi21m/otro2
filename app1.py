import streamlit as st
import cv2
import numpy as np
import pytesseract

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Studio OCR",
    page_icon="📷",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo visual moderno (Encabezado)
st.title("📷 Studio OCR")
st.caption("Captura imágenes con tu cámara, aplica filtros de contraste y extrae texto en tiempo real.")
st.divider()

# --- BARRA LATERAL DE CONFIGURACIÓN ---
with st.sidebar:
    st.header("⚙️ Opciones de Procesamiento")
    
    filtro = st.radio(
        "Filtro de Imagen:",
        ('Sin Filtro', 'Con Filtro (Invertir)'),
        help="Aplica un filtro negativo para resaltar texto si la foto tiene mala iluminación."
    )
    
    st.divider()
    st.info("💡 **Consejo:** Para mejores resultados de OCR, asegúrate de tener buena iluminación y enfocar bien el texto.")

# --- DIAGRAMACIÓN EN COLUMNAS (SIDE-BY-SIDE) ---
col_camara, col_resultado = st.columns([1, 1], gap="large")

# COLUMNA IZQUIERDA: CÁMARA Y PROCESAMIENTO
with col_camara:
    with st.container(border=True):
        st.subheader("1. Captura de Imagen")
        img_file_buffer = st.camera_input("Toma una Foto", label_visibility="collapsed")

# COLUMNA DERECHA: RESULTADOS Y EDICIÓN
with col_resultado:
    with st.container(border=True):
        st.subheader("2. Texto Detectado")
        
        if img_file_buffer is not None:
            # Decodificar imagen
            bytes_data = img_file_buffer.getvalue()
            cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
            
            # Aplicar filtro si se seleccionó
            if filtro == 'Con Filtro (Invertir)':
                cv2_img = cv2.bitwise_not(cv2_img)
            
            # OCR con Pytesseract
            img_rgb = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
            text = pytesseract.image_to_string(img_rgb).strip()
            
            # Métricas rápidas
            palabras = len(text.split()) if text else 0
            st.metric(label="Palabras Detectadas", value=palabras)
            
            if text:
                st.success("¡Texto extraído exitosamente!")
                # Área de texto editable para el usuario
                st.text_area("Resultado:", value=text, height=220)
            else:
                st.warning("⚠️ No se pudo reconocer texto claro en esta imagen. Intenta tomarla de nuevo.")
        else:
            st.info("👈 Toma una foto usando la cámara para comenzar el análisis OCR.")


    


