import os
from flask import Flask, request, render_template, send_file
from huffman import HuffmanCoding

app = Flask(__name__)

# Ensure the necessary directories exist
os.makedirs("static/compressed/uploads", exist_ok=True)
os.makedirs("static/uploads", exist_ok=True)

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
    
    try:
        file.save(file_path)

        # Compress the file
        huffman_coding = HuffmanCoding()
        compressed_file = huffman_coding.compress(file_path)  # Compressed file path returned

        # Debugging: Log the returned compressed file path
        print(f"Compressed file path returned by HuffmanCoding.compress: {compressed_file}")

        # Construct the correct compressed file path
        compressed_file_path = os.path.join("static/compressed/uploads", f"{filename}.huff")
        print(f"Final compressed file path: {compressed_file_path}")

        # Move the compressed file to the correct directory
        os.rename(compressed_file, compressed_file_path)

        # Return the compression result
        return render_template('uploading.html', filename=filename, status='Compression complete')

    except Exception as e:
        # Debugging: Log the exception details
        print(f"Error occurred during compression: {e}")
        
        # Remove the uploaded file in case of an error
        if os.path.exists(file_path):
            os.remove(file_path)
        
        return render_template('uploading.html', filename=filename, status=f"An error occurred: {e}")

@app.route('/download/<filename>')
def download_file(filename):
    # Send the compressed file to the user
    compressed_file_path = os.path.join("static/compressed/uploads", f"{filename}.huff")
    
    if not os.path.exists(compressed_file_path):
        return "File not found", 404
    
    return send_file(compressed_file_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
