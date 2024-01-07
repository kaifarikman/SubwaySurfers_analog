import pygame_menu as pm
import db
import pygame
import resources.colors as colors
import utils
import phrases.phrases as phrases_menu
import gamemenu.audio as audio


class MainMenu:
    def __init__(self, width, height, screen):
        self.width = width
        self.height = height
        self.screen = screen
        self.main_menu = self.create_main_menu()
        self.data = {
            "nickname": "",
            "music": True,
            "sound": True,
            "skin": "skin2",
            "wallpaper": "wallpaper2",
            "record": self.record()
        }

    def record(self):
        now_record = utils.get_record()
        return now_record

    def start_game(self):
        from gamemenu.game import Game
        self.music_bool, self.sound_bool = bool(self.data.get("music")), bool(self.data.get("sound"))
        audio.connect_music(self.music_bool)
        audio.connect_sound(self.sound_bool)
        game_instance = Game(self.data)
        game_instance.run()

    def create_settings_menu(self):
        def save_settings_callback():
            data = utils.get_information(settings.get_input_data())
            self.data = data
            db.update_information(data)

        settings = pm.Menu(title=phrases_menu.SETTINGS,
                           width=self.width,
                           height=self.height,
                           theme=pm.themes.THEME_BLUE)
        settings._theme.widget_font_size = 25
        settings._theme.widget_font_color = colors.BLACK
        settings._theme.widget_alignment = pm.locals.ALIGN_LEFT

        settings.add.text_input(
            title=phrases_menu.NICKNAME_TEXT, textinput_id="nickname"
        )
        settings.add.toggle_switch(
            title=phrases_menu.MUSIC_TEXT, default=True, toggleswitch_id="music"
        )
        settings.add.toggle_switch(
            title=phrases_menu.SOUND_TEXT, default=True, toggleswitch_id="sound"
        )

        settings.add.dropselect(
            title=phrases_menu.SKINS_TEXT, items=phrases_menu.SKINS, toggleswitch_id="skin",
            selector_id="skin", default=True
        )

        settings.add.dropselect(
            title=phrases_menu.WALLPAPERS_TEXT, items=phrases_menu.WALLPAPERS,
            toggleswitch_id="wallpaper", default=True
        )

        settings.add.label(
            title=f"{phrases_menu.RECORD_TEXT} {self.record()}"
        )

        settings.add.button(title=phrases_menu.commit, action=save_settings_callback,
                            font_color=colors.WHITE, background_color=colors.GREEN)

        settings.add.button(title=phrases_menu.back,
                            action=pm.events.BACK, align=pm.locals.ALIGN_CENTER)

        return settings

    def create_main_menu(self):
        main_menu = pm.Menu(title=phrases_menu.MAIN_MENU,
                            width=self.width,
                            height=self.height,
                            theme=pm.themes.THEME_GREEN)
        main_menu._theme.widget_alignment = pm.locals.ALIGN_CENTER

        settings_menu = self.create_settings_menu()

        main_menu.add.label(title=f'Ваш рекорд {self.record()}', font_color=colors.BLUE,
                            background_color=colors.GREEN)

        main_menu.add.label(title='')

        main_menu.add.button(title=phrases_menu.PLAY, action=self.start_game,
                             font_color=colors.WHITE, background_color=colors.RED)

        main_menu.add.label(title="")

        main_menu.add.button(title=phrases_menu.SETTINGS, action=settings_menu,
                             font_color=colors.WHITE, background_color=colors.GREEN)

        main_menu.add.label(title="")

        main_menu.add.button(title=phrases_menu.EXIT, action=pm.events.EXIT,
                             font_color=colors.WHITE, background_color=colors.RED)

        return main_menu

    def run(self):
        self.main_menu.mainloop(self.screen)


def self_menu():
    screen = pygame.display.set_mode((500, 700))
    mm = MainMenu(500, 700, screen)
    mm.run()
