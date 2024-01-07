import pygame
import os

from sprites.player import Player
from sprites.obstacle import Obstacle
from sprites.background import Background
from sprites.coins import Coin
from sprites.backwall import MovingObject
from db import update_record
import resources.colors as colors
from gamemenu.pause_file import PauseButton
import gamemenu.audio as audio
import utils


class Game:
    def __init__(self, user_information):
        self.user_information = user_information
        self.saved_coins = 0
        self.WIN_WIDTH = 500
        self.WIN_HEIGHT = 700
        self.X_INIT = self.WIN_WIDTH / 2
        self.Y_INIT = 600
        self.MOVE_SPEED = 5
        self.stop_game = False
        self.WIN = pygame.display.set_mode((self.WIN_WIDTH, self.WIN_HEIGHT))
        self.music_bool, self.sound_bool = bool(self.user_information.get("music")), bool(
            self.user_information.get("sound"))
        audio.connect_music(self.music_bool)
        skin = user_information.get("skin")
        wallpaper = user_information.get("wallpaper")
        dictionary = utils.nature()
        obstacle = dictionary[wallpaper]["Obstacle"]
        coin = dictionary[wallpaper]["Coin"]
        self.player_img = pygame.transform.scale2x(
            pygame.image.load(os.path.join("resources/images/skins", f"{skin}.png")).convert_alpha())
        self.bg_img = pygame.transform.scale2x(
            pygame.image.load(os.path.join("resources/images/wallpapers", f"{wallpaper}.png")).convert_alpha())
        self.obs_img = pygame.transform.scale2x(pygame.image.load(obstacle).convert_alpha())
        self.coin_img = pygame.transform.scale2x(pygame.image.load(coin).convert_alpha())
        self.moving_object_img = pygame.transform.scale2x(
            pygame.image.load(os.path.join("resources/images/backwalls", "backwall.png")).convert_alpha())
        self.moving_object = MovingObject(self.moving_object_img, self.WIN_WIDTH, self.Y_INIT, self.MOVE_SPEED)
        self.FONT = pygame.font.SysFont("comicsans", 30)
        self.death_coins = 0

    def run(self):
        from menu.menu import MainMenu
        player = Player(self.player_img, self.X_INIT, self.Y_INIT)
        move_speed = self.MOVE_SPEED
        move_speed_int = int(move_speed)
        base = Background(move_speed_int, self.bg_img)
        obstacles = [Obstacle(move_speed_int, self.obs_img)]
        coins = [Coin(move_speed_int, self.coin_img)]
        clock = pygame.time.Clock()
        run = True
        debug = False
        while run:
            moving_object = MovingObject(self.moving_object_img, self.X_INIT, self.Y_INIT, self.MOVE_SPEED)
            moving_object.move()
            clock.tick(60)
            base.move()
            base.update_speed(move_speed_int)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        player.set_state('Left')
                        audio.connect_sound(self.sound_bool)
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        player.set_state('Right')
                        audio.connect_sound(self.sound_bool)
                    if event.key == pygame.K_ESCAPE:
                        pb = PauseButton(self.WIN_WIDTH, self.WIN_HEIGHT, self.WIN, self.saved_coins, self.saved_speed,
                                         self.user_information)
                        pb.run()
            player.set_speed()
            player.move()
            for obstacle in obstacles:
                self.obstacle_height = obstacle.height()
                self.obstacle_width = obstacle.width()
                obstacle.move()
                if obstacle.collide(player):
                    self.death_coins = self.saved_coins
                    audio.connect_music(False)
                    audio.connect_sound(False)
                    audio.death_sound(True)
                    mm = MainMenu(500, 700, self.WIN)
                    mm.run()
                if obstacle.passed:
                    obstacles.pop(obstacles.index(obstacle))
                    obstacles.append(Obstacle(move_speed_int, self.obs_img))
                    obstacle.update_speed(move_speed_int)
            for coin in coins:
                self.coin_width = coin.width()
                self.coin_height = coin.height()
                if (self.obstacle_height not in range(self.coin_height - 75, self.coin_height + 75)) or (
                        self.coin_width != self.obstacle_width):
                    coin.move_coin()
                    if coin.coin_collide(player):
                        player.score += 1
                        coins.pop(coins.index(coin))
                        coins.append(Coin(move_speed_int, self.coin_img))
                        coin.reset(self.WIN_WIDTH)
                        coin.update_speed(move_speed_int)
                        self.saved_coins += 1
                    elif moving_object.collide_with_coin(coin):  # false
                        coins.pop(coins.index(coin))
                        coins.append(Coin(move_speed_int, self.coin_img))
                    coin.check_height()
            self.draw_window(self.WIN, base, player, obstacles, debug, coins)
            moving_object.draw(self.WIN)
            move_speed += 0.001
            move_speed_int = int(move_speed)
            self.saved_speed = move_speed_int

        update_record(str(player.score))

    def draw_window(self, win, base, player, obstacles, debug, coins, keys=[]):
        base.draw(win)
        player.draw(win)
        for obs in obstacles:
            obs.draw(win)
        for c in coins:
            c.draw(win)
        self.draw_score(self.saved_coins, win)
        if debug:
            pos_label = self.FONT.render(f"Pos: {player.x}", 1, (255, 0, 0))
            win.blit(pos_label, (15, 10))
            vel_label = self.FONT.render(f"Vel: {player.vel}", 1, (255, 0, 0))
            win.blit(vel_label, (15, 30))
            state_label = self.FONT.render(f"State: {player.state}", 1, (255, 0, 0))
            win.blit(state_label, (15, 50))
            moving_label = self.FONT.render(f"State: {player.is_moving}", 1, (255, 0, 0))
            win.blit(moving_label, (15, 70))
            if len(keys) != 0:
                i = 0
                for key in keys:
                    key_label = self.FONT.render(f"Key: {key}", 1, (255, 0, 0))
                    win.blit(key_label, (15, 70 + i * 20))
                    i += 1
        pygame.display.update()

    def draw_score(self, score, win):
        score_label = self.FONT.render(f"Собрано монет: {score}", 1, colors.BLUE)
        score_label1 = self.FONT.render(f"Пауза - ESC", 3, colors.GREY)
        win.blit(score_label, (15, 10))
        win.blit(score_label1, (15, 40))


class ContGame:
    def __init__(self, user_information, coins, speed):
        self.user_information = user_information
        self.saved_coins = coins
        self.WIN_WIDTH = 500
        self.WIN_HEIGHT = 700
        self.X_INIT = self.WIN_WIDTH / 2
        self.Y_INIT = 600
        self.MOVE_SPEED = speed
        self.stop_game = False
        self.WIN = pygame.display.set_mode((self.WIN_WIDTH, self.WIN_HEIGHT))
        self.music_bool, self.sound_bool = bool(self.user_information.get("music")), bool(
            self.user_information.get("sound"))
        self.first_play = True
        audio.connect_music(self.music_bool, self.first_play)
        skin = user_information.get("skin")
        wallpaper = user_information.get("wallpaper")
        dictionary = utils.nature()
        obstacle = dictionary[wallpaper]["Obstacle"]
        coin = dictionary[wallpaper]["Coin"]
        self.player_img = pygame.transform.scale2x(
            pygame.image.load(os.path.join("resources/images/skins", f"{skin}.png")).convert_alpha())
        self.bg_img = pygame.transform.scale2x(
            pygame.image.load(os.path.join("resources/images/wallpapers", f"{wallpaper}.png")).convert_alpha())
        self.obs_img = pygame.transform.scale2x(
            pygame.image.load(obstacle).convert_alpha())
        self.coin_img = pygame.transform.scale2x(
            pygame.image.load(coin).convert_alpha())
        self.moving_object_img = pygame.transform.scale2x(
            pygame.image.load(os.path.join("resources/images/backwalls", "backwall.png")).convert_alpha())
        self.moving_object = MovingObject(self.moving_object_img, self.WIN_WIDTH, self.Y_INIT, self.MOVE_SPEED)
        self.FONT = pygame.font.SysFont("comicsans", 30)
        self.death_coins = 0

    def run(self):
        from menu.menu import MainMenu
        self.first_play = False
        player = Player(self.player_img, self.X_INIT, self.Y_INIT)
        move_speed = self.MOVE_SPEED
        move_speed_int = int(move_speed)
        base = Background(move_speed_int, self.bg_img)
        obstacles = [Obstacle(move_speed_int, self.obs_img)]
        coins = [Coin(move_speed_int, self.coin_img)]
        clock = pygame.time.Clock()
        run = True
        debug = False
        start = True
        while run:
            audio.connect_music(self.music_bool, start)
            start = False
            moving_object = MovingObject(self.moving_object_img, self.X_INIT, self.Y_INIT, self.MOVE_SPEED)
            moving_object.move()
            clock.tick(60)
            base.move()
            base.update_speed(move_speed_int)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        player.set_state('Left')
                        audio.connect_sound(self.sound_bool)
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        player.set_state('Right')
                        audio.connect_sound(self.sound_bool)
                    if event.key == pygame.K_ESCAPE:
                        pb = PauseButton(self.WIN_WIDTH, self.WIN_HEIGHT, self.WIN, self.saved_coins, self.saved_speed,
                                         self.user_information)
                        pb.run()
            player.set_speed()
            player.move()
            for obstacle in obstacles:
                self.obstacle_width = obstacle.width()
                self.obstacle_height = obstacle.height()
                obstacle.move()
                if obstacle.collide(player):
                    self.death_coins = self.saved_coins
                    audio.connect_music(False)
                    audio.connect_sound(False)
                    audio.death_sound(True)
                    mm = MainMenu(500, 700, self.WIN)
                    mm.run()
                    break
                if obstacle.passed:
                    obstacles.pop(obstacles.index(obstacle))
                    obstacles.append(Obstacle(move_speed_int, self.obs_img))
                obstacle.update_speed(move_speed_int)
            for coin in coins:
                self.coin_width = coin.width()
                self.coin_height = coin.height()
                if (self.obstacle_height not in range(self.coin_height - 75, self.coin_height + 75)) or (
                        self.coin_width != self.obstacle_width):
                    coin.move_coin()
                    if coin.coin_collide(player):
                        player.score += 1
                        coins.pop(coins.index(coin))
                        coins.append(Coin(move_speed_int, self.coin_img))
                        coin.reset(self.WIN_WIDTH)
                        coin.update_speed(move_speed_int)
                        self.saved_coins += 1
                    elif moving_object.collide_with_coin(coin):  # false
                        coins.pop(coins.index(coin))
                        coins.append(Coin(move_speed_int, self.coin_img))
                    coin.check_height()
            self.draw_window(self.WIN, base, player, obstacles, debug, coins)
            moving_object.draw(self.WIN)
            move_speed += 0.001
            move_speed_int = int(move_speed)
            self.saved_speed = move_speed_int

        update_record(str(player.score))

    def draw_window(self, win, base, player, obstacles, debug, coins, keys=[]):
        base.draw(win)
        player.draw(win)
        for obs in obstacles:
            obs.draw(win)
        for c in coins:
            c.draw(win)
        self.draw_score(self.saved_coins, win)
        if debug:
            pos_label = self.FONT.render(f"Pos: {player.x}", 1, (255, 0, 0))
            win.blit(pos_label, (15, 10))
            vel_label = self.FONT.render(f"Vel: {player.vel}", 1, (255, 0, 0))
            win.blit(vel_label, (15, 30))
            state_label = self.FONT.render(f"State: {player.state}", 1, (255, 0, 0))
            win.blit(state_label, (15, 50))
            moving_label = self.FONT.render(f"State: {player.is_moving}", 1, (255, 0, 0))
            win.blit(moving_label, (15, 70))
            if len(keys) != 0:
                i = 0
                for key in keys:
                    key_label = self.FONT.render(f"Key: {key}", 1, (255, 0, 0))
                    win.blit(key_label, (15, 70 + i * 20))
                    i += 1
        pygame.display.update()

    def draw_score(self, score, win):
        score_label = self.FONT.render(f"Собрано монет: {score}", 1, colors.BLUE)
        score_label1 = self.FONT.render(f"Пауза - ESC", 3, colors.GREY)
        win.blit(score_label, (15, 10))
        win.blit(score_label1, (15, 40))

    def death_score(self):
        return self.death_coins


def cont_rungame(user_information, coins, speed):
    game_instance = ContGame(user_information, coins, speed)
    game_instance.run()


def rungame(user_information):
    game_instance = Game(user_information)
    game_instance.run()
