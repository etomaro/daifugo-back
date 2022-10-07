from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel  # リクエストbodyを定義するために必要

from game import Board, RandomPlayer, HumanPlayer

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

"""
# -------メモ-----------
postはパラメーター(引数)のデータ型を定義する必要あり

"""

# リクエストbodyを定義
class Settings(BaseModel):
    num_player: int
    player_type1: str
    player_type2: str
    player_type3: str
    player_type4: str
    auto_speed: int
    is_ban: bool
    is_avility: bool
    is_stairs: bool
    is_return_spade3: bool

# リクエストbodyを定義
class Play(BaseModel):
    player_id: str
    action_card: list  # これより下はSettings
    num_player: str
    player_type1: str
    player_type2: str
    player_type3: str
    player_type4: str
    auto_speed: int
    is_ban: bool
    is_avility: bool
    is_stairs: bool
    is_return_spade3: bool  # これより下はGameInfo
    power_cards: list
    die_cards: list
    last_card: list
    last_player: str
    count: int
    revolution: bool
    end_player: dict
    players_order: dict
    id1_cards: list
    id2_cards: list
    id3_cards: list
    id4_cards: list

# front と backで違うプレイヤーIDを使用しているため解消するもの
players_back_to_front = {"id1": "player_type1", "id2": "player_type2", "id3": "player_type3", "id4": "player_type4"}

@app.post("/")
def Start(argSettings: Settings):

    # players["id1"] = RandomPalyer() if settings.playerType1 == "auto" else HumanPlayer()
    # players["id2"] = RandomPalyer() if settings.playerType2 == "auto" else HumanPlayer()
    # players["id3"] = RandomPalyer() if settings.playerType3 == "auto" else HumanPlayer()
    # players["id4"] = RandomPalyer() if settings.playerType4 == "auto" else HumanPlayer()

    # .dict()とすることでSettings型 -> dict型に変更する
    board = Board(settings=argSettings.dict())

    next_player_id, next_actionable_cards, game_info, settings = board.game_start()

    # react側ではlast_cardが1枚の場合でも配列にしているため
    if game_info["last_card"] == "":
        game_info["last_card"] = []
    elif type(game_info["last_card"]) == str:
        game_info["last_card"] = [game_info["last_card"]]
    
    # 次のプレイヤーがCPUの場合、次のアクションを取得
    next_cpu_action = []

    next_front_type = players_back_to_front[next_player_id]
    next_type = settings[next_front_type]
    if next_type == "auto":
        random_player = RandomPlayer()
        next_cpu_action.append(random_player.get_action_card(next_actionable_cards))

    return {"next_player_id":next_player_id, "next_actionable_cards": next_actionable_cards, "game_info": game_info, "next_cpu_action": next_cpu_action}

@app.post("/play")
def Play(play: Play):
    print("Play called")

    player_id = play.player_id

    # react側ではaction_cardが1枚の場合でも配列にしているため
    if len(play.action_card) == 1:
        action_card = play.action_card[0]
    else:
        action_card = play.action_card
    # react側ではlast_cardが1枚の場合でも配列にしているため
    if len(play.last_card) == 0:
        last_card = ""
    elif len(play.last_card) == 1:
        last_card = play.last_card[0]
    else:
        last_card = play.last_card

    game_info = {
        "power_cards": play.power_cards,
        "die_cards": play.die_cards,
        "last_card": last_card,
        "last_player": play.last_player,
        "count": play.count,
        "revolution": play.revolution,
        "end_player": play.end_player,
        "players_order": play.players_order,
        "id1_cards": play.id1_cards,
        "id2_cards": play.id2_cards,
        "id3_cards": play.id3_cards,
        "id4_cards": play.id4_cards
    }
    settings = {
        "num_player": play.num_player,
        "player_type1": play.player_type1,
        "player_type2": play.player_type2,
        "player_type3": play.player_type3,
        "player_type4": play.player_type4,
        "auto_speed": play.auto_speed,
        "is_ban": play.is_ban,
        "is_avility": play.is_avility,
        "is_stairs": play.is_stairs,
        "is_return_spade3": play.is_return_spade3
    }

    board = Board(settings=settings, game_info=game_info)

    next_player_id, next_actionable_cards, game_done, game_info, settings = board.move(player_id, action_card)

    # react側ではlast_cardが1枚の場合でも配列にしているため
    if game_info["last_card"] == "":
        game_info["last_card"] = []
    elif type(game_info["last_card"]) == str:
        game_info["last_card"] = [game_info["last_card"]]
    
    # 次のプレイヤーがCPUの場合、次のアクションを取得
    next_cpu_action = []

    if game_done == False:
        next_front_type = players_back_to_front[next_player_id]
        next_type = settings[next_front_type]
        if next_type == "auto":
            random_player = RandomPlayer()
            next_cpu_action.append(random_player.get_action_card(next_actionable_cards))

    print("next_cpu_action: ", next_cpu_action)

    

    return {"next_player_id": next_player_id, "next_actionable_cards": next_actionable_cards, "game_info": game_info, "next_cpu_action": next_cpu_action}


