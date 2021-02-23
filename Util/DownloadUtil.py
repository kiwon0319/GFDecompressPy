# DownloadUtil.py
# author: Guideung in 36Base
import requests
import hashlib
import os
import shutil
import zipfile
import base64
import pyDes
import re
from Util import Deserializer
from Util import AssetUnpackUtil

# 추출할 텍스트 목록
data_list = ["battle_skill_config", "equip", "fairy", "fairy_skin", "gun", "gun_obtain", "mission_skill_config", "skin"]
extra_list = ["NewCharacterVoice"]

def _getGameHost(_location):
    if _location == "kr":
        return "http://gf-game.girlfrontline.co.kr/index.php/1001/"
    elif _location == "jp":
        return "http://gfjp-game.sunborngame.com/index.php/1001/"
    elif _location == "en":
        return "http://gf-game.sunborngame.com/index.php/1001/"
    elif _location == "ch":
        return "http://gfcn-game.gw.merge.sunborngame.com/index.php/1000/"
    else:
        print("wrong location code! return china server url instead")
        return "http://gfcn-game.gw.merge.sunborngame.com/index.php/1000/"

def _getCDNHost(_location):
    if _location == "kr":
        return "http://gfkrcdn.imtxwy.com/"
    elif _location == "jp":
        return "https://gfjp-cdn.sunborngame.com/"
    elif _location == "en":
        return "https://gfus-cdn.sunborngame.com/"
    elif _location == "ch":
        return "http://gf-cn.cdn.sunborngame.com/"
    else:
        print("wrong location code! return china server url instead")
        return "http://gf-cn.cdn.sunborngame.com/"

def _getUpdateHost(_location):
    if _location == "kr":
        return "http://sn-list.girlfrontline.co.kr/"
    elif _location == "jp":
        return "https://d2p0tz30gps08r.cloudfront.net/"
    elif _location == "en":
        return "http://dkn3dfwjnmzcj.cloudfront.net/"
    elif _location == "ch":
        return "http://gf-cn.cdn.sunborngame.com/"
    else:
        print("wrong location code! return china server url instead")
        return "http://gf-cn.cdn.sunborngame.com/"

class Downloader:
    def __init__(self, _location):
        self.location = _location

        self.url = _getGameHost(_location) + "Index/version"
        self.header = {
            "User-Agent" : "Dalvic/2.1.0 (Linux; U; Android 9; SM-N935k Build/PPR1.180610.011)",
            "X-Unity_Version" : "2017.4.33f1",
            "Content-Type" : "application/x-www-form-urlencoded"
        }
        req = requests.post(self.url, headers=self.header).json()

        self.dataVersion = req["data_version"]
        self.clientVersion = req["client_version"]
        self.minVersion = round((int(self.clientVersion) / 100) * 10)
        self.abVersion = req["ab_version"]

        print("latest version :" + self.dataVersion)

    def downloadStc(self):
        stc_url = self.getStrUrl()

        if os.path.exists("./stc"):
           shutil.rmtree("./stc")
        os.mkdir("./stc")

        print("downloading latest data...")
        print("Url:" + stc_url + "")

        req = requests.get(stc_url)
        with open("./stc/stc.zip", "wb") as f:
            f.write(req.content)

        print("extract zip file...")
        stc_zip = zipfile.ZipFile("./stc/stc.zip")
        stc_zip.extractall("./stc")
        stc_zip.close()

        print("remove zip file")
        os.remove("./stc/stc.zip")

    def downloadAsset(self):
        key = "kxwL8X2+fgM="
        iv = "M9lp+7j2Jdwqr+Yj1h+A"
        bkey = base64.b64decode(key.encode("utf-8"))
        biv = base64.b64decode(iv.encode("utf-8"))

        k = pyDes.des(bkey, pyDes.CBC, biv[:8], pad=None, padmode=pyDes.PAD_PKCS5)
        encrypted_version = k.encrypt(str(self.minVersion) + "_" + str(self.abVersion) + "_AndroidResConfigData")
        encrypted_version = base64.encodebytes(encrypted_version)

        filename = re.sub('[^a-zA-Z0-9]', "", encrypted_version.decode('utf-8'))

        os.makedirs("./Assets_raw/" + self.location, exist_ok= True)

        req = requests.get(self.getAssetUrl(filename))
        with open("./Assets_raw/" + self.location + "/UnityFS.txt", "wb") as f:
            f.write(req.content)

        res_arr = Deserializer.deserialize("./Assets_raw/" + self.location + "/UnityFS.txt")
        asset_url = res_arr[0] + res_arr[1] + ".dat"
        if asset_url == ".dat":
            print("error")
            exit()

        print("Asset URl:" + asset_url)
        req = requests.get(asset_url)
        with open("./Assets_raw/" + self.location + "/texts.zip", "wb") as f:
            f.write(req.content)

        print("extracting text Asset...")
        asset_zip = zipfile.ZipFile("./Assets_raw/" + self.location + "/texts.zip")
        asset_zip.extractall("./Assets_raw/" + self.location)
        asset_zip.close()

        print("remove zip file...")
        os.remove("./Assets_raw/" + self.location + "/texts.zip")

        print("Unpacking AssetFile")
        AssetUnpackUtil.unpack_asset_filtered("./Assets_raw/" + self.location + "/asset_textes.ab", "./results/text/Core/" + self.location, data_list)
        AssetUnpackUtil.unpack_asset_filtered("./Assets_raw/" + self.location + "/asset_textes.ab", "./results/text/Extra/" + self.location, extra_list)

    def getStrUrl(self):
        md5_hash = hashlib.md5()
        md5_hash.update(self.dataVersion.encode("utf-8"))
        _hash = md5_hash.hexdigest()

        return _getCDNHost(self.location) + "data/stc_" + self.dataVersion + _hash + ".zip"

    def getAssetUrl(self, _filename):
        return _getUpdateHost(self.location) + _filename + ".txt"
