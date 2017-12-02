import os
import json

with open('zappa_settings.json', 'r') as f:
    env_vars = json.load(f)['dev']['environment_variables']
    os.environ['PHOTO_BUCKET_NAME'] = env_vars['PHOTO_BUCKET_NAME']
    os.environ['WEBSITE_BUCKET_NAME'] = env_vars['WEBSITE_BUCKET_NAME']

from src.app import app

app.run(debug=True, port=80)