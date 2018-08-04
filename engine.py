import logging
import os

import tcod

from config_files import cfg
from game import GameStates, Game
from gui.menus import options_menu
from loader_functions.data_loader import save_game, load_game
from turn_processing.handle_input import handle_keys
from turn_processing.process_player_actions import process_player_input
from loader_functions.initialize_game import initialize_game
from loader_functions.initialize_logging import initialize_logging
from loader_functions.initialize_window import initialize_window
from rendering.fov_functions import initialize_fov, recompute_fov
from rendering.render_main import clear_all, render_main_screen, render_panels
from rendering.render_windows import render_description_window
from turn_processing.process_turn_results import process_turn_results


def game_loop(game):
    player = game.player
    entities = game.entities
    fov_map = game.fov_map
    con = game.con
    message_log = game.message_log

    game.state = GameStates.PLAYERS_TURN
    game.previous_state = game.state

    targeting_item = None

    fov_recompute = True

    key = tcod.Key()
    # mouse = tcod.Mouse()

    turn = 1
    while not tcod.console_is_window_closed():
        # tcod.sys_set_fps(30)
        # tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS | tcod.EVENT_MOUSE, key, mouse)

        logging.debug(f'Beginning turn {turn}. Recomputing FOV: {fov_recompute}')

        if fov_recompute:
            recompute_fov(fov_map, player.x, player.y)
            fov_recompute = False

        render_main_screen(game, fov_map)
        render_panels(game)

        if game.state == GameStates.CURSOR_ACTIVE:
            render_description_window(game)

        tcod.console_flush()

        clear_all(con, entities)

        tcod.sys_wait_for_event(tcod.EVENT_KEY_PRESS, key, None, True)

        action = handle_keys(key, game.state)
        #mouse_action = handle_mouse(mouse)

        # Process player input into turn results #
        player_turn_results = process_player_input(action, game, fov_map, targeting_item = targeting_item)

        logging.debug(f'Turn {turn} player results: {player_turn_results}')

        # Player turn results is None if the game should exit #
        if player_turn_results is None:
            return True

        # Process turn results #
        processed_turn_results = process_turn_results(player_turn_results, game, fov_map)

        logging.debug(f'Turn {turn} processed results: {player_turn_results}')

        for turn_result in processed_turn_results:
            fov_recompute = turn_result.get('fov_recompute', False)
            targeting_item = turn_result.get('targeting_item', None)

        # Enemies take turns #
        if game.state == GameStates.ENEMY_TURN:
            move_order = sorted(entities, key=lambda i: i.distance_to_ent(player))
            for entity in move_order:
                if entity.ai:
                    enemy_turn_results = entity.ai.take_turn(game, fov_map)

                    for enemy_turn_result in enemy_turn_results:
                        message = enemy_turn_result.get('message')
                        dead_entity = enemy_turn_result.get('dead')

                        if message:
                            message_log.add_message(message)

                        if dead_entity:
                            message = dead_entity.fighter.death(game.map)
                            if dead_entity.is_player:
                                game.state = GameStates.PLAYER_DEAD

                            message_log.add_message(message)

                            if game.state == GameStates.PLAYER_DEAD:
                                break

                    if game.state == GameStates.PLAYER_DEAD:
                        break
            else:
                game.state = GameStates.PLAYERS_TURN


if __name__ == '__main__':
    initialize_logging(debugging=True)
    game = Game(debug=False)
    initialize_window(game)

    choice = options_menu(cfg.GAME_NAME, 'Welcome to the Dungeon', options=['Play a new game', 'Continue last game', 'Quit'], cancel_with_escape=False, sort_by=1)
    if choice == 0:
        game = initialize_game(game)
    elif choice == 1:
        try:
            game = load_game()
        except:
            # TODO show a file loading error popup
            pass
    elif choice == 2:
        exit()

    game.fov_map = initialize_fov(game)

    game_loop(game)
    save_game(game) # TODO placeholder for testing purposes
