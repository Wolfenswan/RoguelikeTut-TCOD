import logging
from random import randint, choice

import tcod

class BaseAI:
    def __init__(self, movement = None, attack=None):
        self.movement = movement

        if movement:
            self.movement.owner = self

        self.attack = attack

        if attack:
            self.attack.owner = self

    def take_turn(self, game, fov_map):

        results = []
        target = game.player
        game_map = game.map
        npc = self.owner

        # free_line = game.map.free_line_between_pos(target.x, target.y, npc.x, npc.y, game)
        # print(free_line)

        # Process action queue and planned action if applicable #
        planned_action_results = npc.actionplan.process_queue()
        if planned_action_results:
            results.extend(planned_action_results)

        # Otherwise check if the npc can see the player #
        elif tcod.map_is_in_fov(fov_map, npc.x, npc.y):
            npc.color_bg = None  # some special attacks modify a character's background color, this resets it

            # Consider using a skill #
            # TODO might be moved into behavior components later #
            if npc.skills:
                npc.cooldown_skills()
                available_skills = npc.available_skills(game)
                if available_skills:
                    skill = choice(available_skills)
                    skill_results = skill.execute(game)
                    results.extend(skill_results)
                    return results

            # If no skill is available, consider moving #
            if npc.distance_to_ent(target) >= 2:
                results.extend(self.movement.decide_move(target, game))

            # Or consider attack, if next to target #
            elif npc.distance_to_ent(target) < 2:
                results.extend(self.movement.decide_attack(target, game))

        # As last alternative, the npc will randomly move around #
        else:
            dx, dy = randint(-1, 1), randint(-1, 1)
            x, y = npc.x + dx, npc.y + dy
            if not game_map.is_wall(x, y):
                npc.move(dx, dy)

        return results
