""" Panels are permanently displayed consoles containing information relevant to the game """
import textwrap

import tcod

from components.actors.status_modifiers import Presence
from config_files import colors, cfg as cfg
from rendering.util_functions import center_x_for_text, setup_console, print_string


def render_panels(game):

    render_player_panel(game, game.top_right_panel, cfg.SIDE_PANEL_X, 0, cfg.SIDE_PANEL_WIDTH,
                       cfg.PLAYER_PANEL_HEIGHT)
    render_status_panel(game, game.status_panel, cfg.STATUS_PANEL_Y, cfg.BOTTOM_PANELS_WIDTH, cfg.STATUS_PANEL_HEIGHT)
    render_object_panel(game, game.lower_right_panel, cfg.SIDE_PANEL_X, cfg.PLAYER_PANEL_HEIGHT + cfg.COMBAT_PANEL_HEIGHT, cfg.SIDE_PANEL_WIDTH,
                       cfg.OBJECT_PANEL_HEIGHT)

    color = colors.dark_gray if not game.player.visible_enemies(game.npc_ents, game.fov_map) else colors.dark_red
    render_enemy_panel(game, game.center_right_panel, cfg.SIDE_PANEL_X, cfg.PLAYER_PANEL_HEIGHT, cfg.SIDE_PANEL_WIDTH,
                       cfg.COMBAT_PANEL_HEIGHT, color)
    render_message_panel(game.combat_log, 'Combat', game.bottom_center_panel, cfg.MSG_PANEL2_X, cfg.BOTTOM_PANELS_Y, cfg.MSG_PANEL2_WIDTH, cfg.BOTTOM_PANELS_HEIGHT, color, game.turn)
    render_message_panel(game.observation_log, 'Observations', game.bottom_left_panel, 0, cfg.BOTTOM_PANELS_Y,
                         cfg.MSG_PANEL1_WIDTH, cfg.BOTTOM_PANELS_HEIGHT, colors.dark_gray, game.turn)

def render_player_panel(game, con, panel_x, panel_y, width, height):
    setup_console(con, caption='Status', borders=True)

    player = game.player
    y = 0

    # Health & Stamina #
    y += 2
    #print_string(con, 1, y, f'Health : {player.fighter.hp}/{player.fighter.max_hp}', color = game.player.fighter.hp_color)
    print_string(con, 1, y, f'Health : %red%{player.fighter.hp}%/{player.fighter.max_hp}')
    print_string(con, 1, y+1,  f'Stamina : %c{player.fighter.stamina}/{player.fighter.max_stamina}%c', color = game.player.fighter.stamina_color)

    # Equipment-derived stats #
    y += 3
    # Defensive Stats #
    surrounded = player.fighter.surrounded_value(game)
    if surrounded == 1:
        print_string(con, 6, y, '*THREATENED*', color=colors.orange)
    if surrounded == 2:
        print_string(con, 6, y, '*SURROUNDED*', color=colors.red)
    print_string(con, 1, y+1, f'Defense: {game.player.fighter.defense}') # TODO implement fighter.modded_defense

    if player.fighter.shield:
        color = colors.dark_gray if not player.fighter.is_blocking else colors.white
        print_string(con, 12, y+1, '*BLOCKING*', color = color)

    # Weapon #
    y += 1
    if player.fighter.weapon and player.fighter.weapon.moveset:
        print_string(con, 1, y+2, f'%c{game.player.fighter.weapon.name}%c:', color=game.player.fighter.weapon.color)
        print_string(con, 2, y+3,
                           f'Attack: {game.player.fighter.weapon.moveset.current_move}/{game.player.fighter.weapon.moveset.moves}')
        print_string(con, 2, y+4, f'Damage: {game.player.fighter.modded_dmg_range[0]}-{game.player.fighter.modded_dmg_range[-1]}')

        print_string(con, 2, y+6, f'Targets:')
        for i, line in enumerate(player.fighter.weapon.moveset.targets_gui):
            #print_string(con, 10, y+5+i, ''.join(line))
            print_string(con, 10, y+5+i, ''.join(line))

    # Quick Slots #
    # y = 14
    # draw_quickslots(con, y, game)

    tcod.console_blit(con, 0, 0, width, height, 0, panel_x, panel_y)

def render_object_panel(game, con, panel_x, panel_y, width, height):
    setup_console(con, caption='Objects', borders=True)

    # check for objects in FOV
    spotted = [ent for ent in (game.item_ents + game.architecture_ents) if ent.is_visible(game.fov_map)]
    #spotted = [ent for ent in game.entities if ent.is_visible(game.fov_map) and (ent.item is not None or ent.architecture is not None)]

    if len(spotted):
        spotted.sort(key=game.player.distance_to_ent)  # sort the spotted array by distance to player

        # initial offsets from panel borders
        y = 2

        for ent in spotted:  # Go through the object names and wrap them according to the panel's width

            if y >= con.height - 2:  # If the limit's of the con are reached, cut the con off
                x = center_x_for_text(width, '~ ~ ~ MORE ~ ~ ~')
                print_string(con, x, y, '~ ~ ~ MORE ~ ~ ~')
                break

            # Draw creature name and stats #
            # Some symbols don't print properly with console_print, that's why it's split into put_char_ex and print
            symbol = '*' if (ent.x, ent.y) == (game.player.x, game.player.y) else f'{ent.char}'
            tcod.console_put_char_ex(con, 1, y, symbol, ent.color, tcod.black)
            wrapped_name = textwrap.wrap(f'{ent.full_name}', width - 3)

            for i, line in enumerate(wrapped_name):
                print_string(con, 3+i, y, '*BLOCKING*', color=ent.color)
                #print_string(con, 3+i, y, f'%c{line}%c' % (tcod.COLCTRL_1, tcod.COLCTRL_STOP))
                y += 2

    tcod.console_blit(con, 0, 0, width, height, 0, panel_x, panel_y)

def render_enemy_panel(game, con, panel_x, panel_y, width, height, color):
    setup_console(con, caption='Enemies', borders=True, bordercolor=color)
    
    # check for monsters in FOV
    spotted = [ent for ent in game.npc_ents if ent.is_visible(game.fov_map) and ent.fighter.hp > 0]
    #spotted = [ent for ent in game.entities if ent.ai and ent.fighter.hp > 0 and ent.is_visible(game.fov_map)]

    if len(spotted):
        spotted.sort(key=game.player.distance_to_ent)  # sort the spotted array by distance to player

        # initial offsets from panel borders
        y = 2

        for ent in spotted:  # Go through the object names and wrap them according to the panel's width
            if y >= con.height - 2:  # If the limit's of the con are reached, cut the con off
                tcod.console_set_default_foreground(con, colors.white)
                x = center_x_for_text(width, '~ ~ ~ MORE ~ ~ ~')
                print_string(con, x, y, '~ ~ ~ MORE ~ ~ ~')
                break

            # Draw creature name and stats #
            tcod.console_set_default_foreground(con, colors.gray)
            tcod.console_set_color_control(tcod.COLCTRL_1, ent.color, tcod.black)
            tcod.console_put_char_ex(con, 1, y, ent.char, ent.color, tcod.black)
            print_string(con, 3, y, ent.full_name, color = ent.color)
            y += 1
            tcod.console_put_char_ex(con, 3, y, chr(192), tcod.gray, tcod.black)
            tcod.console_set_color_control(tcod.COLCTRL_2, ent.fighter.hp_color, tcod.black)
            tcod.console_set_color_control(tcod.COLCTRL_3, ent.fighter.stamina_color, tcod.black)
            status_line = f'%c{ent.fighter.hp_string.title()}%c|%c{ent.fighter.stamina_string.title()}%c'\
                          % (tcod.COLCTRL_2, tcod.COLCTRL_STOP, tcod.COLCTRL_3, tcod.COLCTRL_STOP)
            x = 4

            for status, active in ent.fighter.presence.items():
                if active:
                    tcod.console_set_default_foreground(con, colors.white)
                    status_line += f' %c{status.name[0]}%c' % (tcod.COLCTRL_1, tcod.COLCTRL_STOP)
            print_string(con, 4, y, f'{status_line}')

            y += 1

    tcod.console_blit(con, 0, 0, width, height, 0, panel_x, panel_y)


def render_message_panel(message_log, title, con, panel_x, panel_y, width, height, color, current_turn):
    setup_console(con, caption=title, borders=True, bordercolor=color)

    y = 1
    for message in reversed(message_log.messages):
        if current_turn - message.turn <= 1:
            color_coefficient = 1.0
        elif current_turn - message.turn <= 2:
            color_coefficient = 0.6
        elif current_turn - message.turn <= 3:
            color_coefficient = 0.4
        else:
            color_coefficient = 0.2

        color = tuple(int(color_coefficient * x) for x in message.color)
        print_string(con, message_log.x, y, message.text, color=color)
        y += 1

    tcod.console_blit(con, 0, 0, width, height, 0, panel_x, panel_y)


def render_status_panel(game, console, panel_y, width, height):
    setup_console(console, fgcolor=colors.light_gray)

    draw_bar(console, 1, 1, 20, f'{game.player.fighter.hp_string}', int(game.player.fighter.hp), game.player.fighter.max_hp,
             game.player.fighter.hp_color, tcod.darkest_red)
    draw_bar(console, width-21, 1, 20, f'{game.player.fighter.stamina_string}', int(game.player.fighter.stamina), game.player.fighter.max_stamina,
             game.player.fighter.stamina_color, colors.darkest_blue)

    draw_quickslots(console, 0, game)

    tcod.console_blit(console, 0, 0, width, height, 0, 0, panel_y)
    tcod.console_print_frame(console, 0, 0, width, height)


def draw_bar(panel, x, y, total_width, name, value, maximum, bar_color, back_color):
    bar_width = int(float(value) / maximum * total_width)

    tcod.console_set_default_background(panel, back_color)
    tcod.console_rect(panel, x, y, total_width, 1, False, tcod.BKGND_SCREEN)

    tcod.console_set_default_background(panel, bar_color)
    if bar_width > 0:
        tcod.console_rect(panel, x, y, bar_width, 1, False, tcod.BKGND_SCREEN)

    print_string(panel, int(x + total_width / 2), y, f'%white%{name.title()}%', alignment = tcod.CENTER, background=tcod.BKGND_NONE)


def draw_quickslots(con, y, game):

    player = game.player

    total_slots = player.qu_inventory.capacity
    width = 3 * total_slots # every slot needs 3 pixels
    start_x = cfg.BOTTOM_PANELS_WIDTH // 2 - width // 2
    #start_x = (cfg.SIDE_PANEL_WIDTH // 2 - width // 2) + 2

    if total_slots > 0:
        o_x = start_x
        o_y = y
        tcod.console_put_char_ex(con, o_x, o_y, 218, colors.dark_gray, colors.black)
        tcod.console_put_char_ex(con, o_x, o_y+1, 179, colors.dark_gray, colors.black)
        tcod.console_put_char_ex(con, o_x, o_y+2, 192, colors.dark_gray, colors.black)
        o_x += 1
        for s in range(1,total_slots):
            tcod.console_put_char_ex(con, o_x, o_y, 196, colors.dark_gray, colors.black)
            tcod.console_put_char_ex(con, o_x, o_y+2, 196, colors.dark_gray, colors.black)
            o_x += 1
            tcod.console_put_char_ex(con, o_x, o_y, 194, colors.dark_gray, colors.black)
            tcod.console_put_char_ex(con, o_x, o_y+1, 179, colors.dark_gray, colors.black)
            tcod.console_put_char_ex(con, o_x, o_y+2, 193, colors.dark_gray, colors.black)
            o_x += 1
        tcod.console_put_char_ex(con, o_x, o_y, 196, colors.dark_gray, colors.black)
        tcod.console_put_char_ex(con, o_x, o_y+2, 196, colors.dark_gray, colors.black)
        o_x += 1
        tcod.console_put_char_ex(con, o_x, o_y, 191, colors.dark_gray, colors.black)
        tcod.console_put_char_ex(con, o_x, o_y+1, 179, colors.dark_gray, colors.black)
        tcod.console_put_char_ex(con, o_x, o_y+2, 217, colors.dark_gray, colors.black)

        o_x = start_x + 1
        for i, item in enumerate(player.qu_inventory.items):
            tcod.console_put_char_ex(con, o_x, y, f'{i+1}', colors.white, colors.black)
            print_string(con, o_x, y+1, f'{item.char}', color = item.color)
            o_x += 2
