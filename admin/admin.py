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

class Team:
	def __init__(self, team_id, name, rate):
		self.team_id = team_id
		self.name = name
		self.rate = rate

	def key(self):
		return self.team_id

	def __hash__(self):
		return hash(self.key())

	def __eq__(self, other):
		if self.team_id == other.team_id:
			return True
		return False

	def __str__(self):
		res = ""
		res += "Team(" + self.team_id + "," + self.name + "," + self.rate + ")"
		return res

	def serialize(self):
		return {
			'team_id':self.team_id,
			'name':self.name,
			'rate':self.rate
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

@app.route('/teams', methods=['GET'])
def get_teams():
	connection = mysql.connector.connect(**config)
	cursor = connection.cursor()
	statement = "SELECT * FROM Teams;"
	cursor.execute(statement)
	teams = []
	for (id, name, rate) in cursor:
		t = Team(id, name, rate)
		teams.append(t)
	connection.commit()
	cursor.close()
	connection.close()
	return jsonify(teams=[t.serialize() for t in teams])

@app.route('/teams/<int:team_id>', methods=['GET'])
def get_team(team_id):
	connection = mysql.connector.connect(**config)
	cursor = connection.cursor()
	statement = "SELECT * FROM Teams WHERE id = {};".format(team_id)
	cursor.execute(statement)
	t = None
	for (id, name, rate) in cursor:
		t = Team(id, name, rate)
	connection.commit()
	cursor.close()
	connection.close()

	if t is None:
		return jsonify("Team with id " + str(team_id) + " does not exist.")
	else:
		return jsonify(t.serialize())

@app.route('/matches', methods=['GET'])
def get_matches():
	connection = mysql.connector.connect(**config)
	cursor = connection.cursor()
	statement = "SELECT * FROM Matches;"
	cursor.execute(statement)
	matches = []
	for (id, home_team, away_team, home_victory, draw, away_victory) in cursor:
		m = Match(id, home_team, away_team, home_victory, draw, away_victory)
		matches.append(m)
	connection.commit()
	cursor.close()
	connection.close()
	return jsonify(matches=[m.serialize() for m in matches])

@app.route('/matches/<int:match_id>', methods=['GET'])
def get_match(match_id):
	connection = mysql.connector.connect(**config)
	cursor = connection.cursor()
	statement = "SELECT * FROM Matches WHERE id = {};".format(match_id)
	cursor.execute(statement)
	m = None
	for (id, home_team, away_team, home_victory, draw, away_victory) in cursor:
		m = Match(id, home_team, away_team, home_victory, draw, away_victory)
	connection.commit()
	cursor.close()
	connection.close()

	if m is None:
		return jsonify("Match with id " + str(match_id) + " does not exist.")
	else:
		return jsonify(m.serialize())

@app.route('/matches/add', methods=['POST'])
def add_match():
	params = request.get_json(silent = True)
	if not params:
		return Response(status = 400)

	home_team = params.get('home_team')
	if not home_team:
		return Response(status = 400)

	away_team = params.get('away_team')
	if not away_team:
		return Response(status = 400)

	home_victory = params.get('home_victory')
	if not home_victory:
		return Response(status = 400)

	draw = params.get('draw')
	if not draw:
		return Response(status = 400)

	away_victory = params.get('away_victory')
	if not away_victory:
		return Response(status = 400)

	connection = mysql.connector.connect(**config)
	cursor = connection.cursor()
	statement = "INSERT INTO Matches (home_team, away_team, home_victory, draw, away_victory) VALUES ({},{},{},{},{});".format(home_team, away_team, home_victory, draw, away_victory)
	cursor.execute(statement)
	connection.commit()
	cursor.close()
	connection.close()

	return Response(status = 201)

@app.route('/matches/cancel', methods=['DELETE'])
def delete_match():
	params = request.get_json(silent = True)
	if not params:
		return Response(status = 400)

	match_id = params.get('match_id')
	if not match_id:
		return Response(status = 400)

	connection = mysql.connector.connect(**config)
	cursor = connection.cursor()
	statement = "SELECT * FROM Matches WHERE id = {};".format(match_id)
	cursor.execute(statement)
	m = None
	for (id, home_team, away_team, home_victory, draw, away_victory) in cursor:
		m = Match(id, home_team, away_team, home_victory, draw, away_victory)
	if m is None:
		connection.commit()
		cursor.close()
		connection.close()
		return Response(status = 404)
	else:
		statement = "DELETE FROM Matches WHERE id = {};".format(match_id)
		cursor.execute(statement)
		connection.commit()
		cursor.close()
		connection.close()
		return Response(status = 200)

if __name__ == '__main__':
	app.run(host='0.0.0.0')
