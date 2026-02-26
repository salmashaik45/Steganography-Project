import streamlit as st
import cv2
import numpy as np


def text_to_binary(text):
    return ''.join(format(ord(char), '08b') for char in text)


def binary_to_text(binary):
    chars = [binary[i:i+8] for i in range(0, len(binary), 8)]
    return ''.join(chr(int(char, 2)) for char in chars)


def encode_image(image, secret_message):
    secret_message += "#####"
    binary_message = text_to_binary(secret_message)

    img = image.copy()
    height, width, _ = img.shape
    capacity = height * width * 3

    if len(binary_message) > capacity:
        return None

    data_index = 0

    for row in range(height):
        for col in range(width):
            for channel in range(3):
                if data_index < len(binary_message):
                    img[row, col, channel] = (img[row, col, channel] & 254) | int(binary_message[data_index])
                    data_index += 1

    return img


def decode_image(image):
    binary_data = ""
    height, width, _ = image.shape

    for row in range(height):
        for col in range(width):
            for channel in range(3):
                binary_data += str(image[row, col, channel] & 1)

    all_text = binary_to_text(binary_data)
    return all_text.split("#####")[0]


st.title("Secure Image Steganography")

option = st.radio("Choose Operation:", ["Encode", "Decode"])

uploaded_file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, 1)

    if option == "Encode":
        message = st.text_input("Enter Secret Message")

        if st.button("Encode"):
            encoded_image = encode_image(image, message)

            if encoded_image is not None:
                st.success("Message encoded successfully!")
                _, buffer = cv2.imencode(".png", encoded_image)
                st.download_button(
                    "Download Encoded Image",
                    buffer.tobytes(),
                    file_name="encoded_image.png",
                    mime="image/png"
                )
            else:
                st.error("Message too large for this image.")

    elif option == "Decode":
        if st.button("Decode"):
            decoded_message = decode_image(image)
            st.success(f"Decoded Message: {decoded_message}")