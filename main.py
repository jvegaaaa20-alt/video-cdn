from flask import Flask, request, Response
import os

app = Flask(__name__)

VIDEO_FILE = 'video.mp4'

@app.route('/video.mp4')
def video():
    file_size = os.path.getsize(VIDEO_FILE)
    range_header = request.headers.get('Range', None)

    if range_header:
        byte_start, byte_end = 0, None
        match = range_header.replace('bytes=', '').split('-')
        byte_start = int(match[0])
        byte_end = int(match[1]) if match[1] else file_size - 1

        length = byte_end - byte_start + 1

        with open(VIDEO_FILE, 'rb') as f:
            f.seek(byte_start)
            data = f.read(length)

        rv = Response(data, 206, mimetype='video/mp4', direct_passthrough=True)
        rv.headers.add('Content-Range', f'bytes {byte_start}-{byte_end}/{file_size}')
        rv.headers.add('Accept-Ranges', 'bytes')
        rv.headers.add('Content-Length', str(length))
        return rv

    with open(VIDEO_FILE, 'rb') as f:
        data = f.read()

    rv = Response(data, 200, mimetype='video/mp4')
    rv.headers.add('Accept-Ranges', 'bytes')
    rv.headers.add('Content-Length', str(file_size))
    return rv

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
