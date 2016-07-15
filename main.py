import json
import sys
import os

sys.path += ['AddLinkFlairFromComment']

import LinkFlair

config = json.load(open('config.json'))

LinkFlair.run(config)