from enum import Enum, auto

class GameStates(Enum):
    GAME_PAUSED = auto()
    PLAYERS_TURN = auto()
    CURSOR_ACTIVE = auto()
    EQUIPMENT_ACTIVE = auto()
    SHOW_INVENTORY = auto()
    DROP_INVENTORY = auto()
    ENEMY_TURN = auto()
    TARGETING = auto()
    PLAYER_DEAD = auto()

class Game:
    def __init__(self, debug=False):
        self.debug = debug
        self.state = None
        self.map = None
        self.player = None
        self.entities = None
        self.con = None
        self.panel = None
        self.message_log = None