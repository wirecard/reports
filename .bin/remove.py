import git
import os
from natsort import natsorted
import shutil
import sys
import subprocess

REPO_NAME = "reports"
REPO_LINK = "git://github.com/wirecard/"+REPO_NAME
REPO_ADDRESS = REPO_LINK+".git"

print "Cloning repositories!"

PATH = os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])), REPO_NAME)
git.Git(os.path.dirname(os.path.realpath(sys.argv[0]))).clone(REPO_ADDRESS)

IGNORE = [".bin", ".git", ".travis.yml", "docs", "README.md", "paymentSDK-php"]

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

subprocess.call(['.bin/push.py'])

# r = git.Repo('https://github.com/wirecard/reports.git')
# r.git.add(u=True)
# r.index.commit('Update reports')
# origin = r.remote(name='TPWDCEE-4326')
# origin.push()
