import random
import numpy as np


class QLAgent():
    def __init__(self):
        pass

    def decide_action(self):
        """
        最適なアクションかランダムなアクションかを選択
        """
        pass

    def decide_random_action(self):
        """
        行動できる中でランダムなものを選択
        """
        pass

    def decide_optimal_action(self):
        """
        Qtableから現在の状態に対して最適なアクションを選択
        """
        pass

    def update_q_table(self):
        """
        Qtableを方程式に基づいて更新
        next_stateも影響する
        """
        pass 

    def set_q_table(self):
        """
        Qtableの特定の箇所に特定の値を保存
        """
        pass 

    def save_q_table(self):
        """
        Qtableをファイルに保存
        """
        pass 
    
    def load_q_table(self):
        """
        Qtableのファイルを読み込む
        """
        pass





class RandomPlayer:
    # def play(self, player_id, board, actionable_cards):
#         print(f"""
#  RandomPlayer.play is called.
#  player_id: {player_id}
#  board: {board}
#  actionable_cards: {actionable_cards}       
#         """)
        # 最初のアクションではない場合
        # if board.last_card != "":
        #     actionable_cards.append('skip')  # skipを追加
        # action_card = np.random.choice(actionable_cards)  # randomで選択
        # # print("ramdom choice: ", action_card)
        
        # # アクション
        # next_player, next_actionable_card, game_done, game_info, settings = board.move(player_id, action_card)

        # return next_player, next_actionable_card, game_done, game_info, settings
    
    def get_action_card(self, actinable_cards):
        """
        アクションするカードを取得するだけ(playはしない)
        """
        cards = actinable_cards.copy()
        cards.append('skip')

        # アクションカード選択
        index = random.randrange(len(cards))  # randomなインデックスを取得
        result_card = cards[index]

        return result_card


class HumanPlayer:
    def play(self, player_id, board, actionable_cards):
#         print(f"""
#  HumanPlayer.play is called.
#  player_id: {player_id}
#  board: {board}
#  actionable_cards: {actionable_cards}       
#         """)
        # 最初のアクションではない場合
        if board.last_card != "":
            actionable_cards.append('skip')  # skipを追加
        while True:
            print(f"""
{actionable_cards}
上記の中からカードを選択してください
            """)
            action_card = input()
            # 入力が配列(複数手)の場合listにキャスト
            try:
                action_card = eval(action_card)
            except:
                action_card = action_card

            try:
                # 入力したものがアクション可能ではない場合
                if action_card not in actionable_cards:
                    print("適切なものを入力してください")
                    continue
                # アクション
                next_player, next_actionable_card, game_done, game_info, settings = board.move(player_id, action_card)
                break
            except:
                print("error: アクションエラー")
        
        return next_player, next_actionable_card, game_done, game_info, settings
