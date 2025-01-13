from flask import Flask
import json 
import re
import random

all_cards = []

eingabe = {
    "open_round": {
        "order": ["player1", "player2", "player3"],
            "cards": {
            "player1": {
                "suit": "spades",
                "value": "jack"
            },
            "player2": {
                "suit": "hearts",
                "value": "jack"
            },
            "player3": {

            }
        }
    },
    "hand": [
        {"suit": "spades", "value": "ace"},
        {"suit": "hearts", "value": "8"}

    ],
    "gamemode": {
        "name": "Herz",
        "active_player": "player3"
    },
    "history": {
        "rounds": [
            {
                "cards": {
                    "player1": {"suit": "spades", "value": "ace"},
                    "player3": {"suit": "diamonds", "value": "9"}
                }
            }
        ]
    }
}

def process_ai_move(data):
    data = data
    open_round = data.get("open_round")
    hand = data.get("hand")
    gamemode = data.get("gamemode")
    while hand:
        hand_length = len(hand)
        random_index = random.randint(0, hand_length - 1)
        selected_card = hand.pop(random_index)
        card_to_try = {
            "open_round": open_round,
            "gamemode": gamemode,
            "check_card": selected_card,
            "hand": hand 
        }
        result = get_is_legal_move(card_to_try)
        print(card_to_try)
        print(result)
        if result.get("status") == "true":
            return {"play_card": selected_card}


    return {"error": "Hand is empty!"}



def get_is_legal_move(card_to_try):
    global all_cards
    all_cards.clear()
    open_round = card_to_try.get("open_round")
    hand = card_to_try.get("hand")
    check_card = card_to_try.get("check_card")
    gamemode = card_to_try.get("gamemode")
    gamemode_spieler = gamemode.get("active_player")
    order_list = open_round.get("order")
    erster_spieler = order_list[0]
    all_ülayed_cards = open_round.get("cards")
    firstplayedcard = all_ülayed_cards[erster_spieler]

    gamemode = gamemode.get("name")
    if gamemode == "Null":
        if erster_spieler== gamemode_spieler:
            return {"status": "true"}
        hat_gesuchte_farbe = False
        trumpf_in_hand = False
        anzahlfarbe = 0
        erst_gespielte_farbe = firstplayedcard.get("suit")
        # wenn farbe in muss gespielt werden ansonsten false
        for card in hand:
            if card.get("suit")==erst_gespielte_farbe:
                hat_gesuchte_farbe = True
                break
        #wenn farbe nicht auf hand ist
        if not hat_gesuchte_farbe:
            return {"status": "true"}
        #wenn farbe auf der hand ist
        else:
            if check_card.get("suit")==firstplayedcard.get("suit"):
                return {"status": "true"}
            else :
                return {"status": "false"}
            
    elif gamemode == "Grand":
        if erster_spieler== gamemode_spieler:
            return {"status": "true"}
        hat_gesuchte_farbe = False
        trumpf_in_hand = False
        anzahlfarbe = 0
        erst_gespielte_farbe = firstplayedcard.get("suit")
        erst_gespielt_trumpf = firstplayedcard.get("value")
        #wenn die erste karte trumpf ist
        if erst_gespielt_trumpf == "jack":
            for card in hand:
                if card.get("value")=="jack":
                    trumpf_in_hand = True
            if trumpf_in_hand:
                if check_card.get("value")=="jack":
                    return {"status": "true"}
                else:
                    return {"status": "false"} 
            else:
                return {"status": "true"}
        #wenn nicht trumpf ist
        for card in hand:
            if card.get("suit")==erst_gespielte_farbe:
                if card.get("value")=="jack":
                    continue
                hat_gesuchte_farbe = True
                break
            # hat die farbe nicht alles spielbar
        if not hat_gesuchte_farbe:
            return {"status": "true"}
        #hat farbe, test ob er sie ausspielt oder nicht
        else:
            #einfach wenn farbe passt und nicht jack ist spielbar
            if check_card.get("suit") == firstplayedcard.get("suit") and check_card.get("value") != "jack":
                return {"status": "true"}
                #schaut wie oft farbe auf hand ist, jacks werden ignoriert, wenn mehr als eins muss richtige farbe gespielt sein
            else :
                anzahlfarbe = 0
                for card in hand:
                    if card.get("suit")==erst_gespielte_farbe:
                        if card.get("value")=="jack":
                            continue
                        anzahlfarbe += 1
                if anzahlfarbe >= 1:
                    return {"status": "false"}
                else :
                    return {"status": "true"}    

    elif gamemode == "Kreuz":
        if erster_spieler== gamemode_spieler:
            return {"status": "true"}
        hat_gesuchte_farbe = False
        trumpf_in_hand = False
        anzahlfarbe = 0
        erst_gespielte_farbe = firstplayedcard.get("suit")
        erst_gespielt_trumpf = firstplayedcard.get("value")
        #trumpf ist gelegt
     
        if erst_gespielt_trumpf == "jack" or erst_gespielte_farbe == "clubs":
            # Wenn Trumpf (herz) oder Jack gespielt wurde
            if check_card.get("suit") == "clubs" or check_card.get("value") == "jack":
                return {"status": "true"}

    # Prüfen, ob Trumpf in der Hand vorhanden ist
            trumpf_in_hand = False
            for card in hand:
                if card.get("suit") == "clubs" or card.get("value") == "jack":
                    trumpf_in_hand = True
                    break

    # Wenn Trumpf in der Hand, aber nicht gespielt, Regelverstoß
            if trumpf_in_hand:
                return {"status": "false"}
            else:
        # Wenn kein Trumpf in der Hand, Spielzug ist erlaubt
                return {"status": "true"}
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
                   return {"status": "false"}
               return {"status": "true"} 
            else :
                return {"status": "true"}

    elif gamemode == "Herz":
        if erster_spieler== gamemode_spieler:
            return {"status": "true"}
        hat_gesuchte_farbe = False
        trumpf_in_hand = False
        anzahlfarbe = 0
        erst_gespielte_farbe = firstplayedcard.get("suit")
        erst_gespielt_trumpf = firstplayedcard.get("value")

        if erst_gespielt_trumpf == "jack" or erst_gespielte_farbe == "hearts":
            # Wenn Trumpf (herz) oder Jack gespielt wurde
            if check_card.get("suit") == "hearts" or check_card.get("value") == "jack":
                return {"status": "true"}

    # Prüfen, ob Trumpf in der Hand vorhanden ist
            trumpf_in_hand = False
            for card in hand:
                if card.get("suit") == "hearts" or card.get("value") == "jack":
                    trumpf_in_hand = True
                    break

    # Wenn Trumpf in der Hand, aber nicht gespielt, Regelverstoß
            if trumpf_in_hand:
                return {"status": "false"}
            else:
        # Wenn kein Trumpf in der Hand, Spielzug ist erlaubt
                return {"status": "true"}

        else:
            anzahlfarbe = 0
            for card in hand:
                if card.get("suit")==erst_gespielte_farbe:
                    if card.get("value")=="jack":
                        continue
                    anzahlfarbe += 1
            if anzahlfarbe >= 1:
               if check_card.get("value")=="jack" or check_card.get("suit")!=erst_gespielte_farbe:
                   return {"status": "false"}
               return {"status": "true"} 
            else :
                return {"status": "true"}
    elif gamemode == "Pik":
        if erster_spieler== gamemode_spieler:
            return {"status": "true"}
        hat_gesuchte_farbe = False
        trumpf_in_hand = False
        anzahlfarbe = 0
        erst_gespielte_farbe = firstplayedcard.get("suit")
        erst_gespielt_trumpf = firstplayedcard.get("value")
        if erst_gespielt_trumpf == "jack" or erst_gespielte_farbe == "spades":
            # Wenn Trumpf (herz) oder Jack gespielt wurde
            if check_card.get("suit") == "spades" or check_card.get("value") == "jack":
                return {"status": "true"}

    # Prüfen, ob Trumpf in der Hand vorhanden ist
            trumpf_in_hand = False
            for card in hand:
                if card.get("suit") == "spades" or card.get("value") == "jack":
                    trumpf_in_hand = True
                    break

    # Wenn Trumpf in der Hand, aber nicht gespielt, Regelverstoß
            if trumpf_in_hand:
                return {"status": "false"}
            else:
        # Wenn kein Trumpf in der Hand, Spielzug ist erlaubt
                return {"status": "true"}


        else:
            anzahlfarbe = 0
            for card in hand:
                if card.get("suit")==erst_gespielte_farbe:
                    if card.get("value")=="jack":
                        continue
                    anzahlfarbe += 1
            if anzahlfarbe >= 1:
               if check_card.get("value")=="jack" or check_card.get("suit")!=erst_gespielte_farbe:
                   return {"status": "false"}
               return {"status": "true"}  
            else :
                return {"status": "true"} 
    elif gamemode == "Karo":
        if erster_spieler== gamemode_spieler:
            return {"status": "true"}
        hat_gesuchte_farbe = False
        trumpf_in_hand = False
        anzahlfarbe = 0
        erst_gespielte_farbe = firstplayedcard.get("suit")
        erst_gespielt_trumpf = firstplayedcard.get("value")
        if erst_gespielt_trumpf == "jack" or erst_gespielte_farbe == "diamonds":
            # Wenn Trumpf (herz) oder Jack gespielt wurde
            if check_card.get("suit") == "diamonds" or check_card.get("value") == "jack":
                return {"status": "true"}

    # Prüfen, ob Trumpf in der Hand vorhanden ist
            trumpf_in_hand = False
            for card in hand:
                if card.get("suit") == "diamonds" or card.get("value") == "jack":
                    trumpf_in_hand = True
                    break

    # Wenn Trumpf in der Hand, aber nicht gespielt, Regelverstoß
            if trumpf_in_hand:
                return {"status": "false"}
            else:
        # Wenn kein Trumpf in der Hand, Spielzug ist erlaubt
                return {"status": "true"}

        else:
            anzahlfarbe = 0
            for card in hand:
                if card.get("suit")==erst_gespielte_farbe:
                    if card.get("value")=="jack":
                        continue
                    anzahlfarbe += 1
            if anzahlfarbe >= 1:
               if check_card.get("value")=="jack" or check_card.get("suit")!=erst_gespielte_farbe:
                   return {"status": "false"}
               return {"status": "true"}  
            else :
                return {"status": "true"} 
    else:
        return {"status": "false"}
if __name__ == "__main__":
    print("Testing AI move processing:")
    result_ai = process_ai_move(eingabe)
    print(json.dumps(result_ai, indent=4))

    print("\nTesting legal move check:")
    card_to_try = {
        "open_round": eingabe["open_round"],
        "gamemode": eingabe["gamemode"],
        "check_card": {"suit": "spades", "value": "ace"},
        "hand": eingabe["hand"]
    }
    result_legal = get_is_legal_move(card_to_try)
    print(json.dumps(result_legal, indent=4))