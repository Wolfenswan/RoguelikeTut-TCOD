import tcod

from config_files import cfg

def initialize_window(game):
    """ initializes everything relevant to game window """

    # Set custom font #
    fonts = (
        'arial10x10',  # 0
        'arial12x12',  # 1,
        'consolas10x10_gs_tc', # 2
        'courier10x10_aa_tc',  # 3
        'lucida10x10_gs_tc',  # 4
        'prestige10x10_gs_tc',  # 5
        '',  # 6
        'terminal8x8_gs_ro',  # 7
        'terminal10x10_gs_tc',  # 8
        'terminal12x12_gs_ro'  # 9
    )

    tcod.console_set_custom_font(f'resources/fonts/{fonts[8]}.png', tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)

    tcod.console_init_root(cfg.SCREEN_WIDTH, cfg.SCREEN_HEIGHT, cfg.GAME_NAME, False)

    game.con = tcod.console_new(cfg.SCREEN_WIDTH, cfg.SCREEN_HEIGHT)
    game.bottom_panel = tcod.console_new(cfg.SCREEN_WIDTH, cfg.BOTTOM_PANEL_HEIGHT)