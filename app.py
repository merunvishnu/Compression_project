from flask import Flask, render_template, request, send_file
from PIL import Image
import os
from huffman import HuffmanCoding
from docx import Document
import PyPDF2

app = Flask(__name__)

# Create directories if they don't exist
UPLOAD_FOLDER = "uploads"
COMPRESSED_FOLDER = "compressed"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(COMPRESSED_FOLDER, exist_ok=True)

# Set max upload size to 50MB
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part!', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file!', 400

    filename = file.filename
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    try:
        # Process image files
        if filename.lower().endswith(('jpg', 'jpeg', 'png')):
            compressed_image_path = os.path.join(COMPRESSED_FOLDER, "compressed_" + filename)
            image = Image.open(file_path)
            image.save(compressed_image_path, quality=85, optimize=True)
            return send_file(compressed_image_path, as_attachment=True)

        # Process text files using Huffman Coding
        elif filename.lower().endswith('.txt'):
            huffman = HuffmanCoding()
            compressed_file = huffman.compress(file_path)
            return send_file(compressed_file, as_attachment=True)

        # Process Word files (.docx)
        elif filename.lower().endswith('.docx'):
            document = Document(file_path)
            text = '\n'.join([para.text for para in document.paragraphs])
            huffman = HuffmanCoding()
            compressed_file = huffman.compress_text(text)
            return send_file(compressed_file, as_attachment=True)

        # Process PDF files
        elif filename.lower().endswith('.pdf'):
            with open(file_path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                text = ""
                for page in reader.pages:
                    text += page.extract_text()
            huffman = HuffmanCoding()
            compressed_file = huffman.compress_text(text)
            return send_file(compressed_file, as_attachment=True)

        else:
            return "Unsupported file type! Only images, text, Word, and PDF files are allowed.", 400

    except Exception as e:
        print(f"Error: {e}")
        return "An error occurred while processing your file.", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
