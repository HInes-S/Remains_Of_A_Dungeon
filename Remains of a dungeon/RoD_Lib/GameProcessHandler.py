import select
from .Entities import Enemy, Player
from .Items import Food, Item, Potion, Scroll
from .Objects import Chest, Object, Trap

def sign(num):
    return -1 if num < 0 else 0 if num == 0 else 1

class stepHandler:

    def __init__(self, objects: list[Object], move_map: list[list[bool]], enemies: list[Enemy], player: Player, cameraw: int, camerah: int):

        self.objects = objects
        self.move_map = move_map
        self.enemies = enemies
        self.player = player
        self.camera = Camera(0, 0, cameraw, camerah, len(move_map), len(move_map[0]))
        self.camera.goToPlayer(self.player.x, self.player.y)

    def click(self, x: int, y: int):

        for enemy in self.enemies:
            if enemy.x == x and enemy.y == y:
                enemy.hp -= self.player.dmg
                self.player_attack(enemy)
                if enemy.hp <= 0:
                    self.enemies.remove(enemy)
                return

        for chest in [obj for obj in self.objects if isinstance(obj, Chest)]:
            if chest.x == x and chest.y == y:
                self.open_chest(chest)
                return

    def step(self):
        #Trap check
        for trap in [obj for obj in self.objects if isinstance(obj, Trap) and obj.active]:
            if (self.player.x, self.player.y) == (trap.x, trap.y):
                self.player.hp -= trap.damage
                trap.active = False
                trap.visible = True
                break
        
        for enemy in self.enemies:
            distation = (self.player.x - enemy.x) ** 2 + (self.player.y - enemy.y) ** 2
            #Enemies attack
            if distation == 1:
                self.player.hp -= enemy.dmg
                continue
            #Enemies movement
            if enemy.view_range ** 2 >= distation:
                next_cords = [enemy.x + sign(self.player.x - enemy.x), enemy.y + sign(self.player.y - enemy.y)]
                try:
                    if (self.move_map[next_cords[0]][next_cords[1]] and
                        not (next_cords in [[e.x, e.y] for e in self.enemies if e != enemy]) and
                        [self.player.x, self.player.y] != next_cords):
                        enemy.x, enemy.y = next_cords
                except:
                    continue

    def player_move(self, direction: list[int]):
    
        '''
        direction: [x, y]
        '''

        next_cords = [self.player.x + direction[0], self.player.y + direction[1]]

        try:
            if self.move_map[next_cords[0]][next_cords[1]] and not (next_cords in [[e.x, e.y] for e in self.enemies]):
                self.player.x, self.player.y = next_cords

                if direction[0] < 0:
                    self.camera.Left(self.player.x)
                elif direction[0] > 0:
                    self.camera.Right(self.player.x)

                if direction[1] < 0:
                    self.camera.Up(self.player.y)
                elif direction[1] > 0:
                    self.camera.Down(self.player.y)

                self.step()
            return
        except:
            return

    def player_attack(self, enemy: Enemy):
    
        enemy.hp -= self.player.dmg
        self.step()

    def open_chest(self, chest: Chest):
        
        self.player.add_to_inventory(chest.item)
        self.move_map[chest.x][chest.y] = True
        self.objects.remove(chest)
        self.step()

    def use_item(self, item: Item):
        
        if isinstance(item, Food):
            self.player.hunger -= item.parameter

        elif isinstance(item, Potion):
            self.player.hp += item.parameter
            self.player.hp %= 101

        elif isinstance(item, Scroll):
            self.player.dmg += 1

    def q_item(self, item: Item):
        
        self.player.del_from_inventory(self.player.inventory.index(item))

def setSelectionPos(tilesize: int, mousex: int, mousey: int, playerx: int, playery: int, width: int, height: int):

    precords = [sign(mousex // tilesize - playerx) + playerx, sign(mousey // tilesize - playery) + playery]

    if precords[0] < 0:
        precords[0] = playerx + 1
    elif precords[0] >= width:
        precords[0] = playerx - 1

    if precords[1] < 0:
        precords[1] = playery + 1
    elif precords[1] >= height:
        precords[1] = playery - 1

    return precords

class Camera:

    def __init__(self, x: int, y: int, w: int, h: int, mapw: int, maph: int):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.mapw = mapw
        self.maph = maph

    def goToPlayer(self, px, py):
        self.x = px - self.w // 2
        self.y = py - self.h // 2

        if self.x < 0:
            self.x = 0
        elif self.x + self.w > self.mapw:
            self.x = self.mapw - self.w

        if self.y < 0:
            self.y = 0
        elif self.y + self.h > self.maph:
            self.y = self.maph - self.h


    def getCenter(self):
        return (self.x + self.w // 2, self.y + self.h // 2)

    def Down(self, py: int):
        if self.y + self.h < self.maph and self.getCenter[1] < py:
            self.y += 1

    def Up(self, py: int):
        if self.y - 1 > 0 and self.getCenter[1] > py:
            self.y -= 1

    def Left(self, px: int):
        if self.x - 1 > 0 and self.getCenter[0] > px:
            self.x -= 1

    def Rigth(self, px: int):
        if self.x + self.w < self.maph and self.getCenter[0] < px:
            self.x += 1

class Drawer:

    def __init__(self, 
                 drawfunc, 
                 dungeon_textures: list[list[str]], 
                 walls_textures: list, 
                 objects: list[Object], 
                 enemies: list[Enemy], 
                 player: Player, 
                 select_tile_texture: str, 
                 camera: Camera, 
                 tilesize: int,
                 width_screen: int,
                 height_screen: int):

        '''
        drawfunc(texturepath: str, x: int, y: int, tilesize: int)
        '''

        self.drawfunc = drawfunc
        self.dungeon_textures = dungeon_textures
        self.walls_textures = walls_textures
        self.objects = objects
        self.enemies = enemies
        self.player = player
        self.select_tile_texture = select_tile_texture
        self.camera = camera
        self.tilesize = tilesize
        self.width_screen = width_screen
        self.height_screen = height_screen
        self.w_map = len(dungeon_textures)
        self.h_map = len(dungeon_textures[0])
        self.selection_pos = None
        self.out = []

    def draw_all(self, mouseX: int, mouseY: int):
        
        self.out = []

        self.draw_dungeon()
        self.draw_walls()
        self.draw_objects()
        self.draw_enemies()
        self.draw_player()
        self.draw_select(mouseX, mouseY)

        return self.out

    def draw_dungeon(self):
        
        cx = self.camera.x
        cy = self.camera.y

        for x in range(self.camera.w):
            for y in range(self.camera.h):
                self.out.append(self.drawfunc(self.dungeon_textures[x + cx][y + cy], x * self.tilesize, y * self.tilesize, self.tilesize))

    def draw_walls(self):
        
        needful_walls = [wall for wall in self.walls_textures
                         if wall[0] in range(self.camera.x, self.camera.x + self.camera.w) and
                            wall[1] in range(self.camera.y, self.camera.y + self.camera.h)]

        for wall in needful_walls:
            for part in wall[2]:
                self.out.append(self.drawfunc(part,
                              (wall[0] - self.camera.x) * self.tilesize,
                              (wall[1] - self.camera.y) * self.tilesize,
                              self.tilesize))

    def draw_objects(self):
        
        needful_objects = [obj for obj in self.objects
                           if obj.x in range(self.camera.x, self.camera.x + self.camera.w) and
                              obj.y in range(self.camera.y, self.camera.y + self.camera.h)]

        for obj in needful_objects:
            self.out.append(self.drawfunc(obj.img,
                          (obj.x - self.camera.x) * self.tilesize,
                          (obj.y - self.camera.y) * self.tilesize,
                          self.tilesize))

    def draw_enemies(self):
        
        needful_enemies = [enemy for enemy in self.enemies
                           if enemy.x in range(self.camera.x, self.camera.x + self.camera.w) and
                              enemy.y in range(self.camera.y, self.camera.y + self.camera.h)]

        for enemy in needful_enemies:
            self.out.append(self.drawfunc(enemy.img,
                          (enemy.x - self.camera.x) * self.tilesize,
                          (enemy.y - self.camera.y) * self.tilesize,
                          self.tilesize))

    def draw_player(self):
        
        self.out.append(self.drawfunc(self.player.img,
                      (self.player.x - self.camera.x) * self.tilesize,
                      (self.player.y - self.camera.y) * self.tilesize,
                      self.tilesize))

    def draw_select(self, mouseX: int, mouseY: int):
        
        selection_pos = setSelectionPos(self.tilesize, mouseX, mouseY, self.player.x, self.player.y, self.camera.w, self.camera.h)
        self.selection_pos = selection_pos

        self.out.append(self.drawfunc(self.select_tile_texture,
                      (selection_pos[0] - self.camera.x) * self.tilesize,
                      (selection_pos[1] - self.camera.x) * self.tilesize,
                      self.tilesize))
