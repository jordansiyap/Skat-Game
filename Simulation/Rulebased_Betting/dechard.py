from Rulebased_Betting.bethard_prediction import BetHardPrediction
from Rulebased_Betting.calculatebids import CalculateBids
from Rulebased_Betting.decmedium import DecMedium

"""Regelbasierter KI-Agent für die Auswahl des Spielmodus im mittleren Schwierigkeitsgrad"""
class DecHard:
    @staticmethod
    def make_decision_hard(player_hands, winning_bid, player):
        hand = player_hands[player.lower()]
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
                for i in DecHard.acquire_gamemode(skat_hand):
                    if bid["name"] == i["name"]:
                        return {"gamemode": bid,"player_hands": DecMedium.return_cards_to_skat(skat_hand,bid,player,player_hands)}
        else:
            for bid in bids_hand_handspiel:
                for i in DecHard.acquire_gamemode(hand):
                    if bid["name"] == i["name"]:
                        return {"gamemode": bid,
                                "player_hands": hand}
    """Auswahl des Spielmodus
    Fragt Werte der Hilfsklasse BetHard ab"""
    @staticmethod
    def acquire_gamemode(hand):
        trump_counter = [
            {"name": "Kreuz", "value": str(DecHard.weights(hand,{"name":"Kreuz"}))},
            {"name": "Pik", "value": str(DecHard.weights(hand,{"name":"Pik"}))},
            {"name": "Herz", "value": str(DecHard.weights(hand,{"name":"Herz"}))},
            {"name": "Karo",
             "value": str(DecHard.weights(hand,{"name":"Karo"}))},
            {"name": "Grand", "value": str(DecHard.weights(hand,{"name":"Grand"}))},
            {"name": "Null", "value": str(DecMedium.null_logic_(hand))}
        ]
        trump_counter.sort(reverse=True,key=lambda x: float(x["value"]))
        return trump_counter

    @staticmethod
    def weights(hand,gamemode):
        predictor = BetHardPrediction(hand,gamemode)
        count = 0
        for card in predictor.hand:
            count += float(card["win"])
        return round(count,0)