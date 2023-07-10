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
        firstPart = request.form["firstPart"]
        animal = request.form["animal"]

        system_message = firstPart if firstPart else "You are a helpful assistant."

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": generate_prompt(firstPart, animal)}
            ]
        )
        
        generated_response = response['choices'][0]['message']['content']

        return redirect(url_for("index", result=generated_response))

    result = request.args.get("result")
    return render_template("index.html", result=result)


def generate_prompt(firstPart, animal):
    return f"{animal.capitalize()}"

if __name__ == "__main__":
    app.run(port=5000)