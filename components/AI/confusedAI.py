from random import randint

import game
from gui.messages import Message, MessageType

# OLD TODO replace with convused behavior #
class ConfusedAI:
    def __init__(self, previous_ai, game, number_of_turns=10):
        self.previous_ai = previous_ai
        self.number_of_turns = number_of_turns

    def take_turn(self, game_map, entities):
        results = []

        if self.number_of_turns > 0:
            random_x = self.owner.x + randint(0, 2) - 1
            random_y = self.owner.y + randint(0, 2) - 1

            if random_x != self.owner.x and random_y != self.owner.y:
                self.owner.move_towards((random_x, random_y),game)

            self.number_of_turns -= 1
        else:
            self.owner.ai = self.previous_ai
            results.append({'message': Message(f'The {self.owner.name.title()} is no longer confused!', type=MessageType.BAD)})

        return results