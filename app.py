import eventlet.wsgi
from flask import jsonify, Flask
import socketio
import random
import time
from datetime import datetime

link = "http://localhost:4000"
link_ip = "159.65.144.235"

# standard Python
sio = socketio.Client()

app = Flask(__name__)


def isNowInTimePeriod(startTime, endTime, nowTime):
    if startTime < endTime:
        # startTime <= nowTime <= endTime
        return startTime <= nowTime <= endTime
    else:
        return nowTime >= startTime or nowTime <= endTime


timeStart = '12:00AM'
timeEnd = '12:10AM'
timeEnd = datetime.strptime(timeEnd, "%I:%M%p")
timeStart = datetime.strptime(timeStart, "%I:%M%p")

timeNow = datetime.strptime(str(datetime.now().strftime("%I:%M%p")), "%I:%M%p")


def reset():
    print("reset ... called")
    code = {"code": random.getrandbits()}
    sio.emit("reset_tickets", code)
    return jsonify(code)


while True:
    time.sleep(20)
    if isNowInTimePeriod(timeStart, timeEnd, timeNow):
        reset()
        print("Reseting .... !!")
    else:
        print("its not time to reset yet!!")


@sio.event
def connect():
    print('connection established')


@sio.event
def disconnect():
    print('disconnected from server')


try:
    sio.connect("http://localhost:5000/")
except socketio.exceptions.ConnectionError:
    print("Error! Could not connect to the socket server.")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=9999)
    # eventlet.wsgi.server(eventlet.listen(('', 9999)), app)
