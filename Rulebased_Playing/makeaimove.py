from flask import abort,jsonify

from flask import request

from Rulebased_Playing.make_ai_move_anspielen_medium import MakeAIMoveMediumAnspielen
from Rulebased_Playing.make_ai_move_medium import MakeAIMoveMedium
from Rulebased_Playing.ai_move import AIMove
from Rulebased_Playing.make_ai_move_hard_nullspiel import MakeAiMoveHardNullspiel
from Rulebased_Playing.make_ai_move_anspielen_hard import MakeAIMoveAnspielenHard
from Rulebased_Playing.ai_move_Grand_zweiter import process_ai_move_hard_zweiter_Grand
from Rulebased_Playing.ai_move_Grand_dritter import process_ai_move_hard_dritter_Grand
from Rulebased_Playing.process_ai_move_hard_zweter_dran import process_ai_move_hard_zweiter_Farbspiele
from Rulebased_Playing.process_ai_move_hard_dritter_spieler_dran import process_ai_move_hard_dritter_Farbspiele
from Rulebased_Playing.als_zweiter_dritter import process_ai_move_hard_zweiter

class MakeAIMove:
    @staticmethod
    def make_ai_move():
        data = request.json

        if not data or 'selected_gamemode' not in data or 'open_round' not in data:
            abort(400, description="gamemode or round missing")


        ai_model = data.get("ai_model")
        open_round = data.get("open_round")
        gamemode = data.get("selected_gamemode")["gamemode"]
        hand = data.get("hand")
        history = data.get("history")

        if not hand:
            abort(400, description="hand missing")

        if not gamemode or 'name' not in gamemode:
            abort(400, description="gamemode does not contain name")

        if not open_round or 'order' not in open_round or 'cards' not in open_round:
            abort(400, description="round does not contain order or cards")

        gamemode_name = gamemode.get('name')
        gamemode_active_player = gamemode.get('active_player')
        order = open_round.get('order')
        cards = open_round.get('cards')

        valid_gamemodes = ["Kreuz", "Pik", "Herz", "Karo", "Grand", "Null"]
        if gamemode_name not in valid_gamemodes:
            abort(400, description="invalid gamemode")

        if ai_model == "Easy Rule-based Bot":
            return AIMove.process_ai_move(data)
        elif ai_model == "Average Rule-based Bot":
            if not cards:
                return MakeAIMoveMediumAnspielen.make_ai_move(ai_model, open_round, gamemode, hand, history)
            else:
                return jsonify({"play_card":MakeAIMoveMedium.make_ai_move_medium(cards,gamemode_name, order, hand)})
        elif ai_model == "Hardest Rule-based Bot":
            if gamemode_name == "Null":
                return jsonify({"play_card":MakeAiMoveHardNullspiel.hard_make_ai_move_route(gamemode_active_player, order, cards, hand)})
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