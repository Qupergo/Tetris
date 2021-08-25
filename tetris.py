from file_helper import *
import pygame, random
import numpy as np

BACKGROUND_COLOR = (0, 0, 0)

class Tile:
    def __init__(self, x, y, is_block, color):
        self.x, self.y = x, y
        self.is_block = is_block
        self.color = color

    def set_is_block(self, is_block):
        self.is_block = is_block

    def set_color(self, color):
        self.color = color

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_color(self):
        return self.color

    def get_is_block(self):
        return self.is_block

class Tetris:
    def __init__(self, block_types, block_colors, rows, cols):
        self.board = [[Tile(x, y, False, BACKGROUND_COLOR) for y in range(rows)] for x in range(cols)]
        self.rows, self.cols = rows, cols
        self.block_types = block_types
        self.block_colors = block_colors
        self.current_block = None
        self.__spawn_block()

    #Handles what happens at this current game state
    def update(self):
        current_block = self.__current_block()
        if current_block == None:
            self.__spawn_block()
        else:
            tile_positions = current_block.get_tile_positions()
            if not self.__can_move_down(tile_positions):
                self.__stop_block()
            else:
                self.__move_down(current_block.get_tile_matrix(), current_block.get_color())

    def __can_rotate(self):
        rotated_tile_matrix = self.__current_block().get_rotated_matrix()
        for y, tile_row in enumerate(rotated_tile_matrix):
            for x, block_on_tile in enumerate(tile_row):
                if block_on_tile:
                    if y >= self.get_rows() or self.__tile_is_block(x, y):
                        return False
        return True
    
    def __rotate(self):
        self.__current_block().set_tile_matrix(self.__current_block().get_rotated_matrix())


    def __can_move_down(self, tile_positions):
        for tile_position in tile_positions:
            x, y = tile_position["x"], tile_position["y"]
            if y + 1 >= self.get_rows() or self.__tile_is_block(x, y + 1):
                return False
        return True

    def __move_down(self, tile_matrix, current_block_color):

        old_position = self.__current_block().get_position()
        for y, tile_row in enumerate(tile_matrix):
            for x, block_on_tile in enumerate(tile_row):
                if block_on_tile:
                    self.__get_tile(x + old_position["x"], y + old_position["y"]).set_color(BACKGROUND_COLOR)

        self.__current_block().set_position({"x":old_position["x"], "y":old_position["y"] + 1})

        for tile_position in self.current_block.get_tile_positions():
            x, y = tile_position["x"], tile_position["y"]
            self.__get_tile(x, y).set_color(current_block_color)

    def __tile_is_block(self, x, y):
        return self.__get_tile(x, y).get_is_block()

    def __get_tile(self, x, y):
        return self.get_board()[x][y]

    def get_board(self):
        return self.board

    def __spawn_block(self):
        x, y = cols // 2, 0
        position = {"x": x, "y": y}

        tile_positions, color = self.__get_random_block()
        block = Block(position, tile_positions, color)
        for tile_position in block.get_tile_positions():
            x, y = tile_position["x"], tile_position["y"]
            tile = self.__get_tile(x, y)
            tile.set_is_block(False)
            tile.set_color(block.color)
        self.__set_current_block(block)

    def __stop_block(self):
        for tile_position in self.__current_block().get_tile_positions():
            x, y = tile_position["x"], tile_position["y"]
            self.__get_tile(x, y).set_is_block(True)
        self.__reset_current_block()

    def __get_random_block(self):
        random_block_num = random.randint(0, len(self.__block_types()) - 1)
        return self.__block_types()[random_block_num], self.__block_colors()[random_block_num]

    def __block_types(self):
        return self.block_types
    
    def __block_colors(self):
        return self.block_colors
    
    def __current_block(self):
        return self.current_block

    def __reset_current_block(self):
        self.current_block = None

    def __set_current_block(self, block):
        self.current_block = block

    def get_rows(self):
        return rows

    def get_cols(self):
        return cols

class Block:
    def __init__(self, position, block_type, color):
        self.color = color
        self.tile_matrix = []
        self.position = position
        self.__parse_block_type(block_type)
    
    def get_tile_positions(self):
        
        actual_tile_positions_on_board = []
        for y, row in enumerate(self.tile_matrix):
            for x, item in enumerate(row):
                if item == 1:
                    actual_tile_positions_on_board.append({"x": x + self.position["x"], "y":y + self.position["y"]})

        return actual_tile_positions_on_board
    
    def get_tile_matrix(self):
        return self.tile_matrix
    
    def set_tile_matrix(self, tile_matrix):
        self.tile_matrix = tile_matrix

    def get_color(self):
        return self.color
    
    def get_position(self):
        return self.position
    
    def set_position(self, new_position):
        self.position = new_position

    def __parse_block_type(self, block_type):
        row = []
        for char in block_type:
            if char == ".":
                row.append(True)
            elif char == "/":
                self.__add_tile_row(row)
                row = []
            elif char == "0":
               row.append(False)


    def __add_tile_row(self, tile_row):
        self.tile_matrix.append(tile_row)
    
    def get_rotated_matrix(self, clockwise=False):
        if not clockwise:
            return list(zip(*self.get_tile_matrix[::-1]))

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
        board = self.__tetris().get_board()
        for row in board:
            for tile in row:
                self.__draw_tile(tile.get_x(), tile.get_y(), tile.get_color())
        pygame.display.flip()

    # Reset screen
    def __reset_screen(self):
        # Fill the background with white
        self.__screen().fill(BACKGROUND_COLOR)

    # Display a tile
    def __draw_tile(self, x, y, color):
        size = self.__tile_size()
        position = (x * size, y * size, size, size)
        pygame.draw.rect(self.__screen(), color, position)

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

class Game:
    def __init__(self, fps, width, height, slowness, tetris, size):
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.running = True
        self.frame_count = 0
        self.slowness = slowness
        self.tetris = tetris
        self.graphics = Graphics(width, height, size, tetris)

    def run(self):
        while self.__running():
            self.__add_to_frame_count()
            self.__clock().tick(self.__fps())
            if self.__frame_count() % self.__slowness() == 0:
                self.__tetris().update()
            for event in pygame.event.get():
                self.__check_user_event(event)

            self.__graphics().display_scene()
            
    def __check_user_event(self, event):
        if event.type == pygame.QUIT:
            self.__stop_running()
            # TODO: Hantera user-input
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.__tetris().rotate()
                pass
            if event.key == pygame.K_a:
                pass
            elif event.key == pygame.K_d:
                pass
            if event.key == pygame.K_s:
                pass

    def __running(self):
        return self.running

    def __stop_running(self):
        self.running = False
        pygame.quit()

    def __frame_count(self):
        return self.frame_count

    def __slowness(self):
        return self.slowness

    def __add_to_frame_count(self):
        self.frame_count += 1

    def __tetris(self):
        return self.tetris

    def __clock(self):
        return self.clock

    def __graphics(self):
        return self.graphics

    def __fps(self):
        return self.fps

if __name__ == "__main__":
    file_manager = FileManager("config.json")
    data_manager = JSONManager(file_manager)
    data = data_manager.get_data()

    fps = data["interface"]["fps"]
    height = data["interface"]["screen_height"]
    ratio = float(data["board"]["cols"]) / float(data["board"]["rows"])
    width = int(height * ratio)
    slowness = data["interface"]["slowness"]

    rows = data["board"]["rows"]
    cols = data["board"]["cols"]
    size = width / cols

    block_types = data["blocks"]["types"]
    block_colors = data["blocks"]["colors"]

    tetris = Tetris(block_types, block_colors, rows, cols)
    game = Game(fps, width, height, slowness, tetris, size)
    game.run()