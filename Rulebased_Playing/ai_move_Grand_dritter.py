from flask import Flask, jsonify, request
import json

app = Flask(__name__)

all_cards = []
"""
Methode wenn KI als drittes in der Runde seine Karte ausspielen muss in Grand.
In der Methode wird zusätzlich dann noch unterschieden an an welcher stelle der alleinspieler sitzt.
"""
def process_ai_move_hard_dritter_Grand(data):
    global all_cards
    all_cards.clear()
    
    open_round = data.get("open_round")
    hand = data.get("hand")
    check_card = data.get("check_card")
    gamemode = data.get("gamemode")
    gamemode_spieler = gamemode.get("active_player")
    history = data.get("history")

    order_list = open_round.get("order")
    erster_spieler = order_list[0]
    zweiter_spieler = order_list[1]
    dritter_spieler = order_list[2]
    all_played_cards = open_round.get("cards")
    firstplayedcard = all_played_cards[erster_spieler]
    secondplayedcard = all_played_cards[zweiter_spieler]
    gamemode = gamemode.get("name")

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
        {"suit": "diamonds", "value": "ace"},
        {"suit": "diamonds", "value": "king"},
        {"suit": "diamonds", "value": "queen"},
        {"suit": "diamonds", "value": "jack"},
        {"suit": "diamonds", "value": "10"},
        {"suit": "diamonds", "value": "9"},
        {"suit": "diamonds", "value": "8"},
        {"suit": "diamonds", "value": "7"},
    ]
    
    # trumpf wertigkeit reihenfolge
    grand_trump_values = [
        {"suit": "clubs", "value": "jack", "rank": 23},  # Jack of Clubs (highest)
        {"suit": "spades", "value": "jack", "rank": 22},  # Jack of Spades (2nd highest)
        {"suit": "hearts", "value": "jack", "rank": 21},  # Jack of Hearts (3rd highest)
        {"suit": "diamonds", "value": "jack", "rank": 20},  # Jack of Diamonds
    ]

    # deck ohne karten in der hand
    deck = [card for card in deck if card not in hand]
    
    rest_cards_in_game = []
    for round_data in history["rounds"]:
        rest_cards_in_game.extend(round_data["cards"].values())
    
    # unbekannte karten
    deck = [card for card in deck if card not in rest_cards_in_game]
    
    if gamemode == "Grand":
        trump_suit = "jack"
    else:
        trump_suit = None  

    #kartenwertigkeit
    skat_values_nichttrumpf = {"ace": 11, "10": 10, "king": 4, "queen": 3, "jack": 2, "9": 0, "8": 0, "7": 0}

    def card_value(card):
        """ Get the card value depending on whether it's trump or not """
        for trump_card in grand_trump_values:
            if trump_card["suit"] == card["suit"] and trump_card["value"] == card["value"]:
                return trump_card["rank"]
        return skat_values_nichttrumpf.get(card["value"], 0)

    def is_trump(card):
        """ Check if the card is a trump card (jack) """
        return card["value"] == "jack"

    # Person die im moment die runde gewonnen hat
    def determine_winner(first_card, second_card, first_player, second_player):
        """ Determine the winner of the round """
        first_card_is_trump = is_trump(first_card)
        second_card_is_trump = is_trump(second_card)

        if first_card_is_trump and not second_card_is_trump:
            return first_player
        elif not first_card_is_trump and second_card_is_trump:
            return second_player
        elif first_card_is_trump and second_card_is_trump:
            if card_value(first_card) > card_value(second_card):
                return first_player
            else:
                return second_player
        else:
            if first_card["suit"] == second_card["suit"]:
                if card_value(first_card) > card_value(second_card):
                    return first_player
                else:
                    return second_player
            else:
                return first_player  

    
    won_round_current = determine_winner(firstplayedcard, secondplayedcard, erster_spieler, zweiter_spieler)

    # auswahl in abhängigkeit wer der alleinspieler ist
    if gamemode_spieler == erster_spieler:
        chosen_card = choose_card_alleinspieler_erster(hand, rest_cards_in_game, firstplayedcard, gamemode, grand_trump_values, trump_suit, card_value(firstplayedcard) + card_value(secondplayedcard), won_round_current, gamemode_spieler)
    elif gamemode_spieler == zweiter_spieler:
        chosen_card = choose_card_zweiter_alleinspieler(hand, rest_cards_in_game, firstplayedcard, gamemode, grand_trump_values, trump_suit, card_value(firstplayedcard) + card_value(secondplayedcard), won_round_current, gamemode_spieler)
    else:
        chosen_card = choose_card_alleinspieler_dritter(hand, rest_cards_in_game, firstplayedcard, gamemode, grand_trump_values, trump_suit, card_value(firstplayedcard) + card_value(secondplayedcard), won_round_current, gamemode_spieler)

    return {"play_card": chosen_card}

def choose_card_alleinspieler_erster(hand, rest_cards_in_game, firstplayedcard, gamemode, cardvalues, trump_suit, value_in_pool, won_round_current, gamemode_spieler):
    def card_value(card):
        for skat_values in cardvalues:
            if skat_values["suit"] == card["suit"] and skat_values["value"] == card["value"]:
                return skat_values["rank"]
        return skat_values.get(card["value"], 0)

    def card_color(card):
        return card["suit"]

    def is_trump(card):
        return card["value"] == "jack" or card_color(card) == trump_suit

    first_suit = card_color(firstplayedcard)
    is_first_trump = is_trump(firstplayedcard)

    trump_cards = [card for card in hand if is_trump(card)]
    non_trump_cards = [card for card in hand if not is_trump(card)]
    suits = ["clubs", "spades", "hearts", "diamonds"]
    suit_cards = {suit: [card for card in non_trump_cards if card["suit"] == suit] for suit in suits}

    # Wenn der Wert im Pool mindestens 7 beträgt, wird eine offensivere Spielweise gewählt
    if value_in_pool >= 7:
        if is_first_trump:
            # Höhere Trumpfkarten als die zuerst gespielte Karte suchen
            higher_trump_cards = [card for card in trump_cards if card_value(card) > card_value(firstplayedcard)]
            if higher_trump_cards:
                return min(higher_trump_cards, key=card_value)
            if trump_cards:
                return min(trump_cards, key=card_value)
            else:
                return min(non_trump_cards, key=card_value)
        else:
            # Die zu spielende Karte hängt von der gespielten Farbe ab
            cards_to_play = suit_cards.get(first_suit, [])
            if cards_to_play:
                higher_suit_cards = [card for card in cards_to_play if card_value(card) > card_value(firstplayedcard)]
                if higher_suit_cards:
                    return max(higher_suit_cards, key=card_value)
                else:
                    return min(cards_to_play, key=card_value)

            if trump_cards:
                higher_trumps_trumps = [card for card in trump_cards if card["value"] in ["10", "ace"]]
                if higher_trumps_trumps:
                    return max(higher_trumps_trumps, key=card_value)
                else:
                    return min(trump_cards, key=card_value)

            if non_trump_cards:
                return min(non_trump_cards, key=card_value)
    else:
        # Wenn der Wert im Pool unter 7 liegt, wählt der Spieler eine vorsichtigere Spielweise
        if is_first_trump:
            higher_trump_cards = [card for card in trump_cards if card_value(card) > card_value(firstplayedcard)]
            lower_trump_cards = [card for card in trump_cards if card_value(card) < card_value(firstplayedcard)]
            lower_trump_cards_high_card_value = [card for card in lower_trump_cards if card_value(card) >= 10]

            if lower_trump_cards_high_card_value:
                return min(higher_trump_cards, key=card_value) if higher_trump_cards else min(lower_trump_cards, key=card_value)

            if lower_trump_cards:
                return min(lower_trump_cards, key=card_value)
            else:
                return min(non_trump_cards, key=card_value)
        else:
            cards_to_play = suit_cards.get(first_suit, [])
            if cards_to_play:
                higher_suit_cards = [card for card in cards_to_play if card_value(card) > card_value(firstplayedcard)]
                if higher_suit_cards:
                    return max(higher_suit_cards, key=card_value)
                else:
                    return min(cards_to_play, key=card_value)

            if trump_cards:
                higher_trumps_trumps = [card for card in trump_cards if card["value"] in ["10", "ace"]]
                if higher_trumps_trumps:
                    return max(higher_trumps_trumps, key=card_value)
                else:
                    return min(trump_cards, key=card_value)

            if non_trump_cards:
                return min(non_trump_cards, key=card_value)


def choose_card_zweiter_alleinspieler(hand, rest_cards_in_game, firstplayedcard, gamemode, cardvalues, trump_suit, value_in_pool, won_round_current, gamemode_spieler):
    def card_value(card):
        for skat_values in cardvalues:
            if skat_values["suit"] == card["suit"] and skat_values["value"] == card["value"]:
                return skat_values["rank"]
        return skat_values.get(card["value"], 0)

    def card_color(card):
        return card["suit"]

    def is_trump(card):
        return card["value"] == "jack" or card_color(card) == trump_suit

    first_suit = card_color(firstplayedcard)
    is_first_trump = is_trump(firstplayedcard)

    trump_cards = [card for card in hand if is_trump(card)]
    non_trump_cards = [card for card in hand if not is_trump(card)]
    suits = ["clubs", "spades", "hearts", "diamonds"]
    suit_cards = {suit: [card for card in non_trump_cards if card["suit"] == suit] for suit in suits}

    # Wertige Karten auswählen, wenn der Wert im Pool mindestens 7 beträgt
    if value_in_pool >= 7:
        if is_first_trump:
            higher_trump_cards = [card for card in trump_cards if card_value(card) > card_value(firstplayedcard)]
            if higher_trump_cards:
                return min(higher_trump_cards, key=card_value)
            if trump_cards:
                return min(trump_cards, key=card_value)
            else:
                return min(non_trump_cards, key=card_value)
        else:
            cards_to_play = suit_cards.get(first_suit, [])
            if cards_to_play:
                higher_suit_cards = [card for card in cards_to_play if card_value(card) > card_value(firstplayedcard)]
                if higher_suit_cards:
                    return max(higher_suit_cards, key=card_value)
                else:
                    return min(cards_to_play, key=card_value)
            
            if trump_cards:
                higher_trumps_trumps = [card for card in trump_cards if card["value"] in ["10", "ace"]]
                if higher_trumps_trumps:
                    return max(higher_trumps_trumps, key=card_value)
                else:
                    return min(trump_cards, key=card_value)

            if non_trump_cards:
                return min(non_trump_cards, key=card_value)
    else:
        if is_first_trump:
            higher_trump_cards = [card for card in trump_cards if card_value(card) > card_value(firstplayedcard)]
            lower_trump_cards = [card for card in trump_cards if card_value(card) < card_value(firstplayedcard)]
            lower_trump_cards_high_card_value = [card for card in lower_trump_cards if card_value(card) >= 10]

            if lower_trump_cards_high_card_value:
                return min(higher_trump_cards, key=card_value) if higher_trump_cards else min(lower_trump_cards, key=card_value)

            if lower_trump_cards:
                return min(lower_trump_cards, key=card_value)
            else:
                return min(non_trump_cards, key=card_value)
        else:
            cards_to_play = suit_cards.get(first_suit, [])
            if cards_to_play:
                higher_suit_cards = [card for card in cards_to_play if card_value(card) > card_value(firstplayedcard)]
                if higher_suit_cards:
                    return max(higher_suit_cards, key=card_value)
                else:
                    return min(cards_to_play, key=card_value)

            if trump_cards:
                higher_trumps_trumps = [card for card in trump_cards if card["value"] in ["10", "ace"]]
                if higher_trumps_trumps:
                    return max(higher_trumps_trumps, key=card_value)
                else:
                    return min(trump_cards, key=card_value)

            if non_trump_cards:
                return min(non_trump_cards, key=card_value)

def choose_card_alleinspieler_dritter(hand, rest_cards_in_game, firstplayedcard, gamemode, cardvalues, trump_suit, value_in_pool, won_round_current, gamemode_spieler):
    def card_value(card):
        for skat_values in cardvalues:
            if skat_values["suit"] == card["suit"] and skat_values["value"] == card["value"]:
                return skat_values["rank"]
        return skat_values.get(card["value"], 0)

    def card_color(card):
        return card["suit"]

    def is_trump(card):
        return card["value"] == "jack" or card_color(card) == trump_suit

    first_suit = card_color(firstplayedcard)
    is_first_trump = is_trump(firstplayedcard)

    trump_cards = [card for card in hand if is_trump(card)]
    non_trump_cards = [card for card in hand if not is_trump(card)]
    suits = ["clubs", "spades", "hearts", "diamonds"]
    suit_cards = {suit: [card for card in non_trump_cards if card["suit"] == suit] for suit in suits}

    # Wertige Karten auswählen, wenn der Wert im Pool mindestens 7 beträgt
    if value_in_pool >= 7:
        if is_first_trump:
            higher_trump_cards = [card for card in trump_cards if card_value(card) > card_value(firstplayedcard)]
            if higher_trump_cards:
                return min(higher_trump_cards, key=card_value)
            if trump_cards:
                return min(trump_cards, key=card_value)
            else:
                return min(non_trump_cards, key=card_value)
        else:
            cards_to_play = suit_cards.get(first_suit, [])
            if cards_to_play:
                higher_suit_cards = [card for card in cards_to_play if card_value(card) > card_value(firstplayedcard)]
                if higher_suit_cards:
                    return max(higher_suit_cards, key=card_value)
                else:
                    return min(cards_to_play, key=card_value)
            
            if trump_cards:
                higher_trumps_trumps = [card for card in trump_cards if card["value"] in ["10", "ace"]]
                if higher_trumps_trumps:
                    return max(higher_trumps_trumps, key=card_value)
                else:
                    return min(trump_cards, key=card_value)

            if non_trump_cards:
                return min(non_trump_cards, key=card_value)
    else:
        if is_first_trump:
            higher_trump_cards = [card for card in trump_cards if card_value(card) > card_value(firstplayedcard)]
            lower_trump_cards = [card for card in trump_cards if card_value(card) < card_value(firstplayedcard)]
            lower_trump_cards_high_card_value = [card for card in lower_trump_cards if card_value(card) >= 10]

            if lower_trump_cards_high_card_value:
                return min(higher_trump_cards, key=card_value) if higher_trump_cards else min(lower_trump_cards, key=card_value)

            if lower_trump_cards:
                return min(lower_trump_cards, key=card_value)
            else:
                return min(non_trump_cards, key=card_value)
        else:
            cards_to_play = suit_cards.get(first_suit, [])
            if cards_to_play:
                higher_suit_cards = [card for card in cards_to_play if card_value(card) > card_value(firstplayedcard)]
                if higher_suit_cards:
                    return max(higher_suit_cards, key=card_value)
                else:
                    return min(cards_to_play, key=card_value)

            if trump_cards:
                higher_trumps_trumps = [card for card in trump_cards if card["value"] in ["10", "ace"]]
                if higher_trumps_trumps:
                    return max(higher_trumps_trumps, key=card_value)
                else:
                    return min(trump_cards, key=card_value)

            if non_trump_cards:
                return min(non_trump_cards, key=card_value)







# Flask-API-Endpunkt, um den AI-Zug zu berechnen
data = {
  "open_round": {
    "order": ["player1", "player3", "player2"],
    "cards": {
      "player1": {"suit": "diamonds", "value": "queen"},
      "player3": {"suit": "hearts", "value": "jack"},
      "player2": ""
    }
  },
  "hand": [
    {"suit": "diamonds", "value": "queen"},
    {"suit": "hearts", "value": "ace"},
    {"suit": "spades", "value": "8"},
    {"suit": "hearts", "value": "6"}
  ],
  "check_card": {"suit": "hearts", "value": "jack"},
  "gamemode": {
    "name": "Grand",
    "active_player": "player3"
  },
  "history": {
    "rounds": [
      {
        "order": ["player2", "player1", "player3"],
        "cards": {
          "player1": {"suit": "hearts", "value": "queen"},
          "player2": {"suit": "hearts", "value": "8"},
          "player3": {"suit": "hearts", "value": "9"}
        },
        "winner": "player2",
        "score": 18
      },
      {
        "order": ["player1", "player3", "player2"],
        "cards": {
          "player1": {"suit": "spades", "value": "7"},
          "player2": {"suit": "spades", "value": "ace"},
          "player3": {"suit": "spades", "value": "jack"}
        },
        "winner": "player2",
        "score": 22
      }
    ],
    "betting_order": ["player1", "player3", "player2"]
  }
}
