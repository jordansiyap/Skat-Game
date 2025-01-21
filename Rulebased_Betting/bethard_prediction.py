import math

class BetHardPrediction:
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

    gamemode_to_suit = {"Kreuz": "clubs",
                        "Pik": "spades",
                        "Herz": "hearts",
                        "Karo": "diamonds",
                        "Grand": "jacks",
                        "Null": "zeros"}


    def __init__(self,hand,gamemode):
        for card in hand:
            for all_card in self.deck:
                if card["suit"] == all_card["suit"] and card["value"] == all_card["value"]:
                    self.deck.remove(all_card)
                    break

        self.trump = self.gamemode_to_suit[gamemode["name"]]
        self.hand = self.initialize_hand(hand)

        '''count_clubs = self.count_color("clubs")
        count_spades = self.count_color("spades")
        count_hearts = self.count_color("hearts")
        count_diamonds = self.count_color("diamonds")

        self.clubs_table = self.create_probability_table(count_clubs,"clubs")
        self.spades_table = self.create_probability_table(count_spades,"spades")
        self.hearts_table = self.create_probability_table(count_hearts,"hearts")
        self.diamonds_table = self.create_probability_table(count_diamonds,"diamonds")'''

        for mode in self.gamemode_to_suit.values():
            if mode != self.trump and mode != "jacks" and mode != "zeros":
                self.hand = self.chance_to_win_color_card(self.hand,mode,self.create_probability_table(self.count_color(mode),mode))


    def initialize_hand(self,hand):
        win_hand = []
        for card in hand:
            if card["value"] == "jack":
                win_hand.append({"suit": card["suit"], "value": card["value"], "win": "5"})
            elif card["suit"] == self.trump:
                win_hand.append({"suit": card["suit"], "value": card["value"], "win": "1"})
            else:
                win_hand.append({"suit": card["suit"], "value": card["value"], "win": "0"})
        return win_hand


    def count_color(self,color):
        count = 0
        for card in self.deck:
            if self.trump == color:
                if card["suit"] == color or card["value"] == "jack":
                    count += 1
            else:
                if card["suit"] == color and card["value"] != "jack":
                    count +=1
        return count

    def create_probability_table(self,number,color):
        probability_table = []
        total_hands = math.comb(22,10)
        for i in range(number+1):
            x = math.comb(number,i)*math.comb(22-number,10-i)
            y= x/total_hands
            probability = {"color": color, "min": min(i,number-i), "probability": str(y)}
            probability_table.append(probability)
        return probability_table

    def chance_to_win_color_card(self,hand,color,probability_table):
        color_cards = []

        for card in hand[:]:
            if card["suit"] == color:
                color_cards.append(card)
                hand.remove(card)

        for card in color_cards:
            win = 0
            if card["value"] == "ace":
                for a in probability_table:
                    if int(a["min"]) != 0:
                        win += float(a["probability"])
            if card["value"] == "10":
                if len(color_cards) > 1:
                    for a in probability_table:
                        if int(a["min"]) > 1:
                            win += float(a["probability"])
            if card["value"] == "king":
                if len(color_cards)  > 1:
                    for a in probability_table:
                        if int(a["min"]) > 1:
                            if not BetHardPrediction.check_for_ace(color_cards) and not BetHardPrediction.check_for_ten(color_cards):
                                win += float(math.comb(7-len(color_cards),int(a["min"]))/math.comb(7,int(a["min"]))) * float(a["probability"])
            hand.append({"suit": card["suit"], "value": card["value"], "win": str(round(win,2))})
        return hand

    @staticmethod
    def check_for_ace(hand):
        for card in hand:
            if card["value"] == "ace":
                return True
        return False

    @staticmethod
    def check_for_ten(hand):
        for card in hand:
            if card["value"] == "10":
                return True
        return False






'''if __name__ == '__main__':
    hand =[
        {"suit": "clubs", "value": "ace"},
        {"suit": "clubs", "value": "queen"},
        {"suit": "clubs", "value": "jack"},
        {"suit": "clubs", "value": "8"},
        {"suit": "clubs", "value": "7"},
        {"suit": "hearts", "value": "ace"},
        {"suit": "hearts", "value": "king"},
        {"suit": "spades", "value": "queen"},
        {"suit": "diamonds", "value": "jack"},
        {"suit": "diamonds", "value": "10"},
    ]

    gamemode = {
        "name" : "Kreuz"
    }
    predictor = BetHardPrediction(hand,gamemode)
    print(predictor.hand)'''