from file_helper import *
import pygame, random

BACKGROUND_COLOR = (30, 30, 30)

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

class Tetris:
    def __init__(self, block_types, block_colors, rows, cols):
        self.board = [[Tile(x, y, False, BACKGROUND_COLOR) for y in range(rows)] for x in range(cols)]
        self.rows, self.cols = rows, cols
        self.block_types = block_types
        self.block_colors = block_colors
        self.current_block = None
        self.game_over = False
        self.__spawn_block()

    #Handles what happens at this current game state
    def update(self):
        current_block = self.__current_block()
        if current_block == None:
            self.__spawn_block()
        else:
            self.try_move_down()
        self.__check_rows()

    def try_move_down(self):
        if not self.__can_move_down():
            if self.get_game_over():
                return False
            self.__stop_block()
        else:
            self.__move_down()
            return True
        return False

    def try_fall_down(self):
        while self.try_move_down():
            pass
    
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

    #Checks if the current block can be rotated
    def __can_rotate(self):
        if self.__current_block() is None:
            return False
        position = self.__current_block().get_position()
        rotated_tile_matrix = self.__current_block().get_rotated_matrix()
        for y, tile_row in enumerate(rotated_tile_matrix):
            for x, block_on_tile in enumerate(tile_row):
                if block_on_tile:
                    if self.__out_of_bounds(x + position["x"], y + position["y"]):
                        return False
        return True

    #Check if a position is out of bounds
    def __out_of_bounds(self, x, y):
        if y >= self.get_rows() or y < 0 or x >= self.get_cols() or x < 0:
            return True
        if self.__tile_is_block(x, y):
            return True
        return False

    #Rotates the current block
    def __rotate(self, current_block_color):
        self.__reset_current_block_tiles()
        self.__current_block().set_tile_matrix(self.__current_block().get_rotated_matrix())
        self.__set_current_block_tiles(current_block_color)

    #Checks if a block can move down 1 step
    def __can_move_down(self):
        current_block = self.__current_block()
        if current_block is None:
            return False
        tile_positions = current_block.get_tile_positions()
        for tile_position in tile_positions:
            x, y = tile_position["x"], tile_position["y"]
            if y < -1:
                continue
            if y + 1 >= self.get_rows():
                return False
            if self.__tile_is_block(x, y + 1):
                if y + 1 == 0: #If we cannot move down because there is a block at the top layer, it is game over!
                    self.__end_game()
                return False
        return True

    def try_move(self, right : bool):
        if self.__current_block() is None:
            return False
        
        current_block = self.__current_block()
        tile_positions = current_block.get_tile_positions()
        current_block_color = self.__current_block().get_color()
        if right:
            if self.__can_move_right(tile_positions):
                self.__move_right(tile_positions, current_block_color)
        else:
            if self.__can_move_left(tile_positions):
                self.__move_left(tile_positions, current_block_color)

    def __can_move_left(self, tile_positions):
        for tile_position in tile_positions:
            x, y = tile_position["x"], tile_position["y"]
            if x <= 0:
                return False
            x -= 1
            if y >= 0 and x >= 0:
                if self.__get_tile(x, y).get_is_block():
                    return False
        return True    

    def __can_move_right(self, tile_positions):
        for tile_position in tile_positions:
            x, y = tile_position["x"], tile_position["y"]
            if x  >= (self.get_cols()) - 1:
                return False
            x += 1
            if y >= 0 and x < self.get_cols() - 1:
                if self.__get_tile(x, y).get_is_block():
                    return False
        return True

    def __move_left(self, tile_positions, current_block_color):
        self.__reset_current_block_tiles()
        old_position = self.__current_block().get_position()
        self.__current_block().set_position({"x":old_position["x"] - 1, "y":old_position["y"]})
        self.__set_current_block_tiles(current_block_color)

    def __move_right(self, tile_positions, current_block_color):
        self.__reset_current_block_tiles()
        old_position = self.__current_block().get_position()
        self.__current_block().set_position({"x":old_position["x"] + 1, "y":old_position["y"]})
        self.__set_current_block_tiles(current_block_color)       

    def __end_game(self):
        self.__reset_current_block()
        self.__set_game_over(True)

    #Moves all the tiles above a completed row down
    def __fall_after_completed(self, highest_completed_row):
        for y in range(highest_completed_row, 0, -1):
            for x in range(self.get_cols()):
                above_tile = self.__get_tile(x, y - 1)
                self.__get_tile(x, y).copy_state(above_tile)
                above_tile.reset()

    #Moves down a block 1 step
    def __move_down(self):
        current_block = self.__current_block()
        current_block_color = current_block.get_color()
        tile_positions = current_block.get_tile_positions()
        self.__reset_current_block_tiles()
        old_position = self.__current_block().get_position()
        self.__current_block().set_position({"x":old_position["x"], "y":old_position["y"] + 1})
        self.__set_current_block_tiles(current_block_color)

    def __tile_is_block(self, x, y):
        return self.__get_tile(x, y).get_is_block()

    def __get_tile(self, x, y):
        return self.get_board()[x][y]

    def get_board(self):
        return self.board

    def __spawn_block(self):
        x, y = cols // 2, -2
        position = {"x": x, "y": y}
        tile_positions, color = self.__get_random_block()
        block = Block(position, tile_positions, color)

        for tile_position in block.get_tile_positions():
            x, y = tile_position["x"], tile_position["y"]
            if y >= 0:
                tile = self.__get_tile(x, y)
                tile.set_color(block.get_color())
        self.__set_current_block(block)

    def __stop_block(self):
        current_block = self.__current_block()
        if current_block is None:
            return False
        for tile_position in current_block.get_tile_positions():
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

    def try_to_rotate(self):
        if self.__can_rotate():
            self.__rotate(self.__current_block().get_color())

    def __reset_current_block_tiles(self): 
        for tile_position in self.__current_block().get_tile_positions():
            x, y = tile_position["x"], tile_position["y"]
            if y >= 0:
                self.__get_tile(x, y).reset()
    
    def __set_current_block_tiles(self, color):
        for tile_position in self.current_block.get_tile_positions():
            x, y = tile_position["x"], tile_position["y"]
            if y >= 0:
                self.__get_tile(x, y).set_color(color)

    def get_rows(self):
        return rows

    def get_cols(self):
        return cols
    
    def get_game_over(self):
        return self.game_over

    def __set_game_over(self, game_over):
        self.game_over = game_over

class Block:
    def __init__(self, position, block_type, color):
        self.color = color
        self.tile_matrix = []
        self.position = position
        self.__parse_block_type(block_type)

    def get_tile_positions(self):
        actual_tile_positions_on_board = []
        for y, row in enumerate(self.__tile_matrix()):
            for x, item in enumerate(row):
                if item == 1:
                    actual_tile_positions_on_board.append({"x": x + self.get_position()["x"], "y":y + self.get_position()["y"]})
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

    def __tile_matrix(self):
        return self.tile_matrix

    def __add_tile_row(self, tile_row):
        self.__tile_matrix().append(tile_row)
    
    def get_rotated_matrix(self, clockwise=False):
        if not clockwise:
            return list(zip(*self.get_tile_matrix()[::-1]))

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
                self.__draw_tile(tile.get_x(), tile.get_y(), tile.get_color()) 
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
    def __draw_tile(self, x, y, color):
        size = self.__tile_size()
        position = (x * size + size * 0.05, y * size + size * 0.05, size * 0.9, size * 0.9)
        pygame.draw.rect(self.__screen(), color, position)
        if color != BACKGROUND_COLOR:
            pygame.draw.polygon(self.__screen(), self.__lighten(color), ( #Up
                (x * size + size * 0.05, y * size + size * 0.05), 
                (x * size + size * 0.95, y * size + size * 0.05), 
                (x * size + size * 0.75, y * size + size * 0.25), 
                (x * size + size * 0.25, y * size + size * 0.25)))

            # pygame.draw.polygon(self.__screen(), self.__lighten(color), ( #Left
            #     (x * size + size * 0.05, y * size + size * 0.05), 
            #     (x * size + size * 0.05, y * size + size * 0.95), 
            #     (x * size + size * 0.25, y * size + size * 0.75), 
            #     (x * size + size * 0.25, y * size + size * 0.25)))

            pygame.draw.polygon(self.__screen(), self.__darken(color), ( #Right
                (x * size + size * 0.95, y * size + size * 0.05),
                (x * size + size * 0.95, y * size + size * 0.95), 
                (x * size + size * 0.75, y * size + size * 0.75), 
                (x * size + size * 0.75, y * size + size * 0.25)))

            # pygame.draw.polygon(self.__screen(), self.__darken(color), ( #Down
            #     (x * size + size * 0.05, y * size + size * 0.95), 
            #     (x * size + size * 0.95, y * size + size * 0.95), 
            #     (x * size + size * 0.75, y * size + size * 0.75), 
            #     (x * size + size * 0.25, y * size + size * 0.75)))

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

            if self.__tetris().get_game_over():
                print("Game over")
                return

            if self.__frame_count() % self.__slowness() == 0:
                self.__tetris().update()
            for event in pygame.event.get():
                self.__check_user_event(event)

            self.__graphics().display_scene()
            
    def __check_user_event(self, event):
        tetris = self.__tetris()
        if event.type == pygame.QUIT:
            self.__stop_running()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                tetris.try_to_rotate()
            elif event.key == pygame.K_a:
                tetris.try_move(False)
            elif event.key == pygame.K_d:
                tetris.try_move(True)
            elif event.key == pygame.K_s:
                tetris.try_move_down()
            elif event.key == pygame.K_SPACE:
                tetris.try_fall_down()

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