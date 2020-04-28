import sys
import requests
import time
import json

def get_teams_names(match):
	home_team_id = match['home_team_id']
	away_team_id = match['away_team_id']

	URL = ADMIN_URL + "teams/" + str(home_team_id)
	PARAMS = {}
	r = requests.get(url = URL, params = PARAMS)
	tmp_data = r.json()
	home_team_name = tmp_data['name']

	URL = ADMIN_URL + "teams/" + str(away_team_id)
	PARAMS = {}
	r = requests.get(url = URL, params = PARAMS)
	tmp_data = r.json()
	away_team_name = tmp_data['name']

	return (home_team_name, away_team_name)

def get_teams_and_odds(match_id, bet_type):
	URL = ADMIN_URL + "matches/" + str(match_id)
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
	ADMIN_URL = sys.argv[1]
	SERVICE_URL = sys.argv[2]
	path = ADMIN_URL + "teams"
	print("Wait! The database is not available yet.")
	response = requests.get(path)
	while response.status_code != 200:
		time.sleep(1)
		response = requests.get(path)
	print("Welcome to the IdpBet App!")

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
				URL = ADMIN_URL + "teams"
				PARAMS = {}
				r = requests.get(url = URL, params = PARAMS)
				data = r.json()
				print("%s|%s|%s" %("Team Id".rjust(10), "Name".rjust(20), "Rate".rjust(10)))
				for team in data['teams']:
					print("%10d|%s|%10.1f" %(team['team_id'], team['name'].rjust(20), team['rate']))
			elif option == 2:
				URL = ADMIN_URL + "matches"
				PARAMS = {}
				r = requests.get(url = URL, params = PARAMS)
				data = r.json()
				print("%s|%s|%s|%s|%s|%s" %("Match Id".rjust(10), "Home Team".rjust(20), "Away Team".rjust(20), "1".rjust(10), "X".rjust(10), "2".rjust(10)))
				for match in data['matches']:
					(home_team_name, away_team_name) = get_teams_names(match)
					print("%10d|%20s|%20s|%10.1f|%10.1f|%10.1f" %(match['match_id'], home_team_name, away_team_name, match['home_victory'], match['draw'], match['away_victory']))
			elif option == 3:
				s = input('Select Match Id: ')
				URL = ADMIN_URL + "matches/" + s
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
				URL = ADMIN_URL + "matches/add"
				PARAMS = {'home_team':home_team, 'away_team':away_team, 'home_victory':home_victory, 'draw':draw, 'away_victory':away_victory}
				r = requests.post(url = URL, json = PARAMS)
				if r.status_code == 201:
					print("Successful add.")
			elif option == 5:
				s = input('Select Match Id that you want to cancel: ')
				id = int(s)
				URL = ADMIN_URL + "matches/cancel"
				PARAMS = {'match_id':id}
				r = requests.delete(url = URL, json = PARAMS)
				if r.status_code == 404:
					print("Match with id " + str(id) + " does not exist.")
				elif r.status_code == 200:
					print("Successful cancellation.")
		elif option == 2:
			print("You have chosen the Bet Service.")
			s = input('What operation do you want to do?\n1 - List Best, 2 - Place Bet, 3 - Cancel Bet, 4 - List Tickets, 5 - Place ticket\n')
			option = int(s)
			if option == 1:
				URL = SERVICE_URL + "bets"
				PARAMS = {}
				r = requests.get(url = URL, params = PARAMS)
				data = r.json()
				print("%s|%s|%s|%s|%s" %("Bet Id".rjust(10), "Home Team".rjust(20), "Away Team".rjust(20), "Bet Type".rjust(10), "Odds".rjust(10)))
				for bet in data['bets']:
					(home_team_name, away_team_name, odds) = get_teams_and_odds(bet['match_id'], bet['bet_type'])
					print("%10d|%20s|%20s|%10s|%10.1f" %(bet['bet_id'], home_team_name, away_team_name, bet['bet_type'], odds))
			elif option == 2:
				URL = ADMIN_URL + "matches"
				PARAMS = {}
				r = requests.get(url = URL, params = PARAMS)
				data = r.json()
				print("%s|%s|%s|%s|%s|%s" %("Match Id".rjust(10), "Home Team".rjust(20), "Away Team".rjust(20), "1".rjust(10), "X".rjust(10), "2".rjust(10)))
				for match in data['matches']:
					(home_team_name, away_team_name) = get_teams_names(match)
					print("%10d|%20s|%20s|%10.1f|%10.1f|%10.1f" %(match['match_id'], home_team_name, away_team_name, match['home_victory'], match['draw'], match['away_victory']))
				s = input('Choose the match id that you want to bet on: ')
				URL = ADMIN_URL + "matches/" + s
				PARAMS = {}
				r = requests.get(url = URL, params = PARAMS)
				data = r.json()
				(home_team_name, away_team_name) = get_teams_names(data)
				print("You have chosen match " + s + ": " + home_team_name + " - " + away_team_name)

				bet_type = input("Choose your bet(1, X, 2): ")
				while bet_type != "1" and bet_type != "X" and bet_type != "2":
					print("Invalid bet. Choose again!")
					bet_type = input("Choose your bet(1, X, 2): ")

				URL = SERVICE_URL + "bets/add"
				PARAMS = {'match_id':int(s), 'bet_type':bet_type}
				r = requests.post(url = URL, json = PARAMS)
				if r.status_code == 201:
					print("Successful bet.")
			elif option == 3:
				s = input('Select Bet Id that you want to cancel: ')
				id = int(s)
				URL = SERVICE_URL + "bets/cancel"
				PARAMS = {'bet_id':id}
				r = requests.delete(url = URL, json = PARAMS)
				if r.status_code == 404:
					print("Bet with id " + str(id) + " does not exist.")
				elif r.status_code == 200:
					print("Successful cancellation.")
			elif option == 4:
				URL = SERVICE_URL + "tickets"
				PARAMS = {}
				r = requests.get(url = URL, params = PARAMS)
				data = r.json()
				print("%s|%s|%s|%s" %("Ticket Id".rjust(10), "Total Odds".rjust(15), "Amount".rjust(10), "Potential Gain".rjust(20)))
				for ticket in data['tickets']:
					print("%10d|%15.2f|%10.2f|%20.2f" %(ticket['ticket_id'], ticket['odds'], ticket['amount'], ticket['potential_gain']))
			elif option == 5:
				print()
				URL = SERVICE_URL + "bets"
				PARAMS = {}
				r = requests.get(url = URL, params = PARAMS)
				data = r.json()
				if not data['bets']:
					print("You have not placed any bet yet!")
				else:
					print("Here are your bets:")
					print("%s|%s|%s|%s|%s" %("Bet Id".rjust(10), "Home Team".rjust(20), "Away Team".rjust(20), "Bet Type".rjust(10), "Odds".rjust(10)))
					all_bet_ids = []
					id_to_odds = {}
					for bet in data['bets']:
						all_bet_ids.append(bet['bet_id'])
						(home_team_name, away_team_name, odds) = get_teams_and_odds(bet['match_id'], bet['bet_type'])
						print("%10d|%20s|%20s|%10s|%10.1f" %(bet['bet_id'], home_team_name, away_team_name, bet['bet_type'], odds))
						id_to_odds[bet['bet_id']] = odds
					ids = input('Insert the bets for your new ticket, separated by space: ').split(' ')
					while True:
						ok = True
						for bet_id in ids:
							if int(bet_id) not in all_bet_ids:
								ok = False
								print("Bet " + bet_id + " does not exist! Try again!")
								break
						if not ok:
							ids = input('Insert the bets for your new ticket, separated by space: ').split(' ')
						else:
							break
					total_odds = 1
					for bet_id in ids:
						total_odds = float(total_odds * id_to_odds[int(bet_id)])
					total_odds = round(total_odds, 2)
					print("Good! Your total odds is: " + str(total_odds))
					amount = input("How much would you like to bet? (in RON) ")
					amount = float(amount)

					URL = SERVICE_URL + "tickets/add"
					PARAMS = {'betIDs': ids, 'odds': total_odds, 'amount': amount}
					r = requests.get(url = URL, json = PARAMS)
					if r.status_code == 200:
						print("Ticket placed successfully!")
					else:
						print("Error! Status code is " + str(r.status_code))
		elif option == 3:
			print("Goodbye!")
			break
