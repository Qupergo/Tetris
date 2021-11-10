from file_helper import *
from tetris import *
from game import *

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