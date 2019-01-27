import smartcar
from flask import Flask, redirect, request, jsonify
import requests
import config
import weatherUtil

#initialize variables and constants for the API
app = Flask(__name__)

CLIENT_ID=config.smartcarCONST['CLIENT_ID']#'fb82ca3d-3a39-4709-865d-e09b20ac6525'
SECRET=config.smartcarCONST['SECRET']#'b14b52e3-18da-4d3e-b924-52d4c67a829f'
REDIRECT=config.smartcarCONST['REDIRECT']#'http://localhost:8000/exchange'

access = None

#sets up the scope and client for the API
SCOPE=['read_vehicle_info','read_location','read_odometer','read_vin']

client = smartcar.AuthClient(
    client_id=CLIENT_ID,#os.environ.get('CLIENT_ID'),
    client_secret=SECRET,#os.environ.get('CLIENT_SECRET'),
    redirect_uri=REDIRECT,#os.environ.get('REDIRECT_URI'),
    scope=SCOPE,
    test_mode=False,
)

#home page of the website
@app.route('/',methods=['GET'])
def index():
    return  '''
    <h1> Would you like to get information about a <a href="http://localhost:8000/login">Real Car</a> or a <a href="http://localhost:8000/testlogin">Demo Car</a>?</h1>
    '''

#This page directs you to put in authentication for your real car
@app.route('/login', methods=['GET'])
def login():
    client.test_mode=False
    auth_url = client.get_auth_url()
    print(auth_url)
    return redirect(auth_url)

#This page sets up a demo with random variables
@app.route('/testlogin', methods=['GET'])
def testlogin():
    client.test_mode=True
    auth_url = client.get_auth_url()
    print(auth_url)
    return redirect(auth_url)

#This function sets up the access token once the user has authorized the application to be run with the given scope
@app.route('/exchange', methods=['GET'])
def exchange():
    code = request.args.get('code')
    global access
    access = client.exchange_code(code)
    return vehicle(), 200

#This lists information about the vehicle once the authentication process is complete
@app.route('/vehicle', methods=['GET'])
def vehicle():
    global access
    vehicle_ids = smartcar.get_vehicle_ids(access['access_token'])['vehicles']
    vehicle = smartcar.Vehicle(vehicle_ids[0], access['access_token'])

    #sets up individual variables from the various information provided by the API
    info = vehicle.info()

    odometer = vehicle.odometer()

    location = vehicle.location()

    car_vin = vehicle.vin()
    car_id = info['id']
    car_make = info['make']
    car_model = info['model']
    car_year = info['year']
    lat = location['data'][u'latitude']
    lon = location['data'][u'longitude']
    dist = odometer['data']['distance'] #metric
    
    #uses the location data to find the temperature outside
    temperature = weatherUtil.weather(lat, lon)

    #The html output for the data along with an option to securely disconnect from the app so that the information is not mishandled
    return '''
        <h1> Hello, welcome to your car</h1>
        <h2> Car Make: ''' + str(car_make) + '''</h2>
        <h2> Car Model: ''' + str(car_model) + '''</h2>
        <h2> Car Year: ''' + str(car_year) + '''</h2>
        <h2> Car ID: ''' + str(car_id) + '''</h2>      
        <h2> VIN No: ''' + str(car_vin) + '''</h2>
        <h2> Located at  (''' + str(lat) + ''' , ''' + str(lon) +''')</h2>
        <h2> Mileage: ''' + str(dist) + '''km</h2>
        <h2> The temperature outside is ''' + str(temperature) + "C" + weatherUtil.temperature_description(temperature) + '''<h2/>
        <h2><a href="{}">Disconnect</a><h2/>'''.format(("http://localhost:8000/disconnect"+str(vehicle.disconnect())))

@app.route('/disconnectNone', methods=['GET'])
def disconnectNone():
    return '''
        <h1> You have been securely disconnected from the application. Thank you for choosing our service :) </h1>'''


#main entry point for the program to run through
if __name__ == '__main__':
    app.run(port=8000)
