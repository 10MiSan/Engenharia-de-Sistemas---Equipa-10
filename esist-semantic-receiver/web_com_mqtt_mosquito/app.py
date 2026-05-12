import os
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/transmitter")
def transmitter():
    return render_template("transmitter.html")

@app.route("/receiver")
def receiver():
    return render_template("receiver.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 9000))
    app.run(host="0.0.0.0", port=port, debug=True)
