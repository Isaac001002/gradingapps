import os
from flask import Flask, render_template, request, redirect, url_for, flash
import openai

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev_key")

# Configure OpenAI API
openai.api_key = os.environ["OPENAI_API_KEY"]

# Grade essay function
def grade_essay(essay_text):
    prompt = f"Grade the following essay and provide feedback:\n\n{essay_text}\n\nFeedback:"
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.5,
    )

    feedback = response.choices[0].text.strip()
    return feedback

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        essay_text = request.form["essay"]

        # Call the grade_essay function to get feedback
        feedback = grade_essay(essay_text)

        # Show feedback
        flash(feedback)
        return redirect(url_for("index"))

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
