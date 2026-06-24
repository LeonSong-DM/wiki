import argparse
from collections import ChainMap

default_settings = {"message": "Hello World.", "decorate": "", "space_num": 0}

parser = argparse.ArgumentParser()
parser.add_argument("--message", type=str)
parser.add_argument("--decorate", type=str)
parser.add_argument("--space_num", type=int)

args = parser.parse_args()


user_settings = {
    "message": args.message,
    "decorate": args.decorate,
    "space_num": args.space_num,
}

for key in user_settings:
    if user_settings[key] is None:
        user_settings[key] = default_settings[key]

settings = ChainMap(user_settings, default_settings)


def log(
    message=settings["message"],
    decorate=settings["decorate"],
    space_num=settings["space_num"],
):
    result = " " * space_num + decorate + f" {message} " + decorate
    print(result)


log()
