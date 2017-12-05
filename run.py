import os
import json
import logging

logging.basicConfig()

with open('secrets.json', 'r') as f:
    env_vars = json.load(f)
    for k, v in env_vars.items():
        os.environ[str(k)] = str(v)

with open('zappa_settings.json', 'r') as f:
    env_vars = json.load(f)['dev']['environment_variables']
    for k, v in env_vars.items():
        os.environ[str(k)] = str(v)

from src.app import app

app.run(debug=True, port=80)