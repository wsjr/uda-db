-- Drop tables
DROP TABLE PlayersTournaments CASCADE;
DROP TABLE Tournaments CASCADE;
DROP TABLE Players CASCADE;
DROP TABLE Matches CASCADE;

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

-- Create "Matches" table
CREATE TABLE Matches(
	id SERIAL primary key, 
	winner INT not null DEFAULT 0,
	loser INT DEFAULT 0,
	tid int not null);

\d Matches;

-- Create "Tournaments" table
CREATE TABLE Tournaments(
	id SERIAL primary key, 
	name TEXT not null);

-- Insert "Main" Tournament
INSERT INTO Tournaments (name) VALUES('MAIN_TOURNAMENT');


\d Tournaments;

-- Create "PlayersTournaments" table
CREATE TABLE PlayersTournaments(
	id SERIAL primary key,
	pid int references players(id), 
	tid int references tournaments(id));

\d PlayersTournaments;


CREATE VIEW PlayersWithoutBye as select pid, tid from PlayersTournaments except select winner, tid from Matches where loser = 0 order by pid asc;

CREATE VIEW PlayerWins as select winner as pid, count(winner) as wins, tid from Matches where winner > 0 group by winner, tid;
CREATE VIEW PlayerLosses as select loser as pid, count(loser) as losses, tid from Matches where loser > 0 group by loser, tid;

