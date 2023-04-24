from flask import Flask, request, jsonify
from inference import Inference,Data,Consumer,VideoStream
from flask_cors import CORS
import threading
import numpy as np
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
    data1 = my_consumer.GetIndividualHeatmap(1)
    data1 = np.array(data1)
    data1 = data1.astype(float).tolist()
    new_data1 = [{'x': int(800-data1[i][0]), 'y': int(data1[i][1]), 'value': 1} for i in range(len(data1))]
    new_data1 =[{'x':0,'y':0,'value':0.1},{'x':1600,'y':0,'value':0.1},
                {'x':1600,'y':1000,'value':0.1},{'x':0,'y':1000,'value':0.1}
                ]
    data2 = my_consumer.GetIndividualHeatmap(2)
    data2 = np.array(data2)
    data2 = data2.astype(float).tolist()
    new_data2 = [{'x': int(800-data2[i][0]), 'y': int(data2[i][1]), 'value': 1} for i in range(len(data2))]
   
    print("heatmap size: ")
    print(len(new_data1))
    print(len(new_data2))

    payload = {
            'd_player':new_data1,
            'd_opponent':new_data2
        }


    if request.method == 'POST':
        return jsonify(payload)

    if request.method == 'GET':
        return jsonify(payload)

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