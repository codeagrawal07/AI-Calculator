import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import LLM as llm
import base64
import io

app= Flask(__name__)
CORS(app)
@app.route('/process-image', methods=['POST'])
def handle_image():
    """
    This is the server endpoint that receives the image from JavaScript.
    """
    # Get the JSON data sent from the frontend
    data = request.get_json()
    if not data or 'image' not in data:
        return jsonify({'error': 'No image data provided'}), 400
    
    # **NEW**: Get the prompt text from the request data
    # Provide a default value if the user didn't type anything
    
    user_prompt = data.get('prompt', 'Analyze the image and infer intent.')
    # The image data is a Base64 string, e.g., "data:image/png;base64,iVBORw0KGgo..."
    # We need to strip the header to get the pure Base64 content
    base64_str = data['image'].split(',')[1]
    
    # Decode the Base64 string into binary image data
    image_bytes = base64.b64decode(base64_str)
    
    # Use Pillow to open the image from the binary data
    img = Image.open(io.BytesIO(image_bytes))

    # Get the description from our LLM function
    description = llm.process_image_with_llm(img, user_prompt)
    
    # Send the description back to the frontend in JSON format
    return jsonify({'description': description})

