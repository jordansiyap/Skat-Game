import matplotlib.pyplot as plt
from IPython import display
plt.ion()

def update(not_legal_moves, mean_not_legal_moves):
    display.clear_output(wait=True)
    display.display(plt.gcf())
    plt.clf()
    plt.title('Training...')
    plt.xlabel('Number of Games')
    plt.ylabel('Count')

    # Plot the data
    plt.plot(not_legal_moves, label='win_function')
    plt.plot(mean_not_legal_moves, label='loss_function')
    plt.ylim(ymin=0)

    # Add text annotations
    plt.text(len(not_legal_moves) - 1, not_legal_moves[-1], 
             "(" + str(len(not_legal_moves) - 1) + ", " + str(not_legal_moves[-1]) + ")")
    plt.text(len(mean_not_legal_moves) - 1, mean_not_legal_moves[-1], 
             "(" + str(len(mean_not_legal_moves) - 1) + ", " + str(mean_not_legal_moves[-1]) + ")")

    # Add the legend
    plt.legend()

    plt.show(block=False)
    plt.pause(0.1)  # Pause to update the plot


def get_is_legal_move(card_to_try):

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
        if gamemode == "Nullspiel":
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
                return {"status": "true", "wahlfrei": "true"}   #####
            #wenn farbe auf der hand ist
            else:
                if check_card.get("suit")==firstplayedcard.get("suit"):
                    return {"status": "true" , "wahlfrei": "false"}
                else :
                    return {"status": "false" , "wahlfrei": "false"}
            
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
                        return {"status": "true", "wahlfrei": "false"}
                    else:
                        return {"status": "false", "wahlfrei": "false"} 
                else:
                    return {"status": "true", "wahlfrei": "true"}  ######
            #wenn nicht trumpf ist
            for card in hand:
                if card.get("suit")==erst_gespielte_farbe:
                    if card.get("value")=="jack":
                        continue
                    hat_gesuchte_farbe = True
                    break
                # hat die farbe nicht alles spielbar
            if not hat_gesuchte_farbe:
                return {"status": "true", "wahlfrei": "true"}   ######
            #hat farbe, test ob er sie ausspielt oder nicht
            else:
                #einfach wenn farbe passt und nicht jack ist spielbar
                if check_card.get("suit") == firstplayedcard.get("suit") and check_card.get("value") != "jack":
                    return {"status": "true", "wahlfrei": "false"}
                    #schaut wie oft farbe auf hand ist, jacks werden ignoriert, wenn mehr als eins muss richtige farbe gespielt sein
                else :
                    anzahlfarbe = 0
                    for card in hand:
                        if card.get("suit")==erst_gespielte_farbe:
                            if card.get("value")=="jack":
                                continue
                            anzahlfarbe += 1
                    if anzahlfarbe >= 1:
                        return {"status": "false", "wahlfrei": "false"}
                    else :
                        return {"status": "true", "wahlfrei": "true"}    #####

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
                    return {"status": "true", "wahlfrei": "false"}
                for card in hand:
                    if card.get("suit")=="clubs":
                        if card.get("value")=="jack":
                            continue
                        hat_gesuchte_farbe = True
                        break
                    if card.get("value")== "jack":
                        hat_gesuchte_farbe = True
                        break
                if not hat_gesuchte_farbe:
                    return {"status": "true", "wahlfrei": "true"} #####
                else:
                    return {"status": "false", "wahlfrei": "false"}
            # es wird nicht trumpf anfangs gelegt
            else:
                if check_card.get("value")!="jack" and check_card.get("suit")==erst_gespielte_farbe:
                    return {"status": "true", "wahlfrei": "false"} 
                anzahlfarbe = 0
                for card in hand:
                    if card.get("suit")==erst_gespielte_farbe:
                        if card.get("value")=="jack":
                            continue
                        anzahlfarbe += 1
                #farbe ist in hand vorhanden
                if anzahlfarbe >= 1:
                    return {"status": "false", "wahlfrei": "false"}
                else:
                    return {"status": "true", "wahlfrei": "true"} #####
                

        elif gamemode == "Herz":
            hat_gesuchte_farbe = False
            trumpf_in_hand = False
            anzahlfarbe = 0
            erst_gespielte_farbe = firstplayedcard.get("suit")
            erst_gespielt_trumpf = firstplayedcard.get("value")

            if erst_gespielt_trumpf == "jack" or erst_gespielte_farbe == "hearts":
                if check_card.get("suit") == "hearts" or check_card.get("value")=="jack":
                    return {"status": "true", "wahlfrei": "false"}
                for card in hand:
                    if card.get("suit")=="hearts":
                        if card.get("value")=="jack":
                            continue
                        hat_gesuchte_farbe = True
                        break
                    if card.get("value")=="jack":
                        hat_gesuchte_farbe = True
                        break
                if not hat_gesuchte_farbe:
                    return {"status": "true", "wahlfrei": "true"}  ######
                else:
                    return {"status": "false", "wahlfrei": "false"}

            else:
                if check_card.get("value")!="jack" and check_card.get("suit")==erst_gespielte_farbe:
                    return {"status": "true", "wahlfrei": "false"} 
                anzahlfarbe = 0
                for card in hand:
                    if card.get("suit")==erst_gespielte_farbe:
                        if card.get("value")=="jack":
                            continue
                        anzahlfarbe += 1
                if anzahlfarbe >= 1:
                    return {"status": "false", "wahlfrei": "false"} 
                else :
                    return {"status": "true", "wahlfrei": "true"}  ####
        elif gamemode == "Pik":
            hat_gesuchte_farbe = False
            trumpf_in_hand = False
            anzahlfarbe = 0
            erst_gespielte_farbe = firstplayedcard.get("suit")
            erst_gespielt_trumpf = firstplayedcard.get("value")

            if erst_gespielt_trumpf == "jack" or erst_gespielte_farbe == "spades":
                if check_card.get("suit") == "spades" or check_card.get("value")=="jack":
                    return {"status": "true", "wahlfrei": "false"} 
                for card in hand:
                    if card.get("suit")=="spades":
                        if card.get("value")=="jack":
                            continue
                        hat_gesuchte_farbe = True
                        break
                    if card.get("value")=="jack":
                        hat_gesuchte_farbe = True
                        break
                if not hat_gesuchte_farbe:
                    return {"status": "true", "wahlfrei": "true"}  #####
                else:
                    return {"status": "false", "wahlfrei": "false"}

            else:
                if check_card.get("value")!="jack" and check_card.get("suit")==erst_gespielte_farbe:
                    return {"status": "true", "wahlfrei": "false"} 
                anzahlfarbe = 0
                for card in hand:
                    if card.get("suit")==erst_gespielte_farbe:
                        if card.get("value")=="jack":
                            continue
                        anzahlfarbe += 1
                if anzahlfarbe >= 1:
                    return {"status": "false", "wahlfrei": "false"}  
                else :
                    return {"status": "true", "wahlfrei": "true"}  #####
        elif gamemode == "Karo":
            hat_gesuchte_farbe = False
            trumpf_in_hand = False
            anzahlfarbe = 0
            erst_gespielte_farbe = firstplayedcard.get("suit")
            erst_gespielt_trumpf = firstplayedcard.get("value")

            if erst_gespielt_trumpf == "jack" or erst_gespielte_farbe == "diamonds":
                if check_card.get("suit") == "diamonds" or check_card.get("value")=="jack":
                    return {"status": "true", "wahlfrei": "false"} 
                for card in hand:
                    if card.get("suit")=="diamonds":
                        if card.get("value")=="jack":
                            continue
                        hat_gesuchte_farbe = True
                        break
                    if card.get("value")=="jack":
                        hat_gesuchte_farbe = True
                        break
                if not hat_gesuchte_farbe:
                    return {"status": "true", "wahlfrei": "true"}  #####
                else:
                    return {"status": "false", "wahlfrei": "false"}

            else:
                if check_card.get("value")!="jack" and check_card.get("suit")==erst_gespielte_farbe:
                    return {"status": "true", "wahlfrei": "false"} 
                anzahlfarbe = 0
                for card in hand:
                    if card.get("suit")==erst_gespielte_farbe:
                        if card.get("value")=="jack":
                            continue
                        anzahlfarbe += 1
                if anzahlfarbe >= 1:
                    return {"status": "false", "wahlfrei": "false"}
                else :
                    return {"status": "true", "wahlfrei": "true"} #####
        else:
            return {"status": "false", "wahlfrei": "false"}
