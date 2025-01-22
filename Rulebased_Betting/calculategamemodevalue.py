from flask import request
from Rulebased_Betting.calculatebids import CalculateBids

class CalculateGamemodeValue:
    @staticmethod
    def calculate_gamemode_value():
        data = request.json
        cards = data.get("hand")
        gamemode = data.get("gamemode")["gamemode"]
        skat = data.get("skatbool")
        previous_bets = data.get("previous_bets")
        player_order_next_round=[]

        if previous_bets[0].get("player")["playerId"] == "player4":
            player_order_next_round.append({"playerId":"player2"})
            player_order_next_round.append({"playerId": "player4"})
            player_order_next_round.append({"playerId":"player1"})
        elif previous_bets[0].get("player")["playerId"] == "player2":
            player_order_next_round.append({"playerId":"player1"})
            player_order_next_round.append({"playerId":"player2"})
            player_order_next_round.append({"playerId":"player4"})
        elif previous_bets[0].get("player")["playerId"] == "player1":
            player_order_next_round.append({"playerId":"player4"})
            player_order_next_round.append({"playerId":"player1"})
            player_order_next_round.append({"playerId":"player2"})
        else:
            return {"error message": "impossible player order"}

        player = {"playerId": "player1"}
        hand = cards["cards"]
        multiplier = CalculateGamemodeValue.calculate_multiplier(hand)

        if gamemode.get("name") == "Null":
            if skat:
                return {"selected_gamemode":{"gamemode":{"name": gamemode.get("name"), "active_player": player, "description": "Nullspiel", "betting": "23"},
                                             "player": player},"player_order_next_round": player_order_next_round}
            else:
                return {"selected_gamemode":{"gamemode":{"name": gamemode.get("name"), "active_player": "player1", "description": "Nullspiel Hand", "betting": "35"},
                                             "player": player},"player_order_next_round": player_order_next_round}
        elif gamemode.get("name") == "Karo":
            if skat:
                return {"selected_gamemode":{"gamemode":CalculateBids.create_gamemode(gamemode.get("name"),player,multiplier,CalculateBids.check_clubs_jack(hand)),
                                             "player": player},"player_order_next_round": player_order_next_round}
            else:
                return {"selected_gamemode": {
                    "gamemode": CalculateBids.create_gamemode_hand(gamemode.get("name"), player, multiplier,
                                                              CalculateBids.check_clubs_jack(hand)),
                    "player": player}, "player_order_next_round": player_order_next_round}
        elif gamemode.get("name") == "Herz":
            if skat:
                return {"selected_gamemode":{"gamemode":CalculateBids.create_gamemode(gamemode.get("name"),player,multiplier,CalculateBids.check_clubs_jack(hand)),
                                             "player": player},"player_order_next_round": player_order_next_round}
            else:
                return {"selected_gamemode": {
                    "gamemode": CalculateBids.create_gamemode_hand(gamemode.get("name"), player, multiplier,
                                                              CalculateBids.check_clubs_jack(hand)),
                    "player": player}, "player_order_next_round": player_order_next_round}
        elif gamemode.get("name") == "Pik":
            if skat:
                return {"selected_gamemode":{"gamemode":CalculateBids.create_gamemode(gamemode.get("name"),player,multiplier,CalculateBids.check_clubs_jack(hand)),
                                             "player": player},"player_order_next_round": player_order_next_round}
            else:
                return {"selected_gamemode": {
                    "gamemode": CalculateBids.create_gamemode_hand(gamemode.get("name"), player, multiplier,
                                                              CalculateBids.check_clubs_jack(hand)),
                    "player": player}, "player_order_next_round": player_order_next_round}
        elif gamemode.get("name") == "Kreuz":
            if skat:
                return {"selected_gamemode":{"gamemode":CalculateBids.create_gamemode(gamemode.get("name"),player,multiplier,CalculateBids.check_clubs_jack(hand)),
                                             "player": player},"player_order_next_round": player_order_next_round}
            else:
                return {"selected_gamemode": {
                    "gamemode": CalculateBids.create_gamemode_hand(gamemode.get("name"), player, multiplier,
                                                              CalculateBids.check_clubs_jack(hand)),
                    "player": player}, "player_order_next_round": player_order_next_round}
        elif gamemode.get("name") == "Grand":
            if skat:
                return {"selected_gamemode":{"gamemode":CalculateBids.create_gamemode(gamemode.get("name"),player,multiplier,CalculateBids.check_clubs_jack(hand)),
                                             "player": player},"player_order_next_round": player_order_next_round}
            else:
                return {"selected_gamemode": {
                    "gamemode": CalculateBids.create_gamemode_hand(gamemode.get("name"), player, multiplier,
                                                              CalculateBids.check_clubs_jack(hand)),
                    "player": player}, "player_order_next_round": player_order_next_round}


    @staticmethod
    def calculate_multiplier(hand):
        multiplier = 1
        if CalculateBids.check_clubs_jack(hand):
            #Mit 1 Spiel 2
            multiplier +=1
            if CalculateBids.check_spades_jack(hand):
                #Mit 2 Spiel 3
                multiplier +=1
                if CalculateBids.check_hearts_jack(hand):
                    #Mit 3 Spiel 4
                    multiplier +=1
                    if CalculateBids.check_diamonds_jack(hand):
                        #Mit 4 Spiel 5
                        multiplier +=1
                        return multiplier
                    else:
                        return multiplier
                else:
                    return multiplier
            else:
                return multiplier
        else:
            #Ohne 1 Spiel 2
            multiplier +=1
            if CalculateBids.check_spades_jack(hand):
                return multiplier
            else:
                #Ohne 2 Spiel 3
                multiplier +=1
                if CalculateBids.check_hearts_jack(hand):
                    return multiplier
                else:
                    #Ohne 3 Spiel 4
                    multiplier +=1
                    if CalculateBids.check_diamonds_jack(hand):
                        return multiplier
                    else:
                        #Ohne 4 Spiel 5
                        multiplier +=1
                        return multiplier

