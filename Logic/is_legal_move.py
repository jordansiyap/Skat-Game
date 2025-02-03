from flask import Flask
import json 
import re
from flask import Flask, jsonify, request


"""
Überprüft ob der spieler einen legalen Zug macht, wenn er nicht legal ist gibt es eine status false message ansonsten status true
"""
class IsLegalMove:
    #all_cards = []

    @staticmethod
    def process_legal_move_request(data):
        #global all_cards
        #all_cards.clear()
        all_cards = []
        data = data
        benötigte_felder = ["open_round", "hand", "check_card", "gamemode"]
        fehlende_felder = [feld for feld in benötigte_felder if feld not in data]
        if fehlende_felder:
            return {"status":False, "reason": f"Missing fields: {', '.join(fehlende_felder)}"}

        open_round = data.get("open_round")
        hand = data.get("hand")
        check_card = data.get("check_card")
        gamemode = data.get("gamemode")
        gamemode_spieler = gamemode.get("active_player").get("player_id")

        # Validation steps
        if error_msg_check_card := IsLegalMove.check_card_isvalid(check_card):
            return {"status":False, "reason": error_msg_check_card}
        if error_msg_check_hand := IsLegalMove.hand_is_valid(all_cards,hand):
            return {"status":False, "reason": error_msg_check_hand}
        if check_card not in hand:
            return {"status":False, "reason": "Die gespielte Karte befindet sich nicht in der Hand."}
        if error_msg_check_gamemode := IsLegalMove.gamemode_is_valid(gamemode):
            return {"status":False, "reason": error_msg_check_gamemode}
        if error_msg_check_round := IsLegalMove.open_round_is_valid(open_round, gamemode,all_cards):
            return {"status":False, "reason": error_msg_check_round}
        if error_msg_check_duplilicate := IsLegalMove.check_duplicate(all_cards):
            return {"status":False, "reason": error_msg_check_duplilicate}

        order_list = open_round.get("order")
        erster_spieler = order_list[0]
        all_ülayed_cards = open_round.get("cards")
        firstplayedcard = all_ülayed_cards[erster_spieler]

        gamemode = gamemode.get("name")
        if gamemode == "Null":
            if erster_spieler == gamemode_spieler:
                return {"status":True}
            hat_gesuchte_farbe = False
            trumpf_in_hand = False
            anzahlfarbe = 0
            erst_gespielte_farbe = firstplayedcard.get("suit")
            for card in hand:
                if card.get("suit") == erst_gespielte_farbe:
                    hat_gesuchte_farbe = True
                    break
            if not hat_gesuchte_farbe:
                return {"status":True}
            else:
                if check_card.get("suit") == firstplayedcard.get("suit"):
                    return {"status":True}
                else:
                    return {"status":False, "reason": "Hat die Farbe auf der Hand, aber nicht ausgespielt."}

        elif gamemode == "Grand":
            if erster_spieler == gamemode_spieler:
                return {"status":True}
            hat_gesuchte_farbe = False
            trumpf_in_hand = False
            erst_gespielte_farbe = firstplayedcard.get("suit")
            erst_gespielt_trumpf = firstplayedcard.get("value")
            if erst_gespielt_trumpf == "jack":
                for card in hand:
                    if card.get("value") == "jack":
                        trumpf_in_hand = True
                if trumpf_in_hand:
                    if check_card.get("value") == "jack":
                        return {"status":True}
                    else:
                        return {"status":False, "reason": "Trumpf auf der Hand, aber nicht ausgespielt."}
                else:
                    return {"status":True}
            for card in hand:
                if card.get("suit") == erst_gespielte_farbe:
                    if card.get("value") == "jack":
                        continue
                    hat_gesuchte_farbe = True
                    break
            if not hat_gesuchte_farbe:
                return {"status":True}
            else:
                if check_card.get("suit") == firstplayedcard.get("suit") and check_card.get("value") != "jack":
                    return {"status":True}
                else:
                    anzahlfarbe = 0
                    for card in hand:
                        if card.get("suit") == erst_gespielte_farbe:
                            if card.get("value") == "jack":
                                continue
                            anzahlfarbe += 1
                    if anzahlfarbe >= 1:
                        return {"status":False, "reason": "Karte ausgespielt, obwohl er die angespielte Karte spielen muss."}
                    else:
                        return {"status":True}
        elif gamemode == "Kreuz":
            if erster_spieler== gamemode_spieler:
                return {"status" : True}
            hat_gesuchte_farbe = False
            trumpf_in_hand = False
            anzahlfarbe = 0
            erst_gespielte_farbe = firstplayedcard.get("suit")
            erst_gespielt_trumpf = firstplayedcard.get("value")
            #trumpf ist gelegt
            if erst_gespielt_trumpf == "jack" or erst_gespielte_farbe == "clubs":
                #auf jack oder clubs wird clubs oder jack gelegt
                if check_card.get("suit") == "clubs" or check_card.get("value")=="jack":
                    return {"status":True}
                for card in hand:
                    if card.get("suit")==erst_gespielte_farbe:
                        if card.get("value")=="jack":
                            continue
                        hat_gesuchte_farbe = True
                        break
                    if card.get("value")==erst_gespielt_trumpf:
                        hat_gesuchte_farbe = True
                        break
                if not hat_gesuchte_farbe:
                    return {"status":True}
                else:
                    return {"status":False, "reason":f"trumpf auf hand aber nicht ausgespielt"}
            # es wird nicht trumpf anfangs gelegt
            else:
                anzahlfarbe = 0
                for card in hand:
                    if card.get("suit")==erst_gespielte_farbe:
                        if card.get("value")=="jack":
                            continue
                        anzahlfarbe += 1
                #farbe ist in hand vorhanden
                if anzahlfarbe >= 1:
                   #wenn nicht ausgespielt false
                   if check_card.get("value")=="jack" or check_card.get("suit")!=erst_gespielte_farbe:
                       return {"status":False, "reason": f"müsste die richtige farbe auspielen da auf hand"}
                   return {"status":True}
                else :
                    return {"status":True}

        elif gamemode == "Herz":
            if erster_spieler== gamemode_spieler:
                return {"status" : True}
            hat_gesuchte_farbe = False
            trumpf_in_hand = False
            anzahlfarbe = 0
            erst_gespielte_farbe = firstplayedcard.get("suit")
            erst_gespielt_trumpf = firstplayedcard.get("value")

            if erst_gespielt_trumpf == "Jack" or erst_gespielte_farbe == "hearts":
                if check_card.get("suit") == "hearts" or check_card.get("value")=="Jack":
                    return {"status":True}
                for card in hand:
                    if card.get("suit")==erst_gespielte_farbe:
                        if card.get("value")=="jack":
                            continue
                        hat_gesuchte_farbe = True
                        break
                    if card.get("value")==erst_gespielt_trumpf:
                        hat_gesuchte_farbe = True
                        break
                if not hat_gesuchte_farbe:
                    return {"status":True}
                else:
                    return {"status":False, "reason":f"trumpf auf hand aber nicht ausgespielt"}

            else:
                anzahlfarbe = 0
                for card in hand:
                    if card.get("suit")==erst_gespielte_farbe:
                        if card.get("value")=="jack":
                            continue
                        anzahlfarbe += 1
                if anzahlfarbe >= 1:
                   if check_card.get("value")=="jack" or check_card.get("suit")!=erst_gespielte_farbe:
                       return {"status":False, "reason": f"müsste die richtige farbe auspielen da auf hand"}
                   return {"status":True}
                else :
                    return {"status":True}
        elif gamemode == "Pik":
            if erster_spieler== gamemode_spieler:
                return {"status" : True}
            hat_gesuchte_farbe = False
            trumpf_in_hand = False
            anzahlfarbe = 0
            erst_gespielte_farbe = firstplayedcard.get("suit")
            erst_gespielt_trumpf = firstplayedcard.get("value")

            if erst_gespielt_trumpf == "Jack" or erst_gespielte_farbe == "spades":
                if check_card.get("suit") == "spades" or check_card.get("value")=="Jack":
                    return {"status":True}
                for card in hand:
                    if card.get("suit")==erst_gespielte_farbe:
                        if card.get("value")=="jack":
                            continue
                        hat_gesuchte_farbe = True
                        break
                    if card.get("value")==erst_gespielt_trumpf:
                        hat_gesuchte_farbe = True
                        break
                if not hat_gesuchte_farbe:
                    return {"status":True}
                else:
                    return {"status":False, "reason":f"trumpf auf hand aber nicht ausgespielt"}

            else:
                anzahlfarbe = 0
                for card in hand:
                    if card.get("suit")==erst_gespielte_farbe:
                        if card.get("value")=="jack":
                            continue
                        anzahlfarbe += 1
                if anzahlfarbe >= 1:
                   if check_card.get("value")=="jack" or check_card.get("suit")!=erst_gespielte_farbe:
                       return {"status":False, "reason": f"müsste die richtige farbe auspielen da auf hand"}
                   return {"status":True}
                else :
                    return {"status":True}
        elif gamemode == "Karo":
            if erster_spieler== gamemode_spieler:
                return {"status":True}
            hat_gesuchte_farbe = False
            trumpf_in_hand = False
            anzahlfarbe = 0
            erst_gespielte_farbe = firstplayedcard.get("suit")
            erst_gespielt_trumpf = firstplayedcard.get("value")

            if erst_gespielt_trumpf == "Jack" or erst_gespielte_farbe == "diamonds":
                if check_card.get("suit") == "diamonds" or check_card.get("value")=="Jack":
                    return {"status":True}
                for card in hand:
                    if card.get("suit")==erst_gespielte_farbe:
                        if card.get("value")=="jack":
                            continue
                        hat_gesuchte_farbe = True
                        break
                    if card.get("value")==erst_gespielt_trumpf:
                        hat_gesuchte_farbe = True
                        break
                if not hat_gesuchte_farbe:
                    return {"status":True}
                else:
                    return {"status":False, "reason":f"trumpf auf hand aber nicht ausgespielt"}

            else:
                anzahlfarbe = 0
                for card in hand:
                    if card.get("suit")==erst_gespielte_farbe:
                        if card.get("value")=="jack":
                            continue
                        anzahlfarbe += 1
                if anzahlfarbe >= 1:
                   if check_card.get("value")=="jack" or check_card.get("suit")!=erst_gespielte_farbe:
                       return {"status":False, "reason": f"müsste die richtige farbe auspielen da auf hand"}
                   return {"status":True}
                else :
                    return {"status":True}
        else:
            return {"status":False, "reason": f"kein valider Spielmodus"}


    @staticmethod
    def hand_is_valid(all_cards,hand):
        IsLegalMove.is_Array(hand)
        for card in hand:
            if error_msg_check_card := IsLegalMove.check_card_isvalid(card):
                return "Invalide Karte in Hand, eine Eigenschaft fehlt/ist falsch."
        IsLegalMove.add_to_all_cards(all_cards,hand)
        return ""

    @staticmethod
    def check_card_isvalid(check_card):
        benötigte_felder = ["suit", "value"]
        fehlende_felder = [feld for feld in benötigte_felder if feld not in check_card]
        if fehlende_felder:
            return f"Missing fields: {', '.join(fehlende_felder)}"
        farbe_pattern = r"^(clubs|spades|diamonds|hearts)$"
        karte_pattern = r"^(ace|king|queen|jack|10|[7-9])$"
        farbe = check_card.get("suit")
        karte = check_card.get("value")
        if re.fullmatch(farbe_pattern, farbe) and re.fullmatch(karte_pattern, karte):
            return ""
        else:
            return "Invalide Karte gespielt"

    @staticmethod
    def gamemode_is_valid(gamemode):
        benötigte_felder = ["name", "active_player"]
        fehlende_felder = [feld for feld in benötigte_felder if feld not in gamemode]
        if fehlende_felder:
            return f"Missing fields: {', '.join(fehlende_felder)}"
        active_player = gamemode.get("active_player")
        if IsLegalMove.active_player_is_valid(active_player):
            return ""
        return False

    @staticmethod
    def active_player_is_valid(player):
        player_pattern = "^player[1-3]$"
        if re.match(player_pattern, player):
            return ""
        else:
            return "Spieler nicht valide"

    @staticmethod
    def open_round_is_valid(open_round,gamemode,all_cards):
        benötigte_felder = ["order", "cards"]
        fehlende_felder = [feld for feld in benötigte_felder if feld not in open_round]
        if fehlende_felder:
            return f"Missing fields: {', '.join(fehlende_felder)} von open round"

        IsLegalMove.is_dict(open_round.get("cards"))
        IsLegalMove.is_Array(open_round.get("order"))
        Order = open_round.get("order")
        aktive_player = gamemode.get("active_player")
        gespielte_karten = open_round.get("cards")
        #spieler vorhanden
        erforderliche_spieler = ["player1", "player2", "player3"]
        fehlende_spieler = [spieler for spieler in erforderliche_spieler if spieler not in open_round["order"]]
        if fehlende_spieler:
            return f"Missing fields: {', '.join(fehlende_spieler)} spieler fehlt in order"


        #spielzug für spieler erlaubt
        if len(gespielte_karten) > 3:
            return "Es dürfen maximal 3 Spieler etwas gespielt haben."
        if len(Order) > 3:
            return "Es dürfen maximal 3 Spieler sein in einer runde in order sein"

        for key, value in open_round["cards"].items():
            if not re.match(r"^player[1-3]$", key):
                return "keys von spielern sind falsch"
            if value:

                farbe_pattern = r"^(clubs|spades|diamonds|hearts)$"
                karte_pattern = r"^(ace|king|queen|jack|10|[7-9])$"
                farbe = value.get("suit")
                karte = value.get("value")
                if re.fullmatch(farbe_pattern, farbe) and re.fullmatch(karte_pattern, karte):
                    if value.get("suit")=="" or value.get("value")=="":
                        return "karte als da erkannt aber keine karte beinhaltet in cards von open"
                    if key == aktive_player:
                        return "spieler hat schon karte gelegt diese runde"
                    if IsLegalMove.check_card_isvalid(value):
                        return "karte ist fehlerhaft von gespielten cards"
                else:
                    return "Eine karte auf dem Tisch ist nicht nicht regelkonform"
        bereits_gespielt = [spieler for spieler in Order if gespielte_karten.get(spieler)]
        for i, spieler in enumerate(bereits_gespielt):
            if spieler != Order[i]:
                return "Zugreihenfolge wurde nicht eingehalten"

        bereits_gespielt = [i for i, spieler in enumerate(Order) if gespielte_karten.get(spieler)]
        if len(bereits_gespielt) == 0:
            if Order[0] != aktive_player:
                return "Der aktive Spieler ist nicht an der Reihe"
        else:
            spielerdran = len(bereits_gespielt)
            if Order[spielerdran] != aktive_player:
                return "Der Spieler ist nicht dran"
        IsLegalMove.add_to_all_cards(all_cards,gespielte_karten.values())
        return ""

    @staticmethod
    def add_to_all_cards(all_cards,cards):
        #global all_cards
        for card in cards:
            all_cards.append({"suit": card.get("suit"), "value": card.get("value")})

    @staticmethod
    def check_duplicate(all_cards):
        seen_cards = set()
        #global all_cards
        for card in all_cards:
            suit = card.get("suit")
            value = card.get("value")
            if suit is None or value is None:
                continue
            card_tuple = (suit, value)
            if card_tuple in seen_cards:
                all_cards.clear()
                return f"Duplikat gefunden/geschummelte Karte: {card}"
            seen_cards.add(card_tuple)
        all_cards.clear()
        return ""

    @staticmethod
    def is_dict(check):
        if not isinstance(check, dict):
            return "ein objekt das ein dict sein sollte ist keines"
        return ""

    @staticmethod
    def is_Array(check):

        if not isinstance(check, list):
            return "ein objekt dass ein array sein sollte ist keines"
        return ""

