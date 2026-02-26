import streamlit as st
import cv2
import numpy as np


# ----------------------------
# Utility Functions
# ----------------------------

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
                    img[row, col, channel] = (
                        img[row, col, channel] & 254
                    ) | int(binary_message[data_index])
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

    if "#####" in all_text:
        return all_text.split("#####")[0]
    else:
        return None


# ----------------------------
# UI Configuration
# ----------------------------

st.set_page_config(
    page_title="Secure Image Steganography",
    page_icon="🔐",
    layout="centered"
)

st.markdown(
    """
    <h1 style='text-align: center; color: #4F46E5;'>
    🔐 Secure Image Steganography
    </h1>
    <p style='text-align: center; color: #6B7280; font-size: 16px;'>
    Hide and extract secret messages using LSB-based image encoding.
    </p>
    """,
    unsafe_allow_html=True
)



# ----------------------------
# Upload & Mode Section
# ----------------------------

col1, col2 = st.columns(2)

with col1:
    st.subheader("📂 Upload Image")
    uploaded_file = st.file_uploader(
        "Choose an image file",
        type=["png", "jpg", "jpeg"]
    )

with col2:
    st.subheader("⚙ Operation")
    option = st.radio(
        "Select Mode",
        ["Encode", "Decode"],
        key="operation_mode"
    )



# ----------------------------
# Functional Section
# ----------------------------

if uploaded_file is not None:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, 1)

    

    # ---------------- Encode ----------------
    if option == "Encode":
        st.subheader("✉ Secret Message")
        message = st.text_area(
            "Enter your secret message",
            height=120
        )

        if st.button("Encode Message", use_container_width=True):
            encoded_image = encode_image(image, message)

            if encoded_image is not None:
                st.success("✅ Message encoded successfully!")

                _, buffer = cv2.imencode(".png", encoded_image)
                st.download_button(
                    "⬇ Download Encoded Image",
                    buffer.tobytes(),
                    file_name="encoded_image.png",
                    mime="image/png",
                    use_container_width=True
                )
            else:
                st.error("Message too large for this image.")

    # ---------------- Decode ----------------
    elif option == "Decode":
        if st.button("Decode Message", use_container_width=True):
            decoded_message = decode_image(image)

            if decoded_message:
                st.success(f"🔓 Decoded Message: {decoded_message}")
            else:
                st.error("❌ No hidden message found in this image.")