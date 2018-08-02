class Tile:
    """
    A tile on a map. It may or may not be blocked, and may or may not block sight.
    """
    def __init__(self, blocked, x, y, game_map, block_sight=None, gibbed=False):
        self.blocked = blocked
        self.x, self.y = x, y

        # By default, if a tile is blocked, it also blocks sight
        if block_sight is None:
            block_sight = blocked

        self.block_sight = block_sight
        self.explored = 0
        self.gibbed = gibbed
        self.walkable = False
        self.map = game_map