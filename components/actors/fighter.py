from random import randint, choice

import logging

from config_files import colors
from gameobjects.entity import Entity
from gameobjects.util_functions import fighter_entity_at_pos, entity_at_pos
from gui.messages import Message, MessageType, MessageCategory
from rendering.render_animations import animate_move_line
from rendering.render_order import RenderOrder


class Fighter:
    def __init__(self, hp, stamina, base_av, base_dmg_range, base_vision):
        """

        :param hp:
        :type hp: int
        :param stamina:
        :type stamina: int
        :param defense:
        :type defense: int
        :param power:
        :type power: int
        :param vision:
        :type vision: int

        """
        self.max_hp = hp
        self.__hp = hp
        self.max_stamina = stamina
        self.__stamina = stamina
        self.__base_av = base_av
        self.__base_dmg_range = base_dmg_range
        self.__base_vision = base_vision

        self.is_blocking = False

    @property
    def hp(self):
        return self.__hp

    @property
    def hp_string(self):
        percentage = (self.__hp / self.max_hp * 100)
        if 86.0 <= percentage <= 100.0:
            return 'healthy'
        elif 71.0 <= percentage <= 85.0:
            return 'scratched'
        elif 25.0 <= percentage <= 70.0:
            return 'wounded'
        else:
            return 'near dead'

    @property
    def hp_color(self):
        percentage = (self.__hp / self.max_hp * 100)
        if 86.0 <= percentage <= 100.0:
            return colors.dark_green
        elif 71.0 <= percentage <= 85.0:
            return colors.light_green
        elif 25.0 <= percentage <= 70.0:
            return colors.light_red
        else:
            return colors.dark_red

    @hp.setter
    def hp(self, value):
        if value < 0:
            self.__hp = 0
        elif value > self.max_hp:
            self.__hp = self.max_hp
        else:
            self.__hp = value

    @property
    def stamina(self):
        return self.__stamina

    @property
    def stamina_string(self):
        pass

    @property
    def stamina_color(self):
        pass

    @stamina.setter
    def stamina(self, value):
        if value < 0:
            self.__stamina = 0
        elif value > self.max_stamina:
            self.__stamina = self.max_stamina
        else:
            self.__stamina = value

    # @property
    # def attack_power(self):
    #     """
    #     Power
    #
    #     :return:
    #     :rtype:
    #     """
    #     power = self.base_power
    #     for e in self.owner.paperdoll.equipped_items:
    #         dmg_range = vars(e.item.equipment).get('dmg_range')
    #         if dmg_range:
    #             power += randint(*dmg_range)
    #     return power

    @property
    def base_dmg_range(self):
        """
        Attribute returns the currently equipped weapon's range with the fighter's base power added.
        :return:
        :rtype:
        """
        if self.weapon:
            return (self.__base_dmg_range[0] + self.weapon.dmg_range[0], self.__base_dmg_range[1] + self.weapon.dmg_range[1])
        return (self.__base_dmg_range[0], self.__base_dmg_range[1])

    @property
    def modded_dmg_range(self):
        mod = self.weapon.moveset.dmg_mod
        return (round(self.base_dmg_range[0] * mod), round(self.base_dmg_range[1] * mod))

    @property
    def ignore_armor(self):
        return 0

    @property
    def defense(self):
        defense = self.__base_av
        for e in self.owner.paperdoll.equipped_items:
            av = vars(e.item.equipment).get('av')
            # This extra step is required as av value is set to None for all Equipments during data processing
            if av:
                defense += av
        return defense

    @property
    def vision(self):
        vision = self.__base_vision
        for e in self.owner.paperdoll.equipped_items:
            l_radius = vars(e.item.equipment).get('l_radius')
            # This extra step is required as l_radius value is set to None for all Equipments during data processing
            if l_radius:
                vision += l_radius
        return vision

    @property
    def weapon(self):
        """
        :return: Equipment component of currently equipped weapon.
        """
        weapon_ent = self.owner.paperdoll.weapon_arm.weapon # TODO add check for 2nd hand after implementing dual wielding
        if weapon_ent:
            return weapon_ent.item.equipment
        else:
            return None

    def take_damage(self, amount):
        results = []
        self.hp -= amount

        if self.hp <= 0:
            results.append({'dead': self.owner})

        return results

    def heal(self, amount):
        self.hp += amount

        if self.hp > self.max_hp:
            self.hp = self.max_hp

        logging.debug(f'({self} was healed for {amount}.')

    def attack_setup(self, target, game, mod=1):
        results = []
        ignore_armor = self.ignore_armor
        attack_string = 'attacks'
        extra_targets = []

        if self.weapon:
            move_results = self.weapon.moveset.execute(self.owner, target)
            mod += move_results.get('dmg_mod', 0)
            ignore_armor += move_results.get('ignore_armor', 0)
            attack_string = move_results.get('string', 'attacks')
            extra_targets = move_results.get('extra_targets', [])

        attack_power = choice(self.base_dmg_range) * mod
        damage = round(attack_power - (target.fighter.defense - ignore_armor))
        logging.debug(f'{self.owner.name.title()} attacks {target.name.title()} with {attack_power} power against {target.fighter.defense} defense for {damage} damage.')

        if game.debug['invin'] and target.is_player:
            damage = 0

        results.extend(self.attack_execute(target, damage, attack_string))

        for target_pos in extra_targets:
            if entity_at_pos(game.monster_ents, *target_pos):
                results.extend(self.attack_execute(target, damage//2, 'also hits'))

        return results

    def attack_execute(self, target, damage, attack_string):
        results = []

        # Targets out of stamina will receive double damage, defense value is negated
        # TODO balancing - Armor piercing currently applied as extra damage
        if target.fighter.stamina < 0:
            damage = (damage + target.fighter.defense) * 2

        if damage > 0:
            if target.fighter.is_blocking and target.fighter.stamina > 0:
                results.extend(target.fighter.block(damage))
            else:
                msg_type = MessageType.ALERT if target.is_player else MessageType.COMBAT

                if target == self.owner:
                    target_string = 'itself'
                elif target.is_player:
                    target_string = 'you'
                else:
                    target_string = target.name.title()

                results.append({'message': Message(
                    f'{self.owner.name.title()} {attack_string} {target_string} for {str(damage)} hit points.', type=msg_type)})
                results.extend(target.fighter.take_damage(damage))
        else:
            target.fighter.stamina -= 2 # TODO placeholder until balancing (scale stamina drain with armor encumberance)
            results.append(
                {'message': Message(f'{self.owner.name.title()} {attack_string} {target.name} but does no damage.', type=MessageType.COMBAT)})

        return results

    def block(self, damage):
        results = []
        self.stamina -= damage
        if self.owner.is_player:
            message = Message(f'You were able to block the attack!', type=MessageType.GOOD)
        else:
            message = Message(f'{self.owner.name.title()} was able to block the attack!', type=MessageType.COMBAT)
        results.append({'message': message})
        return results

    def dodge(self, dx, dy, game):
        if self.stamina >= 10:
            animate_move_line(self.owner, dx, dy, 2, game, anim_delay=0.001)
            self.stamina -= 10

    def toggle_blocking(self):
        self.is_blocking = not self.is_blocking

    def death(self, game):
        ent = self.owner
        ent.ai = None
        x, y = ent.x, ent.y
        ent.char = '%'
        ent.color = colors.corpse
        ent.color_bg = colors.black
        game.map.tiles[(x,y)].gibbed = True

        # Create gibs
        # TODO Consider force of impact (amount of damage done beyond 0 hp?) to vary spread
        for i in range(1, randint(2, 4)):
            c_x, c_y = (randint(x - 1, x + 1), randint(y - 1, y + 1))
            game.map.tiles[(c_x,c_y)].gibbed = True
            if not game.map.tiles[(c_x,c_y)].blocked and randint(0, 100) > 85:
                c = Entity(c_x, c_y, '~', colors.corpse, f'{ent.name.title()} bits', is_corpse=True)
                c.render_order = RenderOrder.CORPSE
                game.entities.append(c)

        if ent.is_player:
            message = Message('You died!', type=MessageType.BAD)
        else:
            message = Message(f'The {ent.name.title()} is dead!', type=MessageType.GOOD, category=MessageCategory.OBSERVATION)

            ent.render_order = RenderOrder.CORPSE
            ent.blocks['walk'] = False
            ent.ai = None
            ent.is_corpse = True
            ent.name = f'{ent.name.title()} remains'

        return message
