#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
from operator import itemgetter

MAIN_TOURNAMENT = 'MAIN_TOURNAMENT'


def connect(database_name="tournament"):
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        cursor = db.cursor()
        return db, cursor
    except:
        print("<error message>")


def deleteAllMatches():
    """Remove all the match records from the database."""
    db, cursor = connect()

    # Remove all rows in the Matches table.
    query = "DELETE FROM Matches"
    cursor.execute(query)

    db.commit()
    db.close()


def deleteMatches(tournament=MAIN_TOURNAMENT):
    """Remove all the match records from the database."""
    db, cursor = connect()

    if tournamentExists(tournament):
        tid = getTournamentId(tournament)

        query = "DELETE FROM Matches where tid=%s"
        parameter = (tid,)
        cursor.execute(query, parameter)

        db.commit()
        db.close()
    else:
        raise ValueError(
            "Tournament {name} does NOT exist.".format(name=tournament))


def deleteAllPlayers():
    """Remove all the player records from the database."""
    db, cursor = connect()

    # Remove all the rows in PlayersTournaments table.
    query = "DELETE FROM PlayersTournaments"
    cursor.execute(query)

    db.commit()

    # Remove all entries in the Players table.
    query = "DELETE FROM Players"
    cursor.execute(query)

    db.commit()
    db.close()


def deletePlayers(tournament=MAIN_TOURNAMENT):
    """Remove all the player records from the database."""
    db, cursor = connect()

    if tournamentExists(tournament):
        tid = getTournamentId(tournament)

        query = "DELETE FROM PlayersTournaments where tid=%s"
        parameter = (tid,)
        cursor.execute(query, parameter)

        db.commit()
        db.close()
    else:
        raise ValueError(
            "Tournament {name} does NOT exist.".format(name=tournament))


def countPlayers(tournament=MAIN_TOURNAMENT):
    """Returns the number of players currently registered."""
    db, cursor = connect()

    if tournamentExists(tournament):
        tid = getTournamentId(tournament)

        query = "SELECT count(*) FROM PlayersTournaments where tid=%s"
        parameter = (tid,)
        cursor.execute(query, parameter)
        count = cursor.fetchone()[0]

        db.close()

        return count
    else:
        raise ValueError(
            "Tournament {name} does NOT exist.".format(name=tournament))


def playerExists(name):
    """Checks if a player exists or not already.

    Args:
      name:  the player name

    Returns:
      True, if player exists already. Otherwise, false.
    """
    db, cursor = connect()

    query = "SELECT count(*) FROM Players WHERE name = %s"
    parameter = (name,)
    cursor.execute(query, parameter)
    count = cursor.fetchone()[0]

    db.close()

    return count


def playerExistsInTournament(pid, tid):
    """Checks if a player exists or not already.

    Args:
      name:  the player name

    Returns:
      True, if player exists already. Otherwise, false.
    """
    db, cursor = connect()

    query = "SELECT count(*) FROM PlayersTournaments " +\
            "WHERE pid = %s and tid = %s"
    parameter = ((pid,), (tid,))
    cursor.execute(query, parameter)
    count = cursor.fetchone()[0]

    db.close()

    return count


def getPlayerId(name):
    """Gets player id.

    Args:
      name:  the player name

    Returns:
      Player id
    """
    db, cursor = connect()

    query = "SELECT id FROM Players WHERE name = %s"
    parameter = (name,)
    cursor.execute(query, parameter)
    pid = cursor.fetchone()[0]

    db.close()

    return pid


def tournamentExists(name):
    """Checks if a tournament exists or not already.

    Args:
      name:  the tournament name

    Returns:
      True, if tournament exists already. Otherwise, false.
    """
    db, cursor = connect()

    query = "SELECT count(*) FROM Tournaments WHERE name = %s"
    parameter = (name,)
    cursor.execute(query, parameter)
    count = cursor.fetchone()[0]

    db.close()

    return count


def getTournamentId(name):
    """Gets the tournament id.

    Args:
      name:  the tournament name

    Returns:
      Tournament id.
    """
    db, cursor = connect()

    query = "SELECT id FROM Tournaments WHERE name = %s"
    parameter = (name,)
    cursor.execute(query, parameter)
    tid = cursor.fetchone()[0]

    db.close()

    return tid


def registerPlayer(name, tournament=MAIN_TOURNAMENT):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
      tournament: name of the tournament where the player is participating.
    """
    db, cursor = connect()

    # Create tournament if it doesn't exist
    if tournamentExists(tournament) == False:
        query = "INSERT INTO Tournaments (name) VALUES (%s)"
        parameter = (tournament,)
        cursor.execute(query, parameter)

        db.commit()

    # Make sure the player doesn't exist in the Players table
    if playerExists(name) == False:
        query = "INSERT INTO Players (name) VALUES (%s)"
        parameter = (name,)
        cursor.execute(query, parameter)

        db.commit()

    # Get player id
    pid = getPlayerId(name)

    # Get tournament id
    tid = getTournamentId(tournament)

    # Make sure the player does not exist yet in the tournament.
    if playerExistsInTournament(pid, tid) == False:
        # Insert entry into PlayersTournaments table
        query = "INSERT INTO PlayersTournaments (pid, tid) VALUES (%s, %s)"
        parameter = ((pid,), (tid,))
        cursor.execute(query, parameter)

        db.commit()
    else:
        raise ValueError(
            "Player {name} already exists in tournament. Please check."
            .format(name=name))

    db.close()


def playerStandings(tournament=MAIN_TOURNAMENT):
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or
    a player tied for first place if there is currently a tie.

    Args:
      tournament: name of the tournament where the player is participating.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """

    # Grab all the players
    db, cursor = connect()

    standings = []

    tid = getTournamentId(tournament)

    # Note: I couldn't move this to a VIEW as I couldn't find a way to pass
    #       parameter to a VIEW since I have to pass the tournament id
    #       as seen in this query.
    query = "SELECT p.id, p.name, COALESCE(pwins.wins,0) AS wins, " +\
            "COALESCE(plosses.losses, 0) AS losses FROM Players AS p " +\
            "RIGHT JOIN (SELECT pid, tid FROM PlayersTournaments " +\
            "WHERE tid = %s) " +\
            "AS pt ON p.id = pt.pid " +\
            "LEFT JOIN (SELECT * FROM PlayerWins WHERE tid = %s) " +\
            "AS pwins ON p.id = pwins.pid " +\
            "LEFT JOIN (SELECT * FROM PlayerLosses WHERE tid = %s) " +\
            "AS plosses ON p.id = plosses.pid " +\
            "ORDER BY wins DESC, id ASC"
    parameter = ((tid,), (tid,), (tid,))
    cursor.execute(query, parameter)

    rows = cursor.fetchall()
    for row in rows:
        pid = row[0]
        pname = row[1]
        wins = row[2]
        losses = row[3]
        matches = wins + losses

        standings.append((pid, pname, wins, matches))

    # Close connection
    db.close()

    return standings


def matchExists(winner, loser, tournament=MAIN_TOURNAMENT):
    """Checks if 2 players already played or not.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
      tournament: name of the tournament where the player is participating.

    Returns:
      True, if two players played already. False, otherwise.
    """
    tid = getTournamentId(tournament)

    db, cursor = connect()

    query = "SELECT count(*) FROM Matches WHERE " +\
            "tid = %s AND ((winner=%s and loser=%s) " +\
            "OR (winner=%s and loser=%s))"
    parameter = ((tid,), (winner,), (loser,), (loser,), (winner,))
    cursor.execute(query, parameter)
    count = cursor.fetchone()[0]

    db.close()

    return count


def reportMatch(winner, loser, tournament=MAIN_TOURNAMENT):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
      tournament: name of the tournament where the player is participating.
    """

    result = True
    # Make sure 2 players haven't played yet.
    if (matchExists(winner, loser) == False):
        tid = getTournamentId(tournament)

        db, cursor = connect()

        # Insert winner/loser record
        query = "INSERT INTO Matches (winner, loser, tid) " +\
                "VALUES (%s, %s, %s)"
        parameter = ((winner,), (loser,), (tid,))
        cursor.execute(query, parameter)

        db.commit()
        db.close()
    # 2 players have played already.
    else:
        result = False

    return result


def givePlayerBye(player, tournament=MAIN_TOURNAMENT):
    """Gives the player a bye. Automatic win!

    Args:
      player:  the id number of the player who got bye and automatic win.
      tournament: name of the tournament where the player is participating.
    """
    # print "player {player} gets a bye!".format(player=player)
    reportMatch(player, 0, tournament)


def swissPairings(tournament=MAIN_TOURNAMENT):
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Args:
      tournament: name of the tournament where the player is participating.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """

    count = countPlayers(tournament)
    pairings = []
    tid = getTournamentId(tournament)

    # Even number of players
    if (count % 2 == 0):
        index = 0
        standings = playerStandings(tournament)
        while index < count:
            pair1 = standings[index]
            pair2 = standings[index+1]
            pairing = (pair1[0], pair1[1], pair2[0], pair2[1])
            pairings.append(pairing)
            index += 2
    # Odd number of players
    else:
        db, cursor = connect()

        # Step 1, go thru the select the player id in the standings without bye
        query = "SELECT pid FROM PlayersWithoutBye WHERE tid=%s LIMIT 1"
        parameter = (tid,)
        cursor.execute(query, parameter)
        player_id = cursor.fetchone()[0]

        # Step 2, give the player a bye and an automatic win for the player.
        givePlayerBye(player_id, tournament)

        # Step 3, Return the pairing without the player with bye.
        standings = playerStandings(tournament)
        # Remove from the result the player id who was given a bye. See step 2.
        standings = [(pid, name, wins, matches)
                     for pid, name, wins, matches in standings
                     if pid != player_id]
        count = len(standings)

        index = 0
        while index < count:
            pair1 = standings[index]
            pair2 = standings[index+1]
            pairing = (pair1[0], pair1[1], pair2[0], pair2[1])
            pairings.append(pairing)
            index += 2

        db.close()

    return pairings
