-- Drop database
\c template1;
DROP DATABASE IF EXISTS tournament;

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
	loser INT references players(id),
	tid INT references tournaments(id));

\d Matches;

-- Create "PlayersTournaments" table
CREATE TABLE PlayersTournaments(
	id SERIAL primary key,
	pid INT references players(id), 
	tid INT references tournaments(id));

\d PlayersTournaments;


-- Create Views 
CREATE VIEW PlayersWithoutBye as select pid, tid from PlayersTournaments except select winner, tid from Matches where loser = winner order by pid asc;

CREATE VIEW PlayerWins as select winner as pid, count(winner) as wins, tid from Matches group by winner, tid;
CREATE VIEW PlayerLosses as select loser as pid, count(loser) as losses, tid from Matches where loser != winner group by loser, tid;

-- Create Function
CREATE OR REPLACE FUNCTION PlayerStandings (tournament_id INT) 
	RETURNS TABLE (
 		id INT,
 		name TEXT,
 		wins BIGINT,
 		losses BIGINT
	) AS $$
	BEGIN
 		RETURN QUERY 
 			SELECT 
	 			p.id, p.name, COALESCE(pwins.wins,0) AS wins, COALESCE(plosses.losses, 0) AS losses 
	 			FROM Players AS p
	            RIGHT JOIN (SELECT pid, tid FROM PlayersTournaments WHERE tid = tournament_id) AS pt ON p.id = pt.pid
	            LEFT JOIN (SELECT * FROM PlayerWins WHERE tid = tournament_id) AS pwins ON p.id = pwins.pid
	            LEFT JOIN (SELECT * FROM PlayerLosses WHERE tid = tournament_id) AS plosses ON p.id = plosses.pid
	            ORDER BY wins DESC, id ASC;
	END;
	$$ 
	LANGUAGE 'plpgsql';

