from cProfile import label
from flask import Flask, render_template, request
import json
import http.client

from matplotlib.pyplot import title

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/seriesGraph', methods = ['POST', 'GET'])
def seriesGraph():
    title = request.args.get('seriesTitle')
    seriesKey = getSeriesKey(title)
    season = "1"


    seriesName, labels, values = getIMDBData(seriesKey, season)
    
    return render_template("darkGraph.html", seriesName = seriesName, labels = labels, values = values)

def getSeriesKey(title):
    conn = http.client.HTTPSConnection("imdb-api.com", 443)
    payload = ''
    headers = {}
    title = title.replace(' ', '%20')
    conn.request("GET", "https://imdb-api.com/en/API/SearchSeries/k_37wugmrf/" + title, payload, headers)

    res = conn.getresponse()
    data = res.read()
    
    mvDict = json.loads(data.decode("utf-8"))
    
    return mvDict['results'][0]['id']

def getSeriesSeasons(seriesKey):
    conn = http.client.HTTPSConnection("imdb-api.com", 443)
    payload = ''
    headers = {}
    conn.request("GET", "https://imdb-api.com/en/API/Title/k_37wugmrf/" + seriesKey, payload, headers)
    res = conn.getresponse()
    data = res.read()
    
    mvDict = json.loads(data.decode("utf-8"))

    return mvDict['tvSeriesInfo']['seasons']

def getIMDBData(seriesKey, season):
    labels = []
    values = []
    
    conn = http.client.HTTPSConnection("imdb-api.com", 443)
    payload = ''
    headers = {}
    conn.request("GET", "https://imdb-api.com/API/SeasonEpisodes/k_37wugmrf/" + seriesKey +"/"+season, payload, headers)
    res = conn.getresponse()
    data = res.read()
    # print(data.decode("utf-8"))
    mvDict = json.loads(data.decode("utf-8"))

    title = mvDict['title']

    for i in mvDict['episodes']:
        labels.append((i['episodeNumber']))
        values.append(float(i['imDbRating']))

    return title, labels, values

if __name__ == "__main__":
    app.run( host = "192.168.43.166",debug = True)