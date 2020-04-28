from flask import Flask, jsonify, request, Response
import mysql.connector
import json

app = Flask(__name__)

config = {
	'user':'root',
	'password':'root',
	'host':'db',
	'port':'3306',
	'database':'IdpBet'
}

class Match:
	def __init__(self, match_id, home_team_id, away_team_id, home_victory, draw, away_victory):
		self.match_id = match_id
		self.home_team_id = home_team_id
		self.away_team_id = away_team_id
		self.home_victory = home_victory
		self.draw = draw
		self.away_victory = away_victory

	def key(self):
		return self.match_id

	def __hash__(self):
		return hash(self.key())

	def __eq__(self, other):
		if self.match_id == other.match_id:
			return True
		return False

	def __str__(self):
		res = ""
		res += "Match(" + self.match_id + "," + self.home_team_id + "," + self.away_team_id + ")"
		res += " = {" + self.home_victory + "," + self.draw + "," + self.away_victory
		return res

	def serialize(self):
		return {
			'match_id':self.match_id,
			'home_team_id':self.home_team_id,
			'away_team_id':self.away_team_id,
			'home_victory':self.home_victory,
			'draw':self.draw,
			'away_victory':self.away_victory 
		}

class Bet:
	def __init__(self, bet_id, match_id, bet_type):
		self.bet_id = bet_id
		self.match_id = match_id
		self.bet_type = bet_type

	def key(self):
		return self.bet_id

	def __hash__(self):
		return hash(self.key())

	def __eq__(self, other):
		if self.bet_id == other.bet_id:
			return True
		return False

	def __str__(self):
		res = ""
		res += "Bet(" + self.bet_id + ") = {" + self.match_id + "," + self.bet_type + "}"
		return res

	def serialize(self):
		return {
			'bet_id':self.bet_id,
			'match_id':self.match_id,
			'bet_type':self.bet_type
		}

class Ticket:
	def __init__(self, ticket_id, odds, amount, potential_gain):
		self.ticket_id = ticket_id
		self.odds = odds
		self.amount = amount
		self.potential_gain = potential_gain

	def key(self):
		return self.ticket_id

	def __hash__(self):
		return hash(self.key())

	def __eq__(self, other):
		if self.ticket_id == other.ticket_id:
			return True
		return False

	def __str__(self):
		res = ""
		res += "Ticket(" + self.ticket_id + ") = {" + self.ticket_id + "," + self.odds + "," + self.amount + "," + self.potential_gain + "}"
		return res

	def serialize(self):
		return {
			'ticket_id':self.ticket_id,
			'odds':self.odds,
			'amount':self.amount,
			'potential_gain':self.potential_gain
		}

@app.route('/bets', methods=['GET'])
def get_bets():
	connection = mysql.connector.connect(**config)
	cursor = connection.cursor()
	statement = "SELECT * FROM Bets;"
	cursor.execute(statement)
	bets = []
	for (id, match_id, bet_type) in cursor:
		b = Bet(id, match_id, bet_type)
		bets.append(b)
	connection.commit()
	cursor.close()
	connection.close()
	return jsonify(bets=[b.serialize() for b in bets])

@app.route('/tickets', methods=['GET'])
def get_tickets():
	connection = mysql.connector.connect(**config)
	cursor = connection.cursor()
	statement = "SELECT * FROM Tickets;"
	cursor.execute(statement)
	tickets = []
	for (id, odds, amount, potential_gain) in cursor:
		t = Ticket(id, odds, amount, potential_gain)
		tickets.append(t)
	connection.commit()
	cursor.close()
	connection.close()
	return jsonify(tickets=[t.serialize() for t in tickets])

@app.route('/bets/add', methods=['POST'])
def place_bet():
	params = request.get_json(silent = True)
	if not params:
		return Response(status = 400)

	match_id = params.get('match_id')
	if not match_id:
		return Response(status = 400)

	bet_type = params.get('bet_type')
	if not bet_type:
		return Response(status = 400)

	connection = mysql.connector.connect(**config)
	cursor = connection.cursor()

	statement = "INSERT INTO Bets (match_id, bet_type) VALUES ({},\"{}\");".format(match_id, bet_type)
	cursor.execute(statement)
	connection.commit()
	cursor.close()
	connection.close()

	return Response(status = 201)

@app.route('/bets/cancel', methods=['DELETE'])
def delete_bet():
	params = request.get_json(silent = True)
	if not params:
		return Response(status = 400)

	bet_id = params.get('bet_id')
	if not bet_id:
		return Response(status = 400)

	connection = mysql.connector.connect(**config)
	cursor = connection.cursor()
	statement = "SELECT * FROM Bets WHERE id = {};".format(bet_id)
	cursor.execute(statement)
	b = None
	for (id, match_id, bet_type) in cursor:
		b = Bet(id, match_id, bet_type)
	if b is None:
		connection.commit()
		cursor.close()
		connection.close()
		return Response(status = 404)
	else:
		statement = "DELETE FROM Bets WHERE id = {};".format(bet_id)
		cursor.execute(statement)
		connection.commit()
		cursor.close()
		connection.close()
		return Response(status = 200)

@app.route('/tickets/add', methods=['GET'])
def add_ticket():
	params = request.get_json(silent = True)
	if not params:
		return Response(status = 400)

	betIDs = params.get('betIDs')
	if not betIDs:
		return Response(status = 400)

	total_odds = params.get('odds')
	if not total_odds:
		return Response(status = 400)

	amount = params.get('amount')
	if not amount:
		return Response(status = 400)

	connection = mysql.connector.connect(**config)
	cursor = connection.cursor()

	potential_gain = round(float(total_odds * amount), 2)

	statement = "INSERT INTO Tickets(odds, amount, potential_gain) VALUES ({}, {}, {});".format(total_odds, amount, potential_gain)
	cursor.execute(statement)

	statement = "SELECT * FROM Tickets ORDER BY id DESC LIMIT 0, 1"
	cursor.execute(statement)

	newId = 0
	for (id, _, _, _) in cursor:
		newId = id
		for bid in betIDs:
			statement = "INSERT INTO Ticket_Bet (ticket_id, bet_id) VALUES ({}, {});".format(newId, bid)
			cursor.execute(statement)

	connection.commit()
	cursor.close()
	connection.close()

	return Response(status = 200)

if __name__ == '__main__':
	app.run(host='0.0.0.0')
