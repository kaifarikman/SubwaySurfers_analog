import pygame_menu
from resources import colors
import phrases.phrases as pause_phrases
from gamemenu import audio


class SavedSettings:
    def __init__(self, saved_speed, collected_coins):
        self.saved_speed = saved_speed
        self.saved_coins = collected_coins

    def return_settings(self):
        array = [self.saved_speed, self.saved_coins]
        return array


class PauseButton:
    def __init__(self, width, height, screen, saved_coins, speed, user_info):
        self.speed = speed
        self.saved_coins = saved_coins
        self.width = width
        self.height = height
        self.screen = screen
        self.pause_menu = self.create_pause_menu()
        self.user_info = user_info

    def continue_game(self):
        from gamemenu.game import cont_rungame
        cont_rungame(self.user_info, self.saved_coins, self.speed)

    def return_to_main_menu(self):
        from menu.menu import self_menu
        self_menu()

    def create_pause_menu(self):
        pause_menu = pygame_menu.Menu(title="Пауза",
                                      width=self.width,
                                      height=self.height,
                                      theme=pygame_menu.themes.THEME_GREEN)
        pause_menu._theme.widget_alignment = pygame_menu.locals.ALIGN_CENTER

        pause_menu.add.label(title=f'Ваш счет {self.saved_coins}')

        pause_menu.add.label(title='')

        pause_menu.add.button(title=pause_phrases.PAUSE_PLAY, action=self.continue_game,
                              font_color=colors.WHITE, background_color=colors.RED)

        pause_menu.add.label(title="")

        pause_menu.add.button(title=pause_phrases.RETURN_MAIN_MENU, action=self.return_to_main_menu,
                              font_color=colors.WHITE, background_color=colors.GREEN)

        return pause_menu

    def run(self):
        audio.connect_music(False)
        audio.connect_sound(False)
        self.pause_menu.mainloop(self.screen)
