import unittest
from Rulebased_Betting import beteasy
from Rulebased_Betting.beteasy import BetEasy


class SkatAiBettingTest(unittest.TestCase):
    def test_find_last_bid_noraise(self):
        input_previousbets = [{
            "gamemode": {
                "active_player": {
                    "playerId": "player2"
                },
                "betting": 18,
                "name": "Raise"
            },
            "player": {
                "playerId": "player2"
            }
        },
        {
            "gamemode": {
                "active_player": {
                    "playerId": "player4"
                },
                "betting": 18,
                "name": "Check"
            },
            "player": {
                "playerId": "player4"
            }
        }]
        input_player = {
                "playerId": "player2"
            }
        output = {
            "gamemode": {
                "active_player": {
                    "playerId": "player4"
                },
                "betting": 18,
                "name": "Check"
            },
            "player": {
                "playerId": "player4"
            }
        }

        self.assertEqual(first=BetEasy.find_last_bid(input_previousbets,input_player),second=output)

    def test_find_last_bid_raise(self):
        input_previousbets= [{
            "gamemode": {
                "active_player": {
                    "playerId": "player2"
                },
                "betting": 18,
                "name": "Raise"
            },
            "player": {
                "playerId": "player2"
            }
        },
        {
            "gamemode": {
                "active_player": {
                    "playerId": "player4"
                },
                "betting": 18,
                "name": "Check"
            },
            "player": {
                "playerId": "player4"
            }
        },
        {
            "gamemode": {
                "active_player": {
                    "playerId": "player2"
                },
                "betting": "20",
                "name": "Raise"
            },
            "player": {
                "playerId": "player2"
            }
        }]
        input_player = {
                "playerId": "player2"
            }
        output = {
            "player": {
                "playerId": "player2"
            },
            "gamemode":{
                "active_player": {"playerId": "player2"},
                "betting": "18",
                "name": "Karo"
            }
        }
        self.assertEqual(first=BetEasy.find_last_bid(input_previousbets,input_player),second=output)

if __name__ == '__main__':
    unittest.main(verbosity=2)
