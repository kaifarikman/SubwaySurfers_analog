class MovingObject:
    def __init__(self, img, x, y, speed):
        self.img = img
        self.x = x
        self.y = y
        self.speed = speed

    def move(self):
        self.x -= self.speed

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))

    def is_out_of_bounds(self):
        return self.x < -self.img.get_width()

    def collide_with_coin(self, coin):
        flag1 = self.x < coin.x
        flag2 = self.x + self.img.get_width() > coin.x
        flag3 = self.y < coin.y
        flag4 = self.y + self.img.get_height() > coin.y
        flag_ = flag1 and flag2
        flag__ = flag3 and flag4
        return flag_ and flag__

    def reset(self, win_width):
        self.x = win_width
