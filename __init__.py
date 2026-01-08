from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
                                                                                                                                       
app = Flask(__name__) 

@app.route("/contact/") #a jour
def MaPremiereAPI():
    return render_template("contact.html") 
  
@app.route('/')
def hello_world():
    return render_template('hello.html')#COM
  
@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)
  
@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")
  
@app.route("/histogramme/")
def monhistogramme():
    return render_template("Histogramme.html")
  
@app.route('/extract-minutes/<date_string>')
def extract_minutes(date_string):
    date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
    minutes = date_object.minute
    return jsonify({'minutes': minutes})



@app.route('/commits-data/')
def commits_data():
    url = 'https://api.github.com/repos/BouchraRH/5MCSI_Metriques/commits'

    
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    response = urlopen(req)
    raw_content = response.read()
    commits_json = json.loads(raw_content.decode('utf-8'))

    minutes_count = {str(m): 0 for m in range(60)}

    for commit_item in commits_json:
        date_string = commit_item.get('commit', {}).get('author', {}).get('date')
        if not date_string:
            continue

        date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
        minute = str(date_object.minute)
        minutes_count[minute] += 1

    results = [{'minute': int(k), 'count': v} for k, v in minutes_count.items()]
    results.sort(key=lambda x: x['minute'])

    return jsonify(results=results)


@app.route('/commits/')
def commits():
    return render_template('commits.html')
  
if __name__ == "__main__":
  app.run(debug=True)
