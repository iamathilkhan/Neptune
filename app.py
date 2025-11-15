from flask import Flask, render_template, request
from models.ai_integration import predict_fishing, predict_disaster

app = Flask(__name__, template_folder="templates", static_folder="static")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict", methods=["GET", "POST"])
def predict():
    if request.method == "POST":
        # Get form data
        data = {
            'tdrop': float(request.form.get('tdrop', 28)),
            'tbar': float(request.form.get('tbar', 1013)),
            'tskinice': float(request.form.get('tskinice', 25)),
            'rainocn': float(request.form.get('rainocn', 0.3)),
            'delts': float(request.form.get('delts', 0.5)),
            'latitude': float(request.form.get('latitude', 15.0)),
            'longitude': float(request.form.get('longitude', 75.0))
        }
        # Make predictions
        fish_prob = predict_fishing(data)
        dis_prob = predict_disaster(data)
        fish_pct = fish_prob * 100
        dis_pct = dis_prob * 100
        return render_template("predict.html", prediction=True, fish_pct=fish_pct, dis_pct=dis_pct, **data)
    return render_template("predict.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

if __name__ == "__main__":
    app.run(debug=True)
