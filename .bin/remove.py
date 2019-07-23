import os
from natsort import natsorted
import shutil

PATH = os.path.abspath(os.curdir)+"/"

print('Find unnecessary plugin versions...')

IGNORE = [".bin", ".git", ".travis.yml", "docs", "README.md", "paymentSDK-php", '.idea']

plugin_array = []
help_dict = {}
for dirs in os.listdir(PATH):
    if dirs not in IGNORE:
        plugin_array.append(dirs.replace("-ee", "").split("-"))

for sublist in plugin_array:
    if sublist[0] in help_dict:
        help_dict[sublist[0]].append(sublist[1])
    elif sublist[1] not in help_dict:
        help_dict[sublist[0]] = [sublist[1]]

new_dict = {}
for key, value in help_dict.items():
    rr = natsorted(value)
    if len(rr) > 3:
        new_dict.update({key: rr[0]})

delete = []
for key, value in new_dict.items():
    delete.append(key+'-ee-'+value)

for dirs in os.listdir(PATH):
    for plugin in delete:
        if plugin in dirs:
            shutil.rmtree(os.path.join(PATH, plugin), ignore_errors=True)
