from game import RandomPlayer, HumanPlayer
from game import Board


# 設定
players = {"id1": RandomPlayer(), "id2": RandomPlayer(), "id3": RandomPlayer(), "id4": RandomPlayer()}

board = Board(players)
next_player_id, next_actionable_cards = board.game_start()
while True:
    # action_card = []
    # action_card.append(next_actionable_cards)

    player = players[next_player_id]
    next_player_id, next_actionable_cards, game_done = player.play(next_player_id, board, next_actionable_cards)

    if game_done == True:
        break
