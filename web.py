from flask import Flask, render_template, redirect, url_for
import psutil
import datetime
import os
import gardener

app = Flask(__name__)

def template():
    templateDate = {
        'time' : datetime.datetime.now(),
        'pumpstate' : str(gardener.pump.state),
        'ledstate' : str(gardener.led.state),
        'sensorstate' : str(gardener.sensor.read())
    }
    return templateDate

@app.route("/")
def mainpage():
    templateData = template()
    return render_template('main.html', **templateData)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)

