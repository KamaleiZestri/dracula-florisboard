import tomllib
import json
import shutil
import copy
import os

# TODO read from extension file
version = "3.0.0"

# clean outputs directory
shutil.rmtree("out")
os.mkdir("out")

# load resources
colorsDict:dict = tomllib.load(open("res/colors.toml", "rb"))
baseJSON:dict = json.load(open("res/base.json", "rb"))

#load base.json. build all normal color themes.
draculaNormalThemes:dict = {} 
baseJSON["@defines"] = {}

# for color in colors, copy default. 
for colorKey, color in colorsDict.items():
    theme = copy.deepcopy(colorsDict["plain"])
    outJSON = copy.deepcopy(baseJSON)
    # load non-default variables
    for var, val in color.items():
        theme[var] = val
    # save all variables to theme
    for key in theme:
        outJSON["@defines"][f"--{key}"] = theme[key]
    draculaNormalThemes[colorKey] = outJSON

# build theme
os.mkdir("out/dracula")
shutil.copy("res/extension.json", "out/dracula/extension.json")
os.mkdir("out/dracula/stylesheets")

for key,theme in draculaNormalThemes.items():
    json.dump(theme, open(f"out/dracula/stylesheets/dracula{key}.json", "w"))

# zip to flex, delete temp dir
shutil.make_archive("out/dracula", format="zip", root_dir="out/dracula")
os.rename("out/dracula.zip", f"out/dracula v{version}.flex")
shutil.rmtree("out/dracula")

print(f"Build of 'dracula v{version}.flex' complete.")
