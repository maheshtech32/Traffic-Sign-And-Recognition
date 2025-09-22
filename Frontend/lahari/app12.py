from flask import Flask, render_template, request, jsonify
from PIL import Image
import io
import base64
from ultralytics import YOLO  # YOLOv8
import numpy as np

app = Flask(__name__)

# Load the YOLO model
model = YOLO('C:/Users/hi/Downloads/lahari/lahari/models/best.pt')  # Adjust path as needed

@app.route('/')
def index():
    return render_template('ind.html')  # Ensure your HTML file is named ind.html

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    file = request.files['file']
    img_bytes = file.read()
    img = Image.open(io.BytesIO(img_bytes))

    # Run the image through the model
    results = model(img)

    # Annotate image and convert to base64
    annotated_img = results[0].plot()  # Returns a numpy array
    pil_image = Image.fromarray(annotated_img)  # Convert numpy array to PIL Image
    buffered = io.BytesIO()
    pil_image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    # Process predictions
    predictions = []
    for box in results[0].boxes:
        predictions.append({
            'class': model.names[int(box.cls)],  # Access class name correctly
            'confidence': float(box.conf),       # Convert confidence to float for JSON
            'bbox': box.xyxy[0].tolist()         # Convert bbox coordinates to list
        })

    # Return JSON with the image and predictions
    return jsonify({'image_data': img_str, 'predictions': predictions})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # Run in debug mode for development
