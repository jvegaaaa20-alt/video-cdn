
from flask import Flask, send_file, Response
import os

app = Flask(__name__)

@app.route('/video.mp4')
def video():
    return send_file('video.mp4', mimetype='video/mp4')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
