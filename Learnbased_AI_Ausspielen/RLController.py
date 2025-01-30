

class makeRLmove :
    
    def makeAImove(ai_model, open_round, gamemode, hand, history, RLeasy, RLmedium, RLhard):
                
        if ai_model == "RL Bot (Weakest)":
            return RLeasy.ai_move(open_round, gamemode, hand, history)
        if ai_model == "RL Bot (Average)":
            return RLmedium.ai_move(open_round, gamemode, hand, history)
        else:
            return RLhard.ai_move(open_round, gamemode, hand, history)