import config


def error(msg: str):
    print(f'[ERROR]   {msg}')


def info(msg: str):
    print(f'[INFO]    {msg}')


def debug(msg: str):
    if config.DEBUG:
        print(f'[DEBUG]   {msg}')
