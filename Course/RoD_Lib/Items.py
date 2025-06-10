class Item:

    def __init__(self, texture: str, parameter: int):

        from TextureHandler import isItTexture

        if not isItTexture(texture):
            raise Exception("That's not a texture")
        
        if not isinstance(parameter, int) or parameter < 0:
            raise Exception("Wrong parameter")

        self.__img = texture
        self.__parameter = parameter

    @property
    def img(self):
        return self.__img
    @img.setter
    def img(self, texture: str):
        if not isItTexture(texture):
            raise Exception("That's not a texture")
        self.__img = texture

    @property
    def parameter(self):
        return self.__parameter
    @parameter.setter
    def parameter(self, parameter):
        if not isinstance(parameter, int) or parameter < 0:
            raise Exception("Wrong parameter")
        self.__parameter = parameter

class Weapon(Item):

    def __init__(self, texture: str, damage: int):
        super().__init__(texture, damage)

class Armor(Item):

    def __init__(self, texture: str, defence: int):
        super().__init__(texture, defence)

class Potion(Item):

    def __init__(self, texture: str, heal: int):
        super().__init__(texture, heal)

class Scroll(Item):

    def __init__(self, texture: str, effect: int):
        super().__init__(texture, effect)

class Food(Item):

    def __init__(self, texture: str, saturation: int):
        super().__init__(texture, saturation)