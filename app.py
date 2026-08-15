import streamlit as st
import easyocr
import numpy as np
from PIL import Image

st.title("Urdu OCR -- Code Saviours SI-26")
st.write("Upload an image containing Urdu text and get the extracted text.")

@st.cache_resource
def load_reader():
    return easyocr.Reader(['ur'])

reader = load_reader()

uploaded_file = st.file_uploader("Upload Urdu Image", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Image", use_container_width=True)
    with st.spinner("Extracting text..."):
        result = reader.readtext(np.array(image), detail=0, paragraph=True)
        text = " ".join(result)
    st.subheader("Extracted Urdu Text")
    st.write(text if text else "Could not extract text from this image")
