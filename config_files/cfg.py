#! python3
""" Constant variables """
import tcod

GAME_NAME = 'The Hive'
DEBUG = {
    'no_intro' : True,
    'invincibility': True,
    'reveal_map': True,
    'detailed_ent_info': True,
}
LOGGING = {
    'debug': True,
    'runtime': True,
}

# DISPLAY SETTINGS
SCREEN_WIDTH = 84
SCREEN_HEIGHT = 54
LIMIT_FPS = 30

FONT_DEFAULT = 'Cheepicus_8x8x2.png' # Recommended: Cheepicus_8x8x2.png
FONT_TCOD_LAYOUT = ['arial12x12.png','dejavu12x12_gs_tc.png','dejavu12x12_gs_tc.png','consolas10x10_gs_tc.png']

# DUNGEON SETTINGS #
DUNGEON_LOWEST_LEVEL = 10
DUNGEON_MIN_WIDTH = SCREEN_WIDTH
DUNGEON_MAX_WIDTH = DUNGEON_MIN_WIDTH * 1.4
DUNGEON_MIN_HEIGHT = SCREEN_HEIGHT
DUNGEON_MAX_HEIGHT = DUNGEON_MIN_HEIGHT * 1.4

# TODO Set this up so they are relative in size to dungeon/room #
ROOM_MAX_SIZE = 15
ROOM_MIN_SIZE = 4

# NPC SETTINGS #
MONSTERS_DUNGEON_FACTOR = 4 # total rooms * this
MONSTERS_ROOM_LIMIT = 10 # room width * room height // this

# ITEM SETTINGS #
ITEMS_DUNGEON_FACTOR = 0.5 # total rooms * this
ITEMS_ROOM_LIMIT = 50 # room width * room height // this

# CONTAINER SETTINGS #
# TODO put in relation to max items?
CONTAINER_DUNGEON_FACTOR = 0.5 # total rooms * this
CONTAINER_ROOM_DIVISOR = 30 # room width * room height // this

# STATIC OBJECT SETTINGS #
#SOBJECTS_DUNGEON_FACTOR = 5 # total rooms times this (UNUSED)
SOBJECTS_ROOM_DIVISOR = 10  # room width * room height // this

# Interaction
DASH_EXERT_MULTIPL = 2.5 # Total AV * this

# FOV
FOV_ALGO = tcod.FOV_SHADOW
FOV_LIGHT_WALLS = True
FOV_RADIUS = 7
