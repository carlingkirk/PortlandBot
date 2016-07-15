import json
import sys
import os

sys.path += ['AddLinkFlairFromComment']
sys.path += ['UpdateMenusAndCSS']
sys.path += ['IgnoreReports']
sys.path += ['LimitDomains']
sys.path += ['FlairSetter']

import LinkFlair
import UpdateMenu
import IgnoreReports
import FlairSetter
import LimitDomains

f = open('config.json', 'r')

try:
    config = json.load(f)
finally:
    f.close()

ur = UpdateMenu.UpdateMenu(config)
ur.run(config)
#LinkFlair.run(config)
#IgnoreReports.run(config)
#FlairSetter.run(config)
#LimitDomains.run(config)
