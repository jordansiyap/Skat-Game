from flask import Flask, jsonify, request
import json

app = Flask(__name__)

all_cards = []

def process_ai_move_hard_zweiter_Grand(data):
    global all_cards
    all_cards.clear()
    data = data
    benötigte_felder = ["open_round", "hand", "gamemode"]
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
    all_ülayed_cards = open_round.get("cards")
    firstplayedcard = all_ülayed_cards[erster_spieler]

    gamemode = gamemode.get("name")
    grand_trump_values = [
        {"suit": "clubs", "value": "jack", "rank": 23},
        {"suit": "spades", "value": "jack", "rank": 22},
        {"suit": "hearts", "value": "jack", "rank": 21},
        {"suit": "diamonds", "value": "jack", "rank": 20},
    ]
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
    deck = [card for card in deck if card not in hand]
    rest_cards_in_game = []
    for round_data in history["rounds"]:
        rest_cards_in_game.extend(round_data["cards"].values())
    deck = [card for card in deck if card not in rest_cards_in_game]
    
    if gamemode == "Grand":
        trump_suit = "jack"
        cardvalues = grand_trump_values
    skat_values_nichttrumpf = {"ace": 11, "10": 10, "king": 4, "queen": 3, "jack": 2, "9": 0, "8": 0, "7": 0}

    def card_value(card):
        return skat_values_nichttrumpf.get(card["value"], 0)

    value_in_pool = card_value(firstplayedcard)

    # Wenn der erste Spieler den Solo-Zug macht und der zweite Spieler dran ist
    if gamemode_spieler == erster_spieler:
        chosen_card = choose_card_zweiter_alleinspieler_erster(hand, rest_cards_in_game, firstplayedcard, gamemode, cardvalues, trump_suit, value_in_pool)
    elif gamemode_spieler == zweiter_spieler:
        chosen_card = choose_card_zweiter_alleinspieler_zweiter(hand, rest_cards_in_game, firstplayedcard, gamemode, cardvalues, trump_suit, value_in_pool)
    else:
        chosen_card = choose_card_zweiter_alleinspieler_dritter(hand, rest_cards_in_game, firstplayedcard, gamemode, cardvalues, trump_suit, value_in_pool)

    return {"play_card": chosen_card}


def choose_card_zweiter_alleinspieler_erster(hand, rest_cards_in_game, firstplayedcard, gamemode, cardvalues, trump_suit, value_in_pool):
    skat_values = cardvalues
    skat_values_nichttrumpf = {"ace": 11, "10": 10, "king": 4, "queen": 3, "jack": 2, "9": 0, "8": 0, "7": 0}

    def card_value_nicht_trumpf(card):
        for skat_value in skat_values_nichttrumpf:
            if skat_value["suit"] == card["suit"] and skat_value["value"] == card["value"]:
                return skat_value["rank"]
        return skat_values_nichttrumpf.get(card["value"], 0)

    def card_value(card):
        for skat_value in cardvalues:
            if skat_value["suit"] == card["suit"] and skat_value["value"] == card["value"]:
                return skat_value["rank"]
        return skat_values_nichttrumpf.get(card["value"], 0)

    def card_color(card):
        return card["suit"]

    def is_trump(card):
        return card["value"] == "jack"

    first_suit = card_color(firstplayedcard)
    is_first_trump = is_trump(firstplayedcard)

    trump_cards = [card for card in hand if is_trump(card)]
    non_trump_cards = [card for card in hand if not is_trump(card)]
    clubs_cards = [card for card in non_trump_cards if card["suit"] == "clubs"]
    spades_cards = [card for card in non_trump_cards if card["suit"] == "spades"]
    hearts_cards = [card for card in non_trump_cards if card["suit"] == "hearts"]
    diamonds_cards = [card for card in non_trump_cards if card["suit"] == "diamonds"]

    if is_first_trump:
        higher_trump_cards = [card for card in trump_cards if card_value(card) > card_value(firstplayedcard)]

        if higher_trump_cards:
            return min(higher_trump_cards, key=card_value)
        if trump_cards:
            return min(trump_cards, key=card_value)
        else:
            return min(non_trump_cards, key=card_value)
    else:
        if first_suit == "clubs":
            cards_to_play = clubs_cards
        elif first_suit == "spades":
            cards_to_play = spades_cards
        elif first_suit == "hearts":
            cards_to_play = hearts_cards
        elif first_suit == "diamonds":
            cards_to_play = diamonds_cards

        if cards_to_play:
            higher_trumps = [card for card in cards_to_play if card["value"] in ["10", "ace"]]
            if higher_trumps:
                return max(higher_trumps, key=card_value)
            else:
                higher_suit_cards = [card for card in cards_to_play if card_value(card) > card_value(firstplayedcard)]
                if higher_suit_cards:
                    return min(higher_suit_cards, key=card_value)
                else:
                    return min(cards_to_play, key=card_value)

        if trump_cards:
            if value_in_pool >= 10:
                higher_trumps_trumps = [card for card in trump_cards if card["value"] in ["10", "ace"]]
                if higher_trumps_trumps:
                    return max(higher_trumps_trumps, key=card_value)
                else:
                    return min(trump_cards, key=card_value)

        if non_trump_cards:
            return min(non_trump_cards, key=card_value)
        else:
            return min(trump_cards, key=card_value)

def choose_card_zweiter_alleinspieler_zweiter(hand, rest_cards_in_game, firstplayedcard, gamemode, cardvalues, trump_suit, value_in_pool):
    # Definiert die Bewertungswerte der Karten
    skat_values = cardvalues
    skat_values_nichttrumpf = {"ace": 11, "10": 10, "king": 4, "queen": 3, "jack": 2, "9": 0, "8": 0, "7": 0}

    # Bewertungsfunktion für Kartenwerte
    def card_value(card):
        for skat_value in skat_values:
            if skat_value["suit"] == card["suit"] and skat_value["value"] == card["value"]:
                return skat_value["rank"]
        return skat_values_nichttrumpf.get(card["value"], 0)

    # Funktion zur Bestimmung der Farbe der Karte
    def card_color(card):
        return card["suit"]

    # Funktion zur Bestimmung, ob eine Karte ein Trumpf ist
    def is_trump(card):
        return card["value"] == "jack"

    # Bestimmung der Farbe der ersten gespielten Karte
    first_suit = card_color(firstplayedcard)
    is_first_trump = is_trump(firstplayedcard)

    # Karten nach Trumpf und Nicht-Trumpf filtern
    trump_cards = [card for card in hand if is_trump(card)]
    non_trump_cards = [card for card in hand if not is_trump(card)]

    # Karten nach den Farben (suits) aufteilen
    clubs_cards = [card for card in non_trump_cards if card["suit"] == "clubs"]
    spades_cards = [card for card in non_trump_cards if card["suit"] == "spades"]
    hearts_cards = [card for card in non_trump_cards if card["suit"] == "hearts"]
    diamonds_cards = [card for card in non_trump_cards if card["suit"] == "diamonds"]

    # Wenn die erste gespielte Karte ein Trumpf ist
    if is_first_trump:
        # Alle Trumpfkarten, die die erste gespielte Karte schlagen
        higher_trump_cards = [card for card in trump_cards if card_value(card) > card_value(firstplayedcard)]
        
        # Wenn es Karten gibt, die höher sind als die gespielte Karte und diese Karten im Spielpool sind
        if higher_trump_cards:
            max_rest_card = max(rest_cards_in_game, key=card_value)
            max_higher_trump_card = max(higher_trump_cards, key=card_value)

            if card_value(max_rest_card) > card_value(max_higher_trump_card):
                return min(trump_cards, key=card_value)  # Möglichst niedrige Trumpfkarte spielen
            else:
                return max(higher_trump_cards, key=card_value)  # Höchste Trumpfkarte spielen

        # Wenn keine höheren Trumpfkarten vorhanden sind, aber Trumpfkarten existieren
        if trump_cards:
            return min(trump_cards, key=card_value)  # Niedrigste Trumpfkarte spielen

        # Ansonsten mit einer niedrigen Nicht-Trumpfkarte spielen
        return min(non_trump_cards, key=card_value) 

    # Wenn die erste gespielte Karte kein Trumpf ist
    else:
        # Bestimme, welche Farbe (suit) der erste Spieler gespielt hat
        if first_suit == "clubs":
            cards_to_play = clubs_cards
        elif first_suit == "spades":
            cards_to_play = spades_cards
        elif first_suit == "hearts":
            cards_to_play = hearts_cards
        else:
            cards_to_play = diamonds_cards
        
        # Wenn der Spieler Karten der gleichen Farbe hat und die Farbe bedient werden muss
        if cards_to_play:
            # Wenn der Spieler die Karte 10 oder ein Ass spielt, versuche eine höhere Karte zu spielen
            if firstplayedcard["value"] in ["10", "ace"]:
                higher_suit_cards = [card for card in cards_to_play if card_value(card) > card_value(firstplayedcard)]
                if higher_suit_cards:
                    return max(higher_suit_cards, key=card_value)
            else:
                # Wenn keine höhere Karte vorhanden ist, mit der höchsten Karte der gleichen Farbe abstechen
                higher_suit_cards = [card for card in cards_to_play if card_value(card) > card_value(firstplayedcard)]
                if higher_suit_cards:
                    return min(higher_suit_cards, key=card_value)
                else:
                    return min(cards_to_play, key=card_value)  # Keine höhere Karte, niedrigste Karte spielen

        # Wenn der Spieler die Farbe nicht hat, kann er abstechen
        if trump_cards:
            # Wenn ein hoher Wert (10 oder Ass) im Pool ist, steche ab
            if value_in_pool >= 10:
                higher_trumps_trumps = [card for card in trump_cards if card["value"] in ["10", "ace"]]
                if higher_trumps_trumps:
                    return max(higher_trumps_trumps, key=card_value)
                else:
                    return min(trump_cards, key=card_value)

        # Wenn der Spieler die Farbe nicht hat und keine Trumpfkarte spielt, spiele die niedrigste Nicht-Trumpfkarte
        if non_trump_cards:
            return min(non_trump_cards, key=card_value)
        else:
            return min(trump_cards, key=card_value)

def choose_card_zweiter_alleinspieler_dritter(hand, rest_cards_in_game, firstplayedcard, gamemode, cardvalues, trump_suit, value_in_pool):
    # Definiert die Bewertungswerte der Karten
    skat_values = cardvalues
    skat_values_nichttrumpf = {"ace": 11, "10": 10, "king": 4, "queen": 3, "jack": 2, "9": 0, "8": 0, "7": 0}

    # Bewertungsfunktion für Nicht-Trumpf-Karten
    def card_value_nicht_trumpf(card):
        for skat_value in skat_values_nichttrumpf:
            if skat_value["suit"] == card["suit"] and skat_value["value"] == card["value"]:
                return skat_value["rank"]
        return skat_values_nichttrumpf.get(card["value"], 0)

    # Bewertungsfunktion für alle Karten
    def card_value(card):
        for skat_value in cardvalues:
            if skat_value["suit"] == card["suit"] and skat_value["value"] == card["value"]:
                return skat_value["rank"]
        return skat_values.get(card["value"], 0)

    # Funktion zur Bestimmung der Farbe der Karte
    def card_color(card):
        return card["suit"]

    # Funktion zur Bestimmung, ob eine Karte ein Trumpf ist
    def is_trump(card):
        return card["value"] == "jack"

    # Bestimmung der Farbe der ersten gespielten Karte
    first_suit = card_color(firstplayedcard)
    is_first_trump = is_trump(firstplayedcard)

    # Karten nach Trumpf und Nicht-Trumpf filtern
    trump_cards = [card for card in hand if is_trump(card)]
    non_trump_cards = [card for card in hand if not is_trump(card)]

    # Karten nach den Farben (suits) aufteilen
    clubs_cards = [card for card in non_trump_cards if card["suit"] == "clubs"]
    spades_cards = [card for card in non_trump_cards if card["suit"] == "spades"]
    hearts_cards = [card for card in non_trump_cards if card["suit"] == "hearts"]
    diamonds_cards = [card for card in non_trump_cards if card["suit"] == "diamonds"]

    # Wenn die erste gespielte Karte ein Trumpf ist
    if is_first_trump:
        # Alle Trumpfkarten, die die erste gespielte Karte schlagen
        higher_trump_cards = [card for card in trump_cards if card_value(card) > card_value(firstplayedcard)]

        # Wenn es Karten gibt, die höher sind als die gespielte Karte, spiele die niedrigste dieser Karten
        if higher_trump_cards:
            return min(higher_trump_cards, key=card_value)

        # Wenn keine höheren Trumpfkarten vorhanden sind, aber Trumpfkarten existieren
        if trump_cards:
            return min(trump_cards, key=card_value)  # Möglichst niedrige Trumpfkarte spielen

        # Ansonsten mit einer niedrigen Nicht-Trumpfkarte spielen
        return min(non_trump_cards, key=card_value)

    # Wenn die erste gespielte Karte kein Trumpf ist
    else:
        # Bestimme, welche Farbe (suit) der erste Spieler gespielt hat
        if first_suit == "clubs":
            cards_to_play = clubs_cards
        elif first_suit == "spades":
            cards_to_play = spades_cards
        elif first_suit == "hearts":
            cards_to_play = hearts_cards
        else:
            cards_to_play = diamonds_cards

        # Wenn der Spieler Karten der gleichen Farbe hat und die Farbe bedient werden muss
        if cards_to_play:
            # Wenn der erste Spieler eine 8, 9 oder 7 spielt, versuche mit einer hohen Karte (10 oder Ass) abzustechen
            if firstplayedcard["value"] in ["8", "9", "7"]:
                higher_trumps = [card for card in cards_to_play if card["value"] in ["10", "ace"]]
                if higher_trumps:
                    return max(higher_trumps, key=card_value)

            # Andernfalls versuche, mit einer höheren Karte der gleichen Farbe abzustechen
            higher_suit_cards = [card for card in cards_to_play if card_value(card) > card_value(firstplayedcard)]
            if higher_suit_cards:
                return min(higher_suit_cards, key=card_value)

            # Wenn keine höhere Karte vorhanden ist, spiele die niedrigste Karte der gleichen Farbe
            else:
                return min(cards_to_play, key=card_value)

        # Wenn der Spieler die Farbe nicht hat, kann er abstechen
        if trump_cards:
            # Wenn ein hoher Wert (10 oder Ass) im Pool ist, steche ab
            if value_in_pool >= 10:
                higher_trumps_trumps = [card for card in trump_cards if card["value"] in ["10", "ace"]]
                if higher_trumps_trumps:
                    return max(higher_trumps_trumps, key=card_value)
                else:
                    return min(trump_cards, key=card_value)

        # Wenn der Spieler die Farbe nicht hat und keine Trumpfkarte spielen kann, spiele die niedrigste Nicht-Trumpfkarte
        if non_trump_cards:
            return min(non_trump_cards, key=card_value)

        # Wenn keine Nicht-Trumpfkarten vorhanden sind, spiele eine Trumpfkarte
        else:
            return min(trump_cards, key=card_value)




data = {
  "open_round": {
    "order": ["player1", "player2", "player3"],
    "cards": {
      "player1": {"suit": "diamonds", "value": "jack"},
      "player2": "",
      "player3": ""
    }
  },
  "hand": [
    {"suit": "hearts", "value": "ace"},
    {"suit": "spades", "value": "jack"},
    {"suit": "hearts", "value": "6"}
  ],
  "check_card": {"suit": "hearts", "value": "jack"},
  "gamemode": {
    "name": "Grand",
    "active_player": "player2"
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
        "winner": "player3",
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

