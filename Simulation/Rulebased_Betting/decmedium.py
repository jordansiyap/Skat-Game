from Rulebased_Betting.calculatebids import CalculateBids
from Rulebased_Betting.betmedium import BetMedium
from Rulebased_Betting.deceasy import DecEasy
"""Regelbasierter KI-Agent für die Auswahl des Spielmodus im mittleren Schwierigkeitsgrad"""
class DecMedium:
    @staticmethod
    def make_decision_medium(player_hands, winning_bid, player):
        player=player.lower()
        hand = player_hands[player]

        skat = player_hands["skat"]
        bids_hand = CalculateBids.calculate_bids(hand, player)
        for bid in bids_hand[:]:
            if int(bid.get("betting")) < int(winning_bid.get("betting")):
                bids_hand.remove(bid)
        bids_hand_handspiel = []
        for bid in bids_hand[:]:
            if "Hand" in str(bid.get("description")):
                bids_hand.remove(bid)
                bids_hand_handspiel.append(bid)
        if bids_hand != []:
            skat_hand = hand
            for card in skat:
                skat_hand.append(card)
            bids_skat_hand = CalculateBids.calculate_bids_no_hand(skat_hand, player)
            for bid in bids_skat_hand[:]:
                if int(bid.get("betting")) < int(winning_bid.get("betting")):
                    bids_skat_hand.remove(bid)
            for bid in bids_skat_hand:
                for i in DecMedium.acquire_gamemode(skat_hand):
                    if bid["name"] == i["name"]:
                        return {"gamemode": bid,"player_hands": DecMedium.return_cards_to_skat(skat_hand,bid,player,player_hands)}
        else:
            for bid in bids_hand_handspiel:
                for i in DecMedium.acquire_gamemode(hand):
                    if bid["name"] == i["name"]:
                        return {"gamemode": bid,
                                "player_hands": player_hands}

    """Auswahl des Spielmodus
    Zählt die Trumpfkarten und blanke Farben"""
    @staticmethod
    def acquire_gamemode(hand):
        trump_counter = [
            {"name": "Kreuz", "value": str(BetMedium.count_clubs(hand)+DecMedium.count_color_aces(hand,"clubs")
                                           +DecMedium.count_empty_colors(hand,"clubs"))},
            {"name": "Pik", "value": str(BetMedium.count_spades(hand)+DecMedium.count_color_aces(hand,"spades")
                                         +DecMedium.count_empty_colors(hand,"spades"))},
            {"name": "Herz", "value": str(BetMedium.count_hearts(hand)+DecMedium.count_color_aces(hand,"hearts")
                                          +DecMedium.count_empty_colors(hand,"hearts"))},
            {"name": "Karo", "value": str(BetMedium.count_diamonds(hand)+DecMedium.count_color_aces(hand,"diamonds")
                                          +DecMedium.count_empty_colors(hand,"diamonds"))},
            {"name": "Grand", "value": str(BetMedium.count_jacks(hand)+DecMedium.count_color_aces(hand,"Grand")
                                           +DecMedium.count_empty_colors(hand,"Grand"))},
            {"name": "Null", "value": str(DecMedium.null_logic_(hand))}
        ]
        trump_counter.sort(key=lambda x: int(x["value"]))
        return trump_counter

    @staticmethod
    def count_color_aces(hand,trump):
        counter = 0
        for card in hand:
            if card.get("value") == "ace" and card.get("suit")!= trump:
                counter += 1
        return counter

    """Nullspiel
    Wiegt niedrige Augen gegen hohe Augen auf"""
    @staticmethod
    def null_logic_(hand):
        counter = (DecEasy.count_cards_with_value(hand,"7")+DecEasy.count_cards_with_value(hand,"8")
                   +DecEasy.count_cards_with_value(hand,"9")+DecEasy.count_cards_with_value(hand,"10")
                   -DecEasy.count_cards_with_value(hand,"jack")-DecEasy.count_cards_with_value(hand,"queen")
                   -DecEasy.count_cards_with_value(hand,"ace")-DecEasy.count_cards_with_value(hand,"king"))
        return counter

    """Skat Rückgabe
    Versucht blanke Farben zu erzeugen
    Wirft niedrige Augen ab"""
    @staticmethod
    def return_cards_to_skat(skat_hand,gamemode,player,player_hands):
        skat = []
        active_player = player
        empty_colors = DecMedium.count_colors(skat_hand)
        if gamemode.get("name") == "Null":
            nullcounter = 0
            null_sequence = ["ace","king","queen","jack","10","9","8","7"]
            for i in range(len(empty_colors)):
                if int(empty_colors[i].get("number")) <= 2:
                    hand =skat_hand
                    for card in hand:
                        if card.get("suit") == empty_colors[i].get("suit"):
                            nullcounter += 1
                            skat.append(card)
                            skat_hand.remove(card)
                        if nullcounter == 2:
                            break
                    if nullcounter ==2:
                        break
            if nullcounter < 2:
                for index in range(len(null_sequence)):
                    hand = skat_hand
                    for card in hand:
                        if card.get("value") == null_sequence[index]:
                            nullcounter +=1
                            skat.append(card)
                            skat_hand.remove(card)
                        if nullcounter == 2:
                            break
                    if nullcounter == 2:
                        break
        else:
            lowie_counter =0
            sequence = ["7","8","9","queen","king","ace","jack"]
            trump = "initialise"
            if gamemode.get("name") == "Kreuz":
                trump = "clubs"
            elif gamemode.get("name") == "Pik":
                trump = "spades"
            elif gamemode.get("name") == "Herz":
                trump = "hearts"
            elif gamemode.get("name") == "Karo":
                trump = "diamonds"
            for i in range(len(empty_colors)):
                if int(empty_colors[i].get("number")) <= 2:
                    hand =skat_hand
                    for card in hand:
                        if card.get("suit") == empty_colors[i].get("suit") and card.get("suit") != trump and card.get("value") != "jack":
                            lowie_counter += 1
                            skat.append(card)
                            skat_hand.remove(card)
                        if lowie_counter == 2:
                            break
                    if lowie_counter ==2:
                        break
            if lowie_counter < 2:
                for index in range(len(sequence)):
                    hand = skat_hand
                    for card in hand:
                            if card.get("value") == sequence[index]:
                                lowie_counter +=1
                                skat.append(card)
                                skat_hand.remove(card)
                            if lowie_counter == 2:
                                break
                    if lowie_counter == 2:
                        break
        for i in range(len(list(player_hands))):
            if list(player_hands)[i] != active_player and list(player_hands)[i] != "player3":
                second_player = list(player_hands)[i]
                break
        for i in range(len(list(player_hands))):
            if list(player_hands)[i] != active_player and list(player_hands)[i] != "player3" and list(player_hands)[i] != second_player:
                third_player = list(player_hands)[i]
                break

        new_player_hands = {active_player: skat_hand,
                            "player3": skat,
                            second_player: player_hands[second_player],
                            third_player: player_hands[third_player]
                            }

        return  new_player_hands

    @staticmethod
    def count_colors(hand):
        empty_colors = [{"suit":"clubs","number": "0"},
                        {"suit":"spades","number": "0"},
                        {"suit":"hearts","number": "0"},
                        {"suit":"diamonds","number": "0"}]
        for card in hand:
            if card.get("value") != "jack":
                if card.get("suit") == "clubs":
                    number = int(empty_colors[0].get("number"))+1
                    empty_colors[0] = {"suit":"clubs", "number":str(number)}
                elif card.get("suit") == "spades":
                    number = int(empty_colors[1].get("number")) + 1
                    empty_colors[1] = {"suit": "spades", "number": str(number)}
                elif card.get("suit") == "hearts":
                    number = int(empty_colors[2].get("number")) + 1
                    empty_colors[2] = {"suit": "hearts", "number": str(number)}
                elif card.get("suit") == "diamonds":
                    number = int(empty_colors[3].get("number")) + 1
                    empty_colors[3] = {"suit": "clubs", "number": str(number)}
        return empty_colors



    @staticmethod
    def count_empty_colors(hand,trump):
        counter = 0
        empty_colors = DecMedium.count_colors(hand)
        for i in range(len(empty_colors)):
            if empty_colors[i].get("number") == 0 and empty_colors[i].get("suit") != trump:
                counter +=2
        return counter
