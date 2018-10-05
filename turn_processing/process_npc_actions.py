from debug.timer import debug_timer
from game import GameState

@debug_timer
def process_npc_actions(game):
    player = game.player
    move_order = sorted(game.npc_ents, key=lambda i: i.distance_to_ent(game.player))
    for entity in move_order:
        if entity.ai:
            enemy_turn_results = entity.ai.take_turn(game, game.fov_map)
            player.fighter.surrounded = player.fighter.check_surrounded(game) # Set the player's surrounded value accordingly

            for enemy_turn_result in enemy_turn_results:
                message = enemy_turn_result.get('message')
                dead_entity = enemy_turn_result.get('dead')

                if message:
                    message.add_to_log(game)

                if dead_entity:
                    message = dead_entity.fighter.death(game)
                    if dead_entity.is_player:
                        game.state = GameState.PLAYER_DEAD

                    message.add_to_log(game)

                    if game.state == GameState.PLAYER_DEAD:
                        break

            if game.state == GameState.PLAYER_DEAD:
                break
    else:
        game.state = GameState.PLAYERS_TURN