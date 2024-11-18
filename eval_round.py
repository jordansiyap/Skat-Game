from flask import Flask, jsonify, abort
from flask import request


## actual code starts on line 150, currently missing nullspiel as unclear how to assign points etc

##table of card values
point_table = {"ace": 11,
               "10": 10,
               "king": 4,
               "queen": 3,
               "jack": 2}

##game type specific card orders
kreuz_order =[{"suit": "clubs", "value": "jack"},
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
pik_order =[{"suit": "clubs", "value": "jack"},
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

herz_order =[{"suit": "clubs", "value": "jack"},
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

karo_order =[{"suit": "clubs", "value": "jack"},
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


def find_best(cards, card_order, order, points_table, grand):
    played_cards = list(cards.values())
    players = list(cards.keys())
    current_best = None
    best_card = None
    winner = None
    points = 0

    ##determines suit of first played card to make sure only this and trump suit are counted toward winning the hand
    suit = played_cards[0]["suit"]

    ##if game is grand there are no trump cards outside the jacks so only the suit of first played card is counted as well as jacks
    if not grand:
        trump = card_order[5]["suit"]
    else:
        trump = suit

    ##determine card with the highest rank
    ##if card isnt the right suit/trump it gets ignored otherwise look up the corresponding value and return that
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

    ##determine winner
    for i in range(len(played_cards)):
        if best_card == played_cards[i]:
            winner = players[i]

    ##determine point value
    for card in played_cards:
        value = card["value"]
        points += points_table.get(value, 0)

    ##return closed round
    return {"order": order, "cards": cards, "winner":winner, "score": points}

@app.route('/eval_round', methods=['POST'])
def eval_round_route():
    data = request.get_json()

    if not data or 'gamemode' not in data or 'round' not in data:
        abort(400, description="gamemode or round missing")

    gamemode = data.get('gamemode')
    round_data = data.get('round')

    if not gamemode or 'name' not in gamemode:
        abort(400, description="gamemode does not contain name")

    if not round_data or 'order' not in round_data or 'cards' not in round_data:
        abort(400, description="round does not contain order or cards")

    gamemode_name = gamemode.get('name')
    order = round_data.get('order')
    cards = round_data.get('cards')

    valid_gamemodes = ["Kreuz", "Pik", "Herz", "Karo", "Grand"]
    if gamemode_name not in valid_gamemodes:
        abort(400, description="invalid gamemode")

    grand = False
    correct_order = None
    if gamemode_name == "Kreuz":
        correct_order = kreuz_order
    elif gamemode_name == "Pik":
        correct_order = pik_order
    elif gamemode_name == "Herz":
        correct_order = herz_order
    elif gamemode_name == "Karo":
        correct_order = karo_order
    elif gamemode_name == "Grand":
        correct_order = kreuz_order
        grand = True


    return jsonify(find_best(cards,correct_order,order,point_table,grand))