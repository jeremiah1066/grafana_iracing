from datetime import datetime

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# You can generate a Token from the "Tokens Tab" in the UI
token = "XO2XsIF_k5PLhnxvqzY997QLBjF1Ygx2xD2iH9BKqx88QsWis5FyQTqUqsFgEiiMw87qOVVaZmhJyB9Og3C8BQ=="
org = "iracing"
bucket = "iracing_data"

client = InfluxDBClient(url="http://localhost:8086", token=token)


##
write_api = client.write_api(write_options=SYNCHRONOUS)

data = "mem,host=host1 used_percent=23.43234543"
write_api.write(bucket, org, data)