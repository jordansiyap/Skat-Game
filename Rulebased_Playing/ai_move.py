from flask import Flask
import json 
import re
import random
class AIMove:
    @staticmethod
    def  process_ai_move(data):
        data = data
        open_round = data.get("open_round")
        hand = data.get("hand")
        gamemode = data.get("selected_gamemode")["gamemode"]
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
            result = AIMove.get_is_legal_move(card_to_try)
            if result.get("status") == "true":
                return {"play_card": selected_card}


        return {"error": "Hand is empty!"}


    @staticmethod
    def get_is_legal_move(card_to_try):
        all_cards = []
        open_round = card_to_try.get("open_round")
        hand = card_to_try.get("hand")
        check_card = card_to_try.get("check_card")
        gamemode = card_to_try.get("gamemode")
        order_list = open_round.get("order")
        erster_spieler = order_list[0]["playerId"]
        all_ülayed_cards = open_round.get("cards")
        #print(all_ülayed_cards)
        if len(all_ülayed_cards) > 0:
            firstplayedcard = all_ülayed_cards[erster_spieler]


            gamemode = gamemode.get("name")
            if gamemode == "Null":
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
                hat_gesuchte_farbe = False
                trumpf_in_hand = False
                anzahlfarbe = 0
                erst_gespielte_farbe = firstplayedcard.get("suit")
                erst_gespielt_trumpf = firstplayedcard.get("value")
                #trumpf ist gelegt
                if erst_gespielt_trumpf == "jack" or erst_gespielte_farbe == "clubs":
                    #auf jack oder clubs wird clubs oder jack gelegt
                    if check_card.get("suit") == "clubs" or check_card.get("value")=="jack":
                        return {"status": "true"}
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
                        return {"status": "true"}
                    else:
                        return {"status": "false"}
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
                hat_gesuchte_farbe = False
                trumpf_in_hand = False
                anzahlfarbe = 0
                erst_gespielte_farbe = firstplayedcard.get("suit")
                erst_gespielt_trumpf = firstplayedcard.get("value")

                if erst_gespielt_trumpf == "Jack" or erst_gespielte_farbe == "hearts":
                    if check_card.get("suit") == "hearts" or check_card.get("value")=="Jack":
                        return {"status": "true"}
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
                        return {"status": "true"}
                    else:
                        return {"status": "false"}

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
                hat_gesuchte_farbe = False
                trumpf_in_hand = False
                anzahlfarbe = 0
                erst_gespielte_farbe = firstplayedcard.get("suit")
                erst_gespielt_trumpf = firstplayedcard.get("value")

                if erst_gespielt_trumpf == "Jack" or erst_gespielte_farbe == "spades":
                    if check_card.get("suit") == "spades" or check_card.get("value")=="Jack":
                        return {"status": "true"}
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
                        return {"status": "true"}
                    else:
                        return {"status": "false"}

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
                hat_gesuchte_farbe = False
                trumpf_in_hand = False
                anzahlfarbe = 0
                erst_gespielte_farbe = firstplayedcard.get("suit")
                erst_gespielt_trumpf = firstplayedcard.get("value")

                if erst_gespielt_trumpf == "Jack" or erst_gespielte_farbe == "diamonds":
                    if check_card.get("suit") == "diamonds" or check_card.get("value")=="Jack":
                        return {"status": "true"}
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
                        return {"status": "true"}
                    else:
                        return {"status": "false"}

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
        else:
            return {"status": "true"}
