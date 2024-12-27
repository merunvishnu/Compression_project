import os
from flask import Flask, render_template, request, redirect, url_for
import time
from huffman import HuffmanCoding

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    if request.method == "POST":
        # Check if the file part is present in the request
        file = request.files.get("file")
        
        if not file:
            return redirect(url_for('index'))  # Redirect to the main page if no file is uploaded

        filename = file.filename
        if filename.endswith(('.jpg', '.jpeg', '.png', '.txt', '.docx', '.pdf')):
            file_path = os.path.join("uploads", filename)
            file.save(file_path)

            # Start compression process
            status = "Processing"
            # Use HuffmanCoding to compress the file
            huffman = HuffmanCoding()

            try:
                compressed_file = huffman.compress(file_path)
                status = f"File compressed successfully. <a href='/download/{compressed_file}'>Download here</a>"
            except Exception as e:
                status = f"An error occurred: {str(e)}"
                print(f"Error during compression: {str(e)}")
            
            return render_template("uploading.html", filename=filename, status=status)

        return "Invalid file type. Please upload a valid file."

@app.route("/download/<filename>")
def download_file(filename):
    return redirect(url_for('static', filename=f'compressed/{filename}'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
    
