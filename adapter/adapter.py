import mysql.connector
import os
import time
import requests

from influxdb import InfluxDBClient
from datetime import datetime

db_client = None

def check_last_tiketid():
	config = {
		'user': 'root',
		'password': 'root',
		'host': 'db',
		'port': '3306',
		'database': 'IdpBet'
	}
	connection = mysql.connector.connect(**config)
	cursor = connection.cursor()
	statement = "SELECT * FROM Tickets ORDER BY id DESC LIMIT 0, 1;"
	cursor.execute(statement)

	last_id = 0
	odds = None
	amount = None
	gain = None

	for (id, o, a, g) in cursor:
		last_id = id
		odds = o
		amount = a
		gain = g

	connection.commit()
	cursor.close()
	connection.close()

	return last_id, odds, amount, gain

def influxDB_connection():
	time.sleep(10)
	db_client = InfluxDBClient(host='influxdb', port=8086)
	db_client.create_database('betdb')
	db_client.switch_database('betdb')
	return db_client


if __name__ == '__main__':
	time.sleep(10)
	db_client = influxDB_connection()

	path = "http://admin:5000/teams"
	response = requests.get(path)
	while response.status_code != 200:
		time.sleep(1)
		response = requests.get(path)

	last_id = 0

	while True:
		last_ticket_data = check_last_tiketid()
		current_id = last_ticket_data[0]
		odds = last_ticket_data[1]
		amount = last_ticket_data[2]
		potential_gain = last_ticket_data[3]

		if current_id != 0 and current_id != last_id:
			last_id = current_id

			data_timestamp = datetime.utcnow().isoformat()

			point = {}
			point["measurement"] = "Tickets_Data"

			fields = {}
			fields["Odds"] = odds
			fields["Amount"] = amount
			fields['Potential_Gain'] = potential_gain
			point["fields"] = fields

			point["time"] = data_timestamp

			db_client.write_points([point])
