
##method to be called when ai difficulty is hard and gamemode is nullspiel

class MakeAiMoveHardNullspiel:
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

##determines player considered declarer
    @staticmethod
    def is_declarer(gamemode_active_player, order, cards):
        players = order
        player_id = len(cards)
        player = order[player_id]
        if player == gamemode_active_player:
            return True
        else:
            return False
##determines if player is first to play
    @staticmethod
    def first_to_play(cards):
        if len(cards) == 0:
            return True
        else:
            return False
##determines if player plays before active player
    @staticmethod
    def plays_before_declarer(gamemode_active_player, order, cards, is_first, is_declarer):
        if is_first or is_declarer:
            return True

        order_id = len(cards)
        delcarer_id = None
        for i in range(len(order)):
            if order[i] == gamemode_active_player:
                delcarer_id = i
        if delcarer_id >= order_id:
            return True
        else:
            return False

    ##determine largest card in hand that has correct suit
    @staticmethod
    def largest_card(suit, hand):
        largest_index = 1000
        largest_card = None
        for card in hand:
            if card["suit"] == suit:
                if card in MakeAiMoveHardNullspiel.null_order and largest_index > MakeAiMoveHardNullspiel.null_order.index(card):
                    largest_card = card
                    largest_index = MakeAiMoveHardNullspiel.null_order.index(card)
        return largest_card

    ##determine smallest card in hand that has correct suit
    @staticmethod
    def smallest_card( suit, hand):
        smallest_index = -1
        smallest_card = None
        for card in hand:
            if card["suit"] == suit:
                if card in MakeAiMoveHardNullspiel.null_order and smallest_index < MakeAiMoveHardNullspiel.null_order.index(card):
                    smallest_card = card
                    smallest_index = MakeAiMoveHardNullspiel.null_order.index(card)
        return smallest_card

    @staticmethod
    def make_ai_move_hard_nullspiel(cards, card_order, is_declarer_result, is_first, before_declarer, hand,
                                    main_player):
        suit_counts = {
            "hearts": 0,
            "spades": 0,
            "diamonds": 0,
            "clubs": 0
        }

        if is_first:
            if is_declarer_result:
                ##case 1 ai is declarer and goes first
                for card in hand:
                    suit_counts[card["suit"]] += 1

                largest_suit = max(suit_counts, key=suit_counts.get)
                return MakeAiMoveHardNullspiel.smallest_card(largest_suit, hand)
            else:
                ##case 2 ai is opponent and goes first
                preferred_values = {
                    "7",
                    "8",
                    "9",
                    "10"
                }
                suits = {
                    "hearts": [],
                    "spades": [],
                    "diamonds": [],
                    "clubs": []
                }
                contains_preferred = {}

                for card in hand:
                    suits[card["suit"]].append(card)

                for suit, cards in suits.items():
                    if any(card["value"] in preferred_values for card in cards):
                        contains_preferred[suit] = cards

                if contains_preferred:
                    smallest_suit = min(contains_preferred, key=lambda suit: len(contains_preferred[suit]))
                    return MakeAiMoveHardNullspiel.smallest_card(smallest_suit, contains_preferred[smallest_suit])
                else:
                    ##you could add advanced logic here but since its unlikely to not have a single 7 8 9 or 10 in 10 cards (about 0.0124%.) this logic is fine
                    return hand[0]
        else:
            ##ai is not first
            ##common logic in all cases is determining the highest value card played so far, the suit to be followed and if said suit is in the ai's hand
            current_best = None
            best_card = None
            contains_suit = False
            played_cards = []
            ##determine suit of first played card
            for i in range(len(list(cards))):
                played_cards.append(cards[list(cards)[i]])
            """for thing in cards:
                print(thing)
                played_cards.append(thing.values())"""
            suit = played_cards[0]["suit"]
            ##determine if desired suit is in hand
            for card in hand:
                if card["suit"] == suit:
                    contains_suit = True
                    break
            ##determine highest card played so far
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

            if is_declarer_result:
                ##case 3 ai is the declarer and not first
                value_order = [
                    "7",
                    "8",
                    "9",
                    "10",
                    "jack",
                    "queen",
                    "king",
                    "ace"
                ]
                current_closest = None
                closest = None
                difference = None
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
                smallest = None
                smallest_value = 1000
                if closest is None:
                    if contains_suit:
                        only_suit = []
                        for card in hand:
                            if card["suit"] == suit:
                                only_suit.append(card)
                        closest = max(only_suit, key=lambda x: card_order.index(x))
                    else:
                        ## this plays the largest card in hand if the hand doesnt contain the suit to be followed
                        for card in hand:
                            if smallest is None:
                                smallest = card
                                smallest_value = value_order.index(card["value"])
                            elif smallest_value > value_order.index(card["value"]):
                                smallest = card
                                smallest_value = value_order.index(card["value"])
                        closest = smallest
                return closest
            else:
                ##case 4 ai is not the delcarer and not first
                low_cards = {
                    "7",
                    "8"
                }
                ac_ki_qu = {
                    "ace",
                    "king",
                    "queen"
                }
                if not contains_suit:
                    ##universal case of ai not having the needed suit in hand
                    hand_by_suit = {
                        "hearts": [],
                        "spades": [],
                        "diamonds": [],
                        "clubs": []
                    }
                    for card in hand:
                        hand_by_suit[card["suit"]].append(card)

                    non_empty_suits = {}

                    for suit in hand_by_suit:
                        if len(hand_by_suit[suit]) > 0:
                            non_empty_suits[suit] = hand_by_suit[suit]
                    return MakeAiMoveHardNullspiel.largest_card(min(non_empty_suits, key=lambda suit: len(non_empty_suits[suit])), hand)

                if len(played_cards) == 1 and before_declarer:
                    ## case 4-1 ai is in position 2 and before the declarer
                    ## follow the play of the other opponent
                    print(best_card["value"])
                    if best_card["value"] in low_cards:
                        return MakeAiMoveHardNullspiel.smallest_card(suit, hand)
                    elif best_card["value"] in ac_ki_qu:
                        return MakeAiMoveHardNullspiel.largest_card(suit, hand)
                    else:
                        diff = None
                        c_closest = None
                        to_play = None
                        for card in hand:
                            if card["suit"] == suit:
                                for i in range(len(card_order)):
                                    if card == card_order[i]:
                                        if c_closest is None:
                                            diff = i - current_best
                                            c_closest = i
                                            to_play = card
                                        elif i > current_best and i - current_best < diff:
                                            diff = i - c_closest
                                            c_closest = i
                                            to_play = card
                        return to_play
                else:
                    ##determine if best card was played by declarer
                    declarer_played_best = None
                    player_with_best_card = None
                    for player, card_played in cards.items():
                        if best_card in card_played:
                            player_with_best_card = player
                            break
                    if main_player == player_with_best_card:
                        declarer_played_best = True
                    else:
                        declarer_played_best = False

                    if declarer_played_best:
                        ##case 4-2 ai in 3rd position best card is declarers
                        if best_card["value"] in low_cards:
                            return MakeAiMoveHardNullspiel.largest_card(suit, hand)
                        else:
                            if len(played_cards) == 1 and before_declarer:
                                ## case 4-1 ai is in position 2 and before the declarer
                                ## follow the play of the other opponent
                                if best_card["value"] in low_cards:
                                    return MakeAiMoveHardNullspiel.smallest_card(suit, hand)
                                elif best_card["value"] in ac_ki_qu:
                                    return MakeAiMoveHardNullspiel.largest_card(suit, hand)
                                else:
                                    diff = None
                                    c_closest = None
                                    to_play = None
                                    for card in hand:
                                        if card["suit"] == suit:
                                            for i in range(len(card_order)):
                                                if card == card_order[i]:
                                                    if c_closest is None and i > current_best:
                                                        diff = i - current_best
                                                        c_closest = i
                                                        to_play = card
                                                    elif i > current_best and i - current_best < diff:
                                                        diff = i - c_closest
                                                        c_closest = i
                                                        to_play = card
                                    return to_play
                            else:
                                ##determine if best card was played by declarer
                                declarer_played_best = None
                                player_with_best_card = None
                                for player, card_played in cards.items():
                                    if best_card in card_played:
                                        player_with_best_card = player
                                        break
                                if main_player == player_with_best_card:
                                    declarer_played_best = True
                                else:
                                    declarer_played_best = False

                                if declarer_played_best:
                                    ##case 4-2 ai in 3rd position best card is declarers
                                    if best_card["value"] in low_cards:
                                        return MakeAiMoveHardNullspiel.largest_card(suit, hand)
                                    else:
                                        diff = None
                                    c_closest = None
                                    to_play = None
                                    for card in hand:
                                        if card["suit"] == suit:
                                            for i in range(len(card_order)):
                                                if card == card_order[i]:
                                                    if c_closest is None and i > current_best:
                                                        diff = i - current_best
                                                        c_closest = i
                                                        to_play = card
                                                    elif i > current_best and i - current_best < diff:
                                                        diff = i - c_closest
                                                        c_closest = i
                                                        to_play = card
                                    return to_play
                    else:
                        ##case 4-3 ai in 3rd position and best card is other opponents
                        return MakeAiMoveHardNullspiel.largest_card(suit, hand)


    @staticmethod
    def hard_make_ai_move_route(gamemode_active_player,order,cards,hand):
        '''data = request.get_json()

        if not data or 'gamemode' not in data or 'round' not in data:
            abort(400, description="gamemode or round missing")

        gamemode = data.get('gamemode')
        round_data = data.get('round')

        if not gamemode or 'name' not in gamemode:
            abort(400, description="gamemode does not contain name")

        if not gamemode or 'active_player' not in gamemode:
            abort(400, description="gamemode does not contain active player")

        if not round_data or 'order' not in round_data or 'cards' not in round_data:
            abort(400, description="round does not contain order or cards")

        gamemode_name = gamemode.get('name')
        gamemode_active_player = gamemode.get('active_player')
        order = round_data.get('order')
        cards = round_data.get('cards')

        valid_gamemodes = ["Nullspiel"]
        if gamemode_name not in valid_gamemodes:
            abort(400, description="invalid gamemode")'''

        is_declarer_result = MakeAiMoveHardNullspiel.is_declarer(gamemode_active_player, order, cards)
        is_first = MakeAiMoveHardNullspiel.first_to_play(cards)
        before_declarer = MakeAiMoveHardNullspiel.plays_before_declarer(gamemode_active_player, order, cards, is_first, is_declarer_result)

        return MakeAiMoveHardNullspiel.make_ai_move_hard_nullspiel(cards,MakeAiMoveHardNullspiel.null_order,is_declarer_result,is_first,before_declarer,hand,gamemode_active_player)