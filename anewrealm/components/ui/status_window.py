from components.ui.widgets.window import BorderedWindow
from constants import MAPWINDOW_WIDTH, STATUSWINDOW_WIDTH, \
    STATUSWINDOW_HEIGHT


class StatusWindow(BorderedWindow):
    """The Window that the status view is drawn in.

    This window is responsible for displaying the status of objects or
    entities in the game. This is where health bars, statuses,
    item descriptions etc. are drawn in.

    """

    def __init__(self):
        super().__init__(x=MAPWINDOW_WIDTH,
                         width=STATUSWINDOW_WIDTH,
                         height=STATUSWINDOW_HEIGHT,
                         title='STATUS')
