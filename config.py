import json

global config
with open('./config.json', 'r') as f:
    config = json.load(f)