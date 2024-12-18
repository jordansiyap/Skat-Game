from flask import Flask, request, jsonify
import random

app = Flask(__name__)

# Übersetzung von deutschen zu englischen Farben
TRUMP_TRANSLATION = {
    "Kreuz": "clubs",
    "Pik": "spades",
    "Herz": "hearts",
    "Karo": "diamonds"
}

# Kartenwerte für die Wertberechnung
card_values = {
    "ace": 11,
    "10": 10,
    "king": 4,
    "queen": 3,
    "jack": 2,
    "9": 0,
    "8": 0,
    "7": 0
}


@app.route('/make_ai_move', methods=['POST'])
def make_ai_move():
    # Eingabedaten erhalten
    data = request.json
    
    ai_model = data.get("ai_model")
    open_round = data.get("open_round")
    gamemode = data.get("gamemode")
    hand = data.get("hand")
    history = data.get("history")

    # Hier ist die implementierung  der Logik für die mittlere KI Bei Anspielen
    if ai_model == "Average Rule-based Bot":
        play_card = choose_card(hand, gamemode, history, open_round)

    return jsonify({"play_card": play_card})

def choose_card(hand, gamemode, history, open_round):
    """ 
    Die Strategie basiert darauf, dass die KI ständig versucht, den Punkt zu gewinnen.
    Implementierung der KI-Strategie basierend auf der Beschreibung:
    -Die KI verhählt sich genauso wie das Medium KI falls sie die höchste Trumpfkarte im Hand besitzt.
    -Falls nein die KI spielt die Höchste Farbkarte im Spiel falls sie im Hand vorhanden ist, die Bedingung für das Spielen diese
        höchste Karte ist ein bisschen anders als bei Medium-KI, die Beingung ist, dass es mindestens 3 Karten von dieser Farbe im Hände
        andere Spieler zusammen(damit ist es noch sehr wenig wahrscheinlich, dass die KI sich mit einem Trumpf stechen lässt)
    -Falls die beide obige Optionen nicht gelten, die KI verhält sich nicht dummerweise wie das Medium KI, indem sie die direkt eine beliebige
        Karte von niedrigsten Wert im Hand spielt. Hier die Hard-KI gibt sich mehr Chance für kommenden Rounds, indem sie zuerst
        eine Statistik der verbleibenden Karten im Spiel und in der Hand die KI sucht die Farbe die nicht so viel im Hand andere Spieler auftaucht,
        bzw. die KI schaut ob sie die meinstens Trumpfkarte im Hand besitzt.
        -Falls die KI nicht die Höchste Trumpf besitzt, aber besitzt sie die Höchste Anzahl von Trumpf, dann spielt sie eine Trumpfkarte mit
            mit dem niedrigsten Wert um so früh wie möglich die wenige Trumpfkarten im Hand andere zu entziehen,so kann die KI in nächsten rounds immer dominant bezüglich Trumpfkarte.
        -Im schlechten Falls spielt die KI nicht mehr eine beliebige KI im Hand, sondern versucht die KI die FarbKarken loszuwerden
          die am meinstens im Hand stehen, aber fast abwesennd in Hand andere Spieler ist.
    """

    KI_ist_alleinspieler = is_declarer(gamemode.get("active_player"),
                                       open_round.get("order"),
                                       open_round.get("cards"))


    trump_suit = TRUMP_TRANSLATION.get(gamemode['name'], None)
    if gamemode['name'] == "Grand":
        trump_suit = "Grand"

    #Falls Farbspiele oder Grandspiele
    # Handkarten und nach Farben und Trumpfkarten trennen
    hand_by_suit = split_hand_by_suit(hand, trump_suit)

    # 1. Das Prüfen, ob die höchste Trumpfkarte in der Hand ist
    if trump_suit:
        
        trump_cards_with_priority = get_trump_cards_with_priority(trump_suit)

        remaining_trump_cards = get_remaining_trump_cards(history, trump_cards_with_priority)

        # Höchste verbleibende Trumpfkarte im gesamten Spiel(Diese Karte kann im Hand von der KI oder im Hand andere Spieler sein)
        if remaining_trump_cards:
            highest_remaining_trump = remaining_trump_cards[0]  # Höchste Priorität zuerst

            # Prüfen, ob die KI diese Karte in der Hand hat, falls Ja, Spiele die höchste verbleibende Trumpfkarte
            for trump_card_info in trump_cards_with_priority:
                card = trump_card_info["card"]
                if card == highest_remaining_trump and card in hand_by_suit.get("trump", []):
                    return card

    # 2. Höchste Karten in anderen Farben finden
    highest_cards_in_hand = get_highest_cards_in_hand(hand, history, trump_suit)

    colors_in_order = [suit for suit in ["clubs", "spades", "hearts", "diamonds"] if suit != trump_suit]

    # Höchste Karten in diesen Farben auswählen
    chosen_card = None
    for suit in colors_in_order:
        if suit in highest_cards_in_hand:
            card = highest_cards_in_hand[suit]

            # Anzahl der verbleibenden Karten dieser Farbe, die bei anderen Spielern sind
            remaining_cards_count = count_cards_in_other_hands(suit, hand, history)

            # Trumpfkarten bereits alle gespielt?
            all_trumps_are_played = len(remaining_trump_cards) == 0

            if all_trumps_are_played or remaining_cards_count >= 3:
                if not chosen_card:
                    chosen_card = card
                else:
                    # Wenn mehrere Farben verfügbar sind, wähle zufällig
                    if random.choice([True, False]):
                        chosen_card = card

    # Wenn eine spielbare Karte gefunden wurde, spiele sie
    if chosen_card:
        return chosen_card

    #Die KI passt seine Strategie an, falls sie nicht den Alleinspieler ist und nicht die beste Karte im Hand hat
    if not KI_ist_alleinspieler:
        selected_card =  select_card_not_favorable_for_the_hand_of_the_declarer()
        if selected_card is not None:
            return selected_card
    
    #Falls die KI Alleinspieler ist, oder als Gegespieler nicht ein ungünstige Karte gegen den Alleinspieler, sie verhält sich wie folgt:

    remaining_cards = count_remaining_cards(history, trump_suit)
    hand_cards = count_hand_cards(hand, trump_suit)

    # Finde die Farbe mit der kleinsten Anzahl an verbleibenden Karten
    min_suit = None
    min_count = float('inf')
    # Hier macht man so, die KI sucht die Farbe die nicht so viel im Hand sndere Spieler auftaucht, bzw. die KI schaut ob sie die meinstens Trumpfkarte im Hand besitzt
    for suit, count in remaining_cards.items():
        if count < min_count and hand_cards[suit] > remaining_cards[suit]:
            min_suit = suit
            min_count = count

    #Fallls die KI nicht die Höchste Trumpf besitzt, aber besitzt sie die Höchste Anzahl von Trumpf, dann spielt sie eine Trumpfkarte mit
    #mit dem niedrigsten Wert um so früh wie möglich Trumpf karte im Hand andere zu entziehen
    #so kann die KI in nächsten rounds immer dominant bezüglich Trumpfkarte
    if min_suit == "trump":
        return get_lowest_card([card for card in hand if card["value"] == "jack" or card["suit"] == trump_suit])
    else:
        #Im schlechten Falls spielt die KI nicht mehr eine beliebige KI im Hand, sondern versucht die KI die FarbKarke loszuwerden
        #die am meinstens im Hand steht, aber fast nicht anwesennd in Hand andere Spieler ist.
        return get_lowest_card([card for card in hand if card["suit"] == min_suit])


def split_hand_by_suit(hand, trump_suit):
    """
    Teilt die Karten der Hand in Trumpfkarten und Karten jeder weiteren Farbe auf.
    Alle "Jacks" sind unabhängig von ihrer Farbe Trumpfkarten.
    Falls für eine Farbe keine Karten in der Hand sind, wird eine leere Liste hinzugefügt.

    :param hand: Die Karten in der Hand der KI.
    :param trump_suit: Die Trumpffarbe (z. B. "hearts").
    :return: Ein Dictionary mit den Farben als Schlüssel und den Listen der Karten als Werte.
    """

    hand_split = {
        "trump": [],
        "clubs": [],
        "spades": [],
        "hearts": [],
        "diamonds": []
    }

    # Entferne die Trrumpffarbe aus den anderen Farben(Bei "Grand" es ist immer False)
    if trump_suit in hand_split:
        del hand_split[trump_suit]

    for card in hand:
        if card['value'] == "jack" or card['suit'] == trump_suit:
            # Alle Jacks oder Karten der Trumpffarbe(Falls Farbspiel) gehören zu Trumpf
            hand_split["trump"].append(card)
        else:
            hand_split[card['suit']].append(card)

    return hand_split



def get_played_cards(history):
    """Extrahiert alle gespielten Karten aus der History."""
    played_cards = []
    for round_data in history.get("rounds", []):
        played_cards.extend(round_data.get("cards", {}).values())
    return played_cards

def get_highest_card(cards):
    """Findet die höchste Karte basierend auf card_values."""
    if not cards:
        return None
    return max(cards, key=lambda card: card_values[card['value']])

def get_lowest_card(cards):
    """Findet die niedrigste Karte basierend auf card_values."""
    if not cards:
        return None
    return min(cards, key=lambda card: card_values[card['value']])

def get_remaining_cards(suit, history):
    """Findet die verbleibenden Karten (noch nich gespielte Karten) in einer bestimmten Farbe."""
    all_cards_in_suit = [
        {"suit": suit, "value": value} for value in card_values.keys()
    ]
    played_cards = get_played_cards(history)
    return [
        card for card in all_cards_in_suit
        if card not in played_cards
    ]

def get_remaining_trump_cards(history, list_of_all_Trump_cards):
    """Findet die verbleibenden Trumpfkarten im Spiel (Also die Trumpfkarten, die noch nicht gespielt wurde)"""

    remaining_trump_cards = [
            card_info["card"]
            for card_info in list_of_all_Trump_cards
            if card_info["card"] not in get_played_cards(history)
        ]
    return remaining_trump_cards

def get_highest_cards_in_hand(hand, history, trump_suit):
    """
    Überprüft, ob die höchste Karte jeder Farbe, die noch nicht gespielt wurde, in der Hand ist.
    Gibt ein Wörterbuch zurück, in dem jede Farbe der höchsten Karte in der Hand zugeordnet ist.
    Falls für eine Farbe, die höchste noch nicht gespielte nicht im Hand steht(Also es befindet sich im hand andere Spieler) so
    wird nichts für die entsprechende Farbe zurückgegeben.
    Bsp_Ausgabe: {
                    "hearts": {"suit": "hearts", "value": "ace"},
                    "spades": {"suit": "spades", "value": "queen"}
                }
    """
    suits = [suit for suit in ["clubs", "spades", "hearts", "diamonds"] if suit != trump_suit]
    highest_cards_in_hand = {}

    for suit in suits:
        # Finde die verbleibenden Karten dieser Farbe
        remaining_cards = get_remaining_cards(suit, history)
        if not remaining_cards:
            continue  # Keine verbleibenden Karten, weiter zur nächsten Farbe

        highest_remaining_card = get_highest_card(remaining_cards)

        cards_in_suit = [card for card in hand if card['suit'] == suit]
        if highest_remaining_card in cards_in_suit:
            highest_cards_in_hand[suit] = highest_remaining_card

    return highest_cards_in_hand


def count_cards_in_other_hands(suit, hand, history):
    """
    Bestimmt die Anzahl der Karten einer bestimmten Farbe (suit), 
    die noch nicht gespielt wurden und nicht im Hand der KI liegen.
    Diese Karten werden als im Besitz der beiden anderen Spieler angesehen.

    :param suit: Die Farbe, für die die Berechnung erfolgt (z. B. "hearts").
    :param hand: Die Karten in der Hand der KI.
    :param history: Die Spielhistorie, die gespielte Karten enthält.
    :return: Anzahl der Karten in dieser Farbe, die noch im Besitz der anderen Spieler sind.
    """
    
    all_cards_in_suit = [{"suit": suit, "value": value} for value in card_values.keys()]
    
    played_cards = get_played_cards(history)
    hand_cards_in_suit = [card for card in hand if card['suit'] == suit]

    remaining_cards = [
        card for card in all_cards_in_suit
        if card not in played_cards and card not in hand_cards_in_suit
    ]

    # Anzahl der verbleibenden Karten, die nicht in der Hand der KI liegen
    return len(remaining_cards)

def get_trump_cards_with_priority(trump_suit):
    """
    Gibt alle Trumpfkarten für die gegebene Farbe zurück, sortiert nach ihrer Priorität.
    Die höchste Priorität hat "clubs: jack", gefolgt von den anderen Jacks, und dann die Karten der Farbe.
    Falls den suit = Grand gibt alle Bubbe in der geordnete Reihenfolge zurück, suit = Null  dibt leere Liste zurück.

    :param suit: Die Trumpffarbe (z. B. "hearts").
    :return: Eine Liste von Dictionaries mit den Trumpfkarten und ihrer Priorität.

    Bsp:  get_trump_cards_with_priority("clubs") aufgerufen :
        [{'card': {'suit': 'clubs', 'value': 'jack'}, 'priority': 11},
          {'card': {'suit': 'spades', 'value': 'jack'}, 'priority': 10},
            {'card': {'suit': 'hearts', 'value': 'jack'}, 'priority': 9},
              {'card': {'suit': 'diamonds', 'value': 'jack'}, 'priority': 8},
                {'card': {'suit': 'clubs', 'value': 'ace'}, 'priority': 7},
                  {'card': {'suit': 'clubs', 'value': '10'}, 'priority': 6},
                    {'card': {'suit': 'clubs', 'value': 'king'}, 'priority': 5},
                      {'card': {'suit': 'clubs', 'value': 'queen'}, 'priority': 4},
                        {'card': {'suit': 'clubs', 'value': '9'}, 'priority': 3},
                          {'card': {'suit': 'clubs', 'value': '8'}, 'priority': 2},
                            {'card': {'suit': 'clubs', 'value': '7'}, 'priority': 1}]

    """
    # Priorität für Jacks, unabhängig von ihrer Farbe
    jack_priority = {
        "clubs": 11,
        "spades": 10,
        "hearts": 9,
        "diamonds": 8
    }

    
    value_priority = {
        "ace": 7,
        "10": 6,
        "king": 5,
        "queen": 4,
        "9": 3,
        "8": 2,
        "7": 1
    }

    trump_cards_with_priority = []

    #Falls Spielarte Null ist, dann geben wir eine Leere Liste Zurück.
    if trump_suit == "Null":
        return trump_cards_with_priority

    # Zuerst die Jacks hinzufügen
    for jack_suit, priority in jack_priority.items():
        trump_cards_with_priority.append({
            "card": {"suit": jack_suit, "value": "jack"},
            "priority": priority
        })

    # Falls spielarte Grand ist, dann stoppen wir uns hier, und geben wir alle Bubbe zurück.
    if trump_suit == "Grand":
        return trump_cards_with_priority

    # Danach die Karten der Trumpffarbe hinzufügen, basierend auf den Kartenwerten
    for value, priority in value_priority.items():
        trump_cards_with_priority.append({
            "card": {"suit": trump_suit, "value": value},
            "priority": priority
        })

    # Die Trumpfkarten nach Priorität sortieren (höchste Priorität zuerst)
    trump_cards_with_priority.sort(key=lambda x: x["priority"], reverse=True)

    return trump_cards_with_priority


def get_remaining_cards_im_other_hands_per_suit(history, hand):
    """
    Berechnet pro Farbe die Karten, die noch nicht gespielt, die sich im Hand anderer Spieler Zusammen befinden, 
    basierend auf der History und der Hand der KI.

    :param history: Die Spielhistorie mit gespielten Karten.
    :param hand: Die Karten in der Hand der KI.
    :return: Ein Dictionary mit den verbleibenden(Im Hand anderer Spieler) Karten pro Farbe.
    """
    suits = ["clubs", "spades", "hearts", "diamonds"]
    all_cards = {
        suit: [{"suit": suit, "value": value} for value in card_values.keys()]
        for suit in suits
    }

    played_cards = get_played_cards(history)

    # Karten in der Hand der KI
    hand_cards = {suit_card: [] for suit_card in suits}
    for card in hand:
        hand_cards[card['suit']].append(card)

    # Verbleibende Karten berechnen
    remaining_cards = {}
    for suit, cards in all_cards.items():
        remaining_cards[suit] = [
            card for card in cards if card not in played_cards and card not in hand_cards[suit]
        ]

    return remaining_cards

def count_remaining_cards(history, trump_suit):
    """
    Zählt die Anzahl der verbleibenden Karten im Spiel für Trumpfkarten und Farbkarten.

    :param history: Die Spielhistorie mit gespielten Karten.
    :param trump_suit: Die Trumpffarbe im Spiel.
    :return: Ein Dictionary mit den Anzahlen der verbleibenden Karten für jede Farbe.
    """
    suits = ["clubs", "spades", "hearts", "diamonds"]
    remaining_cards = {suit: 0 for suit in suits}
    remaining_cards["trump"] = 0

    if trump_suit in remaining_cards:
        del remaining_cards[trump_suit]

    all_cards = [
        {"suit": suit, "value": value} for suit in suits for value in card_values.keys()
    ]

    played_cards = get_played_cards(history)

    for card in all_cards:
        if card not in played_cards:
            if card["value"] == "jack" or card["suit"] == trump_suit:
                remaining_cards["trump"] += 1
            else:
                remaining_cards[card["suit"]] += 1

    return remaining_cards

def count_hand_cards(hand, trump_suit):
    """
    Zählt die Anzahl der Karten in der Hand der KI für Trumpfkarten und Farbkarten.

    :param hand: Die Karten in der Hand der KI.
    :param trump_suit: Die Trumpffarbe im Spiel.
    :return: Ein Dictionary mit den Anzahlen der Karten in der Hand für jede Farbe.
    """
    suits = ["clubs", "spades", "hearts", "diamonds"]
    hand_cards = {suit: 0 for suit in suits}
    hand_cards["trump"] = 0

    if trump_suit in hand_cards:
        del hand_cards[trump_suit]

    for card in hand:
        if card["value"] == "jack" or card["suit"] == trump_suit:
            hand_cards["trump"] += 1
        else:
            hand_cards[card["suit"]] += 1

    return hand_cards

def analyse_alleinspieler_previous_actions(history, gamemode, trump_suit):
    """
    Analysiert die Aktionen des Alleinspielers in der Mittelhand oder Hinterhand und gibt
    die gespielten Karten von dem Alleinspieler zurück, mit denen er gestochen hat.

    :param history: Die Spielhistorie mit allen Runden.
    :param gamemode: Der aktuelle Spielmodus (enthält den Alleinspieler).
    :param trump_suit: Die Trumpffarbe im Spiel.
    :return: Eine Liste von Diktaten mit den Aktionen des Alleinspielers, die den Bedingungen entsprechen.
    """
    alleinspieler = gamemode.get("active_player")
    relevant_actions = []

    for round_data in history.get("rounds", []):
        order = round_data.get("order", [])  # Reihenfolge der Spieler
        cards = round_data.get("cards", {})  # Gespielte Karten in dieser Runde

        if alleinspieler in order:
            # Hier Bestimme die Position des Alleinspielers in der Runde
            position = order.index(alleinspieler)

            # Überprüfen, ob der Alleinspieler in Mittelhand oder Hinterhand sitzt
            if position > 0:  # Mittelhand (1) oder Hinterhand (2)
                alleinspieler_card = cards.get(alleinspieler)
                first_card = cards.get(order[0])  # Karte des ersten Spielers

                if alleinspieler_card and first_card:
                    
                    #Farbspiel
                    if(trump_suit != "Grand"):
                        
                        if ((first_card["suit"] == trump_suit or first_card["value"] == "jack") and
                            (alleinspieler_card["suit"] != trump_suit or alleinspieler_card["value"] != "jack")):
                            relevant_actions.append({
                                "alleinspieler_card": alleinspieler_card,
                                "first_card": first_card
                            })

                        elif ((first_card["suit"] != trump_suit or first_card["value"] != "jack") and
                              (alleinspieler_card["suit"] != first_card["suit"] or alleinspieler_card["value"] == "jack")):
                            relevant_actions.append({
                                "alleinspieler_card": alleinspieler_card,
                                "first_card": first_card
                            })

                    #Granspiele
                    elif(trump_suit == "Grand"):
                
                        if ( first_card["value"] == "jack" and alleinspieler_card["value"] != "jack"):
                            relevant_actions.append({
                                "alleinspieler_card": alleinspieler_card,
                                "first_card": first_card
                            })

                        # 2. Der Alleinspieler spielt eine andere Farbkarte oder eine Trumpfkarte
                        #    als die erste Farbkarte
                        elif (first_card["value"] != "jack" and alleinspieler_card["value"] == "jack"):
                            relevant_actions.append({
                                "alleinspieler_card": alleinspieler_card,
                                "first_card": first_card
                            })


    return relevant_actions

def select_card_not_favorable_for_the_hand_of_the_declarer(hand, history, gamemode, trump_suit):
    """
    Wählt eine Karte aus der Hand, die für den Alleinspieler ungünstig ist, basierend auf der Analyse der History.

    :param hand: Die Karten in der Hand des Spielers.
    :param history: Die Spielhistorie mit allen Runden.
    :param gamemode: Der aktuelle Spielmodus (enthält den Alleinspieler).
    :param trump_suit: Die Trumpffarbe im Spiel.
    :return: Eine Karte aus der Hand.
    """
    # Analyse der Aktionen des Alleinspielers
    previous_actions = analyse_alleinspieler_previous_actions(history, gamemode, trump_suit)

    # Prüfen, ob es eine "first_card" gibt, die eine Trumpfkarte ist
    for action in previous_actions:
        first_card = action.get("first_card")
        if first_card and first_card["suit"] == trump_suit:
            # Gibt eine beliebige Trumpfkarte aus der Hand zurück
            trump_cards_in_hand = [card for card in hand if card["suit"] == trump_suit]
            if trump_cards_in_hand:
                return trump_cards_in_hand[0]

    # Wenn keine Trumpfkarte als "first_card" gefunden wurde
    for action in previous_actions:
        first_card = action.get("first_card")
        if first_card:
            # Gibt eine Karte aus der Hand mit derselben Farbe wie "first_card" zurück
            same_suit_cards = [card for card in hand if card["suit"] == first_card["suit"]]
            if same_suit_cards:
                return same_suit_cards[0]

    return None

def is_declarer(gamemode_active_player, order, cards):
    players = order
    player_id = len(cards)
    self = order[player_id]
    if self == gamemode_active_player:
        return True
    else:
        return False


if __name__ == '__main__':
    app.run(debug=True)
