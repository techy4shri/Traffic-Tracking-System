import streamlit as st
import os
from PIL import Image
import cv2
import numpy as np
from torchvision.models import detection
import torch
from torchvision import models
import json
import base64

# Define vehicle classes (replace with actual class IDs from your model)
vehicle_classes = [2, 3, 5]

# Define image preprocessing function


def process_image():
    uploaded_file = st.file_uploader(
        "Choose an Image", type=["jpg", "jpeg", "png"])
    request_data = st.session_state.get("request_data", None)

    if uploaded_file is not None:
        # Process the image data (using libraries like OpenCV)
        process_button = st.button("Process Image")

    if process_button or request_data is not None:  # OR logic
        try:
            # If request data exists (from previous upload), use it.
            image_data = json.loads(request_data)[
                "imageData"] if request_data else None

            # If no request data, use the saved uploaded file (optional).
            if image_data is None and os.path.exists(os.path.join("temp", filename)):
                with open(os.path.join("temp", filename), "rb") as f:
                    image_bytes = f.read()
                    # Extract data URL from bytes if needed (assuming base64 encoding)
                    image_data = f"data:image/jpeg;base64,{base64.b64encode(image_bytes).decode('utf-8')}"

            # Process the image data (using libraries like OpenCV)
            # ... your image processing logic here ...
            st.success("Image processing complete!")
        except Exception as e:
            st.error(f"Error processing image: {e}")
        filename = f"{st.session_state.get('file_id', 0)}.jpg"
        st.session_state['file_id'] = st.session_state.get(
            'file_id', 0) + 1  # Increment counter for filenames
        with open(os.path.join("temp", filename), "wb") as f:
            f.write(uploaded_file.read())
        # ... your image processing logic here ...
        st.success("Image processing complete!")
    else:
        st.warning("No image uploaded!")
    if os.path.exists(os.path.join("temp", filename)):
        # Read the saved image
        with open(os.path.join("temp", filename), "rb") as f:
            image_bytes = f.read()

    # Process the image data (using libraries like OpenCV)
    # ... your image processing logic here ...
        st.success("Image processing complete!")

    # Optionally, delete the temporary file
        os.remove(os.path.join("temp", filename))


def preprocess_image(image):
    # Resize and normalize the image for model input
    image = cv2.resize(image, (416, 416))  # Adjust size if needed
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    image = image.astype(np.float32) / 255.0
    return image

# Function to display processed image with bounding boxes


def display_processed_image(image_bytes, results, model):
    preprocessed_image = preprocess_image(cv2.imdecode(
        np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR))

    for box, score, label_id in zip(results['boxes'], results['scores'], results['labels']):
        if label_id.item() in vehicle_classes:
            x_min, y_min, x_max, y_max = box.tolist()
            cv2.rectangle(preprocessed_image, (x_min, y_min),
                          (x_max, y_max), (0, 255, 0), 2)

            # Optionally, add label text
            label = f"{model.module.names[label_id.item()]} - {score:.2f}"
            cv2.putText(preprocessed_image, label, (x_min, y_min - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    # Convert processed image back to RGB and display in Streamlit
    rgb_image = cv2.cvtColor(preprocessed_image, cv2.COLOR_BGR2RGB)
    st.image(rgb_image, channels="RGB", use_column_width=True)


def detect_vehicles(image_bytes):
    # Load model, set to evaluation mode
    model = detection.yolo_v5m.model()
    model.eval()
    image_tensor = torch.from_numpy(cv2.imdecode(np.frombuffer(
        image_bytes, np.uint8), cv2.IMREAD_COLOR)).float().unsqueeze(0) / 255.0
    with torch.no_grad():
        results = model(image_tensor)[0]

    # Process detections, count vehicles
    # Assuming boxes is the detection tensor
    vehicle_count = results['boxes'].shape[0]

    return model, results
# Main app function


def main():
    st.title("Image Detection App")
    st.write("Image Detection and Processing App")

    uploaded_file = st.file_uploader(
        "Choose an Image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image_bytes = uploaded_file.read()

        # Call detect_vehicles to get results and model
        model, results = detect_vehicles(image_bytes)
        # Assuming boxes is the detection tensor
        vehicle_count = results['boxes'].shape[0]

        st.success(f"Detected {vehicle_count} vehicles!")
        display_processed_image(image_bytes, results, model)
