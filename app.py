from ai_engine import generate_content


from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Home Page
@app.route("/")
def index():
    return render_template("index.html")

# Generate Content API
@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    subject = data.get("subject")
    topic = data.get("topic")
    content_type = data.get("type")

    result = generate_content(subject, topic, content_type)

    return jsonify({"output": result})


if __name__ == "__main__":
    app.run(debug=True)
