CREATE DATABASE IdpBet;
use IdpBet;

CREATE TABLE IF NOT EXISTS Teams (
	id INT NOT NULL AUTO_INCREMENT,
	name VARCHAR(30),
	rate FLOAT(20),
	PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS Matches (
	id INT NOT NULL AUTO_INCREMENT,
	home_team INT,
	away_team INT,
	home_victory FLOAT(20),
	draw FLOAT(20),
	away_victory FLOAT(20),
	PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS Bets (
	id INT NOT NULL AUTO_INCREMENT,
	match_id INT,
	bet_type VARCHAR(5),
	PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS Tickets (
	id INT NOT NULL AUTO_INCREMENT,
	odds FLOAT(20),
	amount FLOAT(20),
	potential_gain FLOAT(20),
	PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS Ticket_Bet (
	ticket_id INT NOT NULL,
	bet_id INT NOT NULL
);

INSERT INTO Teams
	(name, rate)
VALUES
	('Liverpool', 1.5),
	('Manchester City', 2.5),
	('Leicester City', 3.5),
	('Chelsea', 4.5),
	('Manchester United', 5.5),
	('Tottenham', 6.5),
	('Sheffield United', 7.5),
	('Wolverhampton', 8.5),
	('Arsenal', 9.5),
	('Burnley', 10.5),
	('Everton', 11.5),
	('Southampton', 12.5),
	('Crystal Palace', 13.5),
	('Newcastle United', 14.5),
	('Brighton', 15.5),
	('Bournemouth', 16.5),
	('Aston Villa', 17.5),
	('West Ham', 18.5),
	('Watford', 19.5),
	('Norwich City', 20.5);

INSERT INTO Matches
	(home_team, away_team, home_victory, draw, away_victory)
VALUES
	(1, 16, 1.2, 6.7, 15.0),
	(9, 18, 1.5, 4.5, 6.5),
	(13, 19, 2.5, 3.1, 2.9),
	(7, 20, 1.6, 3.9, 5.5),
	(12, 14, 1.6, 4.15, 5.1),
	(8, 15, 1.7, 3.8, 4.8),
	(10, 6, 3.3, 3.2, 2.2),
	(4, 11, 1.7, 3.9, 4.6),
	(5, 2, 5.5, 4.5, 1.5),
	(3, 17, 1.4, 5.1, 8.0);
