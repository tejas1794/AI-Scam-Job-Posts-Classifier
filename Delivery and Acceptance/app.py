from flask import Flask, render_template, request, redirect, url_for
from joblib import load
import numpy as np

model_pipeline = load("scam_finder.joblib")

result = ""
probability = ""

def get_prediction(query):
    res = model_pipeline.predict_proba([query])
    real = res[0][0]
    scam = res[0][1]
    if real <= scam: return "Scam", str(float(round(scam,4)*100))+'%'
    return "Real",  str(float(round(real,4)*100))+'%'

app = Flask(__name__, template_folder="pages")

@app.route('/')
def home():
    return render_template('forms/Home.html')


@app.route('/', methods=['POST', 'GET'])
def get_data():
    if request.method == 'POST':
        query = request.form['search']
        result, probability = get_prediction(query)
        return render_template('forms/Home.html', result=result, prob = probability)


if __name__ == '__main__':
    app.run(debug=True)
