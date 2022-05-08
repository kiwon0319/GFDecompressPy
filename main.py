# This is python version of GFDecompress
# Aouthor: Guideung
import os
import sys
from Util import DownloadUtil

argv = sys.argv
args = len(argv)

print("=====kr server data=====")
kr = DownloadUtil.Downloader("kr")
kr.downloadAsset()
print("\n")

print("=====global server data=====")
en = DownloadUtil.Downloader("en")
en.downloadAsset()
print("\n")

print("=====jp server data=====")
jp = DownloadUtil.Downloader("jp")
jp.downloadAsset()
print("\n")

print("=====ch server data=====")
ch = DownloadUtil.Downloader("ch")
ch.downloadAsset()

ch.downloadStc()
print("\n")

# gun = json.load(open("./output/stc/gun.json", encoding='UTF8'))
# skin = json.load(open("./output/stc/skin.json", encoding='UTF8'))
# battle_skill_config = json.load(open("./output/stc/battle_skill_config.json", encoding='UTF8'))
# mission_skill_config = json.load(open("./output/stc/mission_skill_config.json", encoding='UTF8'))
# equip = json.load(open("./output/stc/equip.json", encoding= 'UTF-8'))

try:
    if not os.path.exists("./results"):
        os.makedirs("./results")
except OSError:
    print("Error:: Creating directory failed")
    exit()

# JsonUtil.getDollJson(gun, skin, battle_skill_config)
# JsonUtil.getFairyJson(battle_skill_config, mission_skill_config)
# JsonUtil.getEquipJson(equip)
