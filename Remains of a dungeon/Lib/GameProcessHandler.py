from datetime import datetime
import pickle
from locale import currency
import select
from .Entities import Enemy, Player
from .Items import Armor, Food, Item, Potion, Scroll, Weapon
from .Objects import Chest, Object, Trap, Ladder
from .LevelSetter import setLevel

def sign(num):
    return -1 if num < 0 else 0 if num == 0 else 1

class stepHandler:

    def __init__(self, objects: list[Object], move_map: list[list[bool]], enemies: list[Enemy], player: Player, cameraw: int, camerah: int, parent=None):

        self.objects = objects
        self.move_map = move_map
        self.enemies = enemies
        self.player = player
        self.camera = Camera(0, 0, cameraw, camerah, len(move_map), len(move_map[0]))
        self.camera.goToPlayer(self.player.x, self.player.y)
        self.ladder = [obj for obj in objects if isinstance(obj, Ladder)][0]
        self.parent = parent

    def click(self, x: int, y: int):

        for enemy in self.enemies:
            if enemy.x == x and enemy.y == y:
                self.player_attack(enemy)
                if enemy.hp <= 0:
                    self.player.exp += enemy.dmg
                    self.enemies.remove(enemy)
                    if self.player.exp >= self.player.lvl * 2:
                        self.player.exp -= self.player.lvl * 2
                        self.player.setLevel(self.player.lvl + 1)
                return

        for chest in [obj for obj in self.objects if isinstance(obj, Chest)]:
            if (chest.x == x and chest.y == y and
               self.parent != None and
               len(self.player.inventory) < self.parent.inventory.w * self.parent.inventory.h):
                self.open_chest(chest)
                return

        if self.ladder.x == x and self.ladder.y == y:
            return 1

    def step(self):

        if self.player.hunger > 0:
            self.player.hunger -= 1
        else:
            self.player.hp -= 1

        #Trap check
        for trap in [obj for obj in self.objects if isinstance(obj, Trap) and obj.active]:
            if (self.player.x, self.player.y) == (trap.x, trap.y):
                self.player.hp -= trap.damage - min(trap.damage, self.player.defence)
                trap.active = False
                trap.visible = True
                break
        
        for enemy in self.enemies:
            distation = (self.player.x - enemy.x) ** 2 + (self.player.y - enemy.y) ** 2
            #Enemies attack
            if distation == 1:
                self.player.hp -= enemy.dmg - min(self.player.defence, enemy.dmg)
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

        if self.player.hp == 0 and self.parent != None:
            self.parent.death()

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
        if self.y + self.h < self.maph and self.getCenter()[1] < py:
            self.y += 1

    def Up(self, py: int):
        if self.y > 0 and self.getCenter()[1] > py:
            self.y -= 1

    def Left(self, px: int):
        if self.x > 0 and self.getCenter()[0] > px:
            self.x -= 1

    def Right(self, px: int):
        if self.x + self.w < self.mapw and self.getCenter()[0] < px:
            self.x += 1

class Inventory:

    def __init__(self, items: list[Item], width: int, height: int, img: str, itemsize: int, splitsize: int):

        self.cursor = (0, 0)
        self.w = width
        self.h = height
        self.items = items
        self.img = img
        self.itemsize = itemsize
        self.splitsize = splitsize

    def delItem(self):

        try:
            del self.items[self.items.index(self.cursor[1] * self.w + self.cursor[0])]
        except:
            pass

    def useItem(self) -> Item:

        try:
            item = self.items[self.cursor[1] * self.w + self.cursor[0]]
            del self.items[self.items.index(item)]
            return item
        except: pass

    def get_draw(self):

        return self.w, self.items

    def Left(self):
        
        if self.cursor[0] > 0:
            self.cursor = (self.cursor[0] - 1, self.cursor[1])

    def Right(self):
        
        if self.cursor[0] < self.w - 1:
            self.cursor = (self.cursor[0] + 1, self.cursor[1])

    def Up(self):
        
        if self.cursor[1] > 0:
            self.cursor = (self.cursor[0], self.cursor[1] - 1)

    def Down(self):
        
        if self.cursor[1] < self.h - 1:
            self.cursor = (self.cursor[0], self.cursor[1] + 1)

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
                 height_screen: int,
                 parent=None):

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
        self.global_selection_pos = None
        self.out = []
        self.parent = parent

    def draw_all(self, mouse: tuple[int, int]):

        mouseX = mouse[0]
        mouseY = mouse[1]
        
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
            if isinstance(obj, Trap) and obj.visible == False:
                continue
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

        selection_pos = setSelectionPos(self.tilesize, mouseX, mouseY, self.player.x - self.camera.x, self.player.y - self.camera.y, self.w_map, self.h_map)
        self.selection_pos = selection_pos
        self.global_selection_pos = setSelectionPos(self.tilesize, mouseX + self.camera.x * self.tilesize, mouseY + self.camera.y * self.tilesize, self.player.x, self.player.y, self.w_map, self.h_map)

        self.out.append(self.drawfunc(self.select_tile_texture,
                      (selection_pos[0]) * self.tilesize,
                      (selection_pos[1]) * self.tilesize,
                      self.tilesize))

    def draw_inventory(self, inventory: Inventory, cords: tuple[int, int]):

        draw_out = []

        draw_out.append(self.drawfunc(inventory.img, cords[0], cords[1]))

        for i in range(len(inventory.items)):
            draw_out.append(self.drawfunc(inventory.items[i].img,
                                          cords[0] + i % inventory.w * (inventory.itemsize + inventory.splitsize) + inventory.splitsize,
                                          cords[1] + i // inventory.w * (inventory.itemsize + inventory.splitsize) + inventory.splitsize,
                                          inventory.itemsize))

        draw_out.append(self.drawfunc(self.select_tile_texture,
                                      cords[0] + inventory.cursor[0] * (inventory.itemsize + inventory.splitsize) + inventory.splitsize,
                                      cords[1] + inventory.cursor[1] * (inventory.itemsize + inventory.splitsize) + inventory.splitsize,
                                      inventory.itemsize))

        return draw_out

class GameInitiator:

    def __init__(self, drawfunc, w_map, h_map, textures, w_window, h_window, level, player=None):

        self.new_level_options = [drawfunc, w_map, h_map, textures, w_window, h_window, level]

        dungeon_textures, walls_textures, objects, enemies, possibility_movement_map, player_cords = setLevel(w_map, h_map, level, textures)

        if player == None:
            player = Player(textures[3][0])
            player.hp = 100
            player.dmg = 1
            player.setLevel(1)
            player.exp = 1

        player.x, player.y = player_cords

        tilesize = w_window // w_map * 2

        self.step_handler = stepHandler(objects, possibility_movement_map, enemies, player,
                                        min(w_window // tilesize + 1, w_map),
                                        min(h_window // tilesize + 1, h_map),
                                        self)

        self.savedrawerinit = [drawfunc, dungeon_textures, walls_textures, objects,
                               enemies, player, textures[4][0], self.step_handler.camera,
                               tilesize, w_window, h_window, self]

        self.drawer = Drawer(drawfunc, dungeon_textures, walls_textures, objects,
                             enemies, player, textures[4][0], self.step_handler.camera,
                             tilesize, w_window, h_window, self)

        self.standart_tilesize = tilesize
        self.scale = 100
        self.min_tilesize = min(w_window // w_map, h_window // h_map)
        self.max_tilesize = min(w_window, h_window)
        self.current_tilesize = tilesize

        self.dungeon_floor = level

        self.new_level_options.append(player)

        self.isDeath = False

        self.inventory = Inventory(self.step_handler.player.inventory, 5, 4, textures[5][0], 20, 4)

    def __getstate__(self):
        state = self.__dict__.copy()
        if "drawer" in state:
            state["drawer"] = None  # Игнорируем `Surface`
        return state
    
    def __setstate__(self, state):
        self.__dict__.update(state)
        self.drawer = Drawer(*self.savedrawerinit)  # Восстанавливаем объект (если нужно)

    def draw_all(self, mousepos, drawInv: bool, invCords: tuple[int, int] = None):

        draws = []

        draws.extend(self.drawer.draw_all(mousepos))
        if drawInv: draws.extend(self.drawer.draw_inventory(self.inventory, invCords))

        return draws

    def click(self):
        
        if self.step_handler.click(self.drawer.global_selection_pos[0], self.drawer.global_selection_pos[1]) == 1:
            nlo = self.new_level_options
            self.__init__(nlo[0], nlo[1], nlo[2], nlo[3], nlo[4], nlo[5], nlo[6] + 1, nlo[7])

    def zoom(self):
        
        self.scale += 10
        self.scale //= 10
        self.scale *= 10
        self.change_scale()

    def dezoom(self):
        
        self.scale -= 10
        self.scale //= 10
        self.scale *= 10
        self.change_scale()

    def default_scale(self):
        
        self.scale = 100
        self.change_scale()

    def change_scale(self):

        self.current_tilesize = int(float(self.standart_tilesize) * float(self.scale) / 100.0)

        if self.current_tilesize < self.min_tilesize:
            self.current_tilesize = self.min_tilesize
            self.scale = int(float(self.min_tilesize) / float(self.standart_tilesize) * 100)
        elif self.current_tilesize > self.max_tilesize:
            self.current_tilesize = self.max_tilesize
            self.scale = int(float(self.max_tilesize) / float(self.standart_tilesize) * 100)

        self.drawer.tilesize = self.current_tilesize
        self.step_handler.camera.w = min(self.drawer.width_screen // self.current_tilesize + 1, self.drawer.w_map)
        self.step_handler.camera.h = min(self.drawer.height_screen // self.current_tilesize + 1, self.drawer.h_map)
        self.step_handler.camera.goToPlayer(self.drawer.player.x, self.drawer.player.y)

    def getHud(self):
        pl = self.drawer.player
        return Interface.getHud(pl.hp, pl.hunger, pl.exp, pl.lvl, pl.dmg, pl.defence, self.dungeon_floor)

    def death(self):
        self.isDeath = True

    def invLeft(self):
        self.inventory.Left()
    def invRight(self):
        self.inventory.Right()
    def invUp(self):
        self.inventory.Up()
    def invDown(self):
        self.inventory.Down()

    def useItem(self):

        item = self.inventory.useItem()

        if item == None:
            return

        if isinstance(item, Weapon):
            self.step_handler.player.dmg = item.parameter + self.step_handler.player.lvl
        elif isinstance(item, Armor):
            self.step_handler.player.defence = item.parameter + self.step_handler.player.lvl
        elif isinstance(item, Scroll):
            self.step_handler.player.dmg += item.parameter
        elif isinstance(item, Potion):
            self.step_handler.player.hp += item.parameter
        elif isinstance(item, Food):
            self.step_handler.player.hunger += item.parameter

    def save(self):

        saves = []

        try:
            with open("saves.pkl", "rb") as f:
                saves = pickle.load(f)
        except:
            pass

        if len(saves) == 3:
            del saves[0]

        saves.append(self)

        strlinessaves = []
        try:
            with open("saveslist.txt", 'r', encoding='utf-8') as f:
                strlinessaves = [line.strip() for line in f]
        except:
            pass
        if len(strlinessaves) == 3:
            del strlinessaves[0]
        strlinessaves.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        with open("saveslist.txt", 'w', encoding='utf-8') as f:
            f.writelines([s + '\n' for s in strlinessaves])

        with open("saves.pkl", 'wb') as f:
            pickle.dump(saves, f)


class Interface:

    def getHud(hp: int, satiety: int, exp: int, plvl: int, dmg: int, defence: int, floor: int):

        return f"Health: {hp}\nSaturation: {satiety}\nExpirience: {exp}\nLevel: {plvl}\nDamage: {dmg}\nDefence: {defence}\nDungeon floor: {floor}"

class Button:

    def __init__(self, x: int, y: int, w: int, h: int, texture: str, text: str, func):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.img = texture
        self.text = text
        self.func = func

class Menu:

    def play(self):
        
        return "game"

    def settings(self):
        
        return "settings"

    def saves(self):
        
        return "saves"

    def qquit(self):
        
        return "quit"

    def __init__(self, background: str, buttonsTextures: list[str], buttonsCords: list[tuple[int, int]], buttonsSize: list[tuple[int, int]]):

        self.background = background

        self.buttons = [
            Button(buttonsCords[0][0], buttonsCords[0][1],
                   buttonsSize[0][0], buttonsSize[0][1],
                   buttonsTextures[0], "Play", self.play),
            Button(buttonsCords[1][0], buttonsCords[1][1],
                   buttonsSize[1][0], buttonsSize[1][1],
                   buttonsTextures[1], "Settings", self.settings),
            Button(buttonsCords[2][0], buttonsCords[2][1],
                   buttonsSize[2][0], buttonsSize[2][1],
                   buttonsTextures[2], "Saves", self.saves),
            Button(buttonsCords[3][0], buttonsCords[3][1], 
                   buttonsSize[3][0], buttonsSize[3][1],
                   buttonsTextures[3], "Quit", self.qquit),
        ]

    def click(self, mouse):
        
        x, y = mouse

        for button in self.buttons:
            if button.x <= x <= button.x + button.w - 1 and button.y <= y <= button.y + button.h - 1:
                return button.func()

        return "menu"

    def draw(self, draw_func, draw_text):

        out = []

        out.append(draw_func(self.background, 0, 0))

        for button in self.buttons:
            out.append(draw_func(button.img, button.x, button.y))
            out.append(draw_text(button.x, button.y, button.text, button.w, button.h))

        return out

class Saves:

    def __init__(self, savesfilepath: str, background: str, buttonTexture: str, buttonW: int, buttonH: int, buttonHSplit: int, firstCords: tuple[int, int]):

        saves = []

        try:
            with open(savesfilepath, 'r', encoding='utf-8') as f:
                saves = [line.strip() for line in f]
        except:
            pass

        self.bg = background
        self.path = savesfilepath
        self.b_img = buttonTexture
        self.bw = buttonW
        self.bh = buttonH
        self.bsplit = buttonHSplit
        self.begin = firstCords

        self.buttons = []

        for i in range(len(saves)):
            self.buttons.append(Button(self.begin[0], self.begin[1] + (self.bh + self.bsplit) * i, self.bw, self.bh, self.b_img, saves[i], None))

    def click(self, mouse):

        x, y = mouse

        saves = []

        try:
            with open("saves.pkl", "rb") as f:
                saves = pickle.load(f)
        except:
            pass

        for i in range(len(self.buttons)):
            if (self.buttons[i].x <= x <= self.buttons[i].x + self.buttons[i].w - 1 and
                self.buttons[i].y <= y <= self.buttons[i].y + self.buttons[i].h - 1):
                return saves[i]

        return None

    def draw(self, draw_func, text_func):

        out = []

        out.append(draw_func(self.bg, 0, 0))

        for button in self.buttons:
            out.append(draw_func(button.img, button.x, button.y))
            out.append(text_func(button.x, button.y, button.text, button.w, button.h))

        return out

class Settings:

    def wdec(self):
        if self.gw > 20: self.gw -= 1

    def winc(self):
        if self.gw < 200: self.gw += 1

    def hdec(self):
        if self.gh > 20: self.gh -= 1

    def hinc(self):
        if self.gh < 200: self.gh += 1

    def __init__(self, background: str, bxFirst: int, bxSecond: int, by: int, bw: int, bh: int, bsplit: int, bimg: str):

        self.bg = background
        self.gw = 40
        self.gh = 30
        self.buttons = [
            Button(bxFirst, by, bw, bh, bimg, '<', self.wdec),
            Button(bxSecond, by, bw, bh, bimg, '>', self.winc),
            Button(bxFirst, by + bsplit + bh, bw, bh, bimg, '<', self.hdec),
            Button(bxSecond, by + bsplit + bh, bw, bh, bimg, '>', self.hinc)
        ]

    def click(self, mouse):

        x, y = mouse

        for button in self.buttons:
            if button.x <= x <= button.x + button.w - 1 and button.y <= y <= button.y + button.h - 1:
                button.func()

    def draw(self, draw_func, text_func, x1: int, x2: int, y1: int, y2: int):

        out = []

        out.append(draw_func(self.bg, 0, 0))

        for button in self.buttons:
            out.append(draw_func(button.img, button.x, button.y))
            out.append(text_func(button.x, button.y, button.text, button.w, button.h))

        out.append(text_func(x1, y1, "Dungeon width: "))
        out.append(text_func(x2, y1, str(self.gw)))
        out.append(text_func(x1, y2, "Dungeon height: "))
        out.append(text_func(x2, y2, str(self.gh)))

        return out

