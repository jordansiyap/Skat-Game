class MakeRLGamemodeBet:
    @staticmethod
    def make_bet(ai_model,hand,previous_bets,player,agent_easy,agent_medium):
        if ai_model == "RL Bot (Weakest)":
            return agent_easy.act_bet(hand,previous_bets,player)
        if ai_model == "RL Bot (Average)":
            return agent_medium.act_bet(hand,previous_bets,player)

    @staticmethod
    def make_decision(ai_model,hands,previous_bets,player,agent_easy,agent_medium):
        hand = hands[player["playerId"]]
        skat = hands["player3"]

        if ai_model == "RL Bot (Weakest)":
            gamemode,new_hand,new_skat = agent_easy.act_decide(hand,previous_bets,player,skat)
        elif ai_model == "RL Bot (Average)":
            gamemode,new_hand,skat = agent_medium.act_decide(hand,previous_bets,player,skat)
        else:
            return {"error": "wrong model"}

        for i in range(len(list(hands))):
            if list(hands)[i] != player and list(hands)[i] != "player3":
                second_player = list(hands)[i]
                break
        for i in range(len(list(hands))):
            if list(hands)[i] != player and list(hands)[i] != "player3" and list(hands)[i] != second_player:
                third_player = list(hands)[i]
                break

        new_player_hands = {player["playerId"]: new_hand,
                            "player3": skat,
                            second_player: hands[second_player],
                            third_player: hands[third_player]
                            }
        return {"gamemode": gamemode, "player_hands": new_player_hands}