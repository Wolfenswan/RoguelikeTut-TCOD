#! python3
""" Constant variables """
import tcod

from config_files import colors

GAME_NAME = 'RoguelikeTutReloaded'

# Console
SCREEN_WIDTH = 120
SCREEN_HEIGHT = 80
MAP_SCREEN_WIDTH = SCREEN_WIDTH
MAP_SCREEN_HEIGHT = SCREEN_HEIGHT - 18
LIMIT_FPS = 30

# Dungeon settings
DUNGEON_MIN_WIDTH = MAP_SCREEN_WIDTH
DUNGEON_MAX_WIDTH = DUNGEON_MIN_WIDTH * 2
DUNGEON_MIN_HEIGHT = MAP_SCREEN_HEIGHT
DUNGEON_MAX_HEIGHT = DUNGEON_MIN_HEIGHT * 2

# TODO Set this up so they are relative in size to dungeon/room #
ROOM_MAX_SIZE = 15
ROOM_MIN_SIZE = 4
# MAX_MONSTERS = MAX_ROOMS/2 # TODO implement
MAX_ROOM_MONSTERS = 9  # TODO Adjust dynamically to room size
MAX_ROOM_ITEMS = 6  # TODO Adjust dynamically to room size
MAX_ROOM_STATICOBJECTS = 4  # TODO implement

# GUI PANELS
# PANELS_BORDER_COLOR = colors.dark_grey
# PANELS_BORDER_COLOR_ACTIVE = colors.darker_red

# SIDE PANEL
# SIDE_PANEL_WIDTH = SCREEN_WIDTH - MAP_SCREEN_WIDTH  # Difference between screen and map width
# SIDE_PANEL_X = SCREEN_WIDTH - SIDE_PANEL_WIDTH

# BOTTOM STATUS PANEL
STATUS_PANEL_HEIGHT = 3
STATUS_PANEL_Y = MAP_SCREEN_HEIGHT

# BOTTOM PANELs
BOTTOM_PANELS_Y = MAP_SCREEN_HEIGHT + STATUS_PANEL_HEIGHT
BOTTOM_PANELS_HEIGHT = SCREEN_HEIGHT - MAP_SCREEN_HEIGHT - STATUS_PANEL_HEIGHT
BOTTOM_PANELS_WIDTH = SCREEN_WIDTH

# COMBAT PANEL (Enemy list & enemy details)
COMBAT_PANEL_WIDTH = SCREEN_WIDTH // 5

# Message panels
MSG_PANEL_WIDTH = (SCREEN_WIDTH - COMBAT_PANEL_WIDTH) // 2
MSG_PANEL1_X = COMBAT_PANEL_WIDTH
MSG_PANEL2_X = COMBAT_PANEL_WIDTH + MSG_PANEL_WIDTH

# Message display
MSG_X = 2
MSG_HEIGHT = BOTTOM_PANELS_HEIGHT - 3
MSG_WIDTH = MSG_PANEL_WIDTH - MSG_X

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
FOV_RADIUS = 6
