from flask import Flask, request, jsonify
import random

class MakeAIMoveMediumAnspielen:

    TRUMP_TRANSLATION = {
        "Kreuz": "clubs",
        "Pik": "spades",
        "Herz": "hearts",
        "Karo": "diamonds"
    }

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

    @staticmethod
    def make_ai_move(ai_model,open_round,gamemode,hand,history):
        # Hier ist die implementierung  der Logik für die mittlere KI Bei Anspielen
        play_card = MakeAIMoveMediumAnspielen.choose_card(hand, gamemode, history)
        return jsonify({"play_card": play_card})

    @staticmethod
    def choose_card(hand, gamemode, history):
        """
        Die Strategie basiert darauf, dass die KI ständig versucht, den Punkt zu gewinnen.
        Implementierung der KI-Strategie basierend auf der Beschreibung:
        - Prüft zuerst die höchste Trumpfkarte in der Hand (Falls Diese im Hand steht, spielt Diese).
        - Wählt anschließend die höchste Karte aus anderen Farben, falls vorhanden.
        - Verwendet eine Bedingung, um Stiche zu vermeiden, falls noch Trumpfkarten im Spiel sind.
            Bedingung : die KI Spielt diese höchste wertige Karte nur falls die Beide andere Spieler zusammen mindestens 2 karten von dieser
                        Farbe haben(Ich nehme also an, dass die beiden Gegenspieler besetzen gleichwahrscheinlich jeweils eine Karte von
                        dieser Farbe und sind dazu gezwungen es zu spielen)
        - Spielt die niedrigste Karte, wenn keine gewinnbringenden Optionen verfügbar sind.
        """

        # Übersetzung des Trumpfs
        trump_suit = MakeAIMoveMediumAnspielen.TRUMP_TRANSLATION.get(gamemode['name'], None)
        if gamemode['name'] == "Grand":
            trump_suit = "Grand"

        #Falls NullGame
        if gamemode['name'] == "Null":
            return MakeAIMoveMediumAnspielen.choose_card_strategy_by_null_game(hand, history)

        #Falls Farbspiele oder Grandspiele
        # Handkarten und nach Farben und Trumpfkarten trennen
        hand_by_suit = MakeAIMoveMediumAnspielen.split_hand_by_suit(hand, trump_suit)

        # 1. Das Prüfen, ob die höchste Trumpfkarte in der Hand ist
        if trump_suit:
            # Ermitteln aller Trumpfkarten mit Priorität
            trump_cards_with_priority = MakeAIMoveMediumAnspielen.get_trump_cards_with_priority(trump_suit)

            # Verbleibende Trumpfkarten im Spiel
            remaining_trump_cards = MakeAIMoveMediumAnspielen.get_remaining_trump_cards(history, trump_cards_with_priority)

            # Höchste verbleibende Trumpfkarte im gesamten Spiel(Diese Karte kann im Hand von der KI oder im Hand andere Spieler sein)
            if remaining_trump_cards:
                highest_remaining_trump = remaining_trump_cards[0]  # Höchste Priorität zuerst

                # Prüfen, ob die KI diese Karte in der Hand hat, falls Ja, Spiele die höchste verbleibende Trumpfkarte
                for trump_card_info in trump_cards_with_priority:
                    card = trump_card_info["card"]
                    if card == highest_remaining_trump and card in hand_by_suit.get("trump", []):
                        return card

        # 2. Höchste Karten in anderen Farben finden
        highest_cards_in_hand = MakeAIMoveMediumAnspielen.get_highest_cards_in_hand(hand, history, trump_suit)

        # Farben in der Reihenfolge Pik, Herz, Karo prüfen (je nach Spielmodus anpassbar)
        colors_in_order = [suit for suit in ["clubs", "spades", "hearts", "diamonds"] if suit != trump_suit]

        # Höchste Karten in diesen Farben auswählen
        chosen_card = None
        for suit in colors_in_order:
            if suit in highest_cards_in_hand:
                card = highest_cards_in_hand[suit]

                # Anzahl der verbleibenden Karten dieser Farbe, die bei anderen Spielern sind
                remaining_cards_count = MakeAIMoveMediumAnspielen.count_cards_in_other_hands(suit, hand, history)

                # Trumpfkarten bereits alle gespielt?
                all_trumps_are_played = len(remaining_trump_cards) == 0

                if all_trumps_are_played or remaining_cards_count >= 2:
                    # Diese Karte ist spielbar
                    if not chosen_card:
                        chosen_card = card
                    else:
                        # Wenn mehrere Farben verfügbar sind, wähle zufällig
                        if random.choice([True, False]):
                            chosen_card = card

        # Wenn eine spielbare Karte gefunden wurde, spiele sie
        if chosen_card:
            return chosen_card

        # 3. Falls keine Option gefunden wurde, spiele die Karte mit dem niedrigsten Wert
        return MakeAIMoveMediumAnspielen.get_lowest_card(hand)

    @staticmethod
    def choose_card_strategy_by_null_game(hand, history):
        """
        Wählt eine Karte für das Nullspiel aus, um keinen Stich zu machen.
        Strategie:
        - Die KI bestimmt, welche Karten noch im Spiel sind, um das Risiko besser einzuschätzen
        - Falls eine Karte sicher ist (d. h., alle verbleibenden Karten dieser Farbe im Haände andere Spieler sind höher), wird
          diese Karte gespielt.
        - Im schlimmsten Falls, Die KI spielt standardmäßig die Karte mit dem niedrigsten Wert im Hand.

        :param hand: Die Karten in der Hand der KI.
        :param history: Die Spielhistorie mit gespielten Karten.
        :return: Die Karte, die die KI spielen möchte.
        """

        null_game_priority_of_cards = {
            "ace": 8,
            "king": 7,
            "queen": 6,
            "jack": 5,
            "10": 4,
            "9": 3,
            "8": 2,
            "7": 1
        }

        # Verbleibende Karten analysieren
        remaining_cards = MakeAIMoveMediumAnspielen.get_remaining_cards_im_other_hands_per_suit(history, hand)

        # 1. Spiele die Karte mit dem niedrigsten Wert
        lowest_card = MakeAIMoveMediumAnspielen.get_lowest_card(hand)

        # 2. Überprüfen, ob die Farbe der niedrigsten Karte sicher ist
        for card in hand:
            remaining_in_suit = remaining_cards.get(card['suit'], [])
            #Wenn remaining_in_suit leer ist, bedeutet es, dass die KI besitzt eine Karte von einer Farbe, die nicht Hand andere Spieler stehen
            # So diese Karte ist nicht mehr sicher da da die KI als erste dran ist, die ander Spieler können dann nicht bedienen und egal
            #welcehe Karte sie spielen den Stich ist gewonnen, was zu vermeiden ist.
            if not remaining_in_suit:
                continue
            #die KI prüft ob die Karte sicher ist (d.h Keine andere Spieler hat eine Karte mit so einem niedrigem Wert)
            if all(null_game_priority_of_cards[c['value']] > null_game_priority_of_cards[card['value']] for c in remaining_in_suit):
                # Spiele eine sichere Karte
                return card

        # 3. Falls keine sichere Karte, spiele die niedrigste Karte
        return lowest_card



    @staticmethod
    def split_hand_by_suit(hand, trump_suit):
        """
        Teilt die Karten der Hand in Trumpfkarten und Karten jeder weiteren Farbe auf.
        Alle "Jacks" sind unabhängig von ihrer Farbe Trumpfkarten.
        Falls für eine Farbe keine Karten in der Hand sind, wird eine leere Liste hinzugefügt.

        :param hand: Die Karten in der Hand der KI.
        :param trump_suit: Die Trumpffarbe (z. B. "hearts").
        :return: Ein Dictionary mit den Farben als Schlüssel und den Listen der Karten als Werte.
        """
        # hier wir Initialisieren das Ergebnis-Dictionary mit leeren Listen
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

        # Iteriere über die Karten in der Hand
        for card in hand:
            if card['value'] == "jack" or card['suit'] == trump_suit:
                # Alle Jacks oder Karten der Trumpffarbe(Falls Farbspiel) gehören zu Trumpf
                hand_split["trump"].append(card)
            else:
                # Andere Karten nach ihrer Farbe sortieren
                hand_split[card['suit']].append(card)

        return hand_split


    @staticmethod
    def get_played_cards(history):
        """Extrahiert alle gespielten Karten aus der History."""
        played_cards = []
        for round_data in history.get("rounds", []):
            played_cards.extend(round_data.get("cards", {}).values())
        return played_cards

    @staticmethod
    def get_highest_card(cards):
        """Findet die höchste Karte basierend auf card_values."""
        if not cards:
            return None
        return max(cards, key=lambda card: MakeAIMoveMediumAnspielen.card_values[card['value']])

    @staticmethod
    def get_lowest_card(cards):
        """Findet die niedrigste Karte basierend auf card_values."""
        if not cards:
            return None
        return min(cards, key=lambda card: MakeAIMoveMediumAnspielen.card_values[card['value']])

    @staticmethod
    def get_remaining_cards(suit, history):
        """Findet die verbleibenden Karten (noch nich gespielte Karten) in einer bestimmten Farbe."""
        all_cards_in_suit = [
            {"suit": suit, "value": value} for value in MakeAIMoveMediumAnspielen.card_values.keys()
        ]
        played_cards = MakeAIMoveMediumAnspielen.get_played_cards(history)
        return [
            card for card in all_cards_in_suit
            if card not in played_cards
        ]

    @staticmethod
    def get_remaining_trump_cards(history, list_of_all_Trump_cards):
        """Findet die verbleibenden Trumpfkarten im Spiel (Also die Trumpfkarten, die noch nicht gespielt wurde)"""

        remaining_trump_cards = [
                card_info["card"]
                for card_info in list_of_all_Trump_cards
                if card_info["card"] not in MakeAIMoveMediumAnspielen.get_played_cards(history)
            ]
        return remaining_trump_cards

    @staticmethod
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
            remaining_cards = MakeAIMoveMediumAnspielen.get_remaining_cards(suit, history)
            if not remaining_cards:
                continue  # Keine verbleibenden Karten, weiter zur nächsten Farbe

            # Höchste verbleibende Karte
            highest_remaining_card = MakeAIMoveMediumAnspielen.get_highest_card(remaining_cards)

            # Prüfen, ob die höchste verbleibende Karte in der Hand ist
            cards_in_suit = [card for card in hand if card['suit'] == suit]
            if highest_remaining_card in cards_in_suit:
                highest_cards_in_hand[suit] = highest_remaining_card

        return highest_cards_in_hand

    @staticmethod
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
        # Alle Karten in dieser Farbe
        all_cards_in_suit = [{"suit": suit, "value": value} for value in MakeAIMoveMediumAnspielen.card_values.keys()]

        # Karten, die bereits gespielt wurden
        played_cards = MakeAIMoveMediumAnspielen.get_played_cards(history)

        # Karten, die sich im Hand der KI befinden
        hand_cards_in_suit = [card for card in hand if card['suit'] == suit]

        # Karten, die noch nicht gespielt wurden
        remaining_cards = [
            card for card in all_cards_in_suit
            if card not in played_cards and card not in hand_cards_in_suit
        ]

        # Anzahl der verbleibenden Karten, die nicht in der Hand der KI liegen
        return len(remaining_cards)

    @staticmethod
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

        # Alle Trumpfkarten mit Priorität
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


    @staticmethod
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
            suit: [{"suit": suit, "value": value} for value in MakeAIMoveMediumAnspielen.card_values.keys()]
            for suit in suits
        }

        # Gespielte Karten aus der History
        played_cards = MakeAIMoveMediumAnspielen.get_played_cards(history)

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
