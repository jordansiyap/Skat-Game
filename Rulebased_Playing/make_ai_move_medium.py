from flask import Flask, jsonify, abort
from flask import request
##code starts on line 176
## currently nullspiel logic is still missing

class MakeAIMoveMedium:
    def __init__(self):
        pass



    @staticmethod
    def make_ai_move_medium(cards, gamemode_name, order, hand):
        kreuz_order = [{"suit": "clubs", "value": "jack"},
                       {"suit": "spades", "value": "jack"},
                       {"suit": "hearts", "value": "jack"},
                       {"suit": "diamonds", "value": "jack"},
                       {"suit": "clubs", "value": "ace"},
                       {"suit": "clubs", "value": "king"},
                       {"suit": "clubs", "value": "queen"},
                       {"suit": "clubs", "value": "10"},
                       {"suit": "clubs", "value": "9"},
                       {"suit": "clubs", "value": "8"},
                       {"suit": "clubs", "value": "7"},
                       {"suit": "spades", "value": "ace"},
                       {"suit": "spades", "value": "king"},
                       {"suit": "spades", "value": "queen"},
                       {"suit": "spades", "value": "10"},
                       {"suit": "spades", "value": "9"},
                       {"suit": "spades", "value": "8"},
                       {"suit": "spades", "value": "7"},
                       {"suit": "hearts", "value": "ace"},
                       {"suit": "hearts", "value": "king"},
                       {"suit": "hearts", "value": "queen"},
                       {"suit": "hearts", "value": "10"},
                       {"suit": "hearts", "value": "9"},
                       {"suit": "hearts", "value": "8"},
                       {"suit": "hearts", "value": "7"},
                       {"suit": "diamonds", "value": "ace"},
                       {"suit": "diamonds", "value": "king"},
                       {"suit": "diamonds", "value": "queen"},
                       {"suit": "diamonds", "value": "10"},
                       {"suit": "diamonds", "value": "9"},
                       {"suit": "diamonds", "value": "8"},
                       {"suit": "diamonds", "value": "7"},
                       ]
        pik_order = [{"suit": "clubs", "value": "jack"},
                     {"suit": "spades", "value": "jack"},
                     {"suit": "hearts", "value": "jack"},
                     {"suit": "diamonds", "value": "jack"},
                     {"suit": "spades", "value": "ace"},
                     {"suit": "spades", "value": "king"},
                     {"suit": "spades", "value": "queen"},
                     {"suit": "spades", "value": "10"},
                     {"suit": "spades", "value": "9"},
                     {"suit": "spades", "value": "8"},
                     {"suit": "spades", "value": "7"},
                     {"suit": "clubs", "value": "ace"},
                     {"suit": "clubs", "value": "king"},
                     {"suit": "clubs", "value": "queen"},
                     {"suit": "clubs", "value": "10"},
                     {"suit": "clubs", "value": "9"},
                     {"suit": "clubs", "value": "8"},
                     {"suit": "clubs", "value": "7"},
                     {"suit": "hearts", "value": "ace"},
                     {"suit": "hearts", "value": "king"},
                     {"suit": "hearts", "value": "queen"},
                     {"suit": "hearts", "value": "10"},
                     {"suit": "hearts", "value": "9"},
                     {"suit": "hearts", "value": "8"},
                     {"suit": "hearts", "value": "7"},
                     {"suit": "diamonds", "value": "ace"},
                     {"suit": "diamonds", "value": "king"},
                     {"suit": "diamonds", "value": "queen"},
                     {"suit": "diamonds", "value": "10"},
                     {"suit": "diamonds", "value": "9"},
                     {"suit": "diamonds", "value": "8"},
                     {"suit": "diamonds", "value": "7"},
                     ]

        herz_order = [{"suit": "clubs", "value": "jack"},
                      {"suit": "spades", "value": "jack"},
                      {"suit": "hearts", "value": "jack"},
                      {"suit": "diamonds", "value": "jack"},
                      {"suit": "hearts", "value": "ace"},
                      {"suit": "hearts", "value": "king"},
                      {"suit": "hearts", "value": "queen"},
                      {"suit": "hearts", "value": "10"},
                      {"suit": "hearts", "value": "9"},
                      {"suit": "hearts", "value": "8"},
                      {"suit": "hearts", "value": "7"},
                      {"suit": "clubs", "value": "ace"},
                      {"suit": "clubs", "value": "king"},
                      {"suit": "clubs", "value": "queen"},
                      {"suit": "clubs", "value": "10"},
                      {"suit": "clubs", "value": "9"},
                      {"suit": "clubs", "value": "8"},
                      {"suit": "clubs", "value": "7"},
                      {"suit": "spades", "value": "ace"},
                      {"suit": "spades", "value": "king"},
                      {"suit": "spades", "value": "queen"},
                      {"suit": "spades", "value": "10"},
                      {"suit": "spades", "value": "9"},
                      {"suit": "spades", "value": "8"},
                      {"suit": "spades", "value": "7"},
                      {"suit": "diamonds", "value": "ace"},
                      {"suit": "diamonds", "value": "king"},
                      {"suit": "diamonds", "value": "queen"},
                      {"suit": "diamonds", "value": "10"},
                      {"suit": "diamonds", "value": "9"},
                      {"suit": "diamonds", "value": "8"},
                      {"suit": "diamonds", "value": "7"},
                      ]

        karo_order = [{"suit": "clubs", "value": "jack"},
                      {"suit": "spades", "value": "jack"},
                      {"suit": "hearts", "value": "jack"},
                      {"suit": "diamonds", "value": "jack"},
                      {"suit": "diamonds", "value": "ace"},
                      {"suit": "diamonds", "value": "king"},
                      {"suit": "diamonds", "value": "queen"},
                      {"suit": "diamonds", "value": "10"},
                      {"suit": "diamonds", "value": "9"},
                      {"suit": "diamonds", "value": "8"},
                      {"suit": "diamonds", "value": "7"},
                      {"suit": "spades", "value": "ace"},
                      {"suit": "spades", "value": "king"},
                      {"suit": "spades", "value": "queen"},
                      {"suit": "spades", "value": "10"},
                      {"suit": "spades", "value": "9"},
                      {"suit": "spades", "value": "8"},
                      {"suit": "spades", "value": "7"},
                      {"suit": "hearts", "value": "ace"},
                      {"suit": "hearts", "value": "king"},
                      {"suit": "hearts", "value": "queen"},
                      {"suit": "hearts", "value": "10"},
                      {"suit": "hearts", "value": "9"},
                      {"suit": "hearts", "value": "8"},
                      {"suit": "hearts", "value": "7"},
                      {"suit": "clubs", "value": "ace"},
                      {"suit": "clubs", "value": "king"},
                      {"suit": "clubs", "value": "queen"},
                      {"suit": "clubs", "value": "10"},
                      {"suit": "clubs", "value": "9"},
                      {"suit": "clubs", "value": "8"},
                      {"suit": "clubs", "value": "7"},
                      ]

        null_order = [{"suit": "clubs", "value": "ace"},
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

        value_order = [
            "7",
            "8",
            "9",
            "queen",
            "king",
            "10",
            "ace"
            "jack"
        ]

        grand = False
        nullspiel = False
        card_order = None
        if gamemode_name == "Kreuz":
            card_order = kreuz_order
        elif gamemode_name == "Pik":
            card_order = pik_order
        elif gamemode_name == "Herz":
            card_order = herz_order
        elif gamemode_name == "Karo":
            card_order = karo_order
        elif gamemode_name == "Null":
            card_order = null_order
            nullspiel = True
        elif gamemode_name == "Grand":
            card_order = kreuz_order
            grand = True
        ##this is the logic for if a card has already been played
        played_cards = []
        for i in range(len(list(cards))):
            played_cards.append(cards[list(cards)[i]])
        '''for object in cards:
            played_cards.append(object.values())'''
        suit = played_cards[0]["suit"]
        current_best = None
        best_card = None
        current_closest = None
        closest = None
        difference = None
        contains_suit = False
        contains_only_trump = True

        if not grand:
            trump = card_order[5]["suit"]
        else:
            trump = suit

        ##theoretically we can skip most of the logic if both trump and suit are false for performance
        ##determine if hand only contains trumps
        for card in hand:
            if card["suit"] != trump:
                contains_only_trump = False

        ##determine if hand contains suit or not
        for card in hand:
            if card["suit"] == suit:
                contains_suit = True



        ##determine card with the highest rank
        ##if card isnt the right suit/trump or a jack it gets ignored otherwise look up the corresponding value and return that
        ##if game is nullspiel ignore jacks as well
        if not nullspiel:
            for card in played_cards:
                if card["suit"] == suit or card["suit"] == trump or card["value"] == "jack":
                    for i in range(len(card_order)):
                        if card == card_order[i]:
                            if current_best is None:
                                current_best = i
                                best_card = card
                            elif i < current_best:
                                current_best = i
                                best_card = card
        else:
            for card in played_cards:
                if card["suit"] == suit:
                    for i in range(len(card_order)):
                        if card == card_order[i]:
                            if current_best is None:
                                current_best = i
                                best_card = card
                            elif i < current_best:
                                current_best = i
                                best_card = card

        ##determine card to be played
        if not nullspiel:
            for card in hand:
                if card["suit"] == suit or card["suit"] == trump or card["value"] == "jack":
                    for i in range(len(card_order)):
                        if card == card_order[i]:
                            if current_closest is None and i < current_best:
                                difference = current_best - i
                                current_closest = i
                                closest = card
                            elif i < current_best and current_best - i < difference:
                                difference = current_closest - i
                                current_closest = i
                                closest = card
        else:
            for card in hand:
                if card["suit"] == suit:
                    for i in range(len(card_order)):
                        if card == card_order[i]:
                            if current_closest is None and i > current_best:
                                difference = i - current_best
                                current_closest = i
                                closest = card
                            elif i > current_best and i - current_best < difference:
                                difference = i - current_closest
                                current_closest = i
                                closest = card


        ##if there is no better card determine lowest card in suit
        ##if no card in suit is held determine smallest card in hand and play that
        smallest = None
        smallest_value = 0

        if closest is None:
            if contains_suit:
                only_suit = []
                for card in hand:
                    if card["suit"] == suit:
                        only_suit.append(card)
                closest = max(only_suit, key=lambda x: card_order.index(x))
            elif contains_only_trump:
                closest = max(hand, key=lambda x: card_order.index(x))
            else:
                for card in hand:
                    if card["suit"] != trump:
                        if smallest is None:
                            smallest = card
                            smallest_value = value_order.index(card["value"])
                        elif smallest_value > value_order.index(card["value"]):
                            smallest = card
                            smallest_value = value_order.index(card["value"])
            closest = smallest

        return closest