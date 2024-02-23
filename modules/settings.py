import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    # Bot settings

    def __init__(self) -> None:
        try:
            pass
        except AssertionError as e:
            print(e)
            exit()
