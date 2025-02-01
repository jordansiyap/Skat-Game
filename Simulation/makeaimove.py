from Rulebased_Playing.make_ai_move_anspielen_medium import MakeAIMoveMediumAnspielen
from Rulebased_Playing.make_ai_move_medium import MakeAIMoveMedium
from Rulebased_Playing.ai_move import AIMove
from Rulebased_Playing.make_ai_move_hard_nullspiel import MakeAiMoveHardNullspiel
from Rulebased_Playing.make_ai_move_anspielen_hard import MakeAIMoveAnspielenHard
from Rulebased_Playing.als_zweiter_dritter import process_ai_move_hard_zweiter

def make_ai_move(data):

    ai_model = data.get("ai_model")
    open_round = data.get("open_round")
    gamemode = data.get("gamemode")
    hand = data.get("hand")
    history = data.get("history")

    gamemode_name = gamemode.get('name')
    gamemode_active_player = gamemode.get('active_player')
    order = open_round.get('order')
    cards = open_round.get('cards')

    valid_gamemodes = ["Kreuz", "Pik", "Herz", "Karo", "Grand", "Null"]


    if ai_model == 0:#"Easy Rule-based Bot":
        return AIMove.process_ai_move(data)
    elif ai_model == 1:#"Average Rule-based Bot":
        if not cards:
            return MakeAIMoveMediumAnspielen.make_ai_move(ai_model, open_round, gamemode, hand, history)
        else:
            return {"play_card":MakeAIMoveMedium.make_ai_move_medium(cards,gamemode_name, order, hand)}
    elif ai_model == 2:#"Hardest Rule-based Bot":
        if gamemode_name == "Null":
            print("\ngamemode_active_player", gamemode_active_player)
            print("order", order)
            print("cards", cards)
            print("hand", hand)
            return {"play_card":MakeAiMoveHardNullspiel.hard_make_ai_move_route(gamemode_active_player, order, cards, hand)}
        else:
            if not cards:
                return MakeAIMoveAnspielenHard.make_ai_move(ai_model, open_round, gamemode, hand, history)
            else:
                return process_ai_move_hard_zweiter(data)


    elif ai_model == "RL Bot (Weakest)":
        return {"message": "easy learnbased"}
    elif ai_model == "RL Bot (Average)":
        return {"message": "medium learnbased"}
    elif ai_model == "RL Bot (Hardest)":
        return {"message": "hard learnbased"}