import db
import os


def get_information(data: dict) -> dict:
    skin = "skin2"
    wallpaper = "wallpaper2"

    for obj in data.values():
        if type(obj) is tuple:
            select = str(obj[0][1])
            if select.startswith('skin'):
                skin = select
            if select.startswith('wallpaper'):
                wallpaper = select

    information = {
        "nickname": data.get("nickname"),
        "music": data.get("music"),
        "sound": data.get("sound"),
        "skin": skin,
        "wallpaper": wallpaper,
        "record": get_record()
    }
    return information


def nature() -> dict:
    d = {
        "wallpaper1": {"Obstacle": os.path.join("resources//images//obstacles", "obstacle1.png"),
                       "Coin": os.path.join("resources//images//coins", "coin1.png")},
        "wallpaper2": {"Obstacle": os.path.join("resources//images//obstacles", "obstacle2.png"),
                       "Coin": os.path.join("resources//images//coins", "coin2.png")}
    }
    return d


def get_record() -> str:
    information = db.get_information_from_db()
    return information[5] if information else '0'
