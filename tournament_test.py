#!/usr/bin/env python
#
# Test cases for tournament.py
# These tests are not exhaustive, but they should cover the majority of cases.
#
# If you do add any of the extra credit options, be sure to add/modify these test cases
# as appropriate to account for your module's added functionality.

from tournament import *
from operator import itemgetter

def testCount():
    """
    Test for initial player count,
             player count after 1 and 2 players registered,
             player count after players deleted.
    """
    deleteMatches()
    deletePlayers()
    c = countPlayers()
    if c == '0':
        raise TypeError(
            "countPlayers should return numeric zero, not string '0'.")
    if c != 0:
        raise ValueError("After deletion, countPlayers should return zero.")
    print "1. countPlayers() returns 0 after initial deletePlayers() execution."
    registerPlayer("Chandra Nalaar")
    c = countPlayers()
    if c != 1:
        raise ValueError(
            "After one player registers, countPlayers() should be 1. Got {c}".format(c=c))
    print "2. countPlayers() returns 1 after one player is registered."
    registerPlayer("Jace Beleren")
    c = countPlayers()
    if c != 2:
        raise ValueError(
            "After two players register, countPlayers() should be 2. Got {c}".format(c=c))
    print "3. countPlayers() returns 2 after two players are registered."
    deletePlayers()
    c = countPlayers()
    if c != 0:
        raise ValueError(
            "After deletion, countPlayers should return zero.")
    print "4. countPlayers() returns zero after registered players are deleted.\n5. Player records successfully deleted."

def testStandingsBeforeMatches():
    """
    Test to ensure players are properly represented in standings prior
    to any matches being reported.
    """
    deleteMatches()
    deletePlayers()
    registerPlayer("Melpomene Murray")
    registerPlayer("Randy Schwartz")
    standings = playerStandings()
    if len(standings) < 2:
        raise ValueError("Players should appear in playerStandings even before "
                         "they have played any matches.")
    elif len(standings) > 2:
        raise ValueError("Only registered players should appear in standings.")
    if len(standings[0]) != 4:
        raise ValueError("Each playerStandings row should have four columns.")
    [(id1, name1, wins1, matches1), (id2, name2, wins2, matches2)] = standings
    if matches1 != 0 or matches2 != 0 or wins1 != 0 or wins2 != 0:
        raise ValueError(
            "Newly registered players should have no matches or wins.")
    if set([name1, name2]) != set(["Melpomene Murray", "Randy Schwartz"]):
        raise ValueError("Registered players' names should appear in standings, "
                         "even if they have no matches played.")
    print "6. Newly registered players appear in the standings with no matches."

def testReportMatches():
    """
    Test that matches are reported properly.
    Test to confirm matches are deleted properly.
    """
    deleteMatches()
    deletePlayers()
    registerPlayer("Bruno Walton")
    registerPlayer("Boots O'Neal")
    registerPlayer("Cathy Burton")
    registerPlayer("Diane Grant")
    standings = playerStandings()
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(id1, id2)
    reportMatch(id3, id4)
    standings = playerStandings()
    for (i, n, w, m) in standings:
        if m != 1:
            raise ValueError("Each player should have one match recorded.")
        if i in (id1, id3) and w != 1:
            raise ValueError("Each match winner should have one win recorded.")
        elif i in (id2, id4) and w != 0:
            raise ValueError("Each match loser should have zero wins recorded.")
    print "7. After a match, players have updated standings."
    deleteMatches()
    standings = playerStandings()
    if len(standings) != 4:
        raise ValueError("Match deletion should not change number of players in standings.")
    for (i, n, w, m) in standings:
        if m != 0:
            raise ValueError("After deleting matches, players should have zero matches recorded.")
        if w != 0:
            raise ValueError("After deleting matches, players should have zero wins recorded.")
    print "8. After match deletion, player standings are properly reset.\n9. Matches are properly deleted."

def testPairings():
    """
    Test that pairings are generated properly both before and after match reporting.
    """
    deleteMatches()
    deletePlayers()
    registerPlayer("Twilight Sparkle")
    registerPlayer("Fluttershy")
    registerPlayer("Applejack")
    registerPlayer("Pinkie Pie")
    registerPlayer("Rarity")
    registerPlayer("Rainbow Dash")
    registerPlayer("Princess Celestia")
    registerPlayer("Princess Luna")
    standings = playerStandings()
    [id1, id2, id3, id4, id5, id6, id7, id8] = [row[0] for row in standings]
    pairings = swissPairings()
    if len(pairings) != 4:
        raise ValueError(
            "For eight players, swissPairings should return 4 pairs. Got {pairs}".format(pairs=len(pairings)))
    reportMatch(id1, id2)
    reportMatch(id3, id4)
    reportMatch(id5, id6)
    reportMatch(id7, id8)
    pairings = swissPairings()
    if len(pairings) != 4:
        raise ValueError(
            "For eight players, swissPairings should return 4 pairs. Got {pairs}".format(pairs=len(pairings)))
    [(pid1, pname1, pid2, pname2), (pid3, pname3, pid4, pname4), (pid5, pname5, pid6, pname6), (pid7, pname7, pid8, pname8)] = pairings
    possible_pairs = set([frozenset([id1, id3]), frozenset([id1, id5]),
                          frozenset([id1, id7]), frozenset([id3, id5]),
                          frozenset([id3, id7]), frozenset([id5, id7]),
                          frozenset([id2, id4]), frozenset([id2, id6]),
                          frozenset([id2, id8]), frozenset([id4, id6]),
                          frozenset([id4, id8]), frozenset([id6, id8])
                          ])
    actual_pairs = set([frozenset([pid1, pid2]), frozenset([pid3, pid4]), frozenset([pid5, pid6]), frozenset([pid7, pid8])])
    for pair in actual_pairs:
        if pair not in possible_pairs:
            raise ValueError(
                "After one match, players with one win should be paired.")
    print "10. After one match, players with one win are properly paired."


# Below are added tests for the following (1) Rematches, (2) Odd number of pairings and (3) Different tournament.

def testRematches():
    """
    Test that pairings are not supposed to rematch or play twice.
    """
    deleteMatches()
    deletePlayers()

    registerPlayer("Player A")
    registerPlayer("Player B")
    standings = playerStandings()
    [id1, id2] = [row[0] for row in standings]
    pairings = swissPairings()
    if len(pairings) != 1:
        raise ValueError(
            "For two players, swissPairings should return 1 pair. Got {pairs}".format(pairs=len(pairings)))
    
    result = reportMatch(id1, id2)
    if (result == False):
        raise ValueError(
            "{id1} and {id2} should have been a valid match. Got invalid match".format(id1=id1, id2=id2))

    result = reportMatch(id1, id2)
    if (result == True):
        raise ValueError(
            "{id1} and {id2} should have been a rematched and NOT a valid match. Got valid match".format(id1=id1, id2=id2))


def checkStandings(standings, expected_wins):
    """
    Utility function to test the player wins against expected wins.
    """
    index = 0
    for row in standings:
        pid = row[0]
        name = row[1]
        wins = row[2]

        if (wins != expected_wins[index]):
            raise ValueError("Player {name} should have gotten {wins} win. " + 
                             "Got {expected_wins} wins instead.".format(name=name, 
                                                                        wins=wins, 
                                                                        expected_wins=expected_wins))
        index += 1


def testOddNumberOfPlayers():
    """
    Test that pairings odd number of players with the use "bye" mechanism.
    """
    deleteMatches()
    deletePlayers()

    # Check odd number of players, introduce "BYE"
    registerPlayer("A")
    registerPlayer("B")
    registerPlayer("C")
    standings = playerStandings()
    [id1, id2, id3] = [row[0] for row in standings]

    # Input: Give 'A' a bye (inside swiss pairings), B wins against C.
    pairings = swissPairings()
    playerStandings()
    if len(pairings) != 1:
        raise ValueError(
            "For 3 players, swissPairings should return 1 pair. Got {pairs}".format(pairs=len(pairings)))
    [(pid1, pname1, pid2, pname2)] = pairings
    reportMatch(pid1, pid2)

    # Output: 
    # -------------
    #  Name | W | L 
    # -------------
    #   A   | 1 | 0
    #   B   | 1 | 0
    #   C   | 0 | 1 
    standings = playerStandings()
    standings.sort(key=itemgetter(2), reverse=True)
    checkStandings(standings, [1, 1, 0])   

    # Input: Give 'B' a bye (inside swiss pairings), C wins against A.
    pairings = swissPairings()
    playerStandings()
    if len(pairings) != 1:
        raise ValueError(
            "For 3 players, swissPairings should return 1 pair. Got {pairs}".format(pairs=len(pairings)))
    [(pid1, pname1, pid2, pname2)] = pairings
    reportMatch(pid2, pid1)
    
    # Output: 
    # -------------
    #  Name | W | L 
    # -------------
    #   B   | 2 | 0
    #   A   | 1 | 1
    #   C   | 1 | 1 
    standings = playerStandings()
    standings.sort(key=itemgetter(2), reverse=True)
    checkStandings(standings, [2, 1, 1]) 

    # Input: Give 'C' a bye (inside swiss pairings), B wins against A.
    pairings = swissPairings()
    playerStandings()
    if len(pairings) != 1:
        raise ValueError(
            "For 3 players, swissPairings should return 1 pair. Got {pairs}".format(pairs=len(pairings)))
    [(pid1, pname1, pid2, pname2)] = pairings
    reportMatch(pid1, pid2)

    # Output: 
    # -------------
    #  Name | W | L 
    # -------------
    #   B   | 3 | 0
    #   C   | 2 | 1
    #   A   | 1 | 2 
    standings = playerStandings()
    standings.sort(key=itemgetter(2), reverse=True)
    checkStandings(standings, [3, 2, 1]) 


def testDifferentTournaments():
    """
    Test it can handle multiple tournaments
    """
    deleteAllMatches()
    deleteAllPlayers()

    # Register A, B, C, A1 and B1 in Main Tournament
    registerPlayer("A")
    registerPlayer("B")
    registerPlayer("C")
    registerPlayer("A1")
    registerPlayer("B1")
    standings = playerStandings()
    [id1, id2, id3, id4, id5] = [row[0] for row in standings]

    # Input: Give 'A' a bye (inside swiss pairings), B wins vs C, A1 wins vs. B1
    pairings = swissPairings()
    playerStandings()
    if len(pairings) != 2:
        raise ValueError(
            "For 5 players, swissPairings should return 2 pairs. Got {pairs}".format(pairs=len(pairings)))
    [(pid1, pname1, pid2, pname2),(pid3, pname3, pid4, pname4)] = pairings
    reportMatch(pid1, pid2)
    reportMatch(pid3, pid4)

    # Output: 
    # -------------
    #  Name | W | L 
    # -------------
    #   A   | 1 | 0
    #   B   | 1 | 0
    #   C   | 0 | 1 
    #   A1  | 1 | 0
    #   B1  | 0 | 1
    standings = playerStandings()
    standings.sort(key=itemgetter(2), reverse=True)
    checkStandings(standings, [1, 1, 1, 0, 0]) 



    # Register A, B, C in T1 Tournament
    registerPlayer("A1", "T1")
    registerPlayer("B1", "T1")
    registerPlayer("C1", "T1")
    standings = playerStandings("T1")
    [id1, id2, id3] = [row[0] for row in standings]
     # Input: Give 'A1' a bye (inside swiss pairings), B1 wins vs C1
    pairings = swissPairings("T1")
    standings = playerStandings("T1")
    if len(pairings) != 1:
        raise ValueError(
            "For 3 players, swissPairings should return 1 pairs. Got {pairs}".format(pairs=len(pairings)))
    [(pid1, pname1, pid2, pname2)] = pairings
    reportMatch(pid1, pid2, "T1")

    # Output: 
    # ---------------
    #  Name  | W | L 
    # ---------------
    #   A1   | 1 | 0
    #   B1   | 1 | 0
    #   C1   | 0 | 1 
    standings = playerStandings("T1")
    standings.sort(key=itemgetter(2), reverse=True)
    checkStandings(standings, [1, 1, 0]) 


if __name__ == '__main__':
    testCount()
    testStandingsBeforeMatches()
    testReportMatches()
    testPairings()
    testRematches()
    testOddNumberOfPlayers()
    testDifferentTournaments()

    print "Success!  All tests pass!"
