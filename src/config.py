import json

CONFIG_FILE_PATH = "./config.json"
CONFIG = json.loads(open(CONFIG_FILE_PATH, "r").read())

def getOandaKeys() -> [str, str]:
    config = CONFIG["oanda"]
    return [config["account"], config["token"]]

print(getOandaKeys())