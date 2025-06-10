from .TextureHandler import isItTexture
from .Items import Item

class Entity:

    def __init__(self, texture: str):

        if not isItTexture(texture):
            raise Exception("That's not a texture")

        self.__img = texture
        self.__x = -1
        self.__y = -1
        self.__hp = 0
        self.__dmg = 0

    @property
    def img(self):
        return self.__img
    @img.setter
    def img(self, texture):
        if not isItTexture(texture):
            raise Exception("That's not a texture")
        self.__img = texture

    @property
    def x(self):
        return self.__x
    @x.setter
    def x(self, x: int):
        if not isinstance(x, int) or x < 0:
            raise Exception("Wrong x")
        self.__x = x

    @property
    def y(self):
        return self.__y
    @y.setter
    def y(self, y: int):
        if not isinstance(y, int) or y < 0:
            raise Exception("Wrong y")
        self.__y = y

    @property
    def hp(self):
        return self.__hp
    @hp.setter
    def hp(self, hp: int):
        if not isinstance(hp, int):
            raise Exception("Wrong hp")
        self.__hp = hp if hp > 0 else 0

    @property
    def dmg(self):
        return self.__dmg
    @dmg.setter
    def dmg(self, dmg: int):
        if not isinstance(dmg, int) or dmg < 0:
            raise Exception("Wrong dmg")
        self.__dmg = dmg


class Enemy(Entity):

    def __init__(self, texture: str):

        super().__init__(texture)
        self.__viewRange = 1

    @property
    def view_range(self):
        return self.__viewRange
    @view_range.setter
    def view_range(self, vrange: int):
        if not isinstance(vrange, int) or vrange < 0:
            raise Exception("Wrong view_range")
        self.__viewRange = vrange

class Player(Entity):

    def __init__(self, texture: str):

        super().__init__(texture)
        self.__exp = 0
        self.__lvl = 0
        self.__inv = list()

    def setLevel(self, lvl: int):
        if not isinstance(lvl, int) or lvl < 0:
            raise Exception("Wrong level")
        self.__lvl = lvl
        self.__hp = 100 + 10 * lvl
        self.__dmg = 1 + lvl
        self.__hunger = 100

    def add_to_inventory(self, item: Item):
        if not isinstance(item, Item):
            raise Exception("Wrong item")
        self.__inv.append(item)

    def del_from_inventory(self, index: int):
        try:
            del self.__inv[index]
        except:
            raise Exception("Wrong index")

    @property
    def inventory(self):
        return self.__inv

    @property
    def lvl(self):
        return self.__lvl

    @property
    def exp(self):
        return self.__exp
    @exp.setter
    def exp(self, exp: int):
        if not isinstance(exp, int) or exp < 0:
            raise Exception("Wrong exp")
        self.__exp = exp

    @property
    def hunger(self):
        return self.__hunger
    @hunger.setter
    def hunger(self, hunger):
        if not isinstance(hunger, int) or hunger < 0:
            raise Exception("Wrong hunger")
