Swiss Tournament DB
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
To run the application, navigate to ***tournament*** folder and create a database schema by typing:
> psql - f tournament.sql

Then, you can execute the tests module by typing:
> python tournament_test.py

Below are  the methods you can use from the ***tournament*** module:

Description | Usage
------------ | -------------
Register a player | registerPlayer(player name, ***[tournament name]***)  |  
Check player standings | playerStandings(***[tournament name]***) 
Get swiss pairings for the next round | swissPairings(***[tournament name]***) 
Match players | reportMatch(winner id, loser id, ***[tournament name]***) 		

**Note:** If a ***tournament name*** is not provided, it will default to the main tournament.

Supported features
==============
- Handles odd number of players. Ensure only 1 "bye" is given to a player which results to an automatic win.
- Prevents rematches between players.
- Supports more than one tournament.