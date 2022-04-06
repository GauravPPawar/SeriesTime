from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    data = [
        ("1", 9.5),
        ("2", 9.6),
        ("3", 9.1),
        ("4", 8.6),
        ("5", 8.5),
        ("6", 8.9),
        ("7", 9.5),
        ("8", 9.6),
        ("9", 9.5),
        ("10", 9.7),
    ]

    # labels = [row[0] for row in data]
    # values = [row[1] for row in data]
    labels = []
    values = []
    for row in data:
        labels.append(row[0])
        values.append(row[1])

    return render_template("darkGraph.html", labels = labels, values = values)

if __name__ == "__main__":
    app.run( host = "192.168.43.166",debug = True)