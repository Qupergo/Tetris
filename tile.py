from graphics import BACKGROUND_COLOR

class Tile:
    def __init__(self, x, y, is_block, color, is_outline=False):
        self.x, self.y = x, y
        self.is_block = is_block
        self.color = color
        self.is_outline = is_outline

    def set_is_block(self, is_block):
        self.is_block = is_block

    def set_color(self, color):
        self.color = color

    def set_is_outline(self, is_outline):
        self.is_outline = is_outline

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_color(self):
        return self.color

    def get_is_block(self):
        return self.is_block

    def get_is_outline(self):
        return self.is_outline
    
    def copy_state(self, another_tile):
        self.set_is_block(another_tile.get_is_block())
        self.set_color(another_tile.get_color())

    def reset(self):
        self.set_is_block(False)
        self.set_is_outline(False)
        self.set_color(BACKGROUND_COLOR)