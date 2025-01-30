from flask import Flask, request, jsonify
import json

app = Flask(__name__)

class EvalGame:
    @staticmethod
    def eval_game():
        # Eingabedaten validieren
        input_data = request.json

        # Überprüfung: Sind die Hauptschlüssel vorhanden?
        required_keys = {'history', 'selected_gamemode'}
        if not required_keys.issubset(input_data.keys()):
            return jsonify({"error": f"Input data is missing required keys: {required_keys}"}), 400

        history = input_data['history']
        selected_gamemode = input_data['selected_gamemode']
        alleinspieler = selected_gamemode.get("gamemode").get('active_player')
        gamemode_name = selected_gamemode.get("gamemode").get('name') #Kreuz, Pik, Herz, Karo, Grand, Null
        betting = int(selected_gamemode.get("gamemode").get('betting'))

        # Überprüfung: Gibt es genau 10 Runden?
        if len(history.get('rounds', [])) != 10:
            return jsonify({"error": "The Game is not yet finished ; The game must have exactly 10 rounds in history"}), 400

        # Überprüfung: Sind genau 3 Spieler in betting_order vorhanden?
        if len(history.get('betting_order', [])) != 3:
            return jsonify({"error": "The game must have exactly 3 players in betting_order"}), 400

        # Überprüfung: Ist der Alleinspieler in betting_order?
        if alleinspieler not in history['betting_order']:
            return jsonify({"error": "The active player must be part of the betting_order"}), 400

        # Überprüfung: Jede Runde hat die erforderlichen Felder
        required_round_keys = {'order', 'cards', 'winner', 'score'}
        for i, round_data in enumerate(history['rounds']):
            if not required_round_keys.issubset(round_data.keys()):
                return jsonify({"error": f"Round {i+1} is missing required keys: {required_round_keys}"}), 400

        # Überprüfung: Jede Runde hat die gleiche Anzahl an Spielern in order
        for i, round_data in enumerate(history['rounds']):
            if len(round_data['order']) != len(history['betting_order']):
                return jsonify({"error": f"Round {i+1} has an invalid order length"}), 400

        # Überprüfung: Jede Karte ist gültig
        valid_suits = {"clubs", "spades", "diamonds", "hearts"}
        valid_values = {"ace", "king", "queen", "jack", "10", "9", "8", "7"}
        for i, round_data in enumerate(history['rounds']):
            for player, card in round_data['cards'].items():
                if card['suit'] not in valid_suits or card['value'] not in valid_values:
                    return jsonify({"error": f"Invalid card for player {player} in round {i+1}"}), 400

        # Überprüfung: Keine negativen Punktzahlen
        for i, round_data in enumerate(history['rounds']):
            if round_data['score'] < 0:
                return jsonify({"error": f"Round {i+1} has an invalid negative score"}), 400

        # Überprüfung: Gewinner jeder Runde muss in der order enthalten sein
        for i, round_data in enumerate(history['rounds']):
            if round_data['winner'] not in round_data['order']:
                return jsonify({"error": f"The winner in round {i+1} is not in the player order"}), 400


        # Bestimmen der Punkten jedes Spielers
        # Nachdem alle Rounds gespielt wurde, hier in dem dict "result" habe ich alle punkten, die jeder Spieler bekommen hat.
        #Im "result" befindet sich nur die Spielers, die mindestens einen Stich gewonnen haben, und mit ihren erreichten Punkten.
        results = {}
        for round in history['rounds']:
            winner = round['winner']
            results[winner] = results.get(winner, {'win': False, 'points': 0})
            results[winner]['points'] += round['score']


        # Hier habe ich die Reihenfolge für das nächste Spiel festlegen
        first_Round_Order_List = history.get('rounds')[0].get('order')
        vorhand = first_Round_Order_List.pop(0)
        first_Round_Order_List.append(vorhand) # Der Vorhand wird Hinterhand
        order_next_game = first_Round_Order_List

        #im "Player_results" befindet sich alle Spieler mit ihren erreichten Punkten, die Players, die keinen Stich gewonnen haben, bekommen 0 Punkten
        player_results = {}
        for player in history['betting_order']:
            player_results[player] = {
                "win": False,
                "points": results[player]['points'] if player in results else 0,
                "cost": 0
            }
        #Berechnung von dem Alleinspieler Punkten mit Skat
        gegenspielern_punkt_zusammen = 0
        for player in history['betting_order']:
            if player != alleinspieler:
                gegenspielern_punkt_zusammen += player_results[player]['points']

        #Alleinspieler Punkten zuweisen
        alleinspieler_punkt_mit_skat = 120 - gegenspielern_punkt_zusammen
        player_results[alleinspieler]['points'] = alleinspieler_punkt_mit_skat

        # ich implementiere hier den Gewinnlogik für den Alleinspieler
        if gamemode_name == "Null":
            # Im Nullspiel gewinnt der Alleinspieler, wenn er keinen Stich macht
            player_results[alleinspieler]['win'] = all(
                not round_data['winner'] == alleinspieler for round_data in history['rounds']
            )
            if(player_results[alleinspieler]['win'] == False):
                # Die Gegenspieler gewinnen, wenn der Alleinspieler nicht gewonnen hat, und der Alleinspieler bekomment -2 mal den Spielwert
                for player in player_results:
                    if player != alleinspieler:
                        player_results[player]['win'] = True

        else:
            # In Farbspielen und Grandspielen gewinnt der Alleinspieler, wenn er mindestens 61 Punkte hat
            if alleinspieler_punkt_mit_skat >= 61:
                player_results[alleinspieler]['win'] = True
            else:
                # Die Gegenspieler gewinnen, wenn der Alleinspieler weniger als 61 Punkte hat
                for player in player_results:
                    if player != alleinspieler:
                        player_results[player]['win'] = True

        #Spielwert in der Ausgabe hinzufügen
        if player_results[alleinspieler]['win'] == True:
            player_results[alleinspieler]['cost'] = betting
        else:
            player_results[alleinspieler]['cost'] = - 2 * betting

        # Die Ausgabe
        output = {
            "players": player_results,
            "order_next_game": order_next_game
        }

        return jsonify(output), 200
