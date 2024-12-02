from calculate_bids import Calculate_Bids

class Bet_Medium():
    def betting_ai_medium(self,hand,previous_bets,player):
        utily_obj = Calculate_Bids()
        valid_bets = utily_obj.calculate_bids(hand, player)
        valid_bets.sort(key=lambda bet: int(bet['betting']))
        last_bid = calculate_weight(hand,previous_bets[-1])

        weighted_valid_bets = []
        for gamemode in valid_bets:
            weighted_valid_bets.append(calculate_weight(hand,gamemode))
        weighted_valid_bets.sort(key=lambda bet: int(bet['betting']))
        result = []
        result.append(last_bid)
        for x in weighted_valid_bets:
            if int(x.get("priority")) > int(last_bid.get("priority")) and int(x.get("betting")) > int(last_bid.get("betting")):
                result.append(x)
                return x
        result.append(last_bid)
        return last_bid


def calculate_weight(hand,gamemode):
    weight=0
    if gamemode.get("name") != "Null":
        weight += count_jacks(hand)*100
        if gamemode.get("name") == "Kreuz":
            weight += count_clubs(hand)*20
        elif gamemode.get("name") == "Pik":
            weight += count_spaes(hand)*20
        elif gamemode.get("name") == "Herz":
            weight += count_hearts(hand)*20
        elif gamemode.get("name") == "Karo":
            weight += count_diamonds(hand)*20
        elif gamemode.get("name") == "Grand":
            weight += count_jacks(hand)*25
    else:
        weight += count_lowies(hand)*50
    weight += int(gamemode.get("betting"))
    return {"name": gamemode.get("name"), "active_player": gamemode.get("active_player"),
                        "description": gamemode.get("description"),
                        "betting": gamemode.get("betting"), "priority": str(weight) }


def count_jacks(hand):
    counter = 0
    for card in hand:
        if card.get("value") == "jack":
            counter +=1
    return counter

def count_clubs(hand):
    counter = 0
    for card in hand:
        if card.get("suit") == "clubs" and card.get("value") != "jack":
            counter +=1
    return counter

def count_spaes(hand):
    counter = 0
    for card in hand:
        if card.get("suit") == "spaes" and card.get("value") != "jack":
            counter +=1
    return counter

def count_hearts(hand):
    counter = 0
    for card in hand:
        if card.get("suit") == "hearts" and card.get("value") != "jack":
            counter +=1
    return counter

def count_diamonds(hand):
    counter = 0
    for card in hand:
        if card.get("suit") == "diamonds" and card.get("value") != "jack":
            counter +=1
    return counter

def count_lowies(hand):
    counter = 0
    for card in hand:
        if card.get("value") != "jack" and card.get("value") != "ace" and card.get("value") != "king" and card.get("value") != "queen":
            counter += 1
    return counter
