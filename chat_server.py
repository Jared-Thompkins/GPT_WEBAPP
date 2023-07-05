from flask import Flask, request, jsonify
import openai

openai.api_key = 'OPENAI_KEY'

app = Flask(__name__)

@app.route('/get-response', methods=['POST'])
def get_response():
    message = request.json['message']
    response = openai.Completion.create(
      engine="text-davinci-002",
      prompt=message,
      max_tokens=60
    )
    return jsonify(response.choices[0].text.strip())

if __name__ == '__main__':
    app.run(port=5000)
