from cProfile import label
from flask import Flask, render_template
import json
import http.client

app = Flask(__name__)

@app.route('/')
def home():
    seriesKey = "tt2364582"
    season = "1"
    seriesName, data = getIMDBData(seriesKey, season)
    # labels = [row[0] for row in data]
    # values = [row[1] for row in data]
    labels = []
    values = []
    for row in data:
        labels.append(row[0])
        values.append(row[1])
    return render_template("darkGraph.html", seriesName = seriesName, labels = labels, values = values)

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
    dt = []
    for i in mvDict['episodes']:
        dt.append((i['episodeNumber'],float(i['imDbRating'])))

    return title, dt

if __name__ == "__main__":
    app.run( host = "192.168.43.166",debug = True)