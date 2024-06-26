import os
import sys

from flask import Flask, jsonify, request

app = Flask(__name__)

current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.insert(0, parent_dir)

from spam_detector import SpamDetector

detector = SpamDetector()

# Endpoint to predict single email
@app.route("/predict", methods=["POST"])
def predict_email():
    data = request.get_json()
    email = data["email"]
    result = detector.predict(email)
    return jsonify({"result": result})


# Endpoint to predict multiple emails
@app.route("/predict_bulk", methods=["POST"])
def predict_emails_bulk():
    data = request.get_json()
    emails_list = data["emails"]
    bulk_result = detector.predict_many(emails_list)
    return jsonify({"results": bulk_result})


if __name__ == "__main__":
    app.run(debug=True)


# Example usage with curl:

# single email
# curl -X POST -H "Content-Type: application/json" -d '{"email": "Congratulations! You have been selected as a winner. Text WON to 44255 to claim your prize."}' http://localhost:5000/predict

# multiple emails
# curl -X POST -H "Content-Type: application/json" -d '{"emails": ["Hello, how are you?", "Get free money now! You have been selected as winner of our prize"]}' http://localhost:5000/predict_bulk
