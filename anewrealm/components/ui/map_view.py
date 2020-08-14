from tcod import Console

from anewrealm.components.map import Map
from anewrealm.components.ui.util import Drawable


class MapView(Drawable):

    def __init__(self, x: int = 0, y: int = 0, width: int = 1,
                 height: int = 1):
        super().__init__(x, y, width, height)
        self._tile_map = None

    @property
    def tile_map(self) -> Map:
        return self._tile_map

    @tile_map.setter
    def tile_map(self, tile_map: Map):
        self._tile_map = tile_map

    def draw(self, console: Console) -> None:
        if not self.tile_map:
            return
        for y, row in enumerate(self.tile_map.tiles):
            for x, tile in enumerate(row):
                console.print(x + self.x, y + self.y, tile, (87, 65, 47),
                              bg=(34, 20, 13))
        for player in self.tile_map.players:
            # TODO: Players are now shifted left because the origin of the
            #  window lies there, however the map starts at x,y = 1. Find a
            #  way to reset the origin of the map
            player.entity.draw(console)
