import streamlit as st
from PIL import Image
import zipfile
import os
import pyheif
import io

def convert_heic_to_png_or_jpg(heic_file, format='PNG'):
    heif_file = pyheif.read(heic_file)
    img = Image.frombytes(
        heif_file.mode, 
        heif_file.size, 
        heif_file.data,
        "raw",
        heif_file.mode,
        heif_file.stride,
    )
    img_converted = img.convert(format)
    return img_converted

def main():
    st.title("HEIC to PNG/JPG Converter")

    uploaded_files = st.file_uploader("Upload your HEIC files", accept_multiple_files=True, type="heic")

    if uploaded_files:
        st.write("Converting...")

        converted_images = []
        for file in uploaded_files:
            converted_img = convert_heic_to_png_or_jpg(file)
            converted_images.append(converted_img)

        # Create a temporary directory to store converted images
        os.makedirs("temp_images", exist_ok=True)
        
        # Save converted images
        for i, img in enumerate(converted_images):
            img.save(f"temp_images/converted_image_{i}.png")

        # Create a zip file containing converted images
        zip_file_path = "converted_images.zip"
        with zipfile.ZipFile(zip_file_path, "w") as zipf:
            for root, _, files in os.walk("temp_images"):
                for file in files:
                    zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), "temp_images"))

        st.success("Conversion successful! Download your zip file below.")
        
        # Offer download link for the zip file
        with open(zip_file_path, "rb") as f:
            zip_data = f.read()
        st.download_button(label="Download converted images", data=zip_data, file_name="converted_images.zip")

        # Cleanup: delete temporary directory and zip file
        for root, _, files in os.walk("temp_images"):
            for file in files:
                os.remove(os.path.join(root, file))
        os.rmdir("temp_images")
        os.remove(zip_file_path)

if __name__ == "__main__":
    main()
        
