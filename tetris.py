from file_helper import *
import pygame, random

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
    
    def copy_state(self, another_tile):
        self.set_is_block(another_tile.get_is_block())
        self.set_color(another_tile.get_color())

    def reset(self):
        self.set_is_block(False)
        self.set_color(BACKGROUND_COLOR)

class Tetris:
    def __init__(self, block_types, rows, cols):
        self.board = [[Tile(x, y, False, BACKGROUND_COLOR) for y in range(rows)] for x in range(cols)]
        self.rows, self.cols = rows, cols
        self.block_types = block_types
        self.current_block = None
        self.__spawn_block()

        # Use this code below to test the row completion mechanic, (and wait for a fitting block)

        # for y in range(rows - 2, rows):
        #     for x in range(cols):
        #         self.board[x][y].set_is_block(True)
        #         self.board[x][y].set_color((255, 0, 255))
        #     self.board[5][y].set_is_block(False)
        #     self.board[6][y].set_is_block(False)
        #     self.board[5][y].set_color(BACKGROUND_COLOR)
        #     self.board[6][y].set_color(BACKGROUND_COLOR)
        # self.board[4][rows - 3].set_color((255, 0, 255))
        # self.board[4][rows - 3].set_is_block(True)

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
                self.__move_down(tile_positions, current_block.get_color())
        self.__check_rows()
    
    #Checks if there are any completed rows
    def __check_rows(self):
        highest_completed_row = None
        amount_of_completed_rows = 0
        y = self.get_rows() - 1
        while y >= 0:
            if self.__check_row(y):
                self.__fall_after_completed(y)
            else:
                y -= 1

    #Checks if a specific row is completed
    def __check_row(self, y):
        for x in range(self.get_cols()):
            if not self.__get_tile(x, y).get_is_block():
                return False
        return True

    #Checks if a block can move down 1 step
    def __can_move_down(self, tile_positions):
        for tile_position in tile_positions:
            x, y = tile_position["x"], tile_position["y"]
            if y < 0:
                continue
            if y + 1 >= self.get_rows() or self.__tile_is_block(x, y + 1):
                return False
        return True

    #Moves all the tiles above a completed row down
    def __fall_after_completed(self, highest_completed_row):
        for y in range(highest_completed_row, 0, -1):
            for x in range(self.get_cols()):
                above_tile = self.__get_tile(x, y - 1)
                self.__get_tile(x, y).copy_state(above_tile)
                above_tile.reset()

    #Moves down a block 1 step
    def __move_down(self, tile_positions, current_block_color):
        new_tile_positions = []
        for tile_position in tile_positions:
            x, y = tile_position["x"], tile_position["y"]
            if y >= 0:
                self.__get_tile(x, y).set_color(BACKGROUND_COLOR)
            new_tile_position = {"x": x, "y": y + 1}
            new_tile_positions.append(new_tile_position)

        for tile_position in new_tile_positions:
            x, y = tile_position["x"], tile_position["y"]
            if y >= 0:
                self.__get_tile(x, y).set_color(current_block_color)

        self.__current_block().set_tile_positions(new_tile_positions)

    def __tile_is_block(self, x, y):
        return self.__get_tile(x, y).get_is_block()

    def __get_tile(self, x, y):
        return self.get_board()[x][y]

    def get_board(self):
        return self.board

    def __spawn_block(self):
        x, y = cols // 2, -2
        position = {"x": x, "y": y}
        random_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        block = Block(position, random.choice(self.__block_types()), random_color)
        for tile_position in block.get_tile_positions():
            x, y = tile_position["x"], tile_position["y"]
            if y >= 0:
                tile = self.__get_tile(x, y)
                tile.set_color(random_color)
        self.__set_current_block(block)

    def __stop_block(self):
        for tile_position in self.__current_block().get_tile_positions():
            x, y = tile_position["x"], tile_position["y"]
            self.__get_tile(x, y).set_is_block(True)
        self.__reset_current_block()

    def __block_types(self):
        return self.block_types
    
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
        self.tile_positions = []
        self.__parse_block_type(block_type, position)
    
    def get_tile_positions(self):
        return self.tile_positions

    def set_tile_positions(self, tile_positions):
        self.tile_positions = tile_positions

    def get_color(self):
        return self.color

    def __parse_block_type(self, block_type, position):
        x, y = position["x"], position["y"]
        for char in block_type:
            if char == ".":
                self.__add_tile_position(x, y)
                x += 1
            elif char == "/":
                y += 1
                x = position["x"]
            elif char == "s":
                x += 1
    
    def __add_tile_position(self, x, y):
        tile_position = {"x": x, "y": y}
        self.tile_positions.append(tile_position)

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

    tetris = Tetris(block_types, rows, cols)
    game = Game(fps, width, height, slowness, tetris, size)
    game.run()