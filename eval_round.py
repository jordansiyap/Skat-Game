class eval_round:

    def __init__(self):
        ##table of card values
        self.point_table = {"ace": 11,
                   "10": 10,
                   "king": 4,
                   "queen": 3,
                   "jack": 2}
        self.kreuz_order = [{"suit": "clubs", "value": "jack"},
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
        self. pik_order = [{"suit": "clubs", "value": "jack"},
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
        self.herz_order = [{"suit": "clubs", "value": "jack"},
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
        self.karo_order = [{"suit": "clubs", "value": "jack"},
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
        self.null_order = [{"suit": "clubs", "value": "ace"},
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


    def eval_round(self,cards, gamemode_name, order):

        grand = False
        nullspiel = False
        card_order = None
        if gamemode_name == "Kreuz":
            card_order = self.kreuz_order
        elif gamemode_name == "Pik":
            card_order = self.pik_order
        elif gamemode_name == "Herz":
            card_order = self.herz_order
        elif gamemode_name == "Karo":
            card_order = self.karo_order
        elif gamemode_name == "Nullspiel":
            card_order = self.null_order
            nullspiel = True
        elif gamemode_name == "Grand":
            card_order = self.kreuz_order
            grand = True
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

        ##determine winner
        for i in range(len(played_cards)):
            if best_card == played_cards[i]:
                winner = players[i]

        ##determine point value
        ##if not nullspiel normal calculation
        ##if nullspiel if winner is player 0 he loses so -1 points
        ##if nullspiel and winner is not player 0 normal calculation
        if not nullspiel:
            for card in played_cards:
                value = card["value"]
                points += self.point_table.get(value, 0)
        else:
            if winner != players[0]:
                for card in played_cards:
                    value = card["value"]
                    points += self.point_table.get(value, 0)
            else:
                points = -1

        ##return closed round
        closed_round ={"order": order, "cards": cards, "winner": winner, "score": points}
        return {"round": closed_round}