from flask import Flask, render_template, request
from keras.models import load_model
import numpy as np

model = load_model('fish.h5')
model_d = load_model('disaster.h5')

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict", methods=["GET", "POST"])
def predict():
    if request.method == "POST":
        month = float(request.form.get("month", 1))
        press = float(request.form.get("pressure", 1000))
        temp = float(request.form.get("temp", 22))
        tdrop = float(request.form.get("tempd", 2))
        rain = float(request.form.get("rain", 0.3))
        tskinice = float(request.form.get("tskinice", 25))

        fish = np.array([[temp, tdrop, rain, press, month]])
        disaster = np.array([[temp, tdrop, tskinice, rain]])
        
        fishing_prob = model.predict(fish)
        disaster_prob = model_d.predict(disaster)

        print(fishing_prob, disaster_prob)
        
        return render_template("predict.html", fishing_prob=fishing_prob, disaster_prob=disaster_prob)
    return render_template("predict.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

if __name__ == "__main__":
    app.run(debug=True)

