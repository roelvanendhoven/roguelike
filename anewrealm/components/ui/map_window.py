from anewrealm.components.ui.widgets.window import BorderedWindow
from anewrealm.constants import MAPWINDOW_WIDTH, MAPWINDOW_HEIGHT
from anewrealm.components.map import Map
from anewrealm.components.ui.map_view import MapView
from components.game import Player


class MapWindow(BorderedWindow):
    """The Window that the map view is drawn in.

    This window is responsible for displaying the map and handling map
    related key events such as movement indication and information popups.

    """

    def __init__(self):
        super().__init__(width=MAPWINDOW_WIDTH,
                         height=MAPWINDOW_HEIGHT,
                         title='MAP')
        self.map_view = MapView()
        self.map_view.tile_map = Map(0)
        self.map_view.tile_map.players = [Player('Roel', (0,255,0)),
                                          Player('Nick', (255,0,0), x = 4,
                                                 y =3)]

    @property
    def map_view(self) -> MapView:
        return self._map_view

    @map_view.setter
    def map_view(self, map_view: MapView):
        self._map_view = map_view
        map_view.x = 1
        map_view.y = 1
        map_view.width = MAPWINDOW_WIDTH - 1
        map_view.height = MAPWINDOW_HEIGHT - 1
        self.contents = [map_view]
