import logging
from random import choice, randint

from config_files import cfg
from data.data_enums import Key, RarityType
from data.data_processing import gen_architecture_from_data, \
    gen_item_from_data, ITEM_DATA, CONTAINER_DATA
from data.data_util import filter_data_dict
from debug.timer import debug_timer
from map.entity_placement.util_functions import find_ent_position

@debug_timer
def place_containers(game):

    dlvl = game.dlvl
    game_map = game.map
    entities = game.entities
    rooms = game_map.rooms.copy()
    possible_objects = CONTAINER_DATA
    max_containers = int(len(rooms) * cfg.CONTAINER_DUNGEON_FACTOR)

    while len(game.container_ents) < max_containers and len(rooms) > 0:
        if len(game.container_ents) + 1 > max_containers:
            logging.debug(
                f'New container would bring dungeon total to {len(game.container_ents) + 1} thus exceed total maximum: ({max_containers})')
            break

        room = choice(rooms)
        logging.debug(f'Picked {room}.')
        while len(room.containers) == room.max_containers:
            logging.debug(f'But {room} has already {len(room.containers)}/{room.max_containers} present.')
            rooms.remove(room)
            if len(rooms) == 0:
                room = None
                break
            room = choice(rooms)
            logging.debug(f'Picked new {room}.')

        if room is None:
            logging.debug(f'No more legal rooms available after placing {len(game.container_ents)} containers.')
            break

        key = filter_data_dict(possible_objects, dlvl)
        data = possible_objects[key]

        # If the container is a blocking object, get a free tile
        pos = find_ent_position(room, data, game, exclusive=True)
        if pos:
            con = gen_architecture_from_data(data, *pos)
            fill_container(con, dlvl, rarity_filter=data[Key.CONTENTS_RARITY], type_filter=data[Key.CONTENTS_TYPE],
                           forced_content=data.get('content_forced'))
            entities.append(con)
            room.containers.append(con)

        logging.debug(f'Placed {con.name} in {room} ({len(room.containers)}/{room.max_containers}). {len(game.container_ents)} of {max_containers} placed.')


def fill_container(container, dlvl, rarity_filter=None, type_filter=None, forced_content=None):
    """
    Fills the given container. Content can be either randomized using the content rarity and filter attributes or forced.

    :param container: Container entity.
    :type container: Entity
    :param dlvl: Current dungeon level
    :param rarity_filter: A tuple of rarity values, corresponding to Rarity Enum members.
    :type rarity_filter: tuple
    :param type_filter: A tuple of entity types, corresponding to EntityType Enum members.
    :type type_filter: tuple
    :param forced_content: A tuple of item data names, corresponding to the item's key in the data dictionaries.
    :type forced_content: tuple
    """

    logging.debug(f'Filling {container}')

    if forced_content:
        for i in forced_content:
            item = gen_item_from_data(ITEM_DATA.get(i), 0, 0)
            container.inventory.add(item)
            if container.inventory.is_full:
                break
    else:
        possible_items = {k: v for k, v in ITEM_DATA.items() if
                          v.get(Key.TYPE) in type_filter
                          and v.get(Key.RARITY, RarityType.COMMON) in rarity_filter}
        num_of_items = randint(0, container.inventory.capacity) # TODO replace with weighted randomness so the chance is lower the closer towards the cap
        logging.debug(f'Creating {num_of_items} items (Capacity: {container.inventory.capacity})')
        for i in range(num_of_items):
            key = filter_data_dict(possible_items, dlvl)
            if key is not None:
                data = possible_items[key]
                item = gen_item_from_data(data, 0, 0)
                container.inventory.add(item)