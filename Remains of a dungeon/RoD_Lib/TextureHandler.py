from .Objects import *

def isItTexture(path: str) -> bool:

    '''
    check, that the path points to a .png image 
    '''

    if not isinstance(path, str):
        raise Exception("Path must be str")

    try:

        # Определяем расширение
        extension = path[-4:]
        if extension != ".png":
            return (False, "Not PNG")

        with open(path, "rb") as file:
            header = file.read(8)  # Читаем первые 8 байтов
            if not header[:8] == b'\x89PNG\r\n\x1a\n':  # Проверка на PNG
                return (False, "Not PNG")

        return True

    except Exception as ex:
        return False

def setDungeonTextures(dungeon: list[list[int]], dungeon_walls: list[list[list[int], list[bool]]], textures: list):

    '''
    textures is a list of the form:
    [
        void : path
        walls : list[8] of path where floor is from the wall: bottom, top, left, right, top left, bottom left, top right, bottom right
        floor : path
        water : path
    ]
    '''

    begin_textures = [textures[0], textures[0], textures[2], textures[3]]
    dungeon_textures = []
    walls_textures = [] # x, y, [textures]

    w = len(dungeon)
    h = len(dungeon[0])

    for x in range(w):
        dungeon_textures.append([])
        for y in range(h):
            dungeon_textures[x].append(begin_textures[dungeon[x][y]])

    for wall in dungeon_walls:
        walls_textures.append([wall[0][0], wall[0][1], [textures[1][i] for i in range(8) if wall[1][i]]])

    return dungeon_textures, walls_textures
