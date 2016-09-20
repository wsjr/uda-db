-- Drop database
\c template1;
DROP DATABASE tournament;

-- Create tournament database
CREATE DATABASE tournament;
\c tournament;

-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.

-- Create "Players" table
CREATE TABLE Players(
	id SERIAL primary key, 
	name TEXT not null);

\d Players;

-- Create "Tournaments" table
CREATE TABLE Tournaments(
	id SERIAL primary key, 
	name TEXT not null);

-- Insert "Main" Tournament
INSERT INTO Tournaments (name) VALUES('MAIN_TOURNAMENT');

\d Tournaments;

-- Create "Matches" table
CREATE TABLE Matches(
	id SERIAL primary key, 
	winner INT references players(id),
	-- NOTE: I couldn't get the foreign key to work here because I insert "0" in the loser's column
	-- 		  when the Player(winner) has a "Bye" in the case of odd number of registered users.
	loser INT not null,
	tid INT references tournaments(id));

\d Matches;

-- Create "PlayersTournaments" table
CREATE TABLE PlayersTournaments(
	id SERIAL primary key,
	pid INT references players(id), 
	tid INT references tournaments(id));

\d PlayersTournaments;


CREATE VIEW PlayersWithoutBye as select pid, tid from PlayersTournaments except select winner, tid from Matches where loser = 0 order by pid asc;

CREATE VIEW PlayerWins as select winner as pid, count(winner) as wins, tid from Matches where winner > 0 group by winner, tid;
CREATE VIEW PlayerLosses as select loser as pid, count(loser) as losses, tid from Matches where loser > 0 group by loser, tid;

