from flask import Flask, jsonify, request
import json

app = Flask(__name__)

all_cards = []

def process_ai_move_hard_zweiter_Farbspiele(data):
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
    clubs_trump_values = [
    {"suit": "clubs", "value": "jack", "rank": 23},  # Jack (highest)
    {"suit": "spades", "value": "jack", "rank": 22},  # Jack of Spades (2nd highest)
    {"suit": "hearts", "value": "jack", "rank": 21},  # Jack of Hearts (3rd highest)
    {"suit": "diamonds", "value": "jack", "rank": 20},  # Jack of Diamonds (4th highest)
    {"suit": "clubs", "value": "ace", "rank": 11},
    {"suit": "clubs", "value": "10", "rank": 10},
    {"suit": "clubs", "value": "king", "rank": 4},
    {"suit": "clubs", "value": "queen", "rank": 3},
    {"suit": "clubs", "value": "9", "rank": 0},
    {"suit": "clubs", "value": "8", "rank": 0},
    {"suit": "clubs", "value": "7", "rank": 0},
    ]
    spades_trump_values = [
    {"suit": "clubs", "value": "jack", "rank": 23},  # Jack of Clubs (highest)
    {"suit": "spades", "value": "jack", "rank": 22},  # Jack (2nd highest)
    {"suit": "hearts", "value": "jack", "rank": 21},  # Jack of Hearts (3rd highest)
    {"suit": "diamonds", "value": "jack", "rank": 20},  # Jack of Diamonds (4th highest)
    {"suit": "spades", "value": "ace", "rank": 11},
    {"suit": "spades", "value": "10", "rank": 10},
    {"suit": "spades", "value": "king", "rank": 4},
    {"suit": "spades", "value": "queen", "rank": 3},
    {"suit": "spades", "value": "9", "rank": 0},
    {"suit": "spades", "value": "8", "rank": 0},
    {"suit": "spades", "value": "7", "rank": 0},
    ]
    hearts_trump_values = [
    {"suit": "clubs", "value": "jack", "rank": 23},  # Jack of Clubs (highest)
    {"suit": "spades", "value": "jack", "rank": 22},  # Jack of Spades (2nd highest)
    {"suit": "hearts", "value": "jack", "rank": 21},  # Jack (3rd highest)
    {"suit": "diamonds", "value": "jack", "rank": 20},  # Jack of Diamonds (4th highest)
    {"suit": "hearts", "value": "ace", "rank": 11},
    {"suit": "hearts", "value": "10", "rank": 10},
    {"suit": "hearts", "value": "king", "rank": 4},
    {"suit": "hearts", "value": "queen", "rank": 3},
    {"suit": "hearts", "value": "9", "rank": 0},
    {"suit": "hearts", "value": "8", "rank": 0},
    {"suit": "hearts", "value": "7", "rank": 0},
    ]
    diamonds_trump_values = [
    {"suit": "clubs", "value": "jack", "rank": 23},  # Jack of Clubs (highest)
    {"suit": "spades", "value": "jack", "rank": 22},  # Jack of Spades (2nd highest)
    {"suit": "hearts", "value": "jack", "rank": 21},  # Jack of Hearts (3rd highest)
    {"suit": "diamonds", "value": "jack", "rank": 20},  # Jack (4th highest)
    {"suit": "diamonds", "value": "ace", "rank": 11},
    {"suit": "diamonds", "value": "10", "rank": 10},
    {"suit": "diamonds", "value": "king", "rank": 4},
    {"suit": "diamonds", "value": "queen", "rank": 3},
    {"suit": "diamonds", "value": "9", "rank": 0},
    {"suit": "diamonds", "value": "8", "rank": 0},
    {"suit": "diamonds", "value": "7", "rank": 0},
    ]
    grand_trump_values = [
    {"suit": "clubs", "value": "jack", "rank": 23},  # Jack of Clubs (highest)
    {"suit": "spades", "value": "jack", "rank": 22},  # Jack of Spades (2nd highest)
    {"suit": "hearts", "value": "jack", "rank": 21},  # Jack of Hearts (3rd highest)
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
    deck = [card for card in deck if card not in hand]
    rest_cards_in_game = []
    for round_data in history["rounds"]:
        rest_cards_in_game.extend(round_data["cards"].values())
    deck = [card for card in deck if card not in rest_cards_in_game]
    if gamemode == "Grand":
        trump_suit = "jack"
    if gamemode == "Kreuz":
        trump_suit = "clubs"
    elif gamemode == "Pik":
        trump_suit = "spades"
    elif gamemode == "Herz":
        trump_suit = "hearts"
    elif gamemode == "Karo":
        trump_suit = "diamonds"
    
    if trump_suit == "jack":
        cardvalues = grand_trump_values
    if trump_suit == "clubs":
        cardvalues = clubs_trump_values
    elif trump_suit == "spades":
        cardvalues = spades_trump_values
    elif trump_suit == "hearts":
        cardvalues = hearts_trump_values
    elif trump_suit == "diamonds":
        cardvalues = diamonds_trump_values


    if (gamemode_spieler == erster_spieler):
        chosen_card = choose_card_zweiter_alleinspieler_erster(hand, rest_cards_in_game, firstplayedcard, gamemode,cardvalues,trump_suit)
    elif(gamemode_spieler == zweiter_spieler):
        chosen_card = choose_card_zweiter_alleinspieler_zweiter(hand, rest_cards_in_game, firstplayedcard, gamemode,cardvalues,trump_suit)
    else:
        chosen_card = choose_card_zweiter_alleinspieler_dritter(hand, rest_cards_in_game, firstplayedcard, gamemode,cardvalues,trump_suit)

    return {"play_card": chosen_card}

def choose_card_zweiter_alleinspieler_erster(hand, rest_cards_in_game, firstplayedcard, gamemode,cardvalues,trump_suit):
    skat_values = cardvalues
    skat_values_nichttrumpf = {"ace": 11, "10": 10, "king": 4, "queen": 3, "jack": 2, "9": 0, "8": 0, "7": 0}
    
    
    def card_value(card):
        # Zusätzliche Bewertung für Jacks nach ihrer Rangfolge
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
    clubs_cards = [card for card in non_trump_cards if card["suit"] == "clubs"]
    spades_cards = [card for card in non_trump_cards if card["suit"] == "spades"]
    hearts_cards = [card for card in non_trump_cards if card["suit"] == "hearts"]
    diamonds_cards = [card for card in non_trump_cards if card["suit"] == "diamonds"]



    if is_first_trump:
        #trumpf ausgespielt values 7-9
        if firstplayedcard["value"] in ["8", "9", "7"]:
            higher_trumps = [card for card in trump_cards if card["value"] in ["10", "ace"]]
            #versucht mit 10 oder ace abzustechen
            if higher_trumps:
                return max(higher_trumps, key=card_value)
            else:
            #wenn nicht möglich mit krate die höher minimal ist abstechen    
                higher_suit_cards = [card for card in trump_cards if card_value(card) > card_value(firstplayedcard)]
                return min(higher_suit_cards,key=card_value)
        #trümfe die höher sind heraussuchen
        higher_trump_cards = [card for card in trump_cards if card_value(card) > card_value(firstplayedcard)]
    
        if higher_trump_cards:
            #minimal höher heraussuchen
            return min(higher_trump_cards, key=card_value)
        if trump_cards:  
            return min(trump_cards,key= card_value)
            #möglcihst wenig punkte rein spielen da kein trumpf  
        else:
            return min(non_trump_cards, key=card_value) 

    # erster spieler spielt keinen trumpf an
    else:
        if (first_suit=="clubs"):
            cards_to_play = clubs_cards 
        if (first_suit=="spades"):
            cards_to_play = spades_cards 
        if (first_suit=="hearts"):
            cards_to_play = hearts_cards 
        if (first_suit=="diamonds"):
            cards_to_play = diamonds_cards
        #hat farbe und muss diese spielen
        if cards_to_play:
            if firstplayedcard["value"] in ["8", "9", "7"]:
                higher_trumps = [card for card in cards_to_play if card["value"] in ["10", "ace"]]
            #versucht mit 10 oder ace abzustechen
            if higher_trumps:
                return max(higher_trumps, key=card_value)
            else:
            #wenn nicht möglich mit krate die höher minimal ist abstechen    
                higher_suit_cards = [card for card in cards_to_play if card_value(card) > card_value(firstplayedcard)]
                if higher_suit_cards:
                    return min(higher_suit_cards,key=card_value)
                #keine höhere minimal allgemein abstechen
                else:
                    return min(cards_to_play,key=card_value)
        #hat die farbe nicht kann abstechen
        if trump_cards:
            higher_trumps_trumps = [card for card in trump_cards if card["value"] in ["10", "ace"]]
            if higher_trumps_trumps:
                return max(higher_trumps_trumps, key=card_value)
            else:
                return min(trump_cards,key=card_value)
        #hat farbe nicht und kann nicht abstechen
        if non_trump_cards:
            return min(non_trump_cards, key=card_value) 

def choose_card_zweiter_alleinspieler_zweiter(hand, rest_cards_in_game, firstplayedcard, gamemode,cardvalues,trump_suit):
    skat_values = cardvalues
    skat_values_nichttrumpf = {"ace": 11, "10": 10, "king": 4, "queen": 3, "jack": 2, "9": 0, "8": 0, "7": 0}
    
    
    def card_value(card):
        # Zusätzliche Bewertung für Jacks nach ihrer Rangfolge
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
    clubs_cards = [card for card in non_trump_cards if card["suit"] == "clubs"]
    spades_cards = [card for card in non_trump_cards if card["suit"] == "spades"]
    hearts_cards = [card for card in non_trump_cards if card["suit"] == "hearts"]
    diamonds_cards = [card for card in non_trump_cards if card["suit"] == "diamonds"]
    rest_cards_in_game

    if is_first_trump:
        #trumpf ausgespielt values 10,ace
        if firstplayedcard["value"] in ["10", "ace"]:
            #hat nicht höchsten trumpf
            if max(rest_cards_in_game, key=card_value)>max(trump_cards, key=card_value):
                return min(trump_cards, key=card_value)
            else:
                max(trump_cards, key=card_value)
        #trümfe die höher sind heraussuchen
        higher_trump_cards = [card for card in trump_cards if card_value(card) > card_value(firstplayedcard)]    
        if higher_trump_cards:
            if max(rest_cards_in_game, key= card_value)>max (higher_trump_cards,key=card_value):
                return min(trump_cards, key=card_value)
            else :
                return max(higher_trump_cards,key=card_value)
        if trump_cards:  
            min(trump_cards,key= card_value)
            #möglcihst wenig punkte rein spielen da kein trumpf  
        else:
            min(non_trump_cards, key=card_value) 

    # erster spieler spielt keinen trumpf an
    else:
        if (first_suit=="clubs"):
            cards_to_play = clubs_cards 
        if (first_suit=="spades"):
            cards_to_play = spades_cards 
        if (first_suit=="hearts"):
            cards_to_play = hearts_cards 
        if (first_suit=="diamonds"):
            cards_to_play = diamonds_cards
        #hat farbe und muss diese spielen
        if cards_to_play:
            if firstplayedcard["value"] in ["10", "ace"]:
                higher_suit_cards = [card for card in cards_to_play if card_value(card) > card_value(firstplayedcard)]
                if higher_suit_cards:
                    return max(higher_suit_cards, key=card_value)
            else:
            #wenn nicht möglich mit krate die höher minimal ist abstechen    
                higher_suit_cards = [card for card in cards_to_play if card_value(card) > card_value(firstplayedcard)]
                if higher_suit_cards:
                    return min(higher_suit_cards,key=card_value)
                #keine höhere minimal allgemein abstechen
                else:
                    return min(cards_to_play,key=card_value)
        #hat die farbe nicht kann abstechen
        if trump_cards:
            higher_trumps_trumps = [card for card in trump_cards if card["value"] in ["10", "ace"]]
            if higher_trumps_trumps:
                return max(higher_trumps_trumps, key=card_value)
            else:
                return min(trump_cards,key=card_value)
        #hat farbe nicht und kann nicht abstechen
        if non_trump_cards:
            return min(non_trump_cards, key=card_value)

def choose_card_zweiter_alleinspieler_dritter(hand, rest_cards_in_game, firstplayedcard, gamemode,cardvalues,trump_suit):
    skat_values = cardvalues
    skat_values_nichttrumpf = {"ace": 11, "10": 10, "king": 4, "queen": 3, "jack": 2, "9": 0, "8": 0, "7": 0}
    
    def card_value(card):
        # Zusätzliche Bewertung für Jacks nach ihrer Rangfolge
        for skat_values in cardvalues:
            if skat_values["suit"] == card["suit"] and skat_values["value"] == card["value"]:
                return skat_values["rank"]
        return skat_values.get(card["value"], 0)
    
    def card_value_value(card):
        # Zusätzliche Bewertung für Jacks nach ihrer Rangfolge
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
    clubs_cards = [card for card in non_trump_cards if card["suit"] == "clubs"]
    spades_cards = [card for card in non_trump_cards if card["suit"] == "spades"]
    hearts_cards = [card for card in non_trump_cards if card["suit"] == "hearts"]
    diamonds_cards = [card for card in non_trump_cards if card["suit"] == "diamonds"]
    rest_cards_in_game

    if is_first_trump:
        if card_value(firstplayedcard)>max(rest_cards_in_game, key= card_value):
                return max(trump_cards,key=card_value_value)
        if firstplayedcard["value"] in ["10", "ace"]:
            #hat nicht höchsten trumpf
            if max(rest_cards_in_game, key=card_value)>max(trump_cards, key=card_value):
                return min(trump_cards, key=card_value)
            else:
                max(trump_cards, key=card_value)
        #trümfe die höher sind heraussuchen
        higher_trump_cards = [card for card in trump_cards if card_value(card) > card_value(firstplayedcard)]    
        if higher_trump_cards:
            if max(rest_cards_in_game, key= card_value)>max(higher_trump_cards,key=card_value):
                return min(trump_cards, key=card_value)
            else :
                return max(higher_trump_cards,key=card_value)
        if trump_cards:  
            min(trump_cards,key= card_value)
            #möglcihst wenig punkte rein spielen da kein trumpf  
        else:
            min(non_trump_cards, key=card_value) 

    # erster spieler spielt keinen trumpf an
    else:
        if (first_suit=="clubs"):
            cards_to_play = clubs_cards 
        if (first_suit=="spades"):
            cards_to_play = spades_cards 
        if (first_suit=="hearts"):
            cards_to_play = hearts_cards 
        if (first_suit=="diamonds"):
            cards_to_play = diamonds_cards
        #hat farbe und muss diese spielen
        if cards_to_play:
            if firstplayedcard["value"] in ["10", "ace"]:
                higher_suit_cards = [card for card in cards_to_play if card_value(card) > card_value(firstplayedcard)]
            if higher_suit_cards:
                return max(higher_suit_cards, key=card_value)
            else:
            #wenn nicht möglich mit krate die höher minimal ist abstechen    
                higher_suit_cards = [card for card in cards_to_play if card_value(card) > card_value(firstplayedcard)]
                if higher_suit_cards:
                    return min(higher_suit_cards,key=card_value)
                #keine höhere minimal allgemein abstechen
                else:
                    return min(cards_to_play,key=card_value)
        #hat die farbe nicht kann abstechen
        if trump_cards:
            higher_trumps_trumps = [card for card in trump_cards if card["value"] in ["10", "ace"]]
            if higher_trumps_trumps:
                return max(higher_trumps_trumps, key=card_value)
            else:
                return min(trump_cards,key=card_value)
        #hat farbe nicht und kann nicht abstechen
        if non_trump_cards:
            return min(non_trump_cards, key=card_value)        

data = {
  "open_round": {
    "order": ["player1", "player3", "player2"],
    "cards": {
      "player1": {"suit": "diamonds", "value": "queen"},
      "player3": "",
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
    "name": "Herz",
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
print(process_ai_move_hard_zweiter_Farbspiele(data))