class Block:
    def __init__(self, position, block_type, color):
        self.color = color
        self.tile_matrix = []
        self.position = position
        self.__parse_block_type(block_type)

    def get_tile_positions(self, specified_matrix = None):
        matrix = self.__tile_matrix()
        if specified_matrix is not None:
            matrix = specified_matrix

        actual_tile_positions_on_board = []
        for y, row in enumerate(matrix):
            for x, item in enumerate(row):
                if item == 1:
                    actual_tile_positions_on_board.append({"x": x + self.get_position()["x"], "y": y + self.get_position()["y"]})
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
    
    def get_rotated_tile_matrix(self, clockwise):
        rotated_matrix = list(zip(*self.get_tile_matrix()[::-1]))
        if clockwise:
            return rotated_matrix
        else:
            rotated_matrix = list(zip(*rotated_matrix[::-1]))
            rotated_matrix = list(zip(*rotated_matrix[::-1]))
        return rotated_matrix

    def get_rotated_tile_positions(self, clockwise):
        rotated_matrix = self.get_rotated_tile_matrix(clockwise)
        return self.get_tile_positions(rotated_matrix)