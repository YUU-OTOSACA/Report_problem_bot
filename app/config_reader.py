import configparser
from dataclasses import dataclass


@dataclass
class TgBot:
    token: str
    admin_id: int
    sheet_name: str
    json: str

@dataclass
class Config:
    tg_bot: TgBot


def load_config(path: str):
    config = configparser.ConfigParser()
    config.read(path)

    tg_bot = config["tg_bot"]

    return Config(
        tg_bot=TgBot(
            token=tg_bot["token"],
            admin_id=int(tg_bot["admin_id"]),
            sheet_name=tg_bot["sheet_name"],
            json=tg_bot["json"]
        )
    )