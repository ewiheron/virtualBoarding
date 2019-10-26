from flask import Flask
from flask import request
import requests
from flask_cors import CORS, cross_origin
import json
import logging



from apscheduler.scheduler import Scheduler

logging.basicConfig()
sched = Scheduler()
sched.start()

app = Flask(__name__)
CORS(app)

position_data = []

@app.route("/flightData") # 2964
@cross_origin()
def flightData():
    url = "http://fsg-datahub.azure-api.net/legacy/Apps/AirportSTR/Flights/Get"

    querystring = {"from":"{from}","till":"{till}"}

    headers = {
        'Ocp-Apim-Subscription-Key': "475b4e5d6c51428693d123cb7ecd9ef5",
        'User-Agent': "PostmanRuntime/7.18.0",
        'Accept': "*/*",
        'Cache-Control': "no-cache",
        'Postman-Token': "42fc9fee-969c-4678-a59b-9c75e47e4913,6e6a4e37-054e-4e93-b0be-7186646b4576",
        'Host': "fsg-datahub.azure-api.net",
        'Accept-Encoding': "gzip, deflate",
        'Connection': "keep-alive",
        'cache-control': "no-cache",
        'Access-Control-Allow-Origin': "localhost"
        }

    response = requests.request("GET", url, headers=headers, params=querystring).text
    array_obj = json.loads(response)
    flight = list(filter(lambda x: x["Flight"]["Number"] == request.args.get('flightNo'), array_obj))[0]
    return flight

@app.route("/getPosition") # 2964
@cross_origin()
def getPos():
    return json.dumps(position_data)


def triang(data):
    obj = json.loads(data)
    data1 = float(obj["device1"])
    data2 = float(obj["device3"])
    distance = 0.1

    s = (data1 + data2 + distance) / 2.0
    y = 2.0 * (abs((s * (s - data1) * (s - data2) * (s - distance))) ** 0.5) / distance
    x = abs(((data1 * data1) - (y * y))) ** 0.5
    return [x, y]

def addPos():
    url = "http://40.68.184.28:8086/get_location"

    

    headers = {
        'User-Agent': "PostmanRuntime/7.18.0",
        'Accept': "*/*",
        'Cache-Control': "no-cache",
        'Postman-Token': "42fc9fee-969c-4678-a59b-9c75e47e4913,6e6a4e37-054e-4e93-b0be-7186646b4576",
        'Host': "fsg-datahub.azure-api.net",
        'Accept-Encoding': "gzip, deflate",
        'Connection': "keep-alive",
        'cache-control': "no-cache",
        'Access-Control-Allow-Origin': "localhost"
        }

    response = requests.request("GET", url, headers=headers).text
    print(triang(response))
    position_data.append(triang(response))
    if(len(position_data) >= 400):
        position_data.pop(0)
    
    
if __name__ == "__main__":
    sched.add_interval_job(addPos, seconds = 1, max_instances=100)
    app.run(debug=True)