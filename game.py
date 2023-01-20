import numpy as np
import random

CARDS = [
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8', 'h9', 'h10', 'h11', 'h12', 'h13',
    'd1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8', 'd9', 'd10', 'd11', 'd12', 'd13',
    's1', 's2', 's3', 's4', 's5', 's6', 's7', 's8', 's9', 's10', 's11', 's12', 's13',
    'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'c9', 'c10', 'c11', 'c12', 'c13',
    'j1'
]
PLAYERS_TWO = ["id1", "id2"]
PLAYERS_THREE = ["id1", "id2", "id3"]
PLAYERS_FOUR = ["id1", "id2", "id3", "id4"]
PLAYERS_ORDER_TWO = {"1": "", "2": ""}
PLAYERS_ORDER_THREE = {"1": "", "2": "", "3": ""}
PLAYERS_ORDER_FOUR = {"1": "", "2": "", "3": "", "4": ""}
PLAYERS_END_TWO = {"1": "", "2": ""}
PLAYERS_END_THREE = {"1": "", "2": "", "3": ""}
PLAYERS_END_FOUR = {"1": "", "2": "", "3": "", "4": ""}
POWER_CARDS = ["3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "1", "2"]  # カードの強さ(インデックスが若いほど弱い)
GAME_INFO = {
    "power_cards": "",
    "die_cards": "",
    "last_card": "",
    "last_player": "",
    "count": "",
    "revolution": "",
    "end_player": "",
    "players_order": "",
    "id1_cards": "",
    "id2_cards": "",
    "id3_cards": "",
    "id4_cards": ""
}

# 4人プレイを想定
class Board:

    def __init__(self, settings, game_info=False):
        """
        game_info = {
            power_cards: POWER_CSRDS,
            die_cards: DIE_CARDS,
            last_card: LAST_CARDS,
            last_player: LAST_PLAYER,
            count: COUNT,
            revolution: REVOLUTION,
            end_player: END_PLAYER,
            players_order: PLAYERS_ORDER,
            id1_cards: ID1_CARDS,
            id2_cards: ID2_CARDS,
            id3_cards: ID3_CARDS,
            id4_cards: ID4_CARDS
        }
        settings: {
            numPlayer: 4,
            autoSpeed: 0.5,
            isBan: true,
            isAvility: false,
            isStairs: true
            isReturnSpade3: false
        }
        """
        self.cards = CARDS.copy()
        if settings["numPlayer"] == 2:
            self.players = PLAYERS_TWO.copy()
        elif settings["numPlayer"] == 3:
            self.players = PLAYERS_THREE.copy()
        elif settings["numPlayer"] == 4:
            self.players = PLAYERS_FOUR.copy()
        else:
            print('プレイ人数が2-4人ではありません')
            raise Exception

        self.settings = settings

        if game_info == False:
            # ゲーム初期化処理
            self.power_cards = POWER_CARDS.copy()
            self.die_cards = []
            self.last_card = ""
            self.last_player = ""
            self.count = 1  # 何回流れたか
            self.turn = 1  # 流れるまでに何回アクション下か
            self.totalAction = 1  # 何回アクションしたか
            self.revolution = False
            self.players_order = self.make_players_order()
            if settings["numPlayer"] == 2:
                self.id1_cards, self.id2_cards = self.delivery_card()
                self.end_player = PLAYERS_END_TWO.copy()
            elif settings["numPlayer"] == 3:
                self.id1_cards, self.id2_cards, self.id3_cards = self.delivery_card()
                self.end_player = PLAYERS_END_THREE.copy()
            elif settings["numPlayer"] == 4:
                self.id1_cards, self.id2_cards, self.id3_cards, self.id4_cards = self.delivery_card()
                self.end_player = PLAYERS_END_FOUR.copy()
            else:
                print('プレイ人数が2-4人ではありません')
                raise Exception
        else:
            # ゲーム状態を反映する
            self.power_cards = game_info["power_cards"]
            self.die_cards = game_info["die_cards"]
            self.last_card = game_info["last_card"]
            self.last_player = game_info["last_player"]
            self.count = game_info["count"]
            self.count = game_info["turn"]
            self.revolution = game_info["revolution"]
            self.end_player = game_info["end_player"]
            self.players_order = game_info["players_order"]
            if settings["numPlayer"] == 2:
                self.id1_cards = game_info["id1_cards"]
                self.id2_cards = game_info["id2_cards"]
            elif settings["numPlayer"] == 3:
                self.id1_cards = game_info["id1_cards"]
                self.id2_cards = game_info["id2_cards"]
                self.id3_cards = game_info["id3_cards"]
            elif settings["numPlayer"] == 4:
                self.id1_cards = game_info["id1_cards"]
                self.id2_cards = game_info["id2_cards"]
                self.id3_cards = game_info["id3_cards"]
                self.id4_cards = game_info["id4_cards"]
            else:
                print('プレイ人数が2-4人ではありません')
                raise Exception

        if settings["numPlayer"] == 2:
            self.id_card_dict = {"id1": self.id1_cards, "id2": self.id2_cards}
        elif settings["numPlayer"] == 3:
            self.id_card_dict = {"id1": self.id1_cards, "id2": self.id2_cards, "id3": self.id3_cards}
        elif settings["numPlayer"] == 4:
            self.id_card_dict = {"id1": self.id1_cards, "id2": self.id2_cards, "id3": self.id3_cards, "id4": self.id4_cards}
        else:
            print('プレイ人数が2-4人ではありません')
            raise Exception

    def game_start(self):
        """
        --ゲームを開始する時のみ使用--
        最初のプレイヤーを決める
        最初のプレイヤーがアクション可能なカード(手持ちカード全部)

        戻り値
          next_player 次のプレイヤー
          next_actionable_card 次のアクション可能なカード(配列)
          game_info
          settings
        """

        first_player_id = self.players_order["1"]
        next_actionable_card = self.get_actionable(self.id_card_dict[first_player_id])
        game_info = self.get_game_state()
        settings = self.settings

        # ------ルール説明---------
        print(f"""-------------------ルール説明-------------------
プレイ人数: {settings["numPlayer"]}
コンピューターの速度: {settings["autoSpeed"]}秒
禁止上がり: {"あり" if settings["isBan"] else "なし"}
特殊カード: {"あり" if settings["isAvility"] else "なし"}
階段: {"あり" if settings["isStairs"] else "なし"}
スぺ3返し: {"あり" if settings["isReturnSpade3"] else "なし"}
------------------------------------------------""")

        # ------プレイ内容出力------
        print(f"""
-------------------ゲーム{str(self.count)}.{str(self.turn)}-------------------
最初にアクションするプレイヤー: {first_player_id}
使用可能なカード: {next_actionable_card}
最後に使用されたカード:
最後にskip以外のアクションしたプレイヤー: """)
        # --------------------------

        return first_player_id, next_actionable_card, game_info, settings
    
    # ゲーム情報を取得
    def get_game_state(self):
        """
        return
          game_info
          settings
        """
        game_info = GAME_INFO.copy()

        game_info["power_cards"] = self.power_cards
        game_info["die_cards"] = self.die_cards
        game_info["last_card"] = self.last_card
        game_info["last_player"] = self.last_player
        game_info["count"] = self.count
        game_info["turn"] = self.turn
        game_info["totalAction"] = self.totalAction
        game_info["revolution"] = self.revolution
        game_info["end_player"] = self.end_player
        game_info["players_order"] = self.players_order
        if self.settings["numPlayer"] == 2:
            game_info["id1_cards"] = self.id1_cards
            game_info["id2_cards"] = self.id2_cards
        elif self.settings["numPlayer"] == 3:
            game_info["id1_cards"] = self.id1_cards
            game_info["id2_cards"] = self.id2_cards
            game_info["id3_cards"] = self.id3_cards
        elif self.settings["numPlayer"] == 4:
            game_info["id1_cards"] = self.id1_cards
            game_info["id2_cards"] = self.id2_cards
            game_info["id3_cards"] = self.id3_cards
            game_info["id4_cards"] = self.id4_cards
        else:
            print('プレイ人数が2-4人ではありません')
            raise Exception

        return game_info
    
    # 順番決め
    def make_players_order(self):
        """
        return
          template: {"1": "id1", "2": "id4", "3": "id2", "4": "id3"}
        """
        #---一旦シャッフルする必要がないと感じたので順番は固定(コメントアウト)---

        # player_list = self.players.copy()
        # np.random.shuffle(player_list)

        # template = PLAYERS_ORDER.copy()
        # template["1"] = player_list.pop(0)
        # template["2"] = player_list.pop(0)
        # template["3"] = player_list.pop(0)
        # template["4"] = player_list.pop(0)

        #-------------------------------------------------------------

        if self.settings["numPlayer"] == 2:
            template = {"1": "id1", "2": "id2"}
        elif self.settings["numPlayer"] == 3:
            template = {"1": "id1", "2": "id2", "3": "id3"}
        elif self.settings["numPlayer"] == 4:
            template = {"1": "id1", "2": "id2", "3": "id3", "4": "id4"}
        else:
            print('プレイ人数が2-4人ではありません')
            raise Exception

        return template
    
    # 手札配り
    def delivery_card(self):
        """
        ロジック上、順番が一番目の人が1枚多い
        2プレイ:
            order1_cards: 1番目の人(27枚)
            order2_cards: 2番目の人(26枚)
        3プレイ:
            order1_cards: 1番目の人(18枚)
            order2_cards: 2番目の人(18枚)
            order3_cards: 3番目の人(17枚)
        4プレイ:
            order1_cards: 1番目の人(14枚)
            order2_cards: 2番目の人(13枚)
            order3_cards: 3番目の人(13枚)
            order4_cards: 4番目の人(13枚)

        return
          player1_cards: id1のカード
          player2_cards: id2のカード
          player3_cards: id3のカード
          player4_cards: id4のカード
        """
        cards = self.cards.copy()
        # players_order = self.players_order.copy()

        np.random.shuffle(cards)
        if self.settings["numPlayer"] == 2:
            order1_cards, order2_cards = cards[0:27], cards[27:53]
            # 並び替えx
            player1_cards = self.card_sort(order1_cards)
            player2_cards = self.card_sort(order2_cards)
            return player1_cards, player2_cards
        elif self.settings["numPlayer"] == 3:
            order1_cards, order2_cards, order3_cards = cards[0:18], cards[18:36], cards[36:53]
            # 並び替えx
            player1_cards = self.card_sort(order1_cards)
            player2_cards = self.card_sort(order2_cards)
            player3_cards = self.card_sort(order3_cards)
            return player1_cards, player2_cards, player3_cards
        elif self.settings["numPlayer"] == 4:
            order1_cards, order2_cards, order3_cards, order4_cards = cards[0:14], cards[14:27], cards[27:40], cards[40:53]
            # 並び替えx
            player1_cards = self.card_sort(order1_cards)
            player2_cards = self.card_sort(order2_cards)
            player3_cards = self.card_sort(order3_cards)
            player4_cards = self.card_sort(order4_cards)
            return player1_cards, player2_cards, player3_cards, player4_cards
        else:
            print('プレイ人数が2-4人ではありません')
            raise Exception
    
    # 1アクション
    def move(self, player_id, card):
        """
        引数
          player_id id1, id2など
          card アクションするカード(複数の場合、配列)
        戻り値
          next_player 次のプレイヤー
          next_actionable_card 次のアクション可能なカード(配列)
          game_done Trueの場合ゲーム終了
          game_info
          settings
        
        処理の流れ
          1. 次のプレイヤーを取得
          2.0 スキップではない場合の処理
          2. 捨てカードに追加
          3. プレイヤーのカードから削除
          4. 最後に捨てられたカードを更新
          5. 革命判定
          6. アガリ判定
          7. ゲーム終了判定
          8. 次のアクション可能なカードを取得
        """
        # ------プレイ内容出力------
        print(f"""
アクションしたプレイヤー: {player_id}
アクションしたカード: {card}
------------------------------------------------
""")
        # --------------------------

        # 1. 次のプレイヤーを取得
        next_player = ""
        now_player_key = [key for key, value in self.players_order.items() if value == player_id]
        if now_player_key == []:
            # 存在しない場合エラー
            print("error: 次のプレイヤーを選択できませんでした")
        else:
            now_player_key = now_player_key[0]
        
        # プレイヤー人数
        end_player_num = 0
        for i in self.end_player.values():
            if i != "":
                end_player_num+=1
        player_num = self.settings["numPlayer"] - end_player_num
        # 次のプレイヤーのインデックスを取得
        next_player_key = ""
        if int(now_player_key) == player_num:
            next_player_key = "1"
        else:
            next_player_key = str(int(now_player_key)+1)
        next_player = self.players_order[next_player_key]

        self.totalAction += 1  # 総プレイ回数をインクリメント

        # 2.0 スキップではない場合の処理
        if card != 'skip':
            # アクションしたカードの数字を取得
            card_num = ""
            if type(card) == list:
                # カードを取り出す(ex:h1)
                for j in card.copy():
                    if j != 'j1':
                        card_num = j
                        break
                # 数字を取り出す
                card_num = int(card_num[1:])
            else:
                if card == 'j1':
                    card_num = 99  # jokerの場合は99
                else:
                    # 数字を取り出す
                    card_num = int(card[1:])

            player_cards = self.id_card_dict[player_id]  # アクションしたプレイヤーの手札を取得
            # 複数枚の場合
            if type(card) == list:
                for i in card:
                    self.die_cards.append(i)  # 捨てカードに追加
                    if i in player_cards:  # プレイヤーの手札から削除
                        self.id_card_dict[player_id].remove(i)
                    else:
                        print("error: 手札に存在しないカードです")
            else:
                # 1枚の場合
                self.die_cards.append(card)
                if card in player_cards:  # プレイヤーの手札から削除
                    self.id_card_dict[player_id].remove(card)
                else:
                    print("error: 手札に存在しないカードです")

            # 最後に捨てられたカードを更新
            self.last_card = card
            self.last_player = player_id
            self.turn += 1  # ターンをインクリ

            # 4枚以上の場合革命
            if len(card) >= 4:
                self.power_cards.reverse()
                if self.revolution:
                    self.revolution = False
                else:
                    self.revolution = True

            # 上がり判定
            if len(self.id_card_dict[player_id]) == 0:
                """
                禁止上がりかどうか
                1. joker
                2. 2(not 革命時)
                3. 3(革命時)
                """
                is_ban = False
                if card_num == 99:
                    is_ban = True
                elif card_num == 2 and not self.revolution:
                    is_ban = True
                elif card_num == 3 and self.revolution:
                    is_ban = True

                # 禁止上がりで上がった場合4着から順位を決める
                if is_ban:
                    last_order_key = ""
                    for key, value in self.end_player.items():
                        # 最後の順位を取得する
                        if value == "":
                            last_order_key = key
                    self.end_player[last_order_key] = player_id
                # 禁止上がりではない場合1着から順位を決める
                else:
                    # 上がったプレイヤーに追加
                    for key, value in self.end_player.items():
                        # 順位が決まっていたら次
                        if value != "":
                            continue
                        else:
                            self.end_player[key] = player_id
                            break
                # 残り何人プレイか
                end_player_num = 0
                for i in self.end_player.values():
                    if i != "":
                        end_player_num+=1
                player_num = self.settings["numPlayer"] - end_player_num

                # 残り一人の場合ゲーム終了
                if player_num == 1:
                    # 上がったプレイヤーに追加
                    for key, value in self.end_player.items():
                        # 順位が決まっていたら次
                        if value != "":
                            continue
                        else:
                            self.end_player[key] = next_player
                    print('-------------------ゲーム終了-------------------')
                    for key, value in self.end_player.items():
                        print(f'{key}位: {value}')
                    print(f"""
総プレイ回数: {self.totalAction}
------------------------------------------------""")
                    game_info = self.get_game_state()
                    settings = self.settings

                    return "", [], True, game_info, settings

                # プレイヤーの順番を再計算
                players_order_value = self.players_order.values()  # 上がる前のプレイヤー順番のplayerIDを取得
                count = 1
                next_players_order = {}
                for i in players_order_value:
                    new_key = f"{count}"
                    # 上がったプレイヤーに存在する場合はスキップ
                    if i in self.end_player.values():
                        continue
                    else:
                        next_players_order[new_key] = i
                        count += 1
                self.players_order = next_players_order  # 更新
                self.last_player = next_player

        else:
            # skipの場合、流れるかどうかのチェック
            # print('skip check: ')
            # print('next_player: ', next_player)
            # print('self.last_player: ', self.last_player)
            if next_player == self.last_player:
                print(f'ゲーム{self.count}は流れました\n')
                self.last_card = ""
                self.last_player = ""
                self.count += 1
                self.turn = 1  # 流れたらターンを初期化
        
        # 次のアクション可能なカードを取得
        next_player_card = self.id_card_dict[next_player]  # 次のアクションするプレイヤーの手札を取得
        next_actionable_card = []
        next_actionable_card = self.get_actionable(next_player_card)

        # ------プレイ内容出力------
        print(f"""-------------------ゲーム{str(self.count)}.{str(self.turn)}-------------------
アクションするプレイヤー: {next_player}
使用可能なカード: {next_actionable_card}
最後に使用されたカード: {self.last_card}
最後にskip以外のアクションしたプレイヤー: {self.last_player}""")
        # --------------------------

        game_info = self.get_game_state()
        settings = self.settings

        return next_player, next_actionable_card, False, game_info, settings
        

    # アクション可能なカードを取得
    def get_actionable(self, cards):
        """
        ※jokerと普通のカードを分けて管理していることに注意する
        引数
          cards 手札
        戻り値
          actionable_cards アクション可能なカードの配列(ex: ["h1", "h5", ["c6", "d6"]])
        """
#         print(f"""
#  get_actionable is called.
#  cards: {cards}     
#         """)
        actionable_cards = []

        # 手札にjokerが存在するかの判定
        joker_value = ""
        joker_flg = False
        if "j1" in cards:
            joker_flg = True
            joker_value = "j1"

        # カードを数値ごとに整理(jokerはcard_dictに貼ってないのに注意!!!)
        card_dict = {
            "1":[], "2":[], "3":[], "4":[], "5":[], "6":[], "7":[], "8":[], "9":[], "10":[], "11":[], "12":[], "13":[]
        }
        for card in cards:
            if card == 'j1':
                continue
            num = card[1:]
            card_dict[str(num)].append(card)

        # print('card_dict: ', card_dict)

        # 最後に捨てられたカードが空文字の時(0枚の時)、どんなカードでもOK
        if self.last_card == "":
            # 1枚のパターン
            actionable_cards = cards.copy()
            for key, value in card_dict.items():
                # jokerがない時
                if not joker_flg:
                    # 2枚のパターン
                    if len(value) == 2:
                        actionable_cards.append(value)
                    elif len(value) == 3:
                        # 3枚のパターン
                        actionable_cards.append([value[0], value[1]])  # 2枚
                        actionable_cards.append([value[0], value[2]])  # 2枚
                        actionable_cards.append([value[1], value[2]])  # 2枚
                        actionable_cards.append([value[0], value[1], value[2]])  # 3枚
                    elif len(value) == 4:
                        # 4枚のパターン
                        actionable_cards.append([value[0], value[1]])  # 2枚
                        actionable_cards.append([value[0], value[2]])  # 2枚
                        actionable_cards.append([value[0], value[3]])  # 2枚
                        actionable_cards.append([value[1], value[2]])  # 2枚
                        actionable_cards.append([value[1], value[3]])  # 2枚
                        actionable_cards.append([value[2], value[3]])  # 2枚
                        actionable_cards.append([value[0], value[1], value[2]])  # 3枚
                        actionable_cards.append([value[0], value[1], value[3]])  # 3枚
                        actionable_cards.append([value[0], value[2], value[3]])  # 3枚
                        actionable_cards.append([value[1], value[2], value[3]])  # 3枚
                        actionable_cards.append([value[0], value[1], value[2], value[3]])  # 4枚
                else:
                    # 1枚のパターン
                    if len(value) == 1:
                        actionable_cards.append([value[0], joker_value])  # 2枚
                    # 2枚のパターン
                    if len(value) == 2:
                        actionable_cards.append(value)  # 2枚
                        actionable_cards.append([value[0], joker_value])  # 2枚
                        actionable_cards.append([value[1], joker_value])  # 2枚
                        actionable_cards.append([value[0], value[1], joker_value])  # 3枚
                    elif len(value) == 3:
                        # 3枚のパターン
                        actionable_cards.append([value[0], value[1]])  # 2枚
                        actionable_cards.append([value[0], value[2]])  # 2枚
                        actionable_cards.append([value[0], joker_value])  # 2枚
                        actionable_cards.append([value[1], value[2]])  # 2枚
                        actionable_cards.append([value[1], joker_value])  # 2枚
                        actionable_cards.append([value[2], joker_value])  # 2枚
                        actionable_cards.append([value[0], value[1], value[2]])  # 3枚
                        actionable_cards.append([value[0], value[1], joker_value])  # 3枚
                        actionable_cards.append([value[0], value[2], joker_value])  # 3枚
                        actionable_cards.append([value[1], value[2], joker_value])  # 3枚
                        actionable_cards.append([value[0], value[1], value[2], joker_value])  # 4枚
                    elif len(value) == 4:
                        # 4枚のパターン
                        actionable_cards.append([value[0], value[1]])  # 2枚
                        actionable_cards.append([value[0], value[2]])  # 2枚
                        actionable_cards.append([value[0], value[3]])  # 2枚
                        actionable_cards.append([value[0], joker_value])  # 2枚
                        actionable_cards.append([value[1], value[2]])  # 2枚
                        actionable_cards.append([value[1], value[3]])  # 2枚
                        actionable_cards.append([value[1], joker_value])  # 2枚
                        actionable_cards.append([value[2], value[3]])  # 2枚
                        actionable_cards.append([value[2], joker_value])  # 2枚
                        actionable_cards.append([value[3], joker_value])  # 2枚
                        actionable_cards.append([value[0], value[1], value[2]])  # 3枚
                        actionable_cards.append([value[0], value[1], value[3]])  # 3枚
                        actionable_cards.append([value[0], value[1], joker_value])  # 3枚
                        actionable_cards.append([value[0], value[2], value[3]])  # 3枚
                        actionable_cards.append([value[0], value[2], joker_value])  # 3枚
                        actionable_cards.append([value[0], value[3], joker_value])  # 3枚
                        actionable_cards.append([value[1], value[2], value[3]])  # 3枚
                        actionable_cards.append([value[1], value[2], joker_value])  # 3枚
                        actionable_cards.append([value[1], value[3], joker_value])  # 3枚
                        actionable_cards.append([value[2], value[3], joker_value])  # 3枚
                        actionable_cards.append([value[0], value[1], value[2], value[3]])  # 4枚
                        actionable_cards.append([value[0], value[1], value[2], joker_value])  # 4枚
                        actionable_cards.append([value[0], value[1], value[3], joker_value])  # 4枚
                        actionable_cards.append([value[0], value[2], value[3], joker_value])  # 4枚
                        actionable_cards.append([value[1], value[2], value[3], joker_value])  # 4枚
                        actionable_cards.append([value[0], value[1], value[2], value[3], joker_value])  # 5枚
                
            return actionable_cards
        
        # 最後に捨てられたカード番号を取得
        # print("last_card: ", self.last_card)
        last_num = self.last_card
        if type(last_num) == list:
            # カードを取り出す(ex:h1)
            for card in last_num:
                if card != 'j1':
                    last_num = card
                    break
            # 数字を取り出す
            last_num = int(last_num[1:])
        else:
            if last_num == 'j1':
                last_num = 99  # jokerの場合は99
            else:
                # 数字を取り出す
                last_num = int(last_num[1:])
        # print("last_num: ", last_num)

        # 最後に捨てられたカード枚数を取得
        if type(self.last_card) == list:
            last_count = len(self.last_card)
        else:
            last_count = 1

        # カードの強さを取得
        power_cards = self.power_cards
        # 最後に捨てられたカードの強さのインデックスを取得
        if last_num == 99:
            power_last_num_index = 99
        else:
            power_last_num_index = int(power_cards.index(str(last_num)))

        # 1枚の場合
        if last_count == 1:
            for card in cards:
                if card == 'j1':
                    continue
                num = card[1:]
                # カードの強さのインデックスを取得
                power_num_index = int(power_cards.index(num))

                # print("power: ", power_num_index)
                # print("last_power: ", power_last_num_index)

                # 最後に捨てられたカードより強い場合、戻り値の配列に追加
                if power_last_num_index < power_num_index :
                    actionable_cards.append(card)
            # jokeが存在する場合
            if joker_flg:
                actionable_cards.append(joker_value)
            return actionable_cards
        elif last_count == 2:
            # 2枚の場合
            for key, value in card_dict.items():
                # カードの強さのインデックスを取得
                power_num_index = int(power_cards.index(key))
                if power_last_num_index >= power_num_index:
                    continue
                # jokerがない時
                if not joker_flg:
                    if len(value) == 2:
                        actionable_cards.append(value)
                    elif len(value) == 3:
                        actionable_cards.append([value[0], value[1]])
                        actionable_cards.append([value[1], value[2]])
                        actionable_cards.append([value[2], value[0]])
                    elif len(value) == 4:
                        actionable_cards.append([value[0], value[1]])
                        actionable_cards.append([value[0], value[2]])
                        actionable_cards.append([value[0], value[3]])
                        actionable_cards.append([value[1], value[2]])
                        actionable_cards.append([value[1], value[3]])
                        actionable_cards.append([value[2], value[3]])
                else:
                    if len(value) == 1:
                        actionable_cards.append([value[0], joker_value])
                    if len(value) == 2:
                        actionable_cards.append(value)
                        actionable_cards.append([value[0], joker_value])
                        actionable_cards.append([value[1], joker_value])
                    elif len(value) == 3:
                        actionable_cards.append([value[0], value[1]])
                        actionable_cards.append([value[0], joker_value])
                        actionable_cards.append([value[1], value[2]])
                        actionable_cards.append([value[1], joker_value])
                        actionable_cards.append([value[2], value[0]])
                        actionable_cards.append([value[2], joker_value])
                    elif len(value) == 4:
                        actionable_cards.append([value[0], value[1]])
                        actionable_cards.append([value[0], value[2]])
                        actionable_cards.append([value[0], value[3]])
                        actionable_cards.append([value[0], joker_value])
                        actionable_cards.append([value[1], value[2]])
                        actionable_cards.append([value[1], value[3]])
                        actionable_cards.append([value[1], joker_value])
                        actionable_cards.append([value[2], value[3]])
                        actionable_cards.append([value[2], joker_value])
                        actionable_cards.append([value[3], joker_value])

        elif last_count == 3:
            # 3枚の場合
            for key, value in card_dict.items():
                # カードの強さのインデックスを取得
                power_num_index = int(power_cards.index(key))
                if power_last_num_index >= power_num_index:
                    continue
                # jokerがない時
                if not joker_flg:
                    if len(value) == 3:
                        actionable_cards.append(value)
                    elif len(value) == 4:
                        actionable_cards.append([value[0], value[1], value[2]])
                        actionable_cards.append([value[0], value[1], value[3]])
                        actionable_cards.append([value[0], value[2], value[3]])
                        actionable_cards.append([value[1], value[2], value[3]])
                else:
                    if len(value) == 2:
                        actionable_cards.append([value[0], value[1], joker_value])
                    if len(value) == 3:
                        actionable_cards.append(value)
                        actionable_cards.append([value[0], value[1], joker_value])
                        actionable_cards.append([value[0], value[2], joker_value])
                        actionable_cards.append([value[1], value[2], joker_value])
                    elif len(value) == 4:
                        actionable_cards.append([value[0], value[1], value[2]])
                        actionable_cards.append([value[0], value[1], value[3]])
                        actionable_cards.append([value[0], value[1], joker_value])
                        actionable_cards.append([value[0], value[2], value[3]])
                        actionable_cards.append([value[0], value[2], joker_value])
                        actionable_cards.append([value[0], value[3], joker_value])
                        actionable_cards.append([value[1], value[2], value[3]])
                        actionable_cards.append([value[1], value[2], joker_value])
                        actionable_cards.append([value[1], value[3], joker_value])
                        actionable_cards.append([value[2], value[3], joker_value])
        elif last_count == 4:
            # 4枚の場合
            for key, value in card_dict.items():
                # カードの強さのインデックスを取得
                power_num_index = int(power_cards.index(key))
                if power_last_num_index >= power_num_index:
                    continue
                # jokerがない時
                if not joker_flg:
                    if len(value) == 4:
                        actionable_cards.append(value)
                else:
                    if len(value) == 3:
                        actionable_cards.append([value[0], value[1], value[2], joker_value])
                    if len(value) == 4:
                        actionable_cards.append(value)
                        actionable_cards.append([value[0], value[1], value[2], joker_value])
                        actionable_cards.append([value[0], value[1], value[3], joker_value])
                        actionable_cards.append([value[0], value[2], value[3], joker_value])
                        actionable_cards.append([value[1], value[2], value[3], joker_value])
        elif last_count == 5:
            # joker1つと4枚使用時
            actionable_cards = []
        else:
            print("error: 最後に捨てられたカードが6枚異常なのは異常です")
        
        return actionable_cards
    
    def card_sort(self, card_list):
        """
        数字の優劣 [3 ~ 13, 1, 2, j]
        マークの優劣 なし
        """
        cards = card_list.copy()

        result_card = []

        # joker flg
        is_joker = True if 'j1' in cards else False

        # カードを数値ごとに整理(jokerはcard_dictに貼ってないのに注意!!!)
        card_dict = {
            "1":[], "2":[], "3":[], "4":[], "5":[], "6":[], "7":[], "8":[], "9":[], "10":[], "11":[], "12":[], "13":[]
        }
        for card in cards:
            if card == 'j1':
                continue
            num = card[1:]
            card_dict[str(num)].append(card)
        
        # 3-13
        key_list = ["3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "1", "2"]
        for i in key_list:
            for j in card_dict[i]:
                result_card.append(j)
        
        # joker
        if (is_joker):
            result_card.append("j1")
        
        return result_card
        
        
        


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
        
# -----------------------mainでこのファイルが実行されたときの処理-----------------------

# 設定
if __name__ == "__main__":
    settings = {
        "numPlayer": 4,
        "autoSpeed": 0.5,
        "isBan": True,
        "isAvility": False,
        "isStairs": False,
        "isReturnSpade3": False
    }
    players = {"id1": RandomPlayer(), "id2": RandomPlayer(), "id3": RandomPlayer(), "id4": RandomPlayer()}
    board = Board(settings=settings)
    next_player_id, next_actionable_cards, game_info, settings = board.game_start()
    while True:
        # action_card = []
        # action_card.append(next_actionable_cards)

        player = players[next_player_id]
        action_card = player.get_action_card(next_actionable_cards)
        next_player_id, next_actionable_cards, game_done, game_info, settings = board.move(next_player_id, action_card)

        if game_done == True:
            break


# -----------------------mainでこのファイルが実行されたときの処理-----------------------