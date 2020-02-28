import sys
import requests
import json

def get_teams_names(match):
	home_team_id = match['home_team_id']
	away_team_id = match['away_team_id']

	URL = "http://" + sys.argv[1] + ":5000/teams/" + str(home_team_id)
	PARAMS = {}
	r = requests.get(url = URL, params = PARAMS)
	tmp_data = r.json()
	home_team_name = tmp_data['name']

	URL = "http://" + sys.argv[1] + ":5000/teams/" + str(away_team_id)
	PARAMS = {}
	r = requests.get(url = URL, params = PARAMS)
	tmp_data = r.json()
	away_team_name = tmp_data['name']

	return (home_team_name, away_team_name)

def get_teams_and_odds(match_id, bet_type):
	URL = "http://" + sys.argv[1] + ":5000/matches/" + str(match_id)
	PARAMS = {}
	r = requests.get(url = URL, params = PARAMS)
	match = r.json()

	(home_team_name, away_team_name) = get_teams_names(match)
	odds = None

	if bet_type == "1":
		odds = match['home_victory']
	elif bet_type == "X":
		odds = match['draw']
	else:
		odds = match['away_victory']

	return (home_team_name, away_team_name, odds)

if __name__ == '__main__':
	while True:
		print("\n")
		s = input('What do you want to test?\n1 - Admin App, 2 - Bet Service, 3 - Close Client\n')
		option = int(s)
		if option == 1:
			print("You have chosen the Admin App.")
			s = input('What operation do you want to do?\n1 - List Teams, 2 - List Matches, ' +
				'3 - List Match By Id, 4 - Add Match, 5 - Cancel Match\n')
			option = int(s)
			if option == 1:
				URL = "http://" + sys.argv[1] + ":5000/teams"
				PARAMS = {}
				r = requests.get(url = URL, params = PARAMS)
				data = r.json()
				print("%s|%s|%s" %("Team Id".rjust(10), "Name".rjust(20), "Rate".rjust(10)))
				for team in data['teams']:
					print("%10d|%s|%10.1f" %(team['team_id'], team['name'].rjust(20), team['rate']))
			elif option == 2:
				URL = "http://" + sys.argv[1] + ":5000/matches"
				PARAMS = {}
				r = requests.get(url = URL, params = PARAMS)
				data = r.json()
				print("%s|%s|%s|%s|%s|%s" %("Match Id".rjust(10), "Home Team".rjust(20), "Away Team".rjust(20), "1".rjust(10), "X".rjust(10), "2".rjust(10)))
				for match in data['matches']:
					(home_team_name, away_team_name) = get_teams_names(match)
					print("%10d|%20s|%20s|%10.1f|%10.1f|%10.1f" %(match['match_id'], home_team_name, away_team_name, match['home_victory'], match['draw'], match['away_victory']))
			elif option == 3:
				s = input('Select Match Id: ')
				URL = "http://" + sys.argv[1] + ":5000/matches/" + s
				PARAMS = {}
				r = requests.get(url = URL, params = PARAMS)
				data = r.json()
				if str(data) == ("Match with id " + s + " does not exist."):
					print(str(data))
				else:
					print("%s|%s|%s|%s|%s|%s" %("Match Id".rjust(10), "Home Team".rjust(20), "Away Team".rjust(20), "1".rjust(10), "X".rjust(10), "2".rjust(10)))
					(home_team_name, away_team_name) = get_teams_names(data)
					print("%10d|%20s|%20s|%10.1f|%10.1f|%10.1f" %(data['match_id'], home_team_name, away_team_name, data['home_victory'], data['draw'], data['away_victory']))
			elif option == 4:
				home_team = int(input('Insert home team id: '))
				away_team = int(input('Insert away team id: '))
				home_victory = float(input('Insert home victory odds: '))
				draw = float(input('Insert draw odds: '))
				away_victory = float(input('Insert away victory odds: '))
				URL = "http://" + sys.argv[1] + ":5000/matches/add"
				PARAMS = {'home_team':home_team, 'away_team':away_team, 'home_victory':home_victory, 'draw':draw, 'away_victory':away_victory}
				r = requests.post(url = URL, json = PARAMS)
				if r.status_code == 201:
					print("Successful add.")
			elif option == 5:
				s = input('Select Match Id that you want to cancel: ')
				id = int(s)
				URL = "http://" + sys.argv[1] + ":5000/matches/cancel"
				PARAMS = {'match_id':id}
				r = requests.delete(url = URL, json = PARAMS)
				if r.status_code == 404:
					print("Match with id " + str(id) + " does not exist.")
				elif r.status_code == 200:
					print("Successful cancellation.")
		elif option == 2:
			print("You have chosen the Bet Service.")
			s = input('What operation do you want to do?\n1 - List Best, 2 - Place Bet, 3 - Cancel Bet\n')
			option = int(s)
			if option == 1:
				URL = "http://" + sys.argv[2] + ":5000/bets"
				PARAMS = {}
				r = requests.get(url = URL, params = PARAMS)
				data = r.json()
				print("%s|%s|%s|%s|%s" %("Bet Id".rjust(10), "Home Team".rjust(20), "Away Team".rjust(20), "Bet Type".rjust(10), "Odds".rjust(10)))
				for bet in data['bets']:
					(home_team_name, away_team_name, odds) = get_teams_and_odds(bet['match_id'], bet['bet_type'])
					print("%10d|%20s|%20s|%10s|%10.1f" %(bet['bet_id'], home_team_name, away_team_name, bet['bet_type'], odds))
			elif option == 2:
				URL = "http://" + sys.argv[1] + ":5000/matches"
				PARAMS = {}
				r = requests.get(url = URL, params = PARAMS)
				data = r.json()
				print("%s|%s|%s|%s|%s|%s" %("Match Id".rjust(10), "Home Team".rjust(20), "Away Team".rjust(20), "1".rjust(10), "X".rjust(10), "2".rjust(10)))
				for match in data['matches']:
					(home_team_name, away_team_name) = get_teams_names(match)
					print("%10d|%20s|%20s|%10.1f|%10.1f|%10.1f" %(match['match_id'], home_team_name, away_team_name, match['home_victory'], match['draw'], match['away_victory']))
				s = input('Choose the match id that you want to bet on: ')
				URL = "http://" + sys.argv[1] + ":5000/matches/" + s
				PARAMS = {}
				r = requests.get(url = URL, params = PARAMS)
				data = r.json()
				(home_team_name, away_team_name) = get_teams_names(data)
				print("You have chosen match " + s + ": " + home_team_name + " - " + away_team_name)

				bet_type = input("Choose your bet(1, X, 2): ")
				while bet_type != "1" and bet_type != "X" and bet_type != "2":
					print("Invalid bet. Choose again!")
					bet_type = input("Choose your bet(1, X, 2): ")

				URL = "http://" + sys.argv[2] + ":5000/bets/add"
				PARAMS = {'match_id':int(s), 'bet_type':bet_type}
				r = requests.post(url = URL, json = PARAMS)
				if r.status_code == 201:
					print("Successful bet.")
			elif option == 3:
				s = input('Select Bet Id that you want to cancel: ')
				id = int(s)
				URL = "http://" + sys.argv[2] + ":5000/bets/cancel"
				PARAMS = {'bet_id':id}
				r = requests.delete(url = URL, json = PARAMS)
				if r.status_code == 404:
					print("Bet with id " + str(id) + " does not exist.")
				elif r.status_code == 200:
					print("Successful cancellation.")
		elif option == 3:
			print("Goodbye!")
			break
