from flask import Flask, request, jsonify # type: ignore
import pickle
import os
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)

# Load the recommendation model on startup
MODEL_PATH = "/pickle/rules.pkl"

if os.path.exists(MODEL_PATH):
    with open(MODEL_PATH, "rb") as f:
        app.model_rules = pickle.load(f)
    app.model_date = datetime.fromtimestamp(os.path.getmtime(MODEL_PATH)).strftime("%Y-%m-%d %H:%M:%S")
else:
    app.model_rules = None
    print(f"Rules file not found at {MODEL_PATH}. Make sure to generate rules.pkl.")

# Define the health endpoint
@app.route("/health", methods=["GET"])
def health_check():
    try:
        # Perform a basic check to ensure the model is loaded
        if app.model_rules is not None:
            return jsonify({
                "status": "healthy",
                "model_loaded": True,
                "model_date": app.model_date
            }), 200
        else:
            return jsonify({
                "status": "unhealthy",
                "model_loaded": False
            }), 500
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "error": str(e)
        }), 500


# Define the recommend endpoint
@app.route("/api/recommend", methods=["POST"])
def recommend():
    if app.model_rules is None:
        return jsonify({"error": "Recommendation model not loaded"}), 500

    # Parse the input JSON
    data = request.get_json()
    if not data or "songs" not in data:
        return jsonify({"error": "Invalid request. 'songs' field is required."}), 400

    user_songs = set(data["songs"])

    # Find matching rules
    matching_rules = app.model_rules[
        app.model_rules["antecedents"].apply(lambda x: user_songs.issubset(x))
    ]

    # Extract and aggregate recommendations
    recommendations = set()
    for consequents in matching_rules["consequents"]:
        recommendations.update(consequents)

    # Remove songs the user already likes
    recommendations = list(recommendations - user_songs)

    # Return the recommendations
    return jsonify({
        "songs": recommendations,
        "version": os.getenv("VERSION"),
        "model_date": app.model_date
    })

# Run the application
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=30502, debug=True)  # Replace 30502 with your allocated port
