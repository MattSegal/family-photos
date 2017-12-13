import os
import sys
import json

with open('zappa_settings.json', 'r') as f:
    env_vars = json.load(f)['dev']['environment_variables']
    for k, v in env_vars.items():
        os.environ[str(k)] = str(v)

from src.app import app
from src.image import resize_image, resize_images

if len(sys.argv) == 3 and sys.argv[1] == 'image':
    resize_image(sys.argv[2])
elif len(sys.argv) == 2 and sys.argv[1] == 'images':
    resize_images()
else:
    app.run(debug=True, port=8000)
