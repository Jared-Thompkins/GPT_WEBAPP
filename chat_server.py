from flask import Flask, request, jsonify
from dotenv import load_dotenv
from flask_cors import CORS
import os
import openai
import json


load_dotenv()
openai.api_key = os.getenv('OPENAI_KEY')

app = Flask(__name__)
CORS(app)

@app.route('/get-response', methods=['POST'])
def get_response():
    message = request.json['message']
    response = openai.Completion.create(
      engine="gpt-3.5-turbo",
      prompt=message,
      max_tokens=60
    )
    return jsonify(response = response.choices[0].text.strip())

if __name__ == '__main__':
    app.run(port=5000)
