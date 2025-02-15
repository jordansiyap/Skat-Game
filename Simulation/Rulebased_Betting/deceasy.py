from Rulebased_Betting.calculatebids import CalculateBids
from Rulebased_Betting.betmedium import BetMedium
"""Regelbasierter KI-Agent für die Auswahl des Spielmodus im einfachen Schwierigkeitsgrad"""
class DecEasy:
    @staticmethod
    def make_decision_easy(player_hands, winning_bid, player):
        hand = player_hands[player.get("playerId")]
        skat = player_hands["player3"]
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
                if bid["name"] == DecEasy.acquire_gamemode(skat_hand):
                    return {"gamemode": bid,"player_hands": DecEasy.return_cards_to_skat(skat_hand,bid,player,player_hands)}
        else:
            for bid in bids_hand_handspiel:
                if bid["name"] == DecEasy.acquire_gamemode(hand):
                    return {"gamemode": bid,
                            "player_hands": player_hands}

    """Auswahl des Spielmodus
    Zählt die Trumpfkarten"""
    @staticmethod
    def acquire_gamemode(hand):
        trump_counter = [
            {"name": "Kreuz", "value": str(BetMedium.count_clubs(hand))},
            {"name": "Pik", "value": str(BetMedium.count_spades(hand))},
            {"name": "Herz", "value": str(BetMedium.count_hearts(hand))},
            {"name": "Karo", "value": str(BetMedium.count_diamonds(hand))},
            {"name": "Grand", "value": str(BetMedium.count_jacks(hand))},
            {"name": "Null", "value": str(DecEasy.count_cards_with_value(hand,"7"))}
        ]
        trump_counter.sort(key=lambda x: int(x["value"]))
        return trump_counter[-1].get("name")

    """Zählt Karten eines bestimmten Werten"""
    @staticmethod
    def count_cards_with_value(hand,value):
        counter = 0
        for card in hand:
            if card.get("value") == value:
                counter += 1
        return counter

    """Skat_Rückgabe
    Wirft die Karten mit den niedrigsten Augen ab"""
    @staticmethod
    def return_cards_to_skat(skat_hand,gamemode,player,player_hands):
        skat = []
        if gamemode.get("name") == "Null":
            nullcounter = 0
            null_sequence = ["ace","king","queen","jack","10","9","8","7"]
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
            if list(player_hands)[i] != player and list(player_hands)[i] != "player3":
                second_player = list(player_hands)[i]
                break
        for i in range(len(list(player_hands))):
            if list(player_hands)[i] != player and list(player_hands)[i] != "player3" and list(player_hands)[i] != second_player:
                third_player = list(player_hands)[i]
                break

        new_player_hands = {player.get("playerId"): skat_hand,
                            "player3": skat,
                            second_player: player_hands[second_player],
                            third_player: player_hands[third_player]
                            }

        return  new_player_hands