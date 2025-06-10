from Items import Item

class Object:

    def __init__(self, texture: str, x: int, y: int, solid: bool):

        from TextureHandler import isItTexture

        if not isItTexture(texture):
            raise Exception("That's not a texture")

        if not isinstance(x, int) or x < 0:
            raise Exception("Wrong x")
        
        if not isinstance(y, int) or y < 0:
            raise Exception("Wrong y")

        if not isinstance(solid, bool):
            raise Exception("Wrong solid")

        self.__img = texture
        self.__x = x
        self.__y = y
        self.__solid = solid

    @property
    def img(self):
        return self.__img
    @img.setter
    def img(self, texture: str):
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

    @property
    def solid(self):
        return self.__solid
    @solid.setter
    def solid(self, solid: bool):
        if not isinstance(solid, bool):
            raise Exception("Wrong solid")
        self.__solid = solid

class Door(Object):
    
    def __init__(self, texture: str, x: int, y: int):
        super().__init__(texture, x, y, False)

class Ladder(Object):
    
    def __init__(self, texture: str, x: int, y: int):
        super().__init__(texture, x, y, True)

class Trap(Object):
    
    def __init__(self, texture: str, x: int, y: int, isVisible: bool, isActive: bool, damage: int):
        super().__init__(texture, x, y, False)

        if not isinstance(isVisible, bool):
            raise Exception("Wrong isVisible option")
        if not isinstance(isActive, bool):
            raise Exception("Wrong isActive option")
        if not isinstance(damage, int) or damage < 0:
            raise Exception("Wrong damage")

        self.__isvisible = isVisible
        self.__isactive = isActive
        self.__dmg = damage

    @property
    def visible(self):
        return self.__isvisible
    @visible.setter
    def visible(self, isVisible: bool):
        if not isinstance(isVisible, bool):
            raise Exception("Wrong isVisible option")
        self.__isvisible = isVisible

    @property
    def active(self):
        return self.__isactive
    @active.setter
    def active(self, isActive: bool):
        if not isinstance(isActive, bool):
            raise Exception("Wrong isActive option")
        self.__isactive = isActive

    @property
    def damage(self):
        return self.__dmg
    @damage.setter
    def damage(self, damage: int):
        if not isinstance(damage, int) or damage < 0:
            raise Exception("Wrong damage")
        self.__dmg = damage

class Chest(Object):
    
    def __init__(self, texture: str, x: int, y: int, item: Item):
        super().__init__(texture, x, y, True)

        if not isinstance(item, Item):
            raise Exception("Wrong Item")

        self.__item = item

    @property
    def item(self):
        return self.__item
    @item.setter
    def item(self, item: Item):
        if not isinstance(item, Item):
            raise Exception("Wrong Item")
        self.__item = item

class Weapon(Object):
    
    def __init__(self, texture: str, x: int, y: int, damage: int):
        super().__init__(texture, x, y, True)

        if not isinstance(damage, int) or damage < 0:
            raise Exception("Wrong damage")

        self.__dmg = damage

    @property
    def damage(self):
        return self.__dmg
    @damage.setter
    def damage(self, damage: int):
        if not isinstance(damage, int) or damage < 0:
            raise Exception("Wrong damage")
        self.__dmg = damage

class Armor(Object):
    
    def __init__(self, texture: str, x: int, y: int, defence: int):
        super().__init__(texture, x, y, True)

        if not isinstance(defence, int) or defence < 0:
            raise Exception("Wrong defence")

        self.__defence = defence

    @property
    def defence(self):
        return self.__defence
    @defence.setter
    def defence(self, defence: int):
        if not isinstance(defence, int) or defence < 0:
            raise Exception("Wrong defence")
        self.__defence = defence

class Potion(Object):
    
    def __init__(self, texture: str, x: int, y: int, heal: int):
        super().__init__(texture, x, y, True)

        if not isinstance(heal, int) or heal < 0:
            raise Exception("Wrong heal")

        self.__heal = heal

    @property
    def heal(self):
        return self.__heal
    @heal.setter
    def heal(self, heal: int):
        if not isinstance(heal, int) or heal < 0:
            raise Exception("Wrong heal")
        self.__heal = heal

class Scroll(Object):
    
    def __init__(self, texture: str, x: int, y: int, effect: int):
        super().__init__(texture, x, y, True)

        if not isinstance(effect, int) or effect < 0:
            raise Exception("Wrong effect")

        self.__effect = effect

    @property
    def effect(self):
        return self.__effect
    @effect.setter
    def effect(self, effect: int):
        if not isinstance(effect, int) or effect < 0:
            raise Exception("Wrong effect")
        self.__effect = effect

class Food(Object):
    
    def __init__(self, texture: str, x: int, y: int, saturation: int):
        super().__init__(texture, x, y, True)

        if not isinstance(saturation, int) or saturation < 0:
            raise Exception("Wrong saturation")

        self.__saturation = saturation

    @property
    def saturation(self):
        return self.__saturation
    @saturation.setter
    def saturation(self, saturation: int):
        if not isinstance(saturation, int) or saturation < 0:
            raise Exception("Wrong saturation")
        self.__saturation = saturation




