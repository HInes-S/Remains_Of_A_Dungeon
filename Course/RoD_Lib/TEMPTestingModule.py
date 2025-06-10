from Entities import Player
from LevelSetter import setLevel
from GameProcessHandler import Drawer, stepHandler, setSelectionPos
import pygame

from Objects import Trap

tsize = 20
WIDTH, HEIGHT = 800, 600

def image(path, tilesize):
    return pygame.transform.scale(pygame.image.load(path), (tilesize, tilesize))

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
    ]
]

dungeon_textures, walls_textures, objects, enemies, possibility_movement_map, player_cords = setLevel(40, 30, 1, textures)

player = Player(r"Tiles/TileSet/Player.png")
player.x, player.y = player_cords
player.hp = 100
player.dmg = 1
player.setLevel(1)
player.exp = 1

step_handler = stepHandler(objects, possibility_movement_map, enemies, player, 40, 30)

select_tile_texture = r"Tiles/TileSet/Select.png"

mousepos = []

def drawfunc(path: str, x: int, y: int, tilesize: int):
    return (pygame.transform.scale(pygame.image.load(path), (tilesize, tilesize)), (x, y))

drawer = Drawer(drawfunc, dungeon_textures, walls_textures, objects, enemies, player, select_tile_texture, step_handler.camera, tsize,
                WIDTH, HEIGHT)

def run():
    
    # Инициализация Pygame
    pygame.init()

    # Настройки окна
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Game")

    sel_pos = []

    # Игровой цикл
    running = True
    while running:

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Закрытие окна
                running = False

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_w:
                    step_handler.player_move([0, -1])
                elif event.key == pygame.K_s:
                    step_handler.player_move([0, 1])
                elif event.key == pygame.K_a:
                    step_handler.player_move([-1, 0])
                elif event.key == pygame.K_d:
                    step_handler.player_move([1, 0])
                
            if event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 1:
                    step_handler.click(drawer.selection_pos[0], drawer.selection_pos[1])
        # Очистка экрана
        screen.fill((0, 0, 0))

        mpos = pygame.mouse.get_pos()
        blit_images = drawer.draw_all(mpos[0], mpos[1])

        for img in blit_images:
            screen.blit(img[0], img[1])

        # Обновление экрана
        pygame.display.flip()

    # Завершение Pygame
    pygame.quit()

run()
