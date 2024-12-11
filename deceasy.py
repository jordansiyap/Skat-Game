from calculatebids import CalculateBids
from betmedium import BetMedium

class DecEasy:
    @staticmethod
    def make_decision_easy(hand, skat, winning_bid, player):
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
                    return bid
        else:
            return bids_hand_handspiel[0]

    @staticmethod
    def acquire_gamemode(hand):
        trump_counter = [
            {"name": "Kreuz", "value": str(BetMedium.count_clubs(hand))},
            {"name": "Pik", "value": str(BetMedium.count_spaes(hand))},
            {"name": "Herz", "value": str(BetMedium.count_hearts(hand))},
            {"name": "Karo", "value": str(BetMedium.count_diamonds(hand))}
        ]
        trump_counter.sort(key=lambda x: int(x["value"]))
        return trump_counter[-1].get("name")