from flask import Flask, render_template, Response
from camera import VideoCamera
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/indexAndMap')
def index_and_map():
    return render_template('indexAndMap.html')


def gen(camera):
    while True:
        frame = camera.get_frame()
        eyes_csd_sec = camera.closed_sec
        if eyes_csd_sec >= 3:
            call_phone()
            # print("hello")
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


"""if camera spot driver is now sleeping, call the phone and give the safe destination location data."""
# @app.route('/api/data')
def call_phone():
    api_endpoint = "https://tl9b7wjalf.execute-api.ap-northeast-2.amazonaws.com/default/helloc"
    response = requests.get(api_endpoint)

    if response.status_code == 200:
        data = response.json()
        index_and_map()
        return data
    else:
        return 'Error: unable to retrieve data from API'

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

