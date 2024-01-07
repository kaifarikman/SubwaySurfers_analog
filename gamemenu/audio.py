import pygame.mixer


def connect_music(music_playing, flag=True):
    from random import choice
    pygame.mixer.init()
    numbers = [1, 2, 3]
    choose = choice(numbers)
    music_path = f'resources/audios/music/music_for_ears{choose}.mp3'
    if music_playing:
        if flag:
            pygame.mixer.Channel(0).play(pygame.mixer.Sound(music_path), -1)
        else:
            pygame.mixer.Channel(0).unpause()
    else:
        pygame.mixer.Channel(0).pause()


def connect_sound(sound_playing, flag=True):
    sound_path = f"resources/audios/sounds/movement_sound.wav"
    pygame.mixer.init()
    if sound_playing:
        if flag:
            pygame.mixer.Channel(1).play(pygame.mixer.Sound(sound_path))
        else:
            pygame.mixer.Channel(1).unpause()
    else:
        pygame.mixer.Channel(1).pause()


def death_sound(death_playing):
    sound_path = f"resources/audios/death/death.mp3"
    pygame.mixer.init()
    if death_playing:
        pygame.mixer.Channel(2).play(pygame.mixer.Sound(sound_path))
    else:
        pygame.mixer.Channel(2).pause()
