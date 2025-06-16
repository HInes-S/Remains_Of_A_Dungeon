from .Objects import *
from .Items import *
from random import randrange
from random import randint
from .Entities import *
from .GeneratorFunctions import generate_final_dungeon_map, generate_enemies
from .TextureHandler import setDungeonTextures

def setObjects(ladder: list, doors: list, traps: list, chests: list, textures: list, level: int):

    '''
    textures is a list of paths to images of: ladder, door, trap, chest, ladder, [weapon, armor, potion, scroll, food]
    '''

    itemShabloons = [Weapon, Armor, Potion, Scroll, Food]

    objects = []

    for door in doors:
        objects.append(Door(textures[0], door[0], door[1]))

    for chest in chests:
        num = randrange(len(itemShabloons))
        chestItem = itemShabloons[num](textures[4][num], randint(level // 2, level))
        objects.append(Chest(textures[2], chest[0], chest[1], chestItem))

    for trap in traps:
        objects.append(Trap(textures[1], trap[0], trap[1], trap[2], trap[3], randint(level, level * 2)))

    objects.append(Ladder(textures[3], ladder[0], ladder[1]))

    return objects

def setEnemies(enemies_cords: list, textures: list[str], level: int):

    enemies = []

    for ecord in enemies_cords:
        enemy = Enemy(textures[randrange(len(textures))])
        enemy.x = ecord[0]
        enemy.y = ecord[1]
        enemy.hp = randint(level * 3, level * 5)
        enemy.dmg = randint(level // 2, level)
        enemy.view_range = randint(1, 4)
        enemies.append(enemy)

    return enemies

def setLevel(width: int, height: int, level: int, textures: list):

    '''
    textures:[
        [void, walls[8], floor, water]
        [door, trap, chest, [weapon, armor, potion, scroll, food]]
        enemies[]
    ]
    '''

    raw_dungeon_textures = textures[0]
    objects_textures = textures[1]
    enemies_textures = textures[2]

    maxRS = min(height - 2, width // 3)
    minRS = 4
    margin = 2

    dungeon, rooms, dungeon_walls, doors, traps, chests = generate_final_dungeon_map(width, height, maxRS, minRS, margin)

    enemies_cords = generate_enemies(rooms, chests, doors, traps, level)

    #Create Ladder
    can_spawn = [[x, y] for r in rooms for x in range(r[0] + 1, r[0] + r[2] - 1, 1) for y in range(r[1] + 1, r[1] + r[3] - 1, 1)]
    can_spawn = [c for c in can_spawn if (not (c in doors)) and
                                         (not (c in chests)) and
                                         (not (c in [[t[0], t[1]] for t in traps])) and
                                         (not (c in enemies_cords))]
    ladder_cords = can_spawn[randrange(len(can_spawn))]
    #Create Ladder

    #Set Player cords
    cr = rooms[randrange(len(rooms))] #choosed room
    for i in range(len(enemies_cords) - 1, -1, -1): #delete enemies from room
        if (enemies_cords[i][0] in range(cr[0] + 1, cr[0] + cr[2] - 1) and
            enemies_cords[i][1] in range(cr[1] + 1, cr[1] + cr[3] - 1)):
            del enemies_cords[i]
    can_spawn = [[x, y] for x in range(cr[0] + 1, cr[0] + cr[2] - 1) for y in range(cr[1] + 1, cr[1] + cr[3] - 1)]
    can_spawn = [c for c in can_spawn if (not (c in doors)) and
                                         (not (c in chests)) and
                                         (not (c in [[t[0], t[1]] for t in traps])) and
                                         c != ladder_cords]
    player_cords = can_spawn[randrange(len(can_spawn))]
    #Set Player cords

    dungeon_textures, walls_textures = setDungeonTextures(dungeon, dungeon_walls, raw_dungeon_textures)

    objects = setObjects(ladder_cords, doors, traps, chests, objects_textures, level)

    enemies = setEnemies(enemies_cords, enemies_textures, level)

    possibility_movement_map = [[True for _ in range(height)] for _ in range(width)]

    # Movement definition
    for dw in dungeon_walls:
        possibility_movement_map[dw[0][0]][dw[0][1]] = False

    for ch in chests:
        possibility_movement_map[ch[0]][ch[1]] = False
    # Movement definition

    return dungeon_textures, walls_textures, objects, enemies, possibility_movement_map, player_cords
