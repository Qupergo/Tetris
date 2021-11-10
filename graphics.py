import pygame

BACKGROUND_COLOR = (30, 30, 30)

class Graphics:
    def __init__(self, width, height, tile_size, tetris):
        self.width, self.height = width, height
        self.tile_size = tile_size
        self.tetris = tetris
        pygame.init()
        self.__create_screen()

    # Set up the drawing window
    def __create_screen(self):
        self.screen = pygame.display.set_mode([self.__width(), self.__height()])

    # Display everything on screen
    def display_scene(self):
        self.__reset_screen()

        size = self.__tile_size()
        rows, cols = int(self.__height() / size), int(self.__width() / size)
        for y in range(rows):
            pygame.draw.line(self.__screen(), (40, 40, 40), (0, y * size), (self.__width(), y * size))
        for x in range(cols):
            pygame.draw.line(self.__screen(), (40, 40, 40), (x * size, 0), (x * size, self.__height()))

        board = self.__tetris().get_board()
        for row in board:
            for tile in row:
                self.__draw_tile(tile.get_x(), tile.get_y(), tile.get_color(), tile.get_is_outline()) 
        pygame.display.flip()

    # Reset screen
    def __reset_screen(self):
        # Fill the background with white
        self.__screen().fill(BACKGROUND_COLOR)

    def __lighten(self, color):
        return (min(255, color[0] * 1.8), min(255, color[1] * 1.8), min(255, color[2] * 1.8))

    def __darken(self, color):
        return (color[0] * 0.8, color[1] * 0.8, color[2] * 0.8)

    # Display a tile
    def __draw_tile(self, x, y, color, outline = False):
        size = self.__tile_size()
        position = (x * size + size * 0.05, y * size + size * 0.05, size * 0.9, size * 0.9)
        pygame.draw.rect(self.__screen(), color, position, 3 * int(outline))
        if color != BACKGROUND_COLOR and not outline:
            pygame.draw.polygon(self.__screen(), self.__lighten(color), ( #Up
                (x * size + size * 0.05, y * size + size * 0.05), 
                (x * size + size * 0.95, y * size + size * 0.05), 
                (x * size + size * 0.75, y * size + size * 0.25), 
                (x * size + size * 0.25, y * size + size * 0.25)))

            pygame.draw.polygon(self.__screen(), self.__darken(color), ( #Right
                (x * size + size * 0.95, y * size + size * 0.05),
                (x * size + size * 0.95, y * size + size * 0.95), 
                (x * size + size * 0.75, y * size + size * 0.75), 
                (x * size + size * 0.75, y * size + size * 0.25)))

    def __width(self):
        return self.width

    def __height(self):
        return self.height

    def __screen(self):
        return self.screen

    def __tile_size(self):
        return self.tile_size

    def __tetris(self):
        return self.tetris