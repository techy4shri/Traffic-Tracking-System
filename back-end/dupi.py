import streamlit as st
import argparse
import io
import os
from PIL import Image
import cv2
import numpy as np
from torchvision.models import detection
import torch
from torchvision import models
from io import BytesIO

vehicle_classes = [2, 3, 5]  

def preprocess_image(image):
    # Resize and normalize the image for model input
    image = cv2.resize(image, (416, 416))  # Adjust size if needed
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    image = image.astype(np.float32) / 255.0
    return image


def main():
    st.title("Image Detection App")
    st.write("Image Detection and Processing App")
    def detect_vehicles(image_bytes):
    #loading thr pre-trained model
    model = detection.yolo_v5m.model()
    model.eval()  # Set the model to evvaluation

    # Preprocess the image (resize, normalize)
    image = cv2.imdecode(np.frombuffer(
        image_bytes, np.uint8), cv2.IMREAD_COLOR)
    image = preprocess_image(image)  # Implement a function for preprocessing

    # Convert image to PyTorch tensor
    image_tensor = torch.from_numpy(image).float().unsqueeze(0) / 255.0

    # Perform inference
    with torch.no_grad():
        results = model(image_tensor)[0]

    # Process detections (filter for vehicle classes, count vehicles)
    vehicle_count = 0
    for box, score, label_id in zip(results['boxes'], results['scores'], results['labels']):
        if label_id.item() in vehicle_classes:  # Check if it's a vehicle class
            vehicle_count += 1

    return vehicle_count

uploaded_file = st.file_uploader("Choose an Image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image_bytes = uploaded_file.read()
        vehicle_count = detect_vehicles(image_bytes)

        st.success(f"Detected {vehicle_count} vehicles!")

        for box, score, label_id in zip(results['boxes'], results['scores'], results['labels']):
            if label_id.item() in vehicle_classes:
                x_min, y_min, x_max, y_max = box.tolist()
                cv2.rectangle(preprocess_image, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

                # Optionally, add label text
                label = f"{model.module.names[label_id.item()]} - {score:.2f}"
                cv2.putText(preprocess_image, label, (x_min, y_min - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        # Convert processed image back to RGB and display in Streamlit
        rgb_image = cv2.cvtColor(preprocess_image, cv2.COLOR_BGR2RGB)
        st.image(rgb_image, channels="RGB", use_column_width=True)# Optionally, display the processed image with bounding boxes
        # ... (implement using OpenCV drawing functions)


//handledimage
 const formData = new FormData();
      formData.append("image", file);

      fetch("/process-image", {
        method: "POST",
        body: file,
      })
        .then((response) => response.json())
        .catch((error) => {
          console.error("Error processing image:", error);
        });

      setSelectedImage(URL.createObjectURL(file)); //set preview
    }