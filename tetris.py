from tile import *
from block import *
from graphics import BACKGROUND_COLOR
import random

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

    #Tries to move down a block
    def try_move_down(self):
        if not self.__try_move(0, 1):
            if self.get_game_over():
                return False
            self.__stop_block()
        else:
            return True
        return False

    #Tries to move a block all the way down
    def try_fall_down(self):
        while self.try_move_down(): continue

    #Tries to move a block right
    def try_move_right(self):
        self.__try_move(1, 0)

    #Tries to move a block left
    def try_move_left(self):
        self.__try_move(-1, 0)

    #Tries to move a block in a specified direction
    def __try_move(self, dx, dy):
        current_block = self.__current_block()
        if current_block is None:
            return False
        tile_positions = current_block.get_tile_positions()
        new_tile_positions = self.__transpose_tile_positions(tile_positions, dx, dy)
        if self.__possible_move(new_tile_positions):
            self.__move(dx, dy, current_block.get_color())
            return True
        else:
            return False

    #Move a block to new coordinates
    def __move(self, dx, dy, current_block_color):
        self.__reset_current_block_tiles()
        old_position = self.__current_block().get_position()
        self.__current_block().set_position({"x": old_position["x"] + dx, "y": old_position["y"] + dy})
        self.__set_current_block_color(current_block_color)

    #Tries to rotate the current block
    def try_rotate(self, clockwise : bool):
        current_block = self.__current_block()
        if current_block is None:
            return False
        rotated_tile_positions = self.__current_block().get_rotated_tile_positions(clockwise)
        if self.__possible_move(rotated_tile_positions):
            self.__rotate(self.__current_block().get_color(), clockwise)

    #Rotates the current block
    def __rotate(self, current_block_color, clockwise : bool):
        self.__reset_current_block_tiles()
        self.__current_block().set_tile_matrix(self.__current_block().get_rotated_tile_matrix(clockwise))
        self.__set_current_block_color(current_block_color)

    #Spawns a new block
    def __spawn_block(self):
        x, y = self.get_cols() // 2, -2
        position = {"x": x, "y": y}
        tile_positions, color = self.__get_random_block()
        block = Block(position, tile_positions, color)

        for tile_position in block.get_tile_positions():
            x, y = tile_position["x"], tile_position["y"]
            if y >= 0:
                tile = self.__get_tile(x, y)
                tile.set_color(block.get_color())
        self.__set_current_block(block)

    #When a block hits other blocks, stop it from falling
    def __stop_block(self):
        current_block = self.__current_block()
        if current_block is None:
            return False
        for tile_position in current_block.get_tile_positions():
            x, y = tile_position["x"], tile_position["y"]
            self.__get_tile(x, y).set_is_block(True)
            self.__get_tile(x, y).set_is_outline(False)
        self.__reset_current_block()

    #Move a set of tile positions in a direction
    def __transpose_tile_positions(self, tile_positions, dx, dy):
        new_tile_positions = []
        for tile_position in tile_positions:
            new_tile_position = {"x": tile_position["x"] + dx, "y": tile_position["y"] + dy}
            new_tile_positions.append(new_tile_position)
        return new_tile_positions

    #Checks if a certain state of tile_positions is valid for a block. In other words, if a block can be moved here without getting out of bounds etc.
    def __possible_move(self, new_tile_positions):
        for tile_position in new_tile_positions:
            x, y = tile_position["x"], tile_position["y"]
            if self.__out_of_bounds(x, y):
                return False
        return True
 
    #Check if a position is out of bounds
    def __out_of_bounds(self, x, y):
        if y >= self.get_rows() or x >= self.get_cols() or x < 0:
            return True
        if y >= 0:
            if self.__tile_is_block(x, y):
                return True
        return False
    
    #Checks if there are any completed rows
    def __check_rows(self):
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

    #Moves all the tiles above a completed row down
    def __fall_after_completed(self, row):
        for y in range(row, 0, -1):
            for x in range(self.get_cols()):
                above_tile = self.__get_tile(x, y - 1)
                self.__get_tile(x, y).copy_state(above_tile)
                above_tile.reset()

    #Reset the state of all tiles on screen in order to update them directly after
    def __reset_current_block_tiles(self): 
        for tile_position in self.__current_block().get_tile_positions():
            x, y = tile_position["x"], tile_position["y"]
            if y >= 0:
                self.__get_tile(x, y).reset()
        for tile_position in self.__get_outline_tile_positions():
            x, y = tile_position["x"], tile_position["y"]
            if y >= 0:
                self.__get_tile(x, y).reset()
    
    #Update the state of all tiles on screen in order to display the moving block
    def __set_current_block_color(self, color):
        for tile_position in self.__get_outline_tile_positions():
            x, y = tile_position["x"], tile_position["y"]
            if y >= 0:
                self.__get_tile(x, y).set_color(color)
                self.__get_tile(x, y).set_is_outline(True)
        for tile_position in self.__current_block().get_tile_positions():
            x, y = tile_position["x"], tile_position["y"]
            if y >= 0:
                self.__get_tile(x, y).set_color(color)
                self.__get_tile(x, y).set_is_outline(False)

    #Calculates the tile positions of the outlines at the bottom
    def __get_outline_tile_positions(self):
        current_block = self.__current_block()
        tile_positions = current_block.get_tile_positions()
        okay_to_move_down = True
        while okay_to_move_down:
            new_tile_positions = self.__transpose_tile_positions(tile_positions, 0, 1)
            if not self.__possible_move(new_tile_positions):
                break
            tile_positions = new_tile_positions
        return tile_positions

    #Puts the game in a game-over state
    def __end_game(self):
        self.__reset_current_block()
        self.__set_game_over(True)

    def __tile_is_block(self, x, y):
        return self.__get_tile(x, y).get_is_block()

    def __get_tile(self, x, y):
        return self.get_board()[x][y]

    def get_board(self):
        return self.board
    
    #Returns a random tetris block
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
        return self.rows

    def get_cols(self):
        return self.cols
    
    def get_game_over(self):
        return self.game_over

    def __set_game_over(self, game_over):
        self.game_over = game_over