import pygame
from menu.menu import MainMenu
import db


def main():
    db.start_session()
    pygame.init()
    pygame.mixer.init()
    width, height = 500, 700
    screen = pygame.display.set_mode((width, height))
    program_menu = MainMenu(width, height, screen)
    program_menu.run()


if __name__ == "__main__":
    main()
