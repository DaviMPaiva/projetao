from flask import Flask, request, jsonify
from inference import Inference,Data,Consumer,VideoStream
from flask_cors import CORS
import threading
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:8080"}})

# global variables
DATA = ''
CAMERA:list[str] = []
COORDINATES:str = None
PROCESSING:bool = None 
HEATMAP_BUFFER:list = ['img1.png', 'img2.png']
#create the lock
lock = threading.Lock()
cord = Data(lock)
#create the consumer
my_consumer = Consumer(cord,798,680)
my_consumer.start()



@app.route('/')
def main():
    return 'server online'

@app.route('/data', methods=['GET'])
def get_data():
    return DATA

@app.route("/cam-ip", methods=["GET", "POST"])
def cam_ip():

    if request.method == 'GET':
            global DATA
            data = DATA

            return jsonify(data)
           
       

    if request.method == 'POST':
        #video stream
        data = request.json
        DATA = data['camera1']
        print(DATA)

        camera1 = data['camera1']
        camera2 = data['camera2']
        vs1 = VideoStream(camera1)
        vs2 = VideoStream(camera2)

        video1 = 'videos/guga1.mp4'
        video2 = 'videos/guga2_flip.mp4'

        #create the producer
        global cord
        my_thread = Inference(video1, video2, cord,vs1,vs2,isStream=False)
        my_thread.start()
        return data
        

@app.route("/coordinates", methods=['GET', 'POST'])
def coordinates():
    if request.method == 'GET':
        if COORDINATES is not None:
            return jsonify(COORDINATES)
        else:
            'Coordinates No Found', 404

    if request.method == 'POST':
        
        COORDINATES = {
            'top_left': request.form['top_left'],
            'top_right': request.form['top_right'],
            'bottom_right': request.form['bottom_right'],
            'bottom_left': request.form['bottom_left']
        }

        #start_rec(CAMERA, COORDINATES)



@app.route("/heatmap", methods=['GET', 'POST'])
def heatmap():
    if request.method == 'POST':
        HEATMAP_BUFFER.append(request.form('img'))

    if request.method == 'GET':
        if len(HEATMAP_BUFFER) > 0:
            return jsonify(HEATMAP_BUFFER)
        else:
            'No Heatmaps found', 404 

@app.route("/distance", methods=['GET'])
def distance():
    if request.method == 'GET':
        d_player = my_consumer.GetDistanceTraveled_m(1)
        d_opponent = my_consumer.GetDistanceTraveled_m(2)

        payload = {
            'd_player':d_player,
            'd_opponent':d_opponent
        }

        return jsonify(payload)


@app.route("/speed", methods=['GET'])
def speed():
    if request.method == 'GET':
        d_player = my_consumer.GetSpeed(1)
        d_opponent = my_consumer.GetSpeed(2)

        payload = {
            'd_player':d_player,
            'd_opponent':d_opponent
        }

        return jsonify(payload)
    

@app.route("/acceleration")
def acceleration():
    pass


@app.route("/teste", methods=['GET'])
def teste():
    my_consumer.test()

if __name__ == "__main__":
    app.run(debug=True)