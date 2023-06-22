from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/storico')
def storico():
    return render_template('storico.html')

if __name__ == "__main__":
    app.run()