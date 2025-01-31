from flask import Flask
import json 
import re
from flask import Flask, jsonify, request
from Rulebased_Playing.process_ai_move_hard_dritter_spieler_dran  import process_ai_move_hard_dritter_Farbspiele
from Rulebased_Playing.process_ai_move_hard_zweter_dran           import process_ai_move_hard_zweiter_Farbspiele
from Rulebased_Playing.ai_move_Grand_zweiter                      import process_ai_move_hard_zweiter_Grand
from Rulebased_Playing.ai_move_Grand_dritter                      import process_ai_move_hard_dritter_Grand

all_cards = []

"""
Methode wenn KI als drittes oder als zweites in der Runde seine Karte ausspielen muss
Unterscheidet noch ein mal zwischen grand und Farbspiel und ruft jeweils dann die logik für die Modis auf
"""


def process_ai_move_hard_zweiter(data):
    global all_cards
    all_cards.clear()
    data = data
    benötigte_felder = ["open_round", "hand", "check_card", "gamemode"]
    fehlende_felder = [feld for feld in benötigte_felder if feld not in data]
    if fehlende_felder:
        return {"status":False, "reason": f"Missing fields: {', '.join(fehlende_felder)}"}
    
    open_round = data.get("open_round")
    hand = data.get("hand")
    check_card = data.get("check_card")
    gamemode = data.get("gamemode")
    gamemode_spieler = gamemode.get("active_player")
    history = data.get("history")

    order_list = open_round.get("order")
    erster_spieler = order_list[0]
    all_played_cards = open_round.get("cards")
    firstplayedcard = all_played_cards[erster_spieler]

    for index, player in enumerate(order_list):
        cards = all_played_cards.get(player, {})
        if not cards:  # Prüfen, ob Karten leer sind
            if gamemode == "Grand":
                if index == 1:
                    process_ai_move_hard_zweiter_Grand(data)
                elif index == 2:
                    process_ai_move_hard_dritter_Grand(data)
            else:  # Farbspiele
                if index == 1:
                    process_ai_move_hard_zweiter_Farbspiele(data)
                elif index == 2:
                    process_ai_move_hard_dritter_Farbspiele(data)
            return


    """
    if gamemode == "Grand":
        for player in data["open_round"]["order"]:
            cards = data["open_round"]["cards"].get(player, {})
            if not cards:  # Prüfen, ob Karten leer sind
                if player == "player1":
                    process_ai_move_hard_zweiter_Grand(data)
                elif player == "player2":
                    process_ai_move_hard_dritter_Grand(data)


    for player in data["open_round"]["order"]:
        cards = data["open_round"]["cards"].get(player, {})
        if not cards:  # Prüfen, ob Karten leer sind
            if player == "player1":
                process_ai_move_hard_zweiter_Farbspiele(data)
            elif player == "player2":
                process_ai_move_hard_dritter_Farbspiele(data)
    """
