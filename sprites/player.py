import pygame


class Player:
    def __init__(self, img, x, y):
        self.IMG_WIDTH = 20
        self.x_init = x - self.IMG_WIDTH
        self.x = x - self.IMG_WIDTH
        self.y = y
        self.state = 0
        self.is_moving = False
        self.vel = 0
        self.img = img
        self.score = 0
        self.MAX_SPEED = 10
        self.MAX_X = 200
        self.INERTIA = 2
        self.OFFSET = 130
        self.MOVE_SPEED = self.OFFSET / 10

    def move(self):
        displacement = self.vel
        self.x += displacement

        target_pos = self.x_init + self.state * self.OFFSET
        # print(f"Target : {target_pos}; x : {self.x}; state : {self.state}")
        if target_pos == self.x:
            self.is_moving = False

    def set_state(self, side='None'):
        if not self.is_moving:
            if side == 'Left':
                self.state -= 1
                self.is_moving = True
                if self.state < -1:
                    self.state = -1
            if side == 'Right':
                self.state += 1
                self.is_moving = True
                if self.state > 1:
                    self.state = 1

    def set_speed(self):
        """
        sets player speed
        """
        if self.is_moving:
            target_pos = self.x_init + self.state * self.OFFSET
            if (self.x - target_pos) > 0:
                self.vel = -self.MOVE_SPEED
            else:
                self.vel = self.MOVE_SPEED
        else:
            self.vel = 0

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))

    def get_mask(self):
        return pygame.mask.from_surface(self.img)

    def set_score(self, coins):
        self.score = coins
