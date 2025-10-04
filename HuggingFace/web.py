from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_URL = os.getenv("HUGGING_FACE_API_URL")
API_KEY = os.getenv("HUGGING_FACE_API_KEY")
headers = {'Authorization': f'Bearer {API_KEY}'}

# Initialize Flask
app = Flask(__name__)
def query(file_bytes):
    try:
        response = requests.post(
            API_URL,
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/octet-stream"  # important
            },
            data=file_bytes
        )

        if response.status_code != 200:
            print("Error from API:", response.status_code, response.text)
            return {"error": f"API returned status code {response.status_code}"}

        return response.json()

    except Exception as e:
        print("Request error:", str(e))
        return {"error": str(e)}

# Routes
@app.route('/')
def index():
    return render_template('index.html')  # Must be in templates folder

@app.route('/upload', methods=['POST'])
def upload():
    if 'file1' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file1']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    modeldata = query(file.read())
    return jsonify(modeldata)

    # Read file bytes and query model
    modeldata = query(file.read())
    return jsonify(modeldata)

# Run app
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
