import tcod
import tcod.console
import tcod.event

from components import particle
import game

# Constants
SCREEN_WIDTH = 50
SCREEN_HEIGHT = 30

GAME_TITLE = "Net Test"

FONT = 'assets/font_12x12.png'
FONT_OPTIONS_MASK = tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD


def init_tcod() -> tcod.console.Console:
    tcod.console_set_custom_font(FONT, FONT_OPTIONS_MASK)

    root_console = tcod.console_init_root(
        SCREEN_WIDTH,
        SCREEN_HEIGHT,
        GAME_TITLE,
        renderer=tcod.RENDERER_SDL2,
        fullscreen=False,
        vsync=True,
        order='F')

    tcod.sys_set_fps(30)
    return root_console


def game_loop(console):

    g = game.Game()
    g.players.append(game.Player('Roel',(50,255,50)))
    g.players.append(game.Player('Dude',(50,50,255)))
    g.players.append(game.Player('Minge',(255,50,50)))
    g.start()

    while True:
        tcod.console_flush()
        console.clear()

        g.draw_state(console)
        console.draw_frame(
            0, 0,
            SCREEN_WIDTH, SCREEN_HEIGHT,
            'Welcome to game :)',
            clear=False
        )

        console.print(1,1, 'Turn: %d | Current Player %s' % (g.turncount, g.current_player.name))

        for event in tcod.event.get():
            if event.type == "QUIT":
                exit()
            if event.type == "KEYDOWN":
                action = game.Action()
                action.type = 'MOVE'
                print(event.sym)
                if event.sym == ord("d"):
                    action.value = (g.current_player.entity.x+1,g.current_player.entity.y)
                if event.sym == ord("a"):
                    action.value = (g.current_player.entity.x-1,g.current_player.entity.y)
                if event.sym == ord("s"):
                    action.value = (g.current_player.entity.x,g.current_player.entity.y+1)
                if event.sym == ord("w"):
                    action.value = (g.current_player.entity.x,g.current_player.entity.y-1)
                g.take_turn(action)



def main():
    root_console = init_tcod()
    game_loop(root_console)
    print("Rogue like Jagger")


if __name__ == "__main__":
    main()
