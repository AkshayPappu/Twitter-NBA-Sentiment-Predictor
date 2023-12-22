from flask import Flask, jsonify, request
from flask_cors import CORS
import joblib
from twitter_model import predict_winner

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route("/predict", methods=['GET'])
def predict():
    team1 = request.args.get('team1', '')
    team2 = request.args.get('team2', '')
    prediction = predict_winner(team1, team2)
    return jsonify(prediction)

if __name__ == "__main__":
    app.run(debug=True)
