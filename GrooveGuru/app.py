from flask import Flask, render_template
from flask_cors import CORS

from flask_plug import fetch_and_process_data

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    result = fetch_and_process_data()
    return render_template('index.html', songs=result)

if __name__ == '__main__':
    app.run(debug=True)
