#!python3
from datetime import datetime

import irsdk
import time
import json


influx_host = "http://192.168.7.109:8086"

## influx

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS, ASYNCHRONOUS


# You can generate a Token from the "Tokens Tab" in the UI
token = "XO2XsIF_k5PLhnxvqzY997QLBjF1Ygx2xD2iH9BKqx88QsWis5FyQTqUqsFgEiiMw87qOVVaZmhJyB9Og3C8BQ=="
org = "iracing"
bucket = "iracing_data"

client = InfluxDBClient(url=influx_host, token=token)
write_api = client.write_api(write_options=ASYNCHRONOUS)
## end influx


# this is our State class, with some helpful variables
class State:
    ir_connected = False
    last_car_setup_tick = -1


# here we check if we are connected to iracing
# so we can retrieve some data
def check_iracing():
    if state.ir_connected and not (ir.is_initialized and ir.is_connected):
        state.ir_connected = False
        # don't forget to reset your State variables
        state.last_car_setup_tick = -1
        # we are shutting down ir library (clearing all internal variables)
        ir.shutdown()
        print('irsdk disconnected')
    elif not state.ir_connected and ir.startup() and ir.is_initialized and ir.is_connected:
        state.ir_connected = True
        print('irsdk connected')


def loop2(ir):
    ir.freeze_var_buffer_latest()

    point = Point("iracing") \
    \
        .field("AirDensity", ir["AirDensity"]) \
        .field("AirPressure", ir["AirPressure"]) \
        .field("AirTemp", ir["AirTemp"])\
    \
        .field("Brake", ir["Brake"]) \
        .field("Clutch", ir["Clutch"]) \
        .field("FuelLevelPct", ir["FuelLevelPct"]) \
        .field("FuelLevel", ir["FuelLevel"])\
        .field("FuelPress", ir["FuelPress"])\
        .field("Gear", ir["Gear"]) \
        .field("LatAccel", ir["LatAccel"])\
    \
        .field("LFbrakeLinePress", ir["LFbrakeLinePress"])\
        .field("LFshockDefl",  ir["LFshockDefl"])\
        .field("LFshockVel", ir["LFshockVel"])\
        .field("LFtempCL", ir["LFtempCL"])\
        .field("LFtempCM", ir["LFtempCM"])\
        .field("LFtempCR", ir["LFtempCR"])\
    \
        .field("LRbrakeLinePress", ir["LRbrakeLinePress"])\
        .field("LRshockDefl", ir["LRshockDefl"])\
        .field("LRshockVel", ir["LRshockVel"]) \
 \
        .field("LongAccel", ir["LongAccel"]) \
        .field("ManifoldPress", ir["ManifoldPress"])\
        .field("Pitch", ir["Pitch"])\
        .field("PitchRate", ir["PitchRate"])\
        .field("RaceLaps", ir["RaceLaps"])\
    \
        .field("RFbrakeLinePress", ir["RFbrakeLinePress"])\
        .field("RFshockDefl", ir["RFshockDefl"])\
        .field("RFshockVel", ir["RFshockVel"])\
    \
        .field("Roll", ir["Roll"])\
        .field("RollRate", ir["RollRate"])\
    \
        .field("RPM", ir["RPM"])\
    \
        .field("RRbrakeLinePress", ir["RRbrakeLinePress"])\
        .field("RRshockDefl", ir["RRshockDefl"])\
        .field("RRshockVel", ir["RRshockVel"])\
    \
        .field("OilPress", ir["OilPress"]) \
        .field("OilTemp", ir["OilTemp"])\
        .field("RPM", ir["RPM"]) \
        .field("Speed", ir["Speed"]) \
        .field("SessionTime", ir["SessionTime"]) \
        .field("SteeringWheelAngle", ir["SteeringWheelAngle"])\
        .field("Throttle", ir["Throttle"]) \
        .field("TrackTempCrew", ir["TrackTempCrew"])\
        .field("VertAccel", ir["VertAccel"])\
        .field("WaterTemp", ir["WaterTemp"]) \
        .field("WindDir", ir["WindDir"])\
        .field("WindVel", ir["WindVel"])\
        .time(datetime.utcnow(), WritePrecision.NS)
    write_api.write(bucket=bucket, org=org, record=point)
    print(f'Metric writen: {ir["SessionTime"]}')


if __name__ == '__main__':
    # initializing ir and state
    ir = irsdk.IRSDK()
    state = State()

    client = InfluxDBClient(url=influx_host, token=token)
    try:
        # infinite loop
        while True:
            # check if we are connected to iracing
            check_iracing()
            # if we are, then process data
            if state.ir_connected:
                loop2(ir)
            # maximum you can use is 1/60
            # cause iracing updates data with 60 fps
            time.sleep(1/60)
    except KeyboardInterrupt:
        # press ctrl+c to exit
        pass
