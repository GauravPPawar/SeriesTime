from cProfile import label
from traceback import print_tb
from flask import Flask, render_template, request
import json
import http.client

from matplotlib.pyplot import title

app = Flask(__name__)

API_LIST = ['k_ixx7e51w','k_37wugmrf', 'k_z9vsnn3s', 'k_awb898yd', 'k_uvbwvms6', 'k_flk6tnw4', 'k_8dgqb4j5', 'k_gtm868dz']
API_Counter = 0
@app.route('/')
def home():
    return render_template("home.html")

@app.route('/seriesGraph', methods = ['POST', 'GET'])
def seriesGraph():
    title = request.args.get('seriesTitle')
    seriesKey = getSeriesKey(title)
    seasons = getSeriesSeasons(seriesKey)
    print(seasons)
    seriesName, labelsList, valuesList, episodeTitlesList = getIMDBData(seriesKey, seasons)
    print(labelsList, valuesList)
    return render_template("darkGraph.html", seriesName = seriesName, labelsList = labelsList, valuesList = valuesList, episodeTitlesList = episodeTitlesList ,seasonCount = len(labelsList))

def getSeriesKey(title):
    conn = http.client.HTTPSConnection("imdb-api.com", 443)
    payload = ''
    headers = {}
    title = title.replace(' ', '%20')
    conn.request("GET", "https://imdb-api.com/en/API/SearchSeries/" + API_LIST[API_Counter] + "/" + title, payload, headers)

    res = conn.getresponse()
    data = res.read()
    
    mvDict = json.loads(data.decode("utf-8"))
    
    return mvDict['results'][0]['id']

def getSeriesSeasons(seriesKey):
    conn = http.client.HTTPSConnection("imdb-api.com", 443)
    payload = ''
    headers = {}
    conn.request("GET", "https://imdb-api.com/en/API/Title/" + API_LIST[API_Counter] + "/"+ seriesKey, payload, headers)
    res = conn.getresponse()
    data = res.read()
    
    mvDict = json.loads(data.decode("utf-8"))

    return mvDict['tvSeriesInfo']['seasons']

def getIMDBData(seriesKey, seasons):
    labelsList = []
    valuesList = []
    episodeTitlesList = []
    l = []
    v = []
    t = []
    title = ''

    for i in range(len(seasons)):
        conn = http.client.HTTPSConnection("imdb-api.com", 443)
        payload = ''
        headers = {}
        conn.request("GET", "https://imdb-api.com/API/SeasonEpisodes/" + API_LIST[API_Counter] + "/"+ seriesKey +"/"+seasons[i], payload, headers)
        res = conn.getresponse()
        data = res.read()
        # print(data.decode("utf-8"))
        mvDict = json.loads(data.decode("utf-8"))

        title = mvDict['title']
        
        for j in mvDict['episodes']:
            l.append((j['episodeNumber']))
            v.append(float(j['imDbRating']))
            et = "S"+seasons[i]+"E"+j['episodeNumber'] + ": "+ j['title'] 
            t.append(et)
        labelsList.append(l)
        valuesList.append(v)
        episodeTitlesList.append(t)
        # print("ll = ", labelsList)
        # print("vl = ", valuesList)
        l = []
        v = []
        t = []
        print(labelsList, valuesList, episodeTitlesList)
    return title, labelsList, valuesList, episodeTitlesList

if __name__ == "__main__":
    app.run(debug = True)