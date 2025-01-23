from Rulebased_Playing.make_ai_move_hard_nullspiel import MakeAiMoveHardNullspiel

if __name__ == '__main__':
    gamemode_active_player = "Player1"
    order = ['Player2', 'Player0', 'Player1']
    cards = {'Player2': {'suit': 'hearts', 'value': 'jack'}}
    hand = [{'suit': 'diamonds', 'value': 'king'}, {'suit': 'clubs', 'value': 'ace'}, {'suit': 'spades','value': 'queen'}, {'suit': 'spades', 'value': '10'}, {'suit': 'spades', 'value': '8'}]
    x = MakeAiMoveHardNullspiel.hard_make_ai_move_route(gamemode_active_player, order, cards, hand)
    print(x)