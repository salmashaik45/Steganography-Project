# 🔐 Secure Image Steganography

An interactive Python application built using Streamlit that hides and extracts secret messages inside digital images using Least Significant Bit (LSB) steganography.

## 🔗 Live Demo:
https://secure-image-steganography.streamlit.app/

## Overview

This application allows users to:

Encode secret text messages inside images

Decode hidden messages from encoded images

Detect whether an image contains embedded data

Preserve image quality using minimal bit modification

The application runs in the browser while being powered entirely by Python.

## How It Works

Digital images are composed of pixels, and each pixel contains three color channels:

Red

Green

Blue

Each channel stores values between 0–255, represented in binary format.

### This project:

Converts the input message into binary.

Modifies only the least significant bit (LSB) of each color channel.

Appends a delimiter (#####) to indicate the end of the message.

During decoding:

Extracts LSB bits

Reconstructs the binary data into text

Checks for the delimiter

If not found → displays “No hidden message found”

By altering only one bit per channel, visual distortion is negligible.

## ✨ Features

LSB-based steganography implementation

Binary-to-text and text-to-binary conversion

Automatic hidden message detection

Graceful handling of non-encoded images

Downloadable encoded image output

Clean and structured Streamlit interface

## 🛠 Tech Stack

Python

OpenCV

NumPy

Streamlit

## 📂 Project Structure

```
secure-image-steganography/
│
├── app.py              # Main Streamlit application
├── requirements.txt    # Project dependencies
├── runtime.txt         # Python version for deployment
├── .gitignore
└── README.md
```

## ▶️ Run Locally

Install dependencies
pip install -r requirements.txt
Start the application
python -m streamlit run app.py

The application will open automatically in your browser.

## 👩‍💻 About Me

I’m Salma, a Computer Science Engineering student graduating in 2027.
I love building interactive projects!