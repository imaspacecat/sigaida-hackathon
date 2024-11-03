from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Path to Ollama installation
OLLAMA_PATH = "/opt/homebrew/bin/ollama"

# Define a route for sentiment analysis
@app.route('/analyze', methods=['POST'])
def analyze_sentiment():
    data = request.get_json()
    text = data.get("text")

    if not text:
        return jsonify({"error": "No text provided"}), 400

    # Run Ollama for sentiment analysis
    try:
        result = subprocess.run(
            [OLLAMA_PATH, "analyze", text],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            return jsonify({"error": "Ollama execution failed", "details": result.stderr}), 500
        
        # Assuming Ollama's output is in JSON format
        sentiment_data = json.loads(result.stdout)

        # Assuming sentiment_data contains a 'scores' key which is an array of scores
        sentiment_scores = sentiment_data.get("scores", [])

        return jsonify(sentiment_scores), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the app
if __name__ == '__main__':
    app.run(port=5000)
