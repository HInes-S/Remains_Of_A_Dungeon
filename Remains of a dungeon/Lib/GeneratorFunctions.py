import random
from typing import Any

'''
Генерация карты подземелья (0 - пустота, 1 - стена, 2 - пол)
* Создаём пустое поле dungeon размером h × w.
* Пытаемся разместить до max_attempts случайных прямоугольных комнат, следя за отступом room_margin.
* Если получилось более одной комнаты – рассчитываем центры, строим минимальное остовное дерево (MST)
  по квадрату дистанций между центрами (алгоритм Краскала с DSU).
* По ребрам MST рисуем “L-образные”, горизонтальные и вертикальные коридоры.
'''

#Зачем нужно: при построении MST мы сортируем все пары комнат по “длине” (квадрат расстояния)
#и берём минимальные рёбра, не образующие цикла.
class UnionFind:
    def __init__(self, size):
        self.parent = list(range(size))
    
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        fx = self.find(x)
        fy = self.find(y)
        if fx != fy:
            self.parent[fy] = fx

def generate_dungeon(w, h, max_room_size=7, min_room_size=3, room_margin=2):
    dungeon = [[0 for _ in range(w)] for _ in range(h)]
    rooms = []
    
    # Генерация комнат
    max_attempts = 100
    for _ in range(max_attempts):
        room_w = random.randint(min_room_size, max_room_size)
        room_h = random.randint(min_room_size, max_room_size)
        x = random.randint(0, w - room_w)
        y = random.randint(0, h - room_h)
        new_room = (x, y, room_w, room_h)
        
        # Проверка коллизий
        collision = False
        new_x1 = x - room_margin
        new_y1 = y - room_margin
        new_x2 = x + room_w + room_margin
        new_y2 = y + room_h + room_margin
        
        for (rx, ry, rw, rh) in rooms:
            exist_x1 = rx - room_margin
            exist_y1 = ry - room_margin
            exist_x2 = rx + rw + room_margin
            exist_y2 = ry + rh + room_margin
            
            if not (new_x2 <= exist_x1 or new_x1 >= exist_x2 or 
                    new_y2 <= exist_y1 or new_y1 >= exist_y2):
                collision = True
                break
        
        if not collision:
            # Рисуем комнату
            for i in range(y, y + room_h):
                for j in range(x, x + room_w):
                    if i == y or i == y + room_h - 1 or j == x or j == x + room_w - 1:
                        dungeon[i][j] = 1  # Стена
                    else:
                        dungeon[i][j] = 2  # Пол
            rooms.append(new_room)
    
    if len(rooms) <= 1:
        add_walls_around_floors(dungeon)
        return dungeon, rooms
    
    # Построение минимального связующего дерева
    centers = [(rx + rw//2, ry + rh//2) for (rx, ry, rw, rh) in rooms]
    edges = []
    n = len(rooms)
    for i in range(n):
        for j in range(i+1, n):
            dx = centers[i][0] - centers[j][0]
            dy = centers[i][1] - centers[j][1]
            distance = dx**2 + dy**2
            edges.append((distance, i, j))
    edges.sort()
    
    uf = UnionFind(n)
    mst = []
    for edge in edges:
        d, i, j = edge
        if uf.find(i) != uf.find(j):
            uf.union(i, j)
            mst.append((i, j))
    
    # Создание путей между комнатами
    for i, j in mst:
        ax, ay = centers[i]
        bx, by = centers[j]
        
        if random.choice([True, False]):
            create_horizontal_path(dungeon, ay, ax, bx)
            create_vertical_path(dungeon, bx, ay, by)
        else:
            create_vertical_path(dungeon, ax, ay, by)
            create_horizontal_path(dungeon, by, ax, bx)
    
    # Добавляем стены вокруг всех полов
    add_walls_around_floors(dungeon)
    
    # Добавляем двери
    doors = add_doors(dungeon, rooms)
    
    return dungeon, rooms, doors

def create_horizontal_path(dungeon, y, x_start, x_end):
    """Создает горизонтальный коридор (только пол)"""
    step = 1 if x_end >= x_start else -1
    for x in range(x_start, x_end + step, step):
        if 0 <= y < len(dungeon) and 0 <= x < len(dungeon[0]):
            # Заменяем только пустоты и стены на пол
            if dungeon[y][x] in [0, 1]:
                dungeon[y][x] = 2

def create_vertical_path(dungeon, x, y_start, y_end):
    """Создает вертикальный коридор (только пол)"""
    step = 1 if y_end >= y_start else -1
    for y in range(y_start, y_end + step, step):
        if 0 <= y < len(dungeon) and 0 <= x < len(dungeon[0]):
            # Заменяем только пустоты и стены на пол
            if dungeon[y][x] in [0, 1]:
                dungeon[y][x] = 2

def add_walls_around_floors(dungeon):
    """Добавляет стены вокруг всех проходимых клеток (пол, вода, двери)"""
    h = len(dungeon)
    w = len(dungeon[0])
    # Создаем временную копию для безопасного чтения
    temp = [row[:] for row in dungeon]
    
    for y in range(h):
        for x in range(w):
            # Если клетка - проходимая
            if temp[y][x] in [2, 3, 4]:
                # Проверяем всех 8 соседей
                for dy in range(-1, 2):
                    for dx in range(-1, 2):
                        if dy == 0 and dx == 0:
                            continue
                        ny, nx = y + dy, x + dx
                        # Если сосед в пределах карты и пустой
                        if 0 <= ny < h and 0 <= nx < w and temp[ny][nx] == 0:
                            dungeon[ny][nx] = 1

def add_doors(dungeon, rooms):

    doors = []

    """Добавляет двери на границах комнат, где есть коридор"""
    for (x, y, rw, rh) in rooms:
        
        for i in range(x, x + rw, 1):
            if dungeon[y][i] == 2:
                dungeon[y][i] = 4
                doors.append((y, i))

        for i in range(x, x + rw, 1):
            if dungeon[y + rh - 1][i] == 2:
                dungeon[y + rh - 1][i] = 4
                doors.append((y + rh - 1, i))

        for i in range(y, y + rh, 1):
            if dungeon[i][x] == 2:
                dungeon[i][x] = 4
                doors.append((i, x))

        for i in range(y, y + rh, 1):
            if dungeon[i][x + rw - 1] == 2:
                dungeon[i][x + rw - 1] = 4
                doors.append((i, x + rw - 1))

    delete_extra_doors(dungeon, doors)

    return doors

def delete_extra_doors(dungeon, doors):

    new_doors = []

    for door in doors:
        if (((dungeon[door[0] + 1][door[1]] == 1) and (dungeon[door[0] - 1][door[1]] == 1)) or
           ((dungeon[door[0]][door[1] + 1] == 1) and (dungeon[door[0]][door[1] - 1] == 1))):
            new_doors.append(door)

    return new_doors

def place_water(rooms, dungeon): # Ф-ция для расставления воды в комнатах
    h = len(dungeon)
    w = len(dungeon[0]) if h > 0 else 0
    
    for room in rooms:
        x, y, rw, rh = room
        
        # Пропускаем комнаты, которые не помещаются в подземелье
        if x < 0 or y < 0 or x + rw > w or y + rh > h:
            continue
        
        # 30% вероятность добавить лужу в комнату
        if random.random() > 0.3:
            continue
            
        # Внутренняя область комнаты (без стен)
        inner_x = x + 1
        inner_y = y + 1
        inner_w = rw - 2
        inner_h = rh - 2
        
        # Минимальные размеры для лужи
        if inner_w < 2 or inner_h < 2:
            continue
        
        # Выбираем стену для привязки (0-север, 1-юг, 2-запад, 3-восток)
        wall_side = random.randint(0, 3)
        
        # Генерируем размеры лужи с ограничениями
        max_length = min(4, inner_w, inner_h)  # Ограничение по обоим измерениям
        length = random.randint(2, max_length) if max_length >= 2 else 2
        
        max_width = min(2, inner_w, inner_h)
        width = random.randint(1, max_width) if max_width >= 1 else 1
        
        # Для маленьких комнат корректируем размеры
        if length < 2 or width < 1:
            continue
        
        # Определяем область для размещения лужи с безопасными проверками
        valid_placement = True
        if wall_side == 0:    # Северная стена
            x_range = inner_w - length
            if x_range < 0:
                continue
            start_x = inner_x + random.randint(0, x_range)
            start_y = inner_y
        elif wall_side == 1:  # Южная стена
            x_range = inner_w - length
            if x_range < 0:
                continue
            start_x = inner_x + random.randint(0, x_range)
            start_y = inner_y + inner_h - width
        elif wall_side == 2:  # Западная стена
            y_range = inner_h - length
            if y_range < 0:
                continue
            start_x = inner_x
            start_y = inner_y + random.randint(0, y_range)
        else:                 # Восточная стена
            y_range = inner_h - length
            if y_range < 0:
                continue
            start_x = inner_x + inner_w - width
            start_y = inner_y + random.randint(0, y_range)
        
        # Рассчитываем конечные координаты
        end_x = start_x + (width if wall_side in (2, 3) else length)
        end_y = start_y + (length if wall_side in (2, 3) else width)
        
        # Проверяем границы
        if end_x > inner_x + inner_w or end_y > inner_y + inner_h:
            continue
        
        # Проверяем, что все клетки - пол
        valid = True
        for i in range(start_y, end_y):
            for j in range(start_x, end_x):
                if dungeon[i][j] != 2:  # Не пол
                    valid = False
                    break
            if not valid:
                break
                
        # Добавляем лужу
        if valid:
            for i in range(start_y, end_y):
                for j in range(start_x, end_x):
                    dungeon[i][j] = 3  # Вода
                    
    return dungeon

def set_walls_direction(dgn): # Ф-ция для определения направления стен
    
    h = len(dgn)
    w = len(dgn[0])

    dgnW = [[[y, x], [False for _ in range(8)]] for y in range(h) for x in range(w) if dgn[y][x] == 1]

    for wall in dgnW:

        try:
            if (dgn[wall[0][0] + 1][wall[0][1]] in [2, 3, 4]):
                wall[1][0] = True
        except:
            pass

        try:
            if (dgn[wall[0][0] - 1][wall[0][1]] in [2, 3, 4]):
                wall[1][1] = True
        except:
            pass

        try:
            if (dgn[wall[0][0]][wall[0][1] - 1] in [2, 3, 4]):
                wall[1][2] = True
        except:
            pass

        try:
            if (dgn[wall[0][0]][wall[0][1] + 1] in [2, 3, 4]):
                wall[1][3] = True
        except:
            pass

        try:
            if (dgn[wall[0][0] - 1][wall[0][1] - 1] in [2, 3, 4]):
                wall[1][4] = True
        except:
            pass

        try:
            if (dgn[wall[0][0] + 1][wall[0][1] - 1] in [2, 3, 4]):
                wall[1][5] = True
        except:
            pass

        try:
            if (dgn[wall[0][0] - 1][wall[0][1] + 1] in [2, 3, 4]):
                wall[1][6] = True
        except:
            pass

        try:
            if (dgn[wall[0][0] + 1][wall[0][1] + 1] in [2, 3, 4]):
                wall[1][7] = True
        except:
            pass

    return dgnW
                

def generate_traps(dungeon, rooms, percentage: float):
    
    #[x: int, y: int, isVisible: bool, isActive: bool]
    traps = []

    for room in rooms:
        for x in range(room[0] + 1, room[0] + room[2] - 2, 1):
            for y in range(room[1] + 1, room[1] + room[3] - 2, 1):
                if dungeon[y][x] == 2:
                    if float(random.randint(1, 1000)) / 10 <= percentage:
                        traps.append([x, y, False, True])

    return traps

def generate_chests(dungeon, rooms, percentage: float):
    
    #[x: int, y: int]
    chests = []

    for room in rooms:
        for x in range(room[0] + 1, room[0] + room[2] - 2, 1):
            for y in range(room[1] + 1, room[1] + room[3] - 2, 1):
                if dungeon[y][x] == 2:
                    if float(random.randint(1, 1000)) / 10 <= percentage:
                        chests.append([x, y])

    return chests


def generate_final_dungeon_map(w, h, max_room_size=7, min_room_size=3, room_margin=2):
    dungeon, rooms, doors = generate_dungeon(w, h, max_room_size, min_room_size, room_margin)
    dungeon_walls = set_walls_direction(dungeon)
    dungeon = place_water(rooms, dungeon)

    doors = delete_extra_doors(dungeon, doors)

    traps = generate_traps(dungeon, rooms, 2)
    chests = generate_chests(dungeon, rooms, 2)

    deli = []
    for i in range(len(traps)):
        for chest in chests:
            if (traps[i][0], traps[i][1]) == (chest[0], chest[1]):
                deli.append(i)
    for i in range(len(deli) - 1, -1, -1):
        del traps[i]

    #Change dungeon_walls from y,x to x,y
    #[[[y, x], [bool*8]]*n] - start data | [[[x, y], [bool*8]]*n] - end data
    dungeon_walls = [[[dw[0][1], dw[0][0]], dw[1]] for dw in dungeon_walls]

    #Change dungeon from [[tile * x] * y] to [[tile * y] * x]
    dungeon = [[row[i] for row in dungeon] for i in range(len(dungeon[0]))]

    #Delete door from dungeon
    dungeon = [[2 if dungeon[x][y] == 4 else dungeon[x][y] for y in range(len(dungeon[0]))] for x in range(len(dungeon))]

    #Change doors orientation
    doors = [[door[1], door[0]] for door in doors]

    return dungeon, rooms, dungeon_walls, doors, traps, chests

def generate_enemies(rooms, chests, doors, traps, max_count_in_room: int):

    obj_cords = [cords for cords in zip([[chest[0], chest[1]] for chest in chests],
                                        [[door[0], door[1]] for door in doors],
                                        [[trap[0], trap[1]] for trap in traps])]

    enemies_cords = []

    for room in rooms:
        can_cords = [[x, y] for x in range(room[0] + 1, room[0] + room[2] - 1)
                            for y in range(room[1] + 1, room[1] + room[3] - 1)]
        can_cords = [cord for cord in can_cords if not (cord in obj_cords)]
        enemy_count = random.randint(0, min(max_count_in_room, len(can_cords)))
        for _ in range(enemy_count):
            index = random.randint(0, len(can_cords) - 1)
            enemies_cords.append(can_cords[index])
            del can_cords[index]

    return enemies_cords