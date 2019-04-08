""" Processes the actions from handle_keys into game-events """
import logging
from typing import List, Optional, Dict

import tcod

from config_files import colors
from data.data_processing import gen_npc_from_data, NPC_DATA_MERGED, ITEM_DATA_MERGED, gen_item_from_data
from data.data_types import ItemType
from game import GameState
from gameobjects.util_functions import entity_at_pos
from gui.manual import display_manual
from gui.menus import item_menu, generic_options_menu, item_list_menu
from debug.menu import debug_menu
from gui.messages import Message, MessageType, MessageCategory
from loader_functions.data_loader import save_game
from rendering.render_animations import animate_move_line, animate_projectile


def process_player_input(action, game, last_turn_results:Optional[Dict]):
    player = game.player

    exit = action.get('exit')
    fullscreen = action.get('fullscreen')
    prepare = action.get('prepare')
    # drop_inventory = action.get('drop_inventory')
    # menu_selection = action.get('menu_selection')
    toggle_look = action.get('toggle_look')
    toggle_fire = action.get('toggle_fire')

    turn_results = []

    targeting_item = last_turn_results.get('targeting_item')
    debug_spawn = last_turn_results.get('debug_spawn')

    # Player Movement and Interaction #
    if game.state in [GameState.PLAYERS_TURN, GameState.PLAYER_RESTING]:
        turn_results.extend(process_player_interaction(game, action))

    # Inventory Interaction #
    if game.state in [GameState.SHOW_INVENTORY, GameState.SHOW_QU_INVENTORY, GameState.SHOW_EQUIPMENT]:
        turn_results.extend(process_inventory_interaction(game, prepare))

    # Cursor Movement & Targeting #
    if game.state in [GameState.CURSOR_ACTIVE, GameState.CURSOR_TARGETING]:
        turn_results.extend(process_cursor_interaction(game, action, targeting_item, debug_spawn))

    if toggle_look:
        game.toggle_cursor(player.pos)

    if toggle_fire:
        if player.active_weapon_is_ranged:
            nearest_ent = player.nearest_entity(game.npc_ents, max_dist=player.active_weapon.attack_range[1])
            pos = nearest_ent.pos if nearest_ent is not None else player.pos
            game.toggle_cursor(pos, state=GameState.CURSOR_TARGETING)
        else:
            turn_results.append({'message': Message('PLACEHOLDER: Need ranged weapon to fire.', type=MessageType.SYSTEM)})

    # Other #
    if exit:
        if game.state in (GameState.SHOW_INVENTORY, GameState.SHOW_QU_INVENTORY, GameState.CURSOR_ACTIVE, GameState.CURSOR_TARGETING):
            game.state = GameState.PLAYERS_TURN
        else:
            if player.fighter.hp > 0:
                #test_menu(game)
                choice = generic_options_menu('Quit Game', 'Do you want to quit the game?', ['Save & Quit', 'Just Quit'], game, sort_by=1, cancel_with_escape=True)
                if choice == 0:
                    save_game(game)
                    return False
                elif choice == 1:
                    return False
            else:
                return False

    if fullscreen:
        tcod.console_set_fullscreen(not tcod.console_is_fullscreen())

    return turn_results

def process_player_interaction(game, action):
    debug = action.get('debug')
    manual = action.get('manual')
    move = action.get('move')
    # dodge = action.get('dodge')
    interact = action.get('interact')
    direction = action.get('dir')
    wait = action.get('wait')
    pickup = action.get('pickup')
    prepare = action.get('prepare')
    quick_use_idx = action.get('quick_use')
    show_inventory = action.get('show_inventory')
    show_equipment = action.get('show_equipment')
    show_prepared = action.get('show_prepared')
    # drop_inventory = action.get('drop_inventory')
    # menu_selection = action.get('menu_selection')
    toggle_dodge = action.get('toggle_dodge')
    toggle_block = action.get('toggle_block')
    toggle_weapon = action.get('toggle_weapon')

    player = game.player
    game_map = game.map
    entities = game.entities
    fov_map = game.fov_map

    results = []

    if move or interact:
        dx, dy = direction
        destination_x, destination_y = player.x + dx, player.y + dy
        dodging = player.fighter.is_dodging

        if not game_map.is_wall(destination_x, destination_y):
            target = entity_at_pos(game.walk_blocking_ents, destination_x, destination_y)

            if target is None and interact:  # Check for non-blocking interactable objects
                target = entity_at_pos(game.interactable_ents, destination_x, destination_y)

            if target:
                if player.can_attack is False:
                    results.append({'message': Message('You are unable to attack!',
                                                       type=MessageType.COMBAT_BAD)})
                elif dodging:
                    Message('PLACEHOLDER: cant dodge into target.', type=MessageType.SYSTEM).add_to_log(game)
                # If a NPC is blocking the way #
                elif target.fighter:
                    if player.fighter.is_blocking:
                        results.append({'message': Message('PLACEHOLDER: cant attack while blocking.',
                                                                type=MessageType.SYSTEM)})
                    else:
                        if player.active_weapon_is_ranged:  # TODO should attacking in melee with a ranged weapon incur penalties or be disabled?
                            attack_results = player.fighter.attack_setup(target, game, dmg_mod_multipl=0.2,
                                                                         ignore_moveset=True)
                            results.append({'message': Message(
                                'PLACEHOLDER: attacking with ranged weapon in melee.', type=MessageType.SYSTEM)})
                        else:
                            attack_results = player.fighter.attack_setup(target, game)

                        results.extend(attack_results)
                # If a static object is blocking the way #
                elif target.architecture:

                    if interact and target.architecture.on_interaction:  # interacting with a architecture entity
                        interaction_results = target.architecture.on_interaction(player, target, game)
                        results.extend(interaction_results)

                    if move and target.architecture.on_collision:  # bumping into the object
                        collision_results = target.architecture.on_collision(player, target, game)
                        results.extend(collision_results)
                # elif move: # TODO Are these still required?
                #     print('PLACEHOLDER: Your way is blocked.')
                # elif interact:
                #     print('PLACEHOLDER: There is nothing to interact with')
            elif move:
                if player.can_move is False:
                    results.append({'message': Message('You are unable to move!',
                                                       type=MessageType.COMBAT_BAD)})
                elif dodging:
                    results.extend(player.fighter.dodge(dx, dy, game))
                else:
                    player.move(dx, dy)

                results.append({'fov_recompute': True})

            if not target or not target.fighter:
                # Movement other than fighting resets the current moveset
                if player.fighter.active_weapon is not None:
                    player.fighter.active_weapon.moveset.cycle_moves(reset=True)

            game.state = GameState.ENEMY_TURN

    # Passing a turn #
    elif wait:
        results.append({'waiting': True})

    # Picking up an item #
    elif pickup:
        items = [item for item in game.item_ents if item.same_pos_as(player)]
        if items:
            # Option menu is displayed if > 1 item is on the ground
            choice = items[0] if len(items) == 1 else \
                item_list_menu(player, items, game, title='Select Item', body='Pick up which item?')
            if choice is not None:
                pickup_results = player.inventory.add(choice)
                results.extend(pickup_results)
        else:
            results.append({'message': Message('There is nothing here.', category=MessageCategory.OBSERVATION)})

    # Combat related #
    if toggle_block:
        results.extend(player.fighter.toggle_blocking())

    if toggle_dodge:
        results.extend(player.fighter.toggle_dodging())

    # No dodging while blocking possible; disable one or the other, depending on input
    if player.fighter.is_blocking and player.fighter.is_dodging:
        if toggle_block:
            player.fighter.toggle_dodging()
        elif toggle_dodge:
            player.fighter.toggle_blocking()
        else:
            logging.debug('ERROR: Both blocking and dodging active.')


    if toggle_weapon:
        new_weapon = player.fighter.toggle_weapon()
        results.append({'weapon_switched': new_weapon})


    # Quick use handling #
    if quick_use_idx and quick_use_idx <= len(player.qu_inventory):
        quick_use_item = player.qu_inventory[quick_use_idx - 1]  # -1 as the idx is passed as a number key
        qu_results = player.qu_inventory.use(quick_use_item, game, entities=entities, fov_map=fov_map)
        results.extend(qu_results)

    # Inventory display #
    if show_inventory or prepare:
        if show_inventory and len(player.inventory) == 0:
            Message('Your inventory is empty.', category=MessageCategory.OBSERVATION).add_to_log(game)
        elif prepare and len(player.inventory.useable_items) > 0:
            Message('You have no items to prepare.', category=MessageCategory.OBSERVATION).add_to_log(game)
        else:
            game.previous_state = game.state
            game.state = GameState.SHOW_INVENTORY

    if show_prepared:
        if len(player.qu_inventory) > 0:
            game.previous_state = game.state
            game.state = GameState.SHOW_QU_INVENTORY
        else:
            Message('You have no items prepared.', category=MessageCategory.OBSERVATION).add_to_log(game)

    if show_equipment:
        if len(player.paperdoll.equipped_items) > 0:
            game.previous_state = game.state
            game.state = GameState.SHOW_EQUIPMENT
        else:
            Message('You have no items equipped.', category=MessageCategory.OBSERVATION).add_to_log(game)

    # Other #
    if manual:
        display_manual()

    if debug:
        results.extend(debug_menu(game))

    return results

def process_inventory_interaction(game, prepare):
    player = game.player
    selected_item_ent = None

    results = []

    if game.state == GameState.SHOW_INVENTORY:
        if not prepare:
            selected_item_ent = item_list_menu(player, player.inventory, game)
        else:
            selected_item_ent = item_list_menu(player, player.inventory.useable_items, game, body='Prepare which item?')

    elif game.state == GameState.SHOW_EQUIPMENT:
        #render_equipment_window(player.paperdoll.equipped_items, game)
        selected_item_ent = item_list_menu(player, player.paperdoll.equipped_items, game, title='Equipment')

    elif game.state == GameState.SHOW_QU_INVENTORY:
        selected_item_ent = item_list_menu(player, player.qu_inventory, game, title='Prepared Items')

    if game.state in [GameState.SHOW_INVENTORY, GameState.SHOW_QU_INVENTORY, GameState.SHOW_EQUIPMENT]:
        if selected_item_ent:
            # Identify unknown items #
            if not selected_item_ent.item.identified:
                selected_item_ent.item.identify()

            inventory = player.inventory
            if game.state == GameState.SHOW_QU_INVENTORY:
                inventory = player.qu_inventory

            if not prepare:
                item_use_choice = item_menu(selected_item_ent, game)
            else:
                item_use_choice = 'p'

            if item_use_choice:
                if item_use_choice == 'u':
                    item_interaction_result = inventory.use(selected_item_ent, game)
                    results.extend(item_interaction_result)
                if item_use_choice == 'e':
                    item_interaction_result = player.paperdoll.equip(selected_item_ent, game)
                    results.extend(item_interaction_result)
                if item_use_choice == 'r':
                    item_interaction_result = player.paperdoll.dequip(selected_item_ent)
                    results.extend(item_interaction_result)
                if item_use_choice == 'p':
                    item_interaction_result = inventory.prepare(selected_item_ent)
                    results.extend(item_interaction_result)
                if item_use_choice == 'd':
                    item_interaction_result = inventory.drop(selected_item_ent)
                    results.extend(item_interaction_result)
            else:
                game.state = game.previous_state
        else:
            game.state = game.previous_state

    return results

def process_cursor_interaction(game, action, targeting_item, debug_spawn):
    results = []

    player = game.player
    cursor = game.cursor
    fov_map = game.fov_map

    move = action.get('move')
    direction = action.get('dir')
    exit = action.get('exit')
    confirm = action.get('confirm')

    if move:
        dx, dy = direction
        destination_x = cursor.x + dx
        destination_y = cursor.y + dy
        if fov_map.fov[destination_y, destination_x]:
            if game.state == GameState.CURSOR_TARGETING:
                if player.active_weapon_is_ranged and targeting_item is None: # If player is aiming with a ranged weapon
                    dist = player.distance_to_pos(destination_x, destination_y)
                    if dist == 0 or dist in range(*player.active_weapon.attack_range):
                        cursor.try_move(dx, dy, game, ignore_entities=True)
                elif targeting_item is not None and player.distance_to_pos(destination_x, destination_y) in\
                        range(*targeting_item.item.useable.on_use_params.get('range', 1)): # If player is aiming with an item
                    cursor.try_move(dx, dy, game, ignore_entities=True)
            else:
                cursor.move(dx, dy)

    if confirm:
        if targeting_item is not None:  # Using an item
            inv = player.inventory if targeting_item in player.inventory else player.qu_inventory
            item_use_results = inv.use(targeting_item, game, target_pos=cursor.pos)
            results.extend(item_use_results)
        elif debug_spawn is not None:   # Using the wizard menu
            if debug_spawn in NPC_DATA_MERGED.keys() and not game.map.is_blocked(*cursor.pos, game.blocking_ents):
                ent = gen_npc_from_data(NPC_DATA_MERGED[debug_spawn], *cursor.pos, game)
                game.entities.append(ent)
            elif debug_spawn in ITEM_DATA_MERGED.keys() and not game.map.is_blocked(*cursor.pos, []):
                item = gen_item_from_data(ITEM_DATA_MERGED[debug_spawn], *cursor.pos)
                game.entities.append(item)
            else:
                results.append({'message':Message('Illegal position', type=MessageType.SYSTEM)})
        elif player.active_weapon_is_ranged:    # Using a ranged weapon
            target = entity_at_pos(game.blocking_ents, *cursor.pos)
            if target is not None and target.fighter is not None:
                attack_results = player.fighter.attack_setup(target, game)
                results.extend(attack_results)
            else:
                animate_projectile(*player.pos, *cursor.pos, game, color=colors.beige) # TODO ranged projectile color can later differ by weapon/ammo type
            results.append({'ranged_attack': True})

    if exit and (targeting_item or player.active_weapon_is_ranged):
        results.append({'targeting_cancelled': True})

    return results