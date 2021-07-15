import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, render_template
import pickle
import os
from gevent.pywsgi import WSGIServer
app = Flask(__name__)
model = pickle.load(open('airpassengers.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict',methods=['POST'])
def y_predict():
    if request.method == "POST":
        ds = request.form["Date"]
        a={"ds":[ds]}
        ds=pd.DataFrame(a)
        prediction = model.predict(ds)
        print(prediction)
        output=round(prediction.iloc[0,15])
        print(output)
        return render_template('home.html',prediction_text="Commuters Inflow on selected date is. {} thousands".format(output))
    return render_template("home.html")
port = os.getenv('VCAP_APP_PORT','8080')
    
if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True, host='0.0.0.0',port=port)
