import unittest

from game import Board, RandomPlayer, HumanPlayer
 
class GameTest(unittest.TestCase):
    """
    テストコードを書くにおいて
    関数名の最初に"test"を入れないとテスト関数として認識されない
    """
    @classmethod
    def setUpClass(self):
        # *** 全体前処理 ***
        self.randomplayer, humanplayer = RandomPlayer(), HumanPlayer()
        self.players = {"id1": RandomPlayer(), "id2": RandomPlayer(), "id3": RandomPlayer(), "id4": RandomPlayer()}
        self.CARDS = [
            'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8', 'h9', 'h10', 'h11', 'h12', 'h13',
            'd1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8', 'd9', 'd10', 'd11', 'd12', 'd13',
            's1', 's2', 's3', 's4', 's5', 's6', 's7', 's8', 's9', 's10', 's11', 's12', 's13',
            'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'c9', 'c10', 'c11', 'c12', 'c13',
            'j1'
        ]
        self.SETTINGS = {
            "numPlayer": 4,
            "playerType1": "manual",
            "playerType2": "manual",
            "playerType3": "manual",
            "playerType4": "manual",
            "autoSpeed": 0.5,
            "isBan": True,
            "isAvility": False,
            "isStairs": False,
            "isReturnSpade3": False
        }
 
    @classmethod
    def tearDownClass(self):
        # *** 全体後処理 ***
        pass
 
    def setUp(self):
        # テスト前処理
        self.board = Board(self.players, self.SETTINGS)
 
    def tearDown(self):
        # テスト後処理
        del(self.board)

    # ----------------------------------init()----------------------------------
    
    def test_board_init(self):
        """
        初期化処理
        """
        self.assertEqual(self.board.cards, self.CARDS)  # カード全種類
        self.assertEqual(self.board.die_cards, [])  # 過去のステカード
        self.assertEqual(self.board.last_card, "")  # 最後のステカード
        self.assertEqual(self.board.last_player, "")
        self.assertEqual(self.board.count, 1)
        self.assertEqual(self.board.end_player, {"1": "", "2": "", "3": "", "4": ""})  # 上がった人
        self.assertEqual(self.board.players, ["id1", "id2", "id3", "id4"])

        # playする順番
        players = self.board.players
        for key, value in self.board.players_order.items():
            # {"1": "", "2": "", "3":, "4": ""}の形かどうか(keyのテスト)
            if key not in ["1", "2", "3", "4"]:
                self.assertTrue(False)
            # valueのテスト
            if value not in players:
                self.assertTrue(False)
            else:
                # 存在したプレイヤーを配列から削除
                players.remove(value)
            print('board_init.ok')

        # 手札
        cards = self.CARDS.copy()
        # カードの数
        # print(f"id1: {self.board.id1_cards}")
        # print(f"cards: {self.board.id_card_dict}")
        # print(f"id2: {self.board.id2_cards}")
        # print(f"id3: {self.board.id3_cards}")
        # print(f"id4: {self.board.id4_cards}")
        card_count = len(self.board.id1_cards) + len(self.board.id2_cards) + len(self.board.id3_cards) + len(self.board.id4_cards)
        self.assertEqual(53, card_count)
        # 全てのカードがあるか
        for card in self.board.id1_cards:
            if card in cards:
                cards.remove(card)
            else:
                self.assertTrue(False)
        for card in self.board.id2_cards:
            if card in cards:
                cards.remove(card)
            else:
                self.assertTrue(False)
        for card in self.board.id3_cards:
            if card in cards:
                cards.remove(card)
            else:
                self.assertTrue(False)
        for card in self.board.id4_cards:
            if card in cards:
                cards.remove(card)
            else:
                self.assertTrue(False)

        # カードプレイヤー辞書
        self.assertEqual(self.board.id_card_dict["id1"], self.board.id1_cards)
        self.assertEqual(self.board.id_card_dict["id2"], self.board.id2_cards)
        self.assertEqual(self.board.id_card_dict["id3"], self.board.id3_cards)
        self.assertEqual(self.board.id_card_dict["id4"], self.board.id4_cards)

    # ----------------------------------game_start()----------------------------------

    def test_game_start(self):
        # 最初のプレイヤーのカードをテスト用に更新
        first_card = [
            'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8', 'h9', 'h10', 'h11', 'h12', 'h13',
            's1'
        ]
        # 最初のプレイヤー
        result_player_id = self.board.players_order["1"]
        self.board.id_card_dict[result_player_id] = first_card

        result_card = [
            'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8', 'h9', 'h10', 'h11', 'h12', 'h13',
            's1',
            ['h1', 's1']
        ]
        first_player_id, next_actionable_card, game_info = self.board.game_start()
        
        self.assertEqual(first_player_id, result_player_id)
        self.assertEqual(next_actionable_card, result_card)
    
    # ----------------------------------get_actionable()----------------------------------
    
    def test_get_actionable_empty(self):
        """
        最後に捨てられたカードがない時
          1, 2, 3, 4枚のカードが選択できる
        """
        # 最初のプレイヤーのカードをテスト用に更新
        first_card = [
            'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8', 'h9', 'h10', 'h11', 'h12', 'h13',
            's12', 's13', 's1',
            'd13', 'd1',
            'c1',
        ]
        # 最後に捨てられたカードを更新
        self.board.last_card = ""
        result = self.board.get_actionable(first_card)

        exp = [
            'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8', 'h9', 'h10', 'h11', 'h12', 'h13',
            's12', 's13', 's1',
            'd13', 'd1',
            'c1',
            ['h12', 's12'],
            ['h13', 's13'], ['h13', 'd13'], ['s13', 'd13'], ['h13', 's13', 'd13'],
            ['h1', 's1'], ['h1', 'd1'], ['h1', 'c1'], ['s1', 'd1'], ['s1', 'c1'], ['d1', 'c1'],
            ['h1', 's1', 'd1'], ['h1', 's1', 'c1'], ['h1', 'd1', 'c1'], ['s1', 'd1', 'c1'],
            ['h1', 's1', 'd1', 'c1']
        ]

        # 個数が正しいか
        self.assertEqual(len(result), len(exp))
        # 値が正しいか
        for card in result:
            # 1枚の時
            if type(card) == str:
                if card in result:
                    self.assertTrue(True)
                else:
                    self.assertTrue(False)
            # 複数枚の時(配列)
            elif type(card) == list:
                # set関数は二重配列の時使えないため
                flg = False
                for exp_card in exp:
                    if set(exp_card) == set(card):
                        flg = True
                        break
                if flg == True:
                    self.assertTrue(True)
                else:
                    print(f"result_card: {card}¥nexp_card: {exp_card}")
                    self.assertTrue(False)
    
    def test_get_actionable_empty_joker(self):
        """
        最後に捨てられたカードがない時(jokerあり)
          1, 2, 3, 4枚のカードが選択できる
        """
        """
        最初のプレイヤーのカードをテスト用に更新
        12: 1つ
        13: 2つ
        1:  3つ
        2:  4つ
        """
        first_card = [
            'h12', 'h13', 'h1', 'h2', 
            's13', 's1', 's2',
            'd1', 'd2',
            'c2',
            'j1'
        ]
        # 最後に捨てられたカードを更新
        self.board.last_card = ""
        result = self.board.get_actionable(first_card)

        exp = [
            'h12', 'h13', 'h1', 'h2', 
            's13', 's1', 's2',
            'd1', 'd2',
            'c2',
            'j1',
            ['h12', 'j1'], 
            ['h13', 'j1'], ['s13', 'j1'], ['h13', 's13'], ['h13', 's13', 'j1'],
            ['h1', 's1'], ['h1', 'd1'], ['h1', 'j1'], ['s1', 'd1'], ['s1', 'j1'], ['d1', 'j1'],
            ['h1', 's1', 'd1'], ['h1', 's1', 'j1'], ['h1', 'd1', 'j1'], ['s1', 'd1', 'j1'],
            ['h1', 's1', 'd1', 'j1'],
            ['h2', 's2'], ['h2', 'd2'], ['h2', 'c2'], ['h2', 'j1'], ['s2', 'd2'], ['s2', 'c2'], ['s2', 'j1'], ['d2', 'c2'], ['d2', 'j1'], ['c2', 'j1'],
            ['h2', 's2', 'd2'], ['h2', 's2', 'c2'], ['h2', 's2', 'j1'], ['h2', 'd2', 'c2'], ['h2', 'd2', 'j1'],
            ['h2', 'c2', 'j1'], ['s2', 'd2', 'c2'], ['s2', 'd2', 'j1'], ['s2', 'c2', 'j1'], ['d2', 'c2', 'j1'],
            ['h2', 's2', 'd2', 'c2'], ['h2', 's2', 'c2', 'j1'], ['h2', 's2', 'd2', 'j1'], ['h2', 'd2', 'c2', 'j1'], ['s2', 'd2', 'c2', 'j1'],
            ['h2', 's2', 'd2', 'c2', 'j1']
        ]

        # 個数が正しいか
        self.assertEqual(len(result), len(exp))
        # 値が正しいか
        for card in result:
            # 1枚の時
            if type(card) == str:
                if card in result:
                    self.assertTrue(True)
                else:
                    self.assertTrue(False)
            # 複数枚の時(配列)
            elif type(card) == list:
                # set関数は二重配列の時使えないため
                flg = False
                for exp_card in exp:
                    if set(exp_card) == set(card):
                        flg = True
                        break
                if flg == True:
                    self.assertTrue(True)
                else:
                    print(f"result_card: {card}¥nexp_card: {exp_card}")
                    self.assertTrue(False)

    def test_get_actionable_empty_revolution(self):
        """
        最後に捨てられたカードがない時(革命時)
          1, 2, 3, 4枚のカードが選択できる
        """
        """
        最初のプレイヤーのカードをテスト用に更新
        12: 1つ
        13: 2つ
        1:  3つ
        2:  4つ
        """
        first_card = [
            'h12', 'h13', 'h1', 'h2', 
            's13', 's1', 's2',
            'd1', 'd2',
            'c2',
            'j1'
        ]
        # 最後に捨てられたカードを更新
        self.board.last_card = ""
        # 革命
        self.board.power_cards.reverse()
        self.board.revolution = True
        result = self.board.get_actionable(first_card)

        exp = [
            'h12', 'h13', 'h1', 'h2', 
            's13', 's1', 's2',
            'd1', 'd2',
            'c2',
            'j1',
            ['h12', 'j1'], 
            ['h13', 'j1'], ['s13', 'j1'], ['h13', 's13'], ['h13', 's13', 'j1'],
            ['h1', 's1'], ['h1', 'd1'], ['h1', 'j1'], ['s1', 'd1'], ['s1', 'j1'], ['d1', 'j1'],
            ['h1', 's1', 'd1'], ['h1', 's1', 'j1'], ['h1', 'd1', 'j1'], ['s1', 'd1', 'j1'],
            ['h1', 's1', 'd1', 'j1'],
            ['h2', 's2'], ['h2', 'd2'], ['h2', 'c2'], ['h2', 'j1'], ['s2', 'd2'], ['s2', 'c2'], ['s2', 'j1'], ['d2', 'c2'], ['d2', 'j1'], ['c2', 'j1'],
            ['h2', 's2', 'd2'], ['h2', 's2', 'c2'], ['h2', 's2', 'j1'], ['h2', 'd2', 'c2'], ['h2', 'd2', 'j1'],
            ['h2', 'c2', 'j1'], ['s2', 'd2', 'c2'], ['s2', 'd2', 'j1'], ['s2', 'c2', 'j1'], ['d2', 'c2', 'j1'],
            ['h2', 's2', 'd2', 'c2'], ['h2', 's2', 'c2', 'j1'], ['h2', 's2', 'd2', 'j1'], ['h2', 'd2', 'c2', 'j1'], ['s2', 'd2', 'c2', 'j1'],
            ['h2', 's2', 'd2', 'c2', 'j1']
        ]

        # 個数が正しいか
        self.assertEqual(len(result), len(exp))
        # 値が正しいか
        for card in result:
            # 1枚の時
            if type(card) == str:
                if card in result:
                    self.assertTrue(True)
                else:
                    self.assertTrue(False)
            # 複数枚の時(配列)
            elif type(card) == list:
                # set関数は二重配列の時使えないため
                flg = False
                for exp_card in exp:
                    if set(exp_card) == set(card):
                        flg = True
                        break
                if flg == True:
                    self.assertTrue(True)
                else:
                    print(f"result_card: {card}¥nexp_card: {exp_card}")
                    self.assertTrue(False)

    def test_get_actionable_one(self):
        """
        最後に捨てられたカードが1枚の時
          1枚のカードが選択できる
        """
        # 最初のプレイヤーのカードをテスト用に更新
        first_card = [
            'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8', 'h9', 'h10', 'h11', 'h12', 'h13',
            's12', 's13', 's1',
            'd13', 'd1',
            'c1',
        ]
        # 最後に捨てられたカードが「d12」
        self.board.last_card = "d12"
        result = self.board.get_actionable(first_card)

        exp = [
            'h1', 'h2', 'h13',
            's13', 's1',
            'd13', 'd1',
            'c1'
        ]

        # 個数が正しいか
        self.assertEqual(len(result), len(exp))
        # 値が正しいか
        for card in result:
            # 1枚の時
            if type(card) == str:
                if card in result:
                    self.assertTrue(True)
                else:
                    self.assertTrue(False)
            # 複数枚の時(配列)
            elif type(card) == list:
                # set関数は二重配列の時使えないため
                flg = False
                for exp_card in exp:
                    if set(exp_card) == set(card):
                        flg = True
                        break
                if flg == True:
                    self.assertTrue(True)
                else:
                    print(f"result_card: {card}¥nexp_card: {exp_card}")
                    self.assertTrue(False)

    def test_get_actionable_one_joker(self):
        """
        最後に捨てられたカードが1枚の時(jokerあり)
          1枚のカードが選択できる
        """
        """
        最初のプレイヤーのカードをテスト用に更新
        12: 1つ
        13: 2つ
        1:  3つ
        2:  4つ
        """
        first_card = [
            'h12', 'h13', 'h1', 'h2', 
            's13', 's1', 's2',
            'd1', 'd2',
            'c2',
            'j1'
        ]
        # 最後に捨てられたカードを更新
        self.board.last_card = "s12"
        result = self.board.get_actionable(first_card)

        exp = [
            'h13', 'h1', 'h2', 
            's13', 's1', 's2',
            'd1', 'd2',
            'c2',
            'j1',
        ]

        # 個数が正しいか
        self.assertEqual(len(result), len(exp))
        # 値が正しいか
        for card in result:
            # 1枚の時
            if type(card) == str:
                if card in result:
                    self.assertTrue(True)
                else:
                    self.assertTrue(False)
            # 複数枚の時(配列)
            elif type(card) == list:
                # set関数は二重配列の時使えないため
                flg = False
                for exp_card in exp:
                    if set(exp_card) == set(card):
                        flg = True
                        break
                if flg == True:
                    self.assertTrue(True)
                else:
                    print(f"result_card: {card}¥nexp_card: {exp_card}")
                    self.assertTrue(False)

    def test_get_actionable_one_revolution(self):
        """
        最後に捨てられたカードが1枚の時(革命時)
          1枚のカードが選択できる
        """
        """
        最初のプレイヤーのカードをテスト用に更新
        12: 1つ
        13: 2つ
        1:  3つ
        2:  4つ
        """
        first_card = [
            'h12', 'h13', 'h1', 'h2', 
            's13', 's1', 's2',
            'd1', 'd2',
            'c2',
            'j1'
        ]
        # 最後に捨てられたカードを更新
        self.board.last_card = "c1"
        # 革命
        self.board.power_cards.reverse()
        self.board.revolution = True
        result = self.board.get_actionable(first_card)

        exp = [
            'h12', 'h13',
            's13',
            'j1',
        ]

        # 個数が正しいか
        self.assertEqual(len(result), len(exp))
        # 値が正しいか
        for card in result:
            # 1枚の時
            if type(card) == str:
                if card in result:
                    self.assertTrue(True)
                else:
                    self.assertTrue(False)
            # 複数枚の時(配列)
            elif type(card) == list:
                # set関数は二重配列の時使えないため
                flg = False
                for exp_card in exp:
                    if set(exp_card) == set(card):
                        flg = True
                        break
                if flg == True:
                    self.assertTrue(True)
                else:
                    print(f"result_card: {card}¥nexp_card: {exp_card}")
                    self.assertTrue(False)
    
    def test_get_actionable_one_joker2(self):
        """
        最後に捨てられたカードが1枚jokerの時
          流れる
        """
        """
        最初のプレイヤーのカードをテスト用に更新
        12: 1つ
        13: 2つ
        1:  3つ
        2:  4つ
        """
        first_card = [
            'h12', 'h13', 'h1', 'h2', 
            's13', 's1', 's2',
            'd1', 'd2',
            'c2'
        ]
        # 最後に捨てられたカードを更新
        self.board.last_card = "j1"
        try:
            result = self.board.get_actionable(first_card)

            # 個数が正しいか
            self.assertEqual(len(result), 0)
            # 値が正しいか
            self.assertEqual(result, [])
        except:
            self.assertTrue(False)

    def test_get_actionable_two(self):
        """
        最後に捨てられたカードが2枚の時
          2枚のカードが選択できる
        """
        # 最初のプレイヤーのカードをテスト用に更新
        first_card = [
            'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8', 'h9', 'h10', 'h11', 'h12', 'h13',
            's12', 's13', 's1',
            'd13', 'd1',
            'c1',
        ]
        # 最後に捨てられたカードが「d12, c12」
        self.board.last_card = ["d12", "c12"]
        result = self.board.get_actionable(first_card)

        exp = [
            ['h13', 's13'], ['h13', 'd13'], ['s13', 'd13'],
            ['h1', 's1'], ['h1', 'd1'], ['h1', 'c1'], ['s1', 'd1'], ['s1', 'c1'], ['d1', 'c1']
        ]

        # 個数が正しいか
        self.assertEqual(len(result), len(exp))
        # 値が正しいか
        for card in result:
            # 1枚の時
            if type(card) == str:
                if card in result:
                    self.assertTrue(True)
                else:
                    self.assertTrue(False)
            # 複数枚の時(配列)
            elif type(card) == list:
                # set関数は二重配列の時使えないため
                flg = False
                for exp_card in exp:
                    if set(exp_card) == set(card):
                        flg = True
                        break
                if flg == True:
                    self.assertTrue(True)
                else:
                    print(f"result_card: {card}¥nexp_card: {exp_card}")
                    self.assertTrue(False)

    def test_get_actionable_two_joker(self):
        """
        最後に捨てられたカードが2枚の時(jokerあり)
          2枚のカードが選択できる
        """
        """
        最初のプレイヤーのカードをテスト用に更新
        12: 1つ
        13: 2つ
        1:  3つ
        2:  4つ
        """
        first_card = [
            'h12', 'h13', 'h1', 'h2', 
            's13', 's1', 's2',
            'd1', 'd2',
            'c2',
            'j1'
        ]
        # 最後に捨てられたカードを更新
        self.board.last_card = ['d13', 'c13']
        result = self.board.get_actionable(first_card)

        exp = [
            ['h1', 's1'], ['h1', 'd1'], ['h1', 'j1'], ['s1', 'd1'], ['s1', 'j1'], ['d1', 'j1'],
            ['h2', 's2'], ['h2', 'd2'], ['h2', 'c2'], ['h2', 'j1'], ['s2', 'd2'], ['s2', 'c2'], ['s2', 'j1'], ['d2', 'c2'], ['d2', 'j1'], ['c2', 'j1']
        ]

        # 個数が正しいか
        self.assertEqual(len(result), len(exp))
        # 値が正しいか
        for card in result:
            # 1枚の時
            if type(card) == str:
                if card in result:
                    self.assertTrue(True)
                else:
                    self.assertTrue(False)
            # 複数枚の時(配列)
            elif type(card) == list:
                # set関数は二重配列の時使えないため
                flg = False
                for exp_card in exp:
                    if set(exp_card) == set(card):
                        flg = True
                        break
                if flg == True:
                    self.assertTrue(True)
                else:
                    print(f"result_card: {card}¥nexp_card: {exp_card}")
                    self.assertTrue(False)

    def test_get_actionable_two_revolution(self):
        """
        最後に捨てられたカードが2枚の時(革命時)
          2枚のカードが選択できる
        """
        """
        最初のプレイヤーのカードをテスト用に更新
        12: 4つ
        13: 3つ
        1:  2つ
        2:  1つ
        """
        first_card = [
            'h12', 'h13', 'h1', 'h2', 
            's12', 's13', 's1',
            'd12', 'd13',
            'c12',
            'j1'
        ]
        # 最後に捨てられたカードを更新
        self.board.last_card = ['d1', 'c1']
        # 革命
        self.board.power_cards.reverse()
        self.board.revolution = True
        result = self.board.get_actionable(first_card)

        exp = [
            ['h12', 's12'], ['h12', 'd12'], ['h12', 'c12'], ['h12', 'j1'], ['s12', 'd12'], ['s12', 'c12'], ['s12', 'j1'], ['d12', 'c12'], ['d12', 'j1'], ['c12', 'j1'],
            ['h13', 's13'], ['h13', 'd13'], ['h13', 'j1'], ['s13', 'd13'], ['s13', 'j1'], ['d13', 'j1']
        ]

        # 個数が正しいか
        self.assertEqual(len(result), len(exp))
        # 値が正しいか
        for card in result:
            # 1枚の時
            if type(card) == str:
                if card in result:
                    self.assertTrue(True)
                else:
                    self.assertTrue(False)
            # 複数枚の時(配列)
            elif type(card) == list:
                # set関数は二重配列の時使えないため
                flg = False
                for exp_card in exp:
                    if set(exp_card) == set(card):
                        flg = True
                        break
                if flg == True:
                    self.assertTrue(True)
                else:
                    print(f"result_card: {card}¥nexp_card: {exp_card}")
                    self.assertTrue(False)

    def test_get_actionable_three(self):
        """
        最後に捨てられたカードが3枚の時
          3枚のカードが選択できる
        """
        # 最初のプレイヤーのカードをテスト用に更新
        first_card = [
            'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8', 'h9', 'h10', 'h11', 'h12', 'h13',
            's13', 's1',
            'd13', 'd1',
            'c1',
        ]
        # 最後に捨てられたカードが「d12, c12, s12」
        self.board.last_card = ["d12", "c12", "s12"]
        result = self.board.get_actionable(first_card)

        exp = [
            ['h13', 's13', 'd13'],
            ['h1', 's1', 'd1'], ['h1', 's1', 'c1'], ['h1', 'd1', 'c1'], ['s1', 'd1', 'c1']
        ]

        # 個数が正しいか
        self.assertEqual(len(result), len(exp))
        # 値が正しいか
        for card in result:
            # 1枚の時
            if type(card) == str:
                if card in result:
                    self.assertTrue(True)
                else:
                    self.assertTrue(False)
            # 複数枚の時(配列)
            elif type(card) == list:
                # set関数は二重配列の時使えないため
                flg = False
                for exp_card in exp:
                    if set(exp_card) == set(card):
                        flg = True
                        break
                if flg == True:
                    self.assertTrue(True)
                else:
                    print(f"result_card: {card}¥nexp_card: {exp_card}")
                    self.assertTrue(False)

    def test_get_actionable_three_joker(self):
        """
        最後に捨てられたカードが3枚の時(jokerあり)
          3枚のカードが選択できる
        """
        first_card = [
            'h12', 'h13', 'h1', 'h2', 
            's13', 's1', 's2',
            'd1', 'd2',
            'c2',
            'j1'
        ]
        # 最後に捨てられたカードを更新
        self.board.last_card = ['s12', 'd12', 'c12']
        result = self.board.get_actionable(first_card)

        exp = [
            ['h13', 's13', 'j1'],
            ['h1', 's1', 'd1'], ['h1', 's1', 'j1'], ['h1', 'd1', 'j1'], ['s1', 'd1', 'j1'],
            ['h2', 's2', 'd2'], ['h2', 's2', 'c2'], ['h2', 's2', 'j1'], ['h2', 'd2', 'c2'], ['h2', 'd2', 'j1'],
            ['h2', 'c2', 'j1'], ['s2', 'd2', 'c2'], ['s2', 'd2', 'j1'], ['s2', 'c2', 'j1'], ['d2', 'c2', 'j1']
        ]

        # 個数が正しいか
        self.assertEqual(len(result), len(exp))
        # 値が正しいか
        for card in result:
            # 1枚の時
            if type(card) == str:
                if card in result:
                    self.assertTrue(True)
                else:
                    self.assertTrue(False)
            # 複数枚の時(配列)
            elif type(card) == list:
                # set関数は二重配列の時使えないため
                flg = False
                for exp_card in exp:
                    if set(exp_card) == set(card):
                        flg = True
                        break
                if flg == True:
                    self.assertTrue(True)
                else:
                    print(f"result_card: {card}¥nexp_card: {exp_card}")
                    self.assertTrue(False)

    def test_get_actionable_three_revolution(self):
        """
        最後に捨てられたカードが3枚の時(革命時)
          3枚のカードが選択できる
        """
        """
        最初のプレイヤーのカードをテスト用に更新
        12: 4つ
        1:  2つ
        2:  1つ
        """
        first_card = [
            'h12', 'h1', 'h2', 
            's12', 's1',
            'd12',
            'c12',
            'j1'
        ]
        # 最後に捨てられたカードを更新
        self.board.last_card = ['s2', 'd2', 'c2']
        # 革命
        self.board.power_cards.reverse()
        self.board.revolution = True
        result = self.board.get_actionable(first_card)

        exp = [
            ['h1', 's1', 'j1'],
            ['h12','s12','d12'],['h12','s12','c12'],['h12','s12','j1'],['h12','d12','c12'],['h12','d12','j1'],
            ['h12','c12','j1'],['s12','d12','c12'],['s12','d12','j1'],['s12','c12','j1'],['d12','c12','j1']
        ]

        # 個数が正しいか
        self.assertEqual(len(result), len(exp))
        # 値が正しいか
        for card in result:
            # 1枚の時
            if type(card) == str:
                if card in result:
                    self.assertTrue(True)
                else:
                    self.assertTrue(False)
            # 複数枚の時(配列)
            elif type(card) == list:
                # set関数は二重配列の時使えないため
                flg = False
                for exp_card in exp:
                    if set(exp_card) == set(card):
                        flg = True
                        break
                if flg == True:
                    self.assertTrue(True)
                else:
                    print(f"result_card: {card}¥nexp_card: {exp_card}")
                    self.assertTrue(False)

    def test_get_actionable_four(self):
        """
        最後に捨てられたカードが4枚の時
          4枚のカードが選択できる
        """
        # 最初のプレイヤーのカードをテスト用に更新
        first_card = [
            'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8', 'h9', 'h10', 'h11', 'h13',
            's13', 's1',
            'd13', 'd1',
            'c1',
        ]
        # 最後に捨てられたカードが「d12, c12, s12」
        self.board.last_card = ["d12", "c12", "s12", "h12"]
        result = self.board.get_actionable(first_card)

        exp = [
            ['h1', 's1', 'd1', 'c1']
        ]

        # 個数が正しいか
        self.assertEqual(len(result), len(exp))
        # 値が正しいか
        for card in result:
            # 1枚の時
            if type(card) == str:
                if card in result:
                    self.assertTrue(True)
                else:
                    self.assertTrue(False)
            # 複数枚の時(配列)
            elif type(card) == list:
                # set関数は二重配列の時使えないため
                flg = False
                for exp_card in exp:
                    if set(exp_card) == set(card):
                        flg = True
                        break
                if flg == True:
                    self.assertTrue(True)
                else:
                    print(f"result_card: {card}¥nexp_card: {exp_card}")
                    self.assertTrue(False)

    def test_get_actionable_four_joker(self):
        """
        最後に捨てられたカードが4枚の時(jokerあり)
          4枚のカードが選択できる
        """
        first_card = [
            'h12', 'h13', 'h1', 'h2', 
            's13', 's1', 's2',
            'd1', 'd2',
            'c2',
            'j1'
        ]
        # 最後に捨てられたカードを更新
        self.board.last_card = ['h11', 's11', 'd11', 'c11']
        result = self.board.get_actionable(first_card)

        exp = [
            ['h1', 's1', 'd1', 'j1'],
            ['h2', 's2', 'd2', 'c2'], ['h2', 's2', 'c2', 'j1'], ['h2', 's2', 'd2', 'j1'], ['h2', 'd2', 'c2', 'j1'], ['s2', 'd2', 'c2', 'j1']
        ]

        # 個数が正しいか
        self.assertEqual(len(result), len(exp))
        # 値が正しいか
        for card in result:
            # 1枚の時
            if type(card) == str:
                if card in result:
                    self.assertTrue(True)
                else:
                    self.assertTrue(False)
            # 複数枚の時(配列)
            elif type(card) == list:
                # set関数は二重配列の時使えないため
                flg = False
                for exp_card in exp:
                    if set(exp_card) == set(card):
                        flg = True
                        break
                if flg == True:
                    self.assertTrue(True)
                else:
                    print(f"result_card: {card}¥nexp_card: {exp_card}")
                    self.assertTrue(False)

    def test_get_actionable_four_revolution(self):
        """
        最後に捨てられたカードが4枚の時(革命時)
          4枚のカードが選択できる
        """
        """
        最初のプレイヤーのカードをテスト用に更新
        12: 4つ
        1:  2つ
        2:  1つ
        """
        first_card = [
            'h12', 'h1', 'h2', 
            's12', 's1',
            'd12',
            'c12',
            'j1'
        ]
        # 最後に捨てられたカードを更新
        self.board.last_card = ['h13', 's13', 'd13', 'c13']
        # 革命
        self.board.power_cards.reverse()
        self.board.revolution = True
        result = self.board.get_actionable(first_card)

        exp = [
            ['h12', 's12', 'd12', 'c12'], ['h12', 's12', 'd12', 'j1'], ['h12', 's12', 'c12', 'j1'],
            ['h12', 'd12', 'c12', 'j1'], ['s12', 'd12', 'c12', 'j1']
        ]

        # 個数が正しいか
        self.assertEqual(len(result), len(exp))
        # 値が正しいか
        for card in result:
            # 1枚の時
            if type(card) == str:
                if card in result:
                    self.assertTrue(True)
                else:
                    self.assertTrue(False)
            # 複数枚の時(配列)
            elif type(card) == list:
                # set関数は二重配列の時使えないため
                flg = False
                for exp_card in exp:
                    if set(exp_card) == set(card):
                        flg = True
                        break
                if flg == True:
                    self.assertTrue(True)
                else:
                    print(f"result_card: {card}¥nexp_card: {exp_card}")
                    self.assertTrue(False)

    def test_get_actionable_five(self):
        """
        最後に捨てられたカードが5枚の時
          joker1つのため返すことができない
        """
        first_card = [
            'h12', 'h13', 'h1', 'h2', 
            's13', 's1', 's2',
            'd1', 'd2',
            'c2'
        ]
        # 最後に捨てられたカードを更新
        self.board.last_card = ['h11', 's11', 'd11', 'c11', 'j1']
        result = self.board.get_actionable(first_card)

        # 個数が正しいか
        self.assertEqual(len(result), 0)
        # 値が正しいか
        self.assertEqual(result, [])

    
    def test_get_actionable_zero(self):
        """
        アクション可能なカードがない時
          空のリストを返す
        """
        # 最初のプレイヤーのカードをテスト用に更新
        first_card = [
            'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8', 'h9', 'h10', 'h11', 'h13'
        ]
        # 最後に捨てられたカードが「d12, c12, s12」
        self.board.last_card = ["d12", "c12", "s12", "h12"]
        result = self.board.get_actionable(first_card)

        # 個数が正しいか
        self.assertEqual(len(result), 0)
        # 値が正しいか
        self.assertEqual(result, [])
    
    # ----------------------------------move()----------------------------------

    def test_move(self):
        """
        アクションをしたときに正常に動くか
        """

        next_player_id, next_actionable_cards, game_info = self.board.game_start()

        first_player_id, second_player_id, third_player_id, forth_player_id = \
            self.board.players_order["1"], self.board.players_order["2"], self.board.players_order["3"], self.board.players_order["4"]

        self.board.id_card_dict[first_player_id] = [
            'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8', 'h9', 'h10', 'h11', 'h12', 'h13'
        ]
        self.board.id_card_dict[second_player_id] = [
            'd1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8', 'd9', 'd10', 'd11', 'd12', 'd13'
        ]
        self.board.id_card_dict[third_player_id] = [
            's1', 's2', 's3', 's4', 's5', 's6', 's7', 's8', 's9', 's10', 's11', 's12', 's13'
        ]
        self.board.id_card_dict[forth_player_id] = [
            'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'c9', 'c10', 'c11', 'c12', 'c13',
            'j1'
        ]

        # 実行
        next_player, next_actionable_card, game_done, game_info = self.board.move(first_player_id, 'h1')

        # 戻り値が正しいか
        self.assertEqual(next_player, second_player_id)  # 次のプレイヤー
        self.assertEqual(['d2'], next_actionable_card)
        self.assertEqual(game_done, False)

        # インスタンス変数が正しいか
        self.assertEqual([
            'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8', 'h9', 'h10', 'h11', 'h12', 'h13'
        ], self.board.id_card_dict[first_player_id])   # 手札が正しいか
        self.assertEqual([
            'd1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8', 'd9', 'd10', 'd11', 'd12', 'd13'
        ], self.board.id_card_dict[second_player_id])   # 手札が正しいか
        self.assertEqual([
            's1', 's2', 's3', 's4', 's5', 's6', 's7', 's8', 's9', 's10', 's11', 's12', 's13'
        ], self.board.id_card_dict[third_player_id])   # 手札が正しいか
        self.assertEqual([
            'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'c9', 'c10', 'c11', 'c12', 'c13',
            'j1'
        ], self.board.id_card_dict[forth_player_id])   # 手札が正しいか

        self.assertEqual(["h1"], self.board.die_cards)  # 墓地
        self.assertEqual("h1", self.board.last_card)  # 最後のカード
        self.assertEqual(first_player_id, self.board.last_player)
        self.assertEqual(1, self.board.count)
        self.assertEqual(False, self.board.revolution)
        self.assertEqual({"1": "", "2": "", "3": "", "4": ""}, self.board.end_player)
    
    def test_move_skip(self):
        """
        skipをしたときに正常に動くか
        """

        next_player_id, next_actionable_cards, game_info = self.board.game_start()

        first_player_id, second_player_id, third_player_id, forth_player_id = \
            self.board.players_order["1"], self.board.players_order["2"], self.board.players_order["3"], self.board.players_order["4"]

        self.board.id_card_dict[first_player_id] = [
            'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8', 'h9', 'h10', 'h11', 'h12', 'h13'
        ]
        self.board.id_card_dict[second_player_id] = [
            'd1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8', 'd9', 'd10', 'd11', 'd12', 'd13'
        ]
        self.board.id_card_dict[third_player_id] = [
            's1', 's2', 's3', 's4', 's5', 's6', 's7', 's8', 's9', 's10', 's11', 's12', 's13'
        ]
        self.board.id_card_dict[forth_player_id] = [
            'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'c9', 'c10', 'c11', 'c12', 'c13',
            'j1'
        ]

        # 実行
        next_player, next_actionable_card, game_done, game_info = self.board.move(first_player_id, 'h1')
        next_player, next_actionable_card, game_done, game_info = self.board.move(second_player_id, "skip")

        # 戻り値が正しいか
        self.assertEqual(next_player, third_player_id)  # 次のプレイヤー
        self.assertEqual(['s2'], next_actionable_card)
        self.assertEqual(game_done, False)

        # インスタンス変数が正しいか
        self.assertEqual([
            'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8', 'h9', 'h10', 'h11', 'h12', 'h13'
        ], self.board.id_card_dict[first_player_id])   # 手札が正しいか
        self.assertEqual([
            'd1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8', 'd9', 'd10', 'd11', 'd12', 'd13'
        ], self.board.id_card_dict[second_player_id])   # 手札が正しいか
        self.assertEqual([
            's1', 's2', 's3', 's4', 's5', 's6', 's7', 's8', 's9', 's10', 's11', 's12', 's13'
        ], self.board.id_card_dict[third_player_id])   # 手札が正しいか
        self.assertEqual([
            'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'c9', 'c10', 'c11', 'c12', 'c13',
            'j1'
        ], self.board.id_card_dict[forth_player_id])   # 手札が正しいか

        self.assertEqual(["h1"], self.board.die_cards)  # 墓地
        self.assertEqual("h1", self.board.last_card)  # 最後のカード
        self.assertEqual(first_player_id, self.board.last_player)  # skipしたプレイヤーにはならないこと
        self.assertEqual(1, self.board.count)
        self.assertEqual(False, self.board.revolution)
        self.assertEqual({"1": "", "2": "", "3": "", "4": ""}, self.board.end_player)
    
    def test_move_others_skip(self):
        """
        他のプレイヤーが皆スキップした時に流れるか
        1番目: h1
        2番目: skip
        3番目: skip
        4番目: skip
        ~流れる~
        """

        next_player_id, next_actionable_cards, game_info = self.board.game_start()

        first_player_id, second_player_id, third_player_id, forth_player_id = \
            self.board.players_order["1"], self.board.players_order["2"], self.board.players_order["3"], self.board.players_order["4"]

        self.board.id_card_dict[first_player_id] = [
            'h1', 'h3'
        ]
        self.board.id_card_dict[second_player_id] = [
            'h2', 'h4', 'h5', 'h6', 'h7', 'h8', 'h9', 'h10', 'h11', 'h12', 'h13',
            'd1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8', 'd9', 'd10', 'd11', 'd12', 'd13'
        ]
        self.board.id_card_dict[third_player_id] = [
            's1', 's2', 's3', 's4', 's5', 's6', 's7', 's8', 's9', 's10', 's11', 's12', 's13'
        ]
        self.board.id_card_dict[forth_player_id] = [
            'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'c9', 'c10', 'c11', 'c12', 'c13',
            'j1'
        ]

        # 実行
        next_player, next_actionable_card, game_done, game_info = self.board.move(first_player_id, 'h1')  # 1番目
        next_player, next_actionable_card, game_done, game_info = self.board.move(second_player_id, "skip")  # 2番目
        next_player, next_actionable_card, game_done, game_info = self.board.move(third_player_id, "skip")  # 3番目
        next_player, next_actionable_card, game_done, game_info = self.board.move(forth_player_id, "skip")  # 4番目


        # 戻り値が正しいか
        self.assertEqual(next_player, first_player_id)  # 次のプレイヤー
        self.assertEqual([
            'h3'
        ], next_actionable_card)  # 全てのハンド
        self.assertEqual(game_done, False)

        # インスタンス変数が正しいか
        self.assertEqual([
            'h3'
        ], self.board.id_card_dict[first_player_id])   # 手札が正しいか
        self.assertEqual([
            'h2', 'h4', 'h5', 'h6', 'h7', 'h8', 'h9', 'h10', 'h11', 'h12', 'h13',
            'd1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8', 'd9', 'd10', 'd11', 'd12', 'd13'
        ], self.board.id_card_dict[second_player_id])   # 手札が正しいか
        self.assertEqual([
            's1', 's2', 's3', 's4', 's5', 's6', 's7', 's8', 's9', 's10', 's11', 's12', 's13'
        ], self.board.id_card_dict[third_player_id])   # 手札が正しいか
        self.assertEqual([
            'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'c9', 'c10', 'c11', 'c12', 'c13',
            'j1'
        ], self.board.id_card_dict[forth_player_id])   # 手札が正しいか

        self.assertEqual(["h1"], self.board.die_cards)  # 墓地
        self.assertEqual("", self.board.last_card)  # 最後のカード
        self.assertEqual("", self.board.last_player)  # skipしたプレイヤーにはならないこと
        self.assertEqual(2, self.board.count)
        self.assertEqual(False, self.board.revolution)
        self.assertEqual({"1": "", "2": "", "3": "", "4": ""}, self.board.end_player)
    
    def test_move_one_end(self):
        """
        一人上がった場合
        """

        next_player_id, next_actionable_cards, game_info = self.board.game_start()

        first_player_id, second_player_id, third_player_id, forth_player_id = \
            self.board.players_order["1"], self.board.players_order["2"], self.board.players_order["3"], self.board.players_order["4"]

        self.board.id_card_dict[first_player_id] = [
            'h1'
        ]
        self.board.id_card_dict[second_player_id] = [
            'd2'
        ]
        self.board.id_card_dict[third_player_id] = [
            'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8', 'h9', 'h10', 'h11', 'h12', 'h13',
            'd1', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8', 'd9', 'd10', 'd11', 'd12', 'd13',
            's1', 's2', 's3', 's4', 's5', 's6', 's7', 's8', 's9', 's10', 's11', 's12', 's13'
        ]
        self.board.id_card_dict[forth_player_id] = [
            'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'c9', 'c10', 'c11', 'c12', 'c13',
            'j1'
        ]

        # 実行
        next_player, next_actionable_card, game_done, game_info = self.board.move(first_player_id, 'h1')  # 1番目

        # 戻り値が正しいか
        self.assertEqual(next_player, second_player_id)  # 次のプレイヤー
        self.assertEqual(game_done, False)

        self.assertEqual(["h1"], self.board.die_cards)  # 墓地
        self.assertEqual("h1", self.board.last_card)  # 最後のカード
        self.assertEqual(second_player_id, self.board.last_player)  # 上がった次のプレイヤーが格納されていること
        self.assertEqual(1, self.board.count)
        self.assertEqual(False, self.board.revolution)
        self.assertEqual(
            {"1": first_player_id, "2": "", "3": "", "4": ""},
            self.board.end_player
        )
        self.assertEqual(
            {"1": second_player_id, "2": third_player_id, "3": forth_player_id},
            self.board.players_order
        )
    
    def test_move_one_end_others_skip(self):
        """
        一人上がったて他のプレイヤーは全てskip
          正常に動くか
        """

        next_player_id, next_actionable_cards, game_info = self.board.game_start()

        first_player_id, second_player_id, third_player_id, forth_player_id = \
            self.board.players_order["1"], self.board.players_order["2"], self.board.players_order["3"], self.board.players_order["4"]

        self.board.id_card_dict[first_player_id] = [
            'h1'
        ]
        self.board.id_card_dict[second_player_id] = [
            'd2'
        ]
        self.board.id_card_dict[third_player_id] = [
            'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8', 'h9', 'h10', 'h11', 'h12', 'h13',
            'd1', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8', 'd9', 'd10', 'd11', 'd12', 'd13',
            's1', 's2', 's3', 's4', 's5', 's6', 's7', 's8', 's9', 's10', 's11', 's12', 's13'
        ]
        self.board.id_card_dict[forth_player_id] = [
            'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'c9', 'c10', 'c11', 'c12', 'c13',
            'j1'
        ]

        # 実行
        next_player, next_actionable_card, game_done, game_info = self.board.move(first_player_id, 'h1')  # 1番目(上がり)
        next_player, next_actionable_card, game_done, game_info = self.board.move(second_player_id, 'skip')  # 2番目
        next_player, next_actionable_card, game_done, game_info = self.board.move(third_player_id, 'skip')  # 3番目
        next_player, next_actionable_card, game_done, game_info = self.board.move(forth_player_id, 'skip')  # 4番目
        
        # 戻り値が正しいか
        self.assertEqual(next_player, second_player_id)  # 次のプレイヤー
        self.assertEqual(game_done, False)

        self.assertEqual(["h1"], self.board.die_cards)  # 墓地
        self.assertEqual("", self.board.last_card)  # 最後のカード
        self.assertEqual("", self.board.last_player)  # 上がった次のプレイヤーが格納されていること
        self.assertEqual(2, self.board.count)
        self.assertEqual(False, self.board.revolution)
        self.assertEqual(
            {"1": first_player_id, "2": "", "3": "", "4": ""},
            self.board.end_player
        )
        self.assertEqual(
            {"1": second_player_id, "2": third_player_id, "3": forth_player_id},
            self.board.players_order
        )

    def test_move_revolution(self):
        """
        革命
        """
        next_player_id, next_actionable_cards, game_info = self.board.game_start()

        first_player_id, second_player_id, third_player_id, forth_player_id = \
            self.board.players_order["1"], self.board.players_order["2"], self.board.players_order["3"], self.board.players_order["4"]

        self.board.id_card_dict[first_player_id] = [
            'h11', 'd11', 's11', 'c11'
        ]
        self.board.id_card_dict[second_player_id] = [
            'h2', 'd2', 's2', 'c2'
        ]
        self.board.id_card_dict[third_player_id] = [
            'h3', 'd3', 's3'
        ]
        self.board.id_card_dict[forth_player_id] = [
            'h1', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8', 'h9', 'h10', 'h11', 'h12', 'h13',
            'd1', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8', 'd9', 'd10', 'd11', 'd12', 'd13',
            's1', 's3', 's4', 's5', 's6', 's7', 's8', 's9', 's10', 's11', 's12', 's13',
            'c1', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'c9', 'c10', 'c11', 'c12', 'c13',
            'j1'
        ]

        # 実行(革命)
        next_player, next_actionable_card, game_done, game_info = self.board.move(first_player_id, ['h11', 'd11', 's11', 'c11'])  # 1番目(革命)

        # 革命のテスト
        self.assertEqual(next_player, second_player_id)  # 次のプレイヤー
        self.assertEqual(game_done, False)

        self.assertEqual(True, self.board.revolution)
        self.assertEqual(next_actionable_card, [])
    
    def test_move_revolution_joker(self):
        """
        革命(jokerあり)
        """
        next_player_id, next_actionable_cards, game_info = self.board.game_start()

        first_player_id, second_player_id, third_player_id, forth_player_id = \
            self.board.players_order["1"], self.board.players_order["2"], self.board.players_order["3"], self.board.players_order["4"]

        self.board.id_card_dict[first_player_id] = [
            'h11', 'd11', 's11', 'j1'
        ]
        self.board.id_card_dict[second_player_id] = [
            'h2', 'd2', 's2'
        ]
        self.board.id_card_dict[third_player_id] = [
            'h3', 'd3', 's3'
        ]
        self.board.id_card_dict[forth_player_id] = [
            'h1', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8', 'h9', 'h10', 'h11', 'h12', 'h13',
            'd1', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8', 'd9', 'd10', 'd11', 'd12', 'd13',
            's1', 's3', 's4', 's5', 's6', 's7', 's8', 's9', 's10', 's11', 's12', 's13',
            'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'c9', 'c10', 'c11', 'c12', 'c13'
        ]

        # 実行(革命)
        next_player, next_actionable_card, game_done, game_info = self.board.move(first_player_id, ['h11', 'd11', 's11', 'j1'])  # 1番目(革命)

        # 革命のテスト
        self.assertEqual(next_player, second_player_id)  # 次のプレイヤー
        self.assertEqual(game_done, False)

        self.assertEqual(True, self.board.revolution)
        self.assertEqual(next_actionable_card, [])

    def test_move_ban(self):
        """
        禁止上がり
        """
        next_player_id, next_actionable_cards, game_info = self.board.game_start()

        first_player_id, second_player_id, third_player_id, forth_player_id = \
            self.board.players_order["1"], self.board.players_order["2"], self.board.players_order["3"], self.board.players_order["4"]

        self.board.id_card_dict[first_player_id] = [
            'h2'
        ]
        self.board.id_card_dict[second_player_id] = [
            'd3'
        ]
        self.board.id_card_dict[third_player_id] = [
            'h1', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8', 'h9', 'h10', 'h11', 'h12', 'h13',
            'd1', 'd2', 'd4', 'd5', 'd6', 'd7', 'd8', 'd9', 'd10', 'd11', 'd12', 'd13',
            's1', 's2', 's3', 's4', 's5', 's6', 's7', 's8', 's9', 's10', 's11', 's12', 's13'
        ]
        self.board.id_card_dict[forth_player_id] = [
            'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'c9', 'c10', 'c11', 'c12', 'c13',
            'j1'
        ]

        # 実行(2)
        next_player, next_actionable_card, game_done, game_info = self.board.move(first_player_id, 'h2')  # 1番目(禁止上がり)

        # 禁止上がりのテスト
        self.assertEqual(next_player, second_player_id)  # 次のプレイヤー
        self.assertEqual(game_done, False)

        self.assertEqual(["h2"], self.board.die_cards)  # 墓地
        self.assertEqual("h2", self.board.last_card)  # 最後のカード
        self.assertEqual(second_player_id, self.board.last_player)  # 上がった次のプレイヤーが格納されていること
        self.assertEqual(1, self.board.count)
        self.assertEqual(False, self.board.revolution)
        self.assertEqual(
            {"1": "", "2": "", "3": "", "4": first_player_id},
            self.board.end_player
        )
        self.assertEqual(
            {"1": second_player_id, "2": third_player_id, "3": forth_player_id},
            self.board.players_order
        )

        # 実行(3)のための準備
        next_player, next_actionable_card, game_done, game_info = self.board.move(second_player_id, 'skip')
        next_player, next_actionable_card, game_done, game_info = self.board.move(third_player_id, 'skip')
        next_player, next_actionable_card, game_done, game_info = self.board.move(forth_player_id, 'skip')

        self.assertEqual(next_player, second_player_id)
        self.assertEqual(self.board.last_card, "")

        # 実行(3)
        next_player, next_actionable_card, game_done, game_info = self.board.move(second_player_id, 'd3')

        # 禁止上がりのテスト
        self.assertEqual(next_player, third_player_id)  # 次のプレイヤー
        self.assertEqual(game_done, False)

        self.assertEqual(["h2", "d3"], self.board.die_cards)  # 墓地
        self.assertEqual("d3", self.board.last_card)  # 最後のカード
        self.assertEqual(third_player_id, self.board.last_player)  # 上がった次のプレイヤーが格納されていること
        self.assertEqual(2, self.board.count)
        self.assertEqual(False, self.board.revolution)
        self.assertEqual(
            {"1": second_player_id, "2": "", "3": "", "4": first_player_id},
            self.board.end_player
        )
        self.assertEqual(
            {"1": third_player_id, "2": forth_player_id},
            self.board.players_order
        )

    def test_move_ban_revolution(self):
        """
        禁止上がり(革命時)
        """
        next_player_id, next_actionable_cards, game_info = self.board.game_start()

        first_player_id, second_player_id, third_player_id, forth_player_id = \
            self.board.players_order["1"], self.board.players_order["2"], self.board.players_order["3"], self.board.players_order["4"]

        self.board.id_card_dict[first_player_id] = [
            'h11', 'd11', 's11', 'c11'
        ]
        self.board.id_card_dict[second_player_id] = [
            'h2'
        ]
        self.board.id_card_dict[third_player_id] = [
            'h3'
        ]
        self.board.id_card_dict[forth_player_id] = [
            'h1', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8', 'h9', 'h10', 'h11', 'h12', 'h13',
            'd1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8', 'd9', 'd10', 'd11', 'd12', 'd13',
            's1', 's2', 's3', 's4', 's5', 's6', 's7', 's8', 's9', 's10', 's11', 's12', 's13',
            'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'c9', 'c10', 'c11', 'c12', 'c13',
            'j1'
        ]

        # 実行(革命)
        next_player, next_actionable_card, game_done, game_info = self.board.move(first_player_id, ['h11', 'd11', 's11', 'c11'])  # 1番目(革命)

        # 革命のテスト
        self.assertEqual(next_player, second_player_id)  # 次のプレイヤー
        self.assertEqual(game_done, False)

        self.assertEqual(True, self.board.revolution)

        # 実行(3)のための準備
        next_player, next_actionable_card, game_done, game_info = self.board.move(second_player_id, 'skip')
        next_player, next_actionable_card, game_done, game_info = self.board.move(third_player_id, 'skip')
        next_player, next_actionable_card, game_done, game_info = self.board.move(forth_player_id, 'skip')

        self.assertEqual(next_player, second_player_id)
        self.assertEqual(self.board.last_card, "")

        # 実行(2)
        next_player, next_actionable_card, game_done, game_info = self.board.move(second_player_id, 'h2')

        # 禁止りではないのテスト
        self.assertEqual(next_player, third_player_id)  # 次のプレイヤー

        # 実行(3)
        next_player, next_actionable_card, game_done, game_info = self.board.move(third_player_id, 'h3')

        # 禁止上がりのテスト
        self.assertEqual(game_done, True)
        self.assertEqual(
            {"1": first_player_id, "2": second_player_id, "3": forth_player_id, "4": third_player_id},
            self.board.end_player
        )
        
    
    def test_move_ban_one_card(self):
        """
        1枚あがり
          1人目が禁止上がりをした場合に4位になるか
          2人目の金仕上がりをした場合に3位になるか
        """
        next_player_id, next_actionable_cards, game_info = self.board.game_start()

        first_player_id, second_player_id, third_player_id, forth_player_id = \
            self.board.players_order["1"], self.board.players_order["2"], self.board.players_order["3"], self.board.players_order["4"]

        self.board.id_card_dict[first_player_id] = [
            'h2'
        ]
        self.board.id_card_dict[second_player_id] = [
            'j1'
        ]
        self.board.id_card_dict[third_player_id] = [
            'h1'
        ]
        self.board.id_card_dict[forth_player_id] = [
            'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'c9', 'c10', 'c11', 'c12', 'c13',
            'h3', 'h4', 'h5', 'h6', 'h7', 'h8', 'h9', 'h10', 'h11', 'h12', 'h13',
            'd1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8', 'd9', 'd10', 'd11', 'd12', 'd13',
            's1', 's2', 's3', 's4', 's5', 's6', 's7', 's8', 's9', 's10', 's11', 's12', 's13'
        ]

        # 実行
        next_player, next_actionable_card, game_done, game_info = self.board.move(first_player_id, 'h2')  # 1番目(禁止上がり)
        next_player, next_actionable_card, game_done, game_info = self.board.move(second_player_id, 'j1')  # 2番目(禁止上がり)

        next_player, next_actionable_card, game_done, game_info = self.board.move(third_player_id, 'skip')
        next_player, next_actionable_card, game_done, game_info = self.board.move(forth_player_id, 'skip')

        next_player, next_actionable_card, game_done, game_info = self.board.move(third_player_id, 'h1')  # 上がり

        # 禁止上がりのテスト
        self.assertEqual(game_done, True)
        self.assertEqual(
            {"1": third_player_id, "2": forth_player_id, "3": second_player_id, "4": first_player_id},
            self.board.end_player
        )
    
    def test_move_ban_two_card(self):
        """
        2枚あがり
          1人目が禁止上がりをした場合に4位になるか
          2人目の金仕上がりをした場合に3位になるか
        """
        next_player_id, next_actionable_cards, game_info = self.board.game_start()

        first_player_id, second_player_id, third_player_id, forth_player_id = \
            self.board.players_order["1"], self.board.players_order["2"], self.board.players_order["3"], self.board.players_order["4"]

        self.board.id_card_dict[first_player_id] = [
            'h2', 'c2'
        ]
        self.board.id_card_dict[second_player_id] = [
            'j1', 'd2'
        ]
        self.board.id_card_dict[third_player_id] = [
            'h1'
        ]
        self.board.id_card_dict[forth_player_id] = [
            'c1', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'c9', 'c10', 'c11', 'c12', 'c13',
            'h3', 'h4', 'h5', 'h6', 'h7', 'h8', 'h9', 'h10', 'h11', 'h12', 'h13',
            'd1', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8', 'd9', 'd10', 'd11', 'd12', 'd13',
            's1', 's2', 's3', 's4', 's5', 's6', 's7', 's8', 's9', 's10', 's11', 's12', 's13'
        ]

        # 実行
        next_player, next_actionable_card, game_done, game_info = self.board.move(first_player_id, ['h2', 'c2'])  # 1番目(禁止上がり)
        next_player, next_actionable_card, game_done, game_info = self.board.move(second_player_id, 'skip')
        next_player, next_actionable_card, game_done, game_info = self.board.move(third_player_id, 'skip')
        next_player, next_actionable_card, game_done, game_info = self.board.move(forth_player_id, 'skip')

        self.assertEqual(next_player, second_player_id)

        next_player, next_actionable_card, game_done, game_info = self.board.move(second_player_id, ['j1', 'd2'])  # 禁止上がり

        next_player, next_actionable_card, game_done, game_info = self.board.move(third_player_id, 'skip')
        next_player, next_actionable_card, game_done, game_info = self.board.move(forth_player_id, 'skip')

        self.assertEqual(next_player, third_player_id)

        next_player, next_actionable_card, game_done, game_info = self.board.move(third_player_id, 'h1')  # 上がり

        # 禁止上がりのテスト
        self.assertEqual(game_done, True)
        self.assertEqual(
            {"1": third_player_id, "2": forth_player_id, "3": second_player_id, "4": first_player_id},
            self.board.end_player
        )








    


    
    