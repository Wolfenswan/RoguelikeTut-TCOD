#! python3
""" Constant variables """
import tcod

DEBUG = True
GAME_NAME = 'RoguelikeTutReloaded'

# Console
MAP_SCREEN_WIDTH = 70
MAP_SCREEN_HEIGHT = 40
SCREEN_WIDTH = MAP_SCREEN_WIDTH + 25
SCREEN_HEIGHT = MAP_SCREEN_HEIGHT + 15
LIMIT_FPS = 30

FONT_DEFAULT = 'arial12x12.png'
FONT_TCOD_LAYOUT = ['arial12x12.png','dejavu12x12_gs_tc.png','dejavu12x12_gs_tc.png','consolas10x10_gs_tc.png']

# DUNGEON SETTINGS #
DUNGEON_MIN_WIDTH = MAP_SCREEN_WIDTH
DUNGEON_MAX_WIDTH = DUNGEON_MIN_WIDTH * 2
DUNGEON_MIN_HEIGHT = MAP_SCREEN_HEIGHT
DUNGEON_MAX_HEIGHT = DUNGEON_MIN_HEIGHT * 2

# TODO Set this up so they are relative in size to dungeon/room #
ROOM_MAX_SIZE = 15
ROOM_MIN_SIZE = 4

# NPC SETTINGS #
MONSTERS_DUNGEON_FACTOR = 4 # total rooms times this
MONSTERS_ROOM_LIMIT = 10 # room width * room height // this

# ITEM SETTINGS #
ITEMS_DUNGEON_FACTOR = 1 # total rooms * this
ITEMS_ROOM_LIMIT = 50 # room width * room height // this

# CONTAINER SETTINGS #
# TODO put in relation to max items?
CONTAINER_DUNGEON_FACTOR = 2 # total rooms * this
CONTAINER_ROOM_DIVISOR = 30 # room width * room height // this

# STATIC OBJECT SETTINGS #
#SOBJECTS_DUNGEON_FACTOR = 5 # total rooms times this (UNUSED)
SOBJECTS_ROOM_DIVISOR = 50  # room width * room height // this

# GUI PANELS
# PANELS_BORDER_COLOR = colors.dark_grey
# PANELS_BORDER_COLOR_ACTIVE = colors.darker_red

# SIDE PANEL
SIDE_PANEL_WIDTH = SCREEN_WIDTH - MAP_SCREEN_WIDTH  # Difference between screen and map width
SIDE_PANEL_X = SCREEN_WIDTH - SIDE_PANEL_WIDTH

# BOTTOM STATUS PANEL
STATUS_PANEL_HEIGHT = 3
STATUS_PANEL_Y = MAP_SCREEN_HEIGHT

# BOTTOM PANELs
BOTTOM_PANELS_Y = MAP_SCREEN_HEIGHT + STATUS_PANEL_HEIGHT
BOTTOM_PANELS_HEIGHT = SCREEN_HEIGHT - MAP_SCREEN_HEIGHT - STATUS_PANEL_HEIGHT
BOTTOM_PANELS_WIDTH = SCREEN_WIDTH - SIDE_PANEL_WIDTH

# PLAYER PANEL
PLAYER_PANEL_WIDTH = SCREEN_WIDTH // 5
PLAYER_PANEL_HEIGHT = round(SCREEN_HEIGHT // 3)

# COMBAT PANEL (Enemy list & enemy details)
COMBAT_PANEL_WIDTH = SCREEN_WIDTH // 5
COMBAT_PANEL_HEIGHT = round(SCREEN_HEIGHT // 3)

# OBJECTS PANEL
OBJECT_PANEL_WIDTH = SCREEN_WIDTH // 5
OBJECT_PANEL_HEIGHT = round(SCREEN_HEIGHT // 3)

# Message panels
MSG_PANEL1_WIDTH = BOTTOM_PANELS_WIDTH // 2 - 4
MSG_PANEL2_WIDTH = BOTTOM_PANELS_WIDTH // 2 + 4
MSG_PANEL1_X = 0
MSG_PANEL2_X = MSG_PANEL1_WIDTH

# Message display
MSG_X = 1
MSG_HEIGHT = BOTTOM_PANELS_HEIGHT - 3
#MSG_WIDTH = MSG_PANEL_WIDTH - MSG_X

# Stat Panel
# STAT_PANEL_HEIGHT = SCREEN_HEIGHT // 3
# BAR_WIDTH = SIDE_PANEL_WIDTH - 2  # Width for the bars displaying health etc

# Inv Panel
# INV_PANEL_HEIGHT_INACTIVE = SCREEN_HEIGHT - STAT_PANEL_HEIGHT - BOTTOM_PANEL_HEIGHT
# INV_PANEL_HEIGHT_ACTIVE = SCREEN_HEIGHT - STAT_PANEL_HEIGHT

# Interaction
INVENTORY_WIDTH = 30

# FOV
FOV_ALGO = tcod.FOV_SHADOW
FOV_LIGHT_WALLS = True
FOV_RADIUS = 7
