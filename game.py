import pygame
from graphics import *

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
            self.__update_slowness()
            self.__clock().tick(self.__fps())

            if self.__tetris().get_game_over():
                return

            if self.__frame_count() % self.__slowness() == 0:
                self.__tetris().update()
            for event in pygame.event.get():
                self.__check_user_event(event)

            self.__graphics().display_scene()

    def __update_slowness(self):
        if self.__frame_count() % 1000 == 0:
            self.slowness = max(5, int(float(self.__slowness()) * 0.9))
            
    def __check_user_event(self, event):
        tetris = self.__tetris()
        if event.type == pygame.QUIT:
            self.__stop_running()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                tetris.try_rotate(clockwise = True)
            elif event.key == pygame.K_LCTRL:
                tetris.try_rotate(clockwise = False)
            elif event.key == pygame.K_a:
                tetris.try_move_left()
            elif event.key == pygame.K_d:
                tetris.try_move_right()
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

    def __set_slowness(self, slowness):
        self.slowness = slowness

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