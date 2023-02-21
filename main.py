from flask import Flask, render_template, Response, redirect, url_for
from camera import VideoCamera
import requests
import time

app = Flask(__name__)
called = False

@app.route('/')
def index():
    global called
    if called == False:
        called = True
        return render_template('index.html')
    else:
        return render_template('indexAndMap.html')

# @app.route('/')
# def second():
#     return render_template('indexAndMap.html')


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


def findmap():
    return redirect(url_for('index'))

"""if camera spot driver is now sleeping, call the phone and give the safe destination location data."""
# @app.route('/api/data')
def call_phone():
    api_endpoint = "https://tl9b7wjalf.execute-api.ap-northeast-2.amazonaws.com/default/helloc"
    response = requests.get(api_endpoint)
    findmap()

    # requests.get('')


    # requests.get('/new_page')

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return 'Error: unable to retrieve data from API'

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

# def map():
#     # return render_template('indexAndMap.html')
#     return redirect('indexAndMap.html')

# @app.route('/new_page')
# def new_page():
#     # return render_template('index.html')
#     return render_template('indexAndMap.html')

# @app.route('/redirect_to_newpage')



# @app.route('/indexAndMap.html', methods=['GET'])
# def make_pin():
#     if request.method == 'GET':
#         # 버튼 클릭 이벤트 발생시
#         # HTML 템플릿 렌더링
#         return render_template('index.html')
#     else:
#         return render_template('index.html')
#     return 'Hello, World!'

# if __name__ == '__main__':
#     app.run()