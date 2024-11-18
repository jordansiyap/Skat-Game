from flask import Flask, request

app = Flask(__name__)

@app.route('/calculate_bids',methods=['GET'])


#Berechnung der Reizwerte aus einer beliebigen Hand
#Die Methode berechnet alle spielbaren Reizwerte aus einer Hand und übergibt diese in Form eines Arrays.
#Die Methode soll als Hilfsmittel für die noch zu implementierende Entscheidungsfindung der KI beim Reizen dienen.
#Eingabe: Json-Objekt mit den Schemas hand und player
#Ausgabe: Array von gamemode Schemas mit Reizwert und Spielartbeschreibung
def calculate_bids():
    #Informationseingabe zur Hand und dem Spieler
    #Keine Überprüfung der Objekte auf Validität (soll im Rahmen der KI-Methode erfolgen)
    calculate_bid = request.json
    hand = calculate_bid.get("hand")
    player = calculate_bid.get("player")

    #Initialisieren des Array mit den immer spielbaren Nullspielvarianten
    valid_bids = [
        {"name": "Null", "active_player": player, "description": "Nullspiel", "betting": "23"},
        {"name": "Null", "active_player": player, "description": "Nullspiel Hand", "betting": "35"},
    ]

    #Hilfsarray mit den Spielarten außer Null
    modes = ["Karo","Herz","Pik","Kreuz","Grand"]

    if check_clubs_jack(hand):
        #Mit 1 Spiel 2
        for x in modes:
            valid_bids.append(create_gamemode(x,player,1,True))
            valid_bids.append(create_gamemode_hand(x,player,1,True))
        if check_spaes_jack(hand):
            #Mit 2 Spiel 3
            for x in modes:
                valid_bids.append(create_gamemode(x,player,2,True))
                valid_bids.append(create_gamemode_hand(x, player, 2, True))
            if check_hearts_jack(hand):
                #Mit 3 Spiel 4
                for x in modes:
                    valid_bids.append(create_gamemode(x,player, 3, True))
                    valid_bids.append(create_gamemode_hand(x, player, 3, True))
                if check_diamonds_jack(hand):
                    #Mit 4 Spiel 5
                    for x in modes:
                        valid_bids.append(create_gamemode(x, player, 4, True))
                        valid_bids.append(create_gamemode_hand(x, player, 4, True))
                    return valid_bids
                else:
                    return valid_bids
            else:
                return valid_bids
        else:
            return valid_bids
    else:
        #Ohne 1 Spiel 2
        for x in modes:
            valid_bids.append(create_gamemode(x, player,1, False))
            valid_bids.append(create_gamemode_hand(x,player,1,False))
        if check_spaes_jack(hand):
            return valid_bids
        else:
            #Ohne 2 Spiel 3
            for x in modes:
                valid_bids.append(create_gamemode(x,player,2,False))
                valid_bids.append(create_gamemode_hand(x, player, 2, False))
            if check_hearts_jack(hand):
                return valid_bids
            else:
                #Ohne 3 Spiel 4
                for x in modes:
                    valid_bids.append(create_gamemode(x, player, 3, False))
                    valid_bids.append(create_gamemode_hand(x, player, 3, False))
                if check_diamonds_jack(hand):
                    return valid_bids
                else:
                    #Ohne 4 Spiel 5
                    for x in modes:
                        valid_bids.append(create_gamemode(x, player, 4, False))
                        valid_bids.append(create_gamemode_hand(x, player, 4, False))
                    return valid_bids


#Hilfsmethode zur Erststellung eines gamemode Objekts
#Eingabe: Spielart, Spieler, Anzahl der fortlaufenden Buben, Zählart (mit Kreuzbude oder ohne Kreuzbube)
#Ausgabe: gamemode Objekt
def create_gamemode(mode,player,number,mit):
    if mit:
        if mode == "Karo":
            return {"name": mode, "active_player": player,
                    "description": "Mit " + str(number) + " Spiel " + str(number+1) + " " + mode,
                    "betting": str((number + 1) * 9) }
        elif mode == "Herz":
            return {"name": mode, "active_player": player,
                    "description": "Mit " + str(number) + " Spiel " + str(number + 1) + " " + mode,
                    "betting": str((number + 1) * 10)}
        elif mode == "Pik":
            return {"name": mode, "active_player": player,
                    "description": "Mit " + str(number) + " Spiel " + str(number + 1) + " " + mode,
                    "betting": str((number + 1) * 11)}
        elif mode == "Kreuz":
            return {"name": mode, "active_player": player,
                    "description": "Mit " + str(number) + " Spiel " + str(number + 1) + " " + mode,
                    "betting": str((number + 1) * 12)}
        elif mode == "Grand":
            return {"name": mode, "active_player": player,
                    "description": "Mit " + str(number) + " Spiel " + str(number + 1) + " " + mode,
                    "betting": str((number + 1) * 24)}
    else:
        if mode == "Karo":
            return {"name": mode, "active_player": player,
                    "description": "Ohne " + str(number) + " Spiel " + str(number+1) + " " + mode,
                    "betting": str((number + 1) * 9) }
        elif mode == "Herz":
            return {"name": mode, "active_player": player,
                    "description": "Ohne " + str(number) + " Spiel " + str(number + 1) + " " + mode,
                    "betting": str((number + 1) * 10)}
        elif mode == "Pik":
            return {"name": mode, "active_player": player,
                    "description": "Ohne " + str(number) + " Spiel " + str(number + 1) + " " + mode,
                    "betting": str((number + 1) * 11)}
        elif mode == "Kreuz":
            return {"name": mode, "active_player": player,
                    "description": "Ohne " + str(number) + " Spiel " + str(number + 1) + " " + mode,
                    "betting": str((number + 1) * 12)}
        elif mode == "Grand":
            return {"name": mode, "active_player": player,
                    "description": "Ohne " + str(number) + " Spiel " + str(number + 1) + " " + mode,
                    "betting": str((number + 1) * 24)}


#Hilfsmethode zur Erststellung eines gamemode Objekts für das Handspiel
#Eingabe: Spielart, Spieler, Anzahl der fortlaufenden Buben, Zählart (mit Kreuzbude oder ohne Kreuzbube)
#Ausgabe: gamemode Objekt
def create_gamemode_hand(mode,player,number,mit):
    if mit:
        if mode == "Karo":
            return {"name": mode, "active_player": player,
                    "description": "Mit " + str(number) + " Spiel " + str(number+1) + " " + mode +" Hand",
                    "betting": str((number + 2) * 9) }
        elif mode == "Herz":
            return {"name": mode, "active_player": player,
                    "description": "Mit " + str(number) + " Spiel " + str(number+1) + " " + mode +" Hand",
                    "betting": str((number + 2) * 10)}
        elif mode == "Pik":
            return {"name": mode, "active_player": player,
                    "description": "Mit " + str(number) + " Spiel " + str(number + 1) + " " + mode + " Hand",
                    "betting": str((number + 2) * 11)}
        elif mode == "Kreuz":
            return {"name": mode, "active_player": player,
                    "description": "Mit " + str(number) + " Spiel " + str(number+1) + " " + mode +" Hand",
                    "betting": str((number + 2) * 12)}
        elif mode == "Grand":
            return {"name": mode, "active_player": player,
                    "description": "Mit " + str(number) + " Spiel " + str(number+1) + " " + mode +" Hand",
                    "betting": str((number + 2) * 24)}
    else:
        if mode == "Karo":
            return {"name": mode, "active_player": player,
                    "description": "Ohne " + str(number) + " Spiel " + str(number+1) + " " + mode +" Hand",
                    "betting": str((number + 2) * 9) }
        elif mode == "Herz":
            return {"name": mode, "active_player": player,
                    "description": "Ohne " + str(number) + " Spiel " + str(number+1) + " " + mode +" Hand",
                    "betting": str((number + 2) * 10)}
        elif mode == "Pik":
            return {"name": mode, "active_player": player,
                    "description": "Ohne " + str(number) + " Spiel " + str(number + 1) + " " + mode + " Hand",
                    "betting": str((number + 2) * 11)}
        elif mode == "Kreuz":
            return {"name": mode, "active_player": player,
                    "description": "Ohne " + str(number) + " Spiel " + str(number+1) + " " + mode +" Hand",
                    "betting": str((number + 2) * 12)}
        elif mode == "Grand":
            return {"name": mode, "active_player": player,
                    "description": "Ohne " + str(number) + " Spiel " + str(number+1) + " " + mode +" Hand",
                    "betting": str((number + 2) * 24)}


#Hilfsmethode zur Überprüfung auf den Kreuzbuben
#Eingabe: hand objekt
#Ausgabe: boolean True bei Anwesenheit des Buben
def check_clubs_jack(hand):
    for card in hand:
        if card.get("suit") == "clubs" and card.get("value") == "jack":
            return True

#Hilfsmethode zur Überprüfung auf den Pikbuben
#Eingabe: hand objekt
#Ausgabe: boolean True bei Anwesenheit des Buben
def check_spaes_jack(hand):
    for card in hand:
        if card.get("suit") == "spaes" and card.get("value") == "jack":
            return True

#Hilfsmethode zur Überprüfung auf den Herzbuben
#Eingabe: hand objekt
#Ausgabe: boolean True bei Anwesenheit des Buben
def check_hearts_jack(hand):
    for card in hand:
        if card.get("suit") == "hearts" and card.get("value") == "jack":
            return True

#Hilfsmethode zur Überprüfung auf den Karobuben
#Eingabe: hand objekt
#Ausgabe: boolean True bei Anwesenheit des Buben
def check_diamonds_jack(hand):
    for card in hand:
        if card.get("suit") == "diamonds" and card.get("value") == "jack":
            return True

if __name__ == '__main__':
    app.run()