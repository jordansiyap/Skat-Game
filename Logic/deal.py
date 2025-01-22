from flask import Flask, jsonify, abort
from flask import request
import random
class Deal:
    def __init__(self):
        pass

    @staticmethod
    def deal(players):

        deck = [
            {"suit": "clubs", "value": "ace"},
            {"suit": "clubs", "value": "king"},
            {"suit": "clubs", "value": "queen"},
            {"suit": "clubs", "value": "jack"},
            {"suit": "clubs", "value": "10"},
            {"suit": "clubs", "value": "9"},
            {"suit": "clubs", "value": "8"},
            {"suit": "clubs", "value": "7"},
            {"suit": "hearts", "value": "ace"},
            {"suit": "hearts", "value": "king"},
            {"suit": "hearts", "value": "queen"},
            {"suit": "hearts", "value": "jack"},
            {"suit": "hearts", "value": "10"},
            {"suit": "hearts", "value": "9"},
            {"suit": "hearts", "value": "8"},
            {"suit": "hearts", "value": "7"},
            {"suit": "spades", "value": "ace"},
            {"suit": "spades", "value": "king"},
            {"suit": "spades", "value": "queen"},
            {"suit": "spades", "value": "jack"},
            {"suit": "spades", "value": "10"},
            {"suit": "spades", "value": "9"},
            {"suit": "spades", "value": "8"},
            {"suit": "spades", "value": "7"},
            {"suit": "diamonds", "value": "ace"},
            {"suit": "diamonds", "value": "king"},
            {"suit": "diamonds", "value": "queen"},
            {"suit": "diamonds", "value": "jack"},
            {"suit": "diamonds", "value": "10"},
            {"suit": "diamonds", "value": "9"},
            {"suit": "diamonds", "value": "8"},
            {"suit": "diamonds", "value": "7"},
        ]
        hands_output = {}
        p1_hand = []
        p2_hand = []
        dealer_hand = []
        skat = []
        hands = [p1_hand, p2_hand, dealer_hand]
        ##create temp copy of deck
        deck_copy = deck.copy()
        ##reorder players so dealer gets cards last (also betting order)
        dealer = players.pop(0)["playerId"]
        players.append(dealer)
        ##shuffle copied deck
        random.shuffle(deck_copy)

        ##unsure of how to create hand if its just a list of cards or also contains "type": "array" etc.
        ##first 3 cards per player
        for hand in hands:
            for i in range(3):
                hand.append(deck_copy.pop())

        ##skat
        skat.append(deck_copy.pop())
        skat.append(deck_copy.pop())

        ##4 cards per hand
        for hand in hands:
            for i in range(4):
                hand.append(deck_copy.pop())

        ##last 9 cards dealt 3 per player
        for hand in hands:
            for i in range(3):
                hand.append(deck_copy.pop())

        hands_output[players[0]["playerId"]]= p1_hand
        hands_output[players[1]["playerId"]] = p2_hand
        hands_output[players[2]["playerId"]] = dealer_hand
        hands_output["player3"] = skat



        return {"hands": hands_output, "betting_order": players}
