from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict", methods=["GET", "POST"])
def predict():
    if request.method == "POST":
        tdrop = float(request.form.get("tdrop", 28))
        rainocn = float(request.form.get("rainocn", 0.3))
        tskinice = float(request.form.get("tskinice", 25))
        
        fishing_prob = 0.5 if tdrop >= 28 and rainocn <= 0.5 else 0.2
        disaster_prob = 0.5 if tskinice >= 29 and rainocn >= 0.6 else 0.1
        
        return render_template("predict.html", fishing_prob=fishing_prob, disaster_prob=disaster_prob)
    return render_template("predict.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

if __name__ == "__main__":
    app.run(debug=True)
