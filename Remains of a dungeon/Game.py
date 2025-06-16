from sched import Event
from Lib.Entities import Player
from Lib.LevelSetter import setLevel
from Lib.GameProcessHandler import GameInitiator, Menu, Saves, Settings
import pygame

from Lib.Objects import Trap

tsize = 50
WIDTH, HEIGHT = 1000, 700

textures = [
    [
        r"Tiles/TileSet/Void.png",
        [
            r"Tiles/Walls2/D.png",
            r"Tiles/Walls2/U.png",
            r"Tiles/Walls2/L.png",
            r"Tiles/Walls2/R.png",
            r"Tiles/Walls2/ULcorner.png",
            r"Tiles/Walls2/DLcorner.png",
            r"Tiles/Walls2/URcorner.png",
            r"Tiles/Walls2/DRcorner.png",
        ],
        r"Tiles/TileSet/Floor.png",
        r"Tiles/TileSet/Water.png",
    ],
    [
        r"Tiles/TileSet/Door.png",
        r"Tiles/TileSet/Trap.png",
        r"Tiles/TileSet/Chest.png",
        r"Tiles/TileSet/Ladder.png",
        [
            r"Tiles/TileSet/Weapon.png",
            r"Tiles/TileSet/Armor.png",
            r"Tiles/TileSet/PotionH.png",
            r"Tiles/TileSet/Scroll.png",
            r"Tiles/TileSet/Food.png",
        ],
    ],
    [
        r"Tiles/TileSet/Enemy1.png",
        r"Tiles/TileSet/Enemy2.png",
    ],
    [
        r"Tiles/TileSet/Player.png"
    ],
    [
        r"Tiles/TileSet/Select.png"
    ],
    [
        r"Tiles/Inventory.png"
    ]
]

mousepos = []

def draw_text(screen: pygame.Surface, text: str, fontsize: int, x: int = -1, y: int = -1):

    font = pygame.font.Font(None, fontsize)

    text_surface = font.render(text, True, (0, 0, 0))
    screen.blit(text_surface, (x - 2, y - 2))
    screen.blit(text_surface, (x + 2, y - 2))
    screen.blit(text_surface, (x - 2, y + 2))
    screen.blit(text_surface, (x + 2, y + 2))

    text_surface = font.render(text, True, (255, 255, 255))

    if x == -1 and y == -1:
        w, h = text_surface.get_width(), text_surface.get_height()
        pos = ((screen.get_width() - w) // 2, (screen.get_height() - h) // 2)
        screen.blit(text_surface, pos)
    else:
        screen.blit(text_surface, (x, y))

def game_drawtext(x: int, y: int, text: str, w: int = 0, h: int = 0, fontsize: int = 30):

    font = pygame.font.Font(None, fontsize)

    size = font.render(text, True, (0, 0, 0)).get_size()

    retImg = pygame.Surface((size[0] + 4, size[1] + 4), pygame.SRCALPHA)

    text_surface = font.render(text, True, (0, 0, 0))
    retImg.blit(text_surface, (0, 0))
    retImg.blit(text_surface, (4, 0))
    retImg.blit(text_surface, (0, 4))
    retImg.blit(text_surface, (4, 4))

    text_surface = font.render(text, True, (255, 255, 255))

    retImg.blit(text_surface, (2, 2))

    tsize = retImg.get_size()

    if tsize[0] <= w and tsize[1] <= h:
        return (retImg, (x + (w - tsize[0]) // 2, y + (h - tsize[1]) // 2))
    else:
        return (retImg, (x, y))

def drawfunc(path: str, x: int, y: int, tilesize: int = -1):
    if tilesize == -1:
        return (pygame.image.load(path), (x, y))
    else:
        return (pygame.transform.scale(pygame.image.load(path), (tilesize, tilesize)), (x, y))

def fgame(screen: pygame.Surface, gameinitiator: GameInitiator, drawInv: bool, events: list[Event]):

    # Обработка событий
        for event in events:
            if event.type == pygame.QUIT:  # Закрытие окна
                running = False

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_w:
                    gameinitiator.step_handler.player_move([0, -1])
                elif event.key == pygame.K_s:
                    gameinitiator.step_handler.player_move([0, 1])
                elif event.key == pygame.K_a:
                    gameinitiator.step_handler.player_move([-1, 0])
                elif event.key == pygame.K_d:
                    gameinitiator.step_handler.player_move([1, 0])

                elif event.key == pygame.K_e:
                    drawInv = not drawInv

                elif event.key == pygame.K_DOWN:
                    gameinitiator.invDown()
                elif event.key == pygame.K_UP:
                    gameinitiator.invUp()
                elif event.key == pygame.K_LEFT:
                    gameinitiator.invLeft()
                elif event.key == pygame.K_RIGHT:
                    gameinitiator.invRight()

                elif event.key == pygame.K_RETURN:
                    gameinitiator.useItem()

                elif event.key == pygame.K_ESCAPE:
                    gameinitiator.save()
                    return "menu", False
                
            elif event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 1:
                    gameinitiator.click()
                elif event.button == 2:
                    gameinitiator.default_scale()

            elif event.type == pygame.MOUSEWHEEL:

                if event.y == 1:
                    gameinitiator.zoom()
                elif event.y == -1:
                    gameinitiator.dezoom()

        # Очистка экрана
        screen.fill((0, 0, 0))

        if gameinitiator.isDeath:
            draw_text(screen, "YOU DIED", 100)
        else:
            mpos = pygame.mouse.get_pos()
            if drawInv:
                blit_images = gameinitiator.draw_all(pygame.mouse.get_pos(), drawInv, (10, 500))
            else:
                blit_images = gameinitiator.draw_all(pygame.mouse.get_pos(), drawInv)

            for img in blit_images:
                screen.blit(img[0], img[1])

            hud = gameinitiator.getHud().split('\n')
            for i in range(len(hud)):
                draw_text(screen, hud[i], 30, 10, 10 + 30 * i)

        return "game", drawInv

def fmenu(screen: pygame.Surface, menu: Menu, events: list[Event], saves: list[Saves]):

    for event in events:
        if event.type == pygame.QUIT:  # Закрытие окна
            pygame.quit()
            return ""

        elif event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1:
                scenestring = menu.click(pygame.mouse.get_pos())
                if scenestring == "saves":
                    saves[0] = Saves("saveslist.txt", r"Tiles/background.png", r"Tiles/button.png", 200, 30, 10, (400, 100))
                return scenestring

    screen.fill((0, 0, 0))

    blit_images = menu.draw(drawfunc, game_drawtext)

    for img in blit_images:
        screen.blit(img[0], img[1])

    return 'menu'

def fsettings(screen: pygame.Surface, settings: Settings, events: list[Event]):

    for event in events:
        if event.type == pygame.QUIT:  # Закрытие окна
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1:
                settings.click(pygame.mouse.get_pos())

        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                return "menu"

    screen.fill((0, 0, 0))

    blit_images = settings.draw(drawfunc, game_drawtext, 350, 650, 300, 350)

    for img in blit_images:
        screen.blit(img[0], img[1])

    return "settings"

def fsaves(screen: pygame.Surface, saves: Saves, events: list[Event]):

    for event in events:
        if event.type == pygame.QUIT:  # Закрытие окна
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1:
                ret = saves.click(pygame.mouse.get_pos())
                if ret != None:
                    return ret

        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                return "menu"

    screen.fill((0, 0, 0))

    blit_images = saves.draw(drawfunc, game_drawtext)

    for img in blit_images:
        screen.blit(img[0], img[1])

    return "saves"

def run():
    
    # Инициализация Pygame
    pygame.init()

    # Настройки окна
    WIDTH, HEIGHT = 1000, 700
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Game")

    sel_pos = []

    drawInv = False

    gameinitiator = GameInitiator(drawfunc, 40, 30, textures, 1000, 700, 1)

    current_scene = "menu"

    menu = Menu(r"Tiles/background.png",
                [r"Tiles/button.png" for _ in range(4)],
                [(400, 200 + 100 * i) for i in range(4)],
                [(200, 30) for _ in range(4)])

    settings = Settings(r"Tiles/background.png",
                        600, 690, 295, 40, 30, 20, r"Tiles/button2.png")

    saves = [Saves("saveslist.txt", r"Tiles/background.png", r"Tiles/button.png", 200, 30, 10, (400, 100))]

    # Игровой цикл
    clock = pygame.time.Clock()
    running = True
    while running:

        clock.tick(60)

        events = pygame.event.get()

        if current_scene == "menu":
            gameinitiator = GameInitiator(drawfunc, settings.gw, settings.gh, textures, 1000, 700, 1)
            current_scene = fmenu(screen, menu, events, saves)
        elif current_scene == "settings":
            current_scene = fsettings(screen, settings, events)
        elif current_scene == "quit":
            break
        elif current_scene == "saves":
            result = fsaves(screen, saves[0], events)
            if isinstance(result, str):
                current_scene = result
            else:
                current_scene = "game"
                gameinitiator = result
        elif current_scene == "game":
            current_scene, drawInv = fgame(screen, gameinitiator, drawInv, events)
        else:
            break

        try:
            pygame.display.flip()
        except:
            pass

    # Завершение Pygame
    pygame.quit()

run()
