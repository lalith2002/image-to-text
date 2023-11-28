!pip install streamlit
!pip install pytesseract
!pip install pdfplumber

import streamlit as st
from PIL import Image
import pytesseract
import pdfplumber

st.title("Extracting Texts from Image and PDF")

# File uploader (supports both images and PDFs)
uploaded_file = st.file_uploader(label="Upload your file here", type=["png", "jpg", "jpeg", "pdf"])

def extract_text_from_image(image):
    # Convert image to grayscale
    gray_image = image.convert('L')

    # Apply thresholding to binarize the image
    thresh = 127
    binary_image = gray_image.point(lambda x: 0 if x < thresh else 255)

    # Extract text using Pytesseract
    text = pytesseract.image_to_string(binary_image, config='--psm 10')
    return text
if uploaded_file is not None:
    file_extension = uploaded_file.name.split(".")[-1]

    if file_extension in ["png", "jpg", "jpeg"]:
        # Handle image files
        input_image = Image.open(uploaded_file)  # Read image
        st.image(input_image)  # Display image

        extracted_text = extract_text_from_image(input_image)
        st.write(extracted_text)

        # Display successful message
        st.balloons()

    elif file_extension == "pdf":
        # Handle PDF files
        with pdfplumber.open(uploaded_file) as pdf:
            pages = pdf.pages

            extracted_text = []
            for page in pages:
                page_image = page.to_image(resolution=200)
                extracted_text.append(extract_text_from_image(page_image))

        st.write(extracted_text)

        # Display successful message
        st.balloons()

    else:
        st.write("Unsupported file format. Please upload an image (PNG, JPG, JPEG) or PDF file.")
else:
    st.write("Upload an image or PDF file")
