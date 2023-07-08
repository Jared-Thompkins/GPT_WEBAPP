from flask import Flask, redirect, render_template, request, url_for
from dotenv import load_dotenv
import os
import openai

app = Flask(__name__)
load_dotenv()
openai.api_key = os.getenv('OPENAI_KEY')

@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        animal = request.form["animal"]

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": generate_prompt(animal)}
            ]
        )
        
        generated_response = response['choices'][0]['message']['content']

        return redirect(url_for("index", result=generated_response))

    result = request.args.get("result")
    return render_template("index.html", result=result)


def generate_prompt(animal):
    return f"""Suggest three names for a {animal.capitalize()} superhero."""

if __name__ == "__main__":
    app.run(port=5000)