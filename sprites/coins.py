from random import randrange
import pygame


class Coin:
    def __init__(self, vel, img) -> None:
        self.MAX_Y = 800
        self.MID = 250
        self.OFFSET = 130
        self.IMG_WIDTH = 20
        self.vel = vel
        self.y = -20
        self.x = self.MID + randrange(-1, 2, 1) * self.OFFSET - self.IMG_WIDTH
        self.img = img
        self.passed = False
        self.passed = False

    def move_coin(self):
        self.y += self.vel
        if self.y > self.MAX_Y:
            self.passed = True

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))

    def reset(self, x):
        self.x = x
        self.passed = False

    def coin_collide(self, player):
        player_mask = player.get_mask()
        mask = pygame.mask.from_surface(self.img)
        offset = (self.x - player.x, self.y - player.y)
        if player_mask.overlap(mask, offset):
            return True
        return False

    def check_height(self):
        if self.y > 700:
            self.reset(self.y)

    def get_surface(self):
        return self.img

    def width(self):
        return self.x

    def height(self):
        return self.y

    def update_speed(self, vel):
        self.vel = vel

    def cords(self):
        return self.x, self.y

    def set_cords(self, new_x, new_y):
        self.x = new_x
        self.y = new_y
