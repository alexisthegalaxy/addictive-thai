import pygame
import os

dir_path = os.path.dirname(os.path.realpath(__file__))


class Fonts(object):
    def __init__(self):
        sarabun_path = f"{dir_path}/../fonts/Sarabun.ttf"
        self.khmer32 = pygame.font.Font(f"{dir_path}/../fonts/Khmer.ttf", 32)
        self.lao32 = pygame.font.Font(f"{dir_path}/../fonts/Lao.ttf", 32)
        self.burmese32 = pygame.font.Font(f"{dir_path}/../fonts/ZawgyiOne.ttf", 32)
        self.sanskrit32 = pygame.font.Font(f"{dir_path}/../fonts/Jaldi.ttf", 32)

        self.sarabun128 = pygame.font.Font(sarabun_path, 128)
        self.sarabun96 = pygame.font.Font(sarabun_path, 96)
        self.sarabun64 = pygame.font.Font(sarabun_path, 64)
        self.sarabun48 = pygame.font.Font(sarabun_path, 48)
        self.sarabun32 = pygame.font.Font(sarabun_path, 32)
        self.sarabun28 = pygame.font.Font(sarabun_path, 28)
        self.sarabun26 = pygame.font.Font(sarabun_path, 26)
        self.sarabun24 = pygame.font.Font(sarabun_path, 24)
        self.sarabun22 = pygame.font.Font(sarabun_path, 22)
        self.sarabun20 = pygame.font.Font(sarabun_path, 20)
        self.sarabun18 = pygame.font.Font(sarabun_path, 18)
        self.sarabun16 = pygame.font.Font(sarabun_path, 16)

