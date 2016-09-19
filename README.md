Tournament DB 
=============
It is a project where we use Postgre DB to simulate the Swiss Tournament.
Based from the number of players registered, this program can give you the
next pairing for the next round. It pairs players with equal number of wins or
close to number of wins. If there are even number of players, it 
doesn't do any extra handling. However, if there are odd number of players,
it introduces the concept of a "bye" where in a player gets only one bye for
the tournament and its an automatic win.

----


How To Use?
=============
- To run the test
	-  do: python tournament_test.py
- To register player:
	- to the main tournament
		- registerPlayer("A")
	- to a different tournament
		- registerPlayer("A", "Tournament1")
- To check player standings:
	- of main tournament
		-  playerStandings()
	- of different tournament
		-  playerStandings("Tournament1")
- To get swiss pairings for the next round:
	- from main tournament
		-  swissPairings()
	- from different tournament
		-  swissPairings("Tournament1")
- To match players:
	- in main tournament
		-  reportMatch(winner id, loser id)
	- in different tournament
		-  reportMatch(winner id, loser id, "Tournament1")				

Supported features
==============
- Handles odd number of players. Ensure only 1 "bye" is given to a player which results to an automatic win.
- Prevents rematches between players.
- Supports more than one tournament.