from flask import Flask, request, render_template
from detector_typo import cek_typo_phishing

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    hasil = ""
    status = ""

    if request.method == "POST":
        url = request.form["url"]
        hasil, status = cek_typo_phishing(url)

    return render_template("index.html", hasil=hasil, status=status)

if __name__ == "__main__":
    app.run(debug=True)