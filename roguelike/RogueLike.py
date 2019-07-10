import tcod
import tcod.console
import tcod.event

import particle

# Constants
SCREEN_WIDTH = 160
SCREEN_HEIGHT = 90

GAME_TITLE = "Rogue Like Jagger"

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
    tcod.console_set_fullscreen(True)
    return root_console


def game_loop(console):
    emitter = particle.Emitter(console, 1, SCREEN_HEIGHT - 1, SCREEN_WIDTH - 23, 1)
    bee = open('assets/bee.txt').read()
    wiz = tcod.image_load('assets/wizard_idle_dark.bmp')
    # wiz.set_key_color((0, 0, 0))
    i = 20
    glow = 0
    while True:
        tcod.console_flush()
        console.clear()
        emitter.create_particle()
        emitter.draw()

        console.draw_frame(
            0, 0,
            SCREEN_WIDTH, SCREEN_HEIGHT,
            'Welcome to game :)',
            clear=False
        )

        wiz.blit(console, SCREEN_WIDTH - 32,  SCREEN_HEIGHT // 2, tcod.BKGND_SCREEN, 1.5, 1.5, 0)
        console.print_box(3, 3, SCREEN_WIDTH - 64, SCREEN_HEIGHT - 3, bee[0:i], fg=(217, 130, 67))
        console.print(SCREEN_WIDTH - 2, 1, str(chr(30)), fg=(252, 149, 71))
        console.print(SCREEN_WIDTH - 2, SCREEN_HEIGHT - 2, str(chr(31)), fg=(252, 149, 71))

        glow = (glow + 0.1) % 6
        if i < len(bee):
            i += 1

        print(glow)
        # console.print(0,0,'lol hi!')
        for event in tcod.event.get():
            if event.type == "QUIT": exit()
            if event.type == "KEYDOWN":
                print(i)


def main():
    root_console = init_tcod()
    game_loop(root_console)
    print("Rogue like Jagger")


if __name__ == "__main__":
    main()
