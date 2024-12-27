import os
from flask import Flask, request, send_file, render_template
from huffman import HuffmanCoding

app = Flask(__name__)

# Ensure the necessary directories exist
os.makedirs("static/uploads", exist_ok=True)
os.makedirs("static/compressed/uploads", exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part", 400
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400

    # Save the uploaded file temporarily
    filename = file.filename
    file_path = os.path.join('static/uploads', filename)
    file.save(file_path)

    # Compress the file
    huffman_coding = HuffmanCoding()
    try:
        compressed_file = huffman_coding.compress(file_path)

        # Ensure the directory exists for the compressed file
        os.makedirs("static/compressed/uploads", exist_ok=True)

        # Move the compressed file to the correct directory
        compressed_file_path = os.path.join("static/compressed/uploads", os.path.basename(compressed_file))
        os.rename(compressed_file, compressed_file_path)

        # Automatically download the compressed file
        return send_file(compressed_file_path, as_attachment=True)
    
    except Exception as e:
        return f"An error occurred during compression: {e}", 500

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
