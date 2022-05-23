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
import UnityPy
from Util import AssetUnpackUtil
from Util import JsonUtil

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
        print("wrong location code! return taiwan server url instead")
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


def deserialize(_file_path, _file_name):
    with open(_file_path, "rb") as f:
        bundle = UnityPy.load(f)

    obj_ptr = bundle.container.get("assets/resources/resdata.asset")
    data = obj_ptr.get_obj().read_typetree()

    res_url = data["resUrl"]
    res_name = ""
    for key, value in enumerate(data["BaseAssetBundles"]):
        if value["assetBundleName"] == _file_name:
            res_name = value["resname"]

    return [res_url, res_name]


class Downloader:
    def __init__(self, _location):
        self.location = _location

        self.url = _getGameHost(_location) + "Index/version"
        self.header = {
            "User-Agent": "Dalvic/2.1.0 (Linux; U; Android 12; SM-F916N Build/SP1A.210812.016)",
            "X-Unity_Version": "2017.4.40c1",
            "Content-Type": "application/x-www-form-urlencoded"
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

        os.makedirs("./Assets_raw/" + self.location, exist_ok=True)

        req = requests.get(self.getAssetUrl(filename))
        with open("./Assets_raw/" + self.location + "/UnityFS.txt", "wb") as f:
            f.write(req.content)

        self.legacyFunction("asset_texttable")
        self.legacyFunction("asset_textes")

        AssetUnpackUtil.unpack_asset_filtered(
            "./Assets_raw/" + self.location + "/asset_textes.ab",
            "./Assets_raw/" + self.location + "/text/Extra/",
            extra_list
        )
        JsonUtil.getDialogueText(self.location, extra_list)

    def getStrUrl(self):
        md5_hash = hashlib.md5()
        md5_hash.update(self.dataVersion.encode("utf-8"))
        _hash = md5_hash.hexdigest()

        return _getCDNHost(self.location) + "data/stc_" + self.dataVersion + _hash + ".zip"

    def getAssetUrl(self, _filename):
        return _getUpdateHost(self.location) + _filename + ".txt"

    def legacyFunction(self, _filename):
        res_arr = deserialize("./Assets_raw/" + self.location + "/UnityFS.txt", _filename)
        if not res_arr:
            print("Legacy Detected")
            return None

        asset_url = res_arr[0] + res_arr[1] + ".ab"
        if asset_url == ".dat":
            exit()

        print("Asset URl:" + asset_url)
        req = requests.get(asset_url)
        with open("./Assets_raw/" + self.location + "/" + _filename + ".ab", "wb") as f:
            f.write(req.content)

        print("Unpacking AssetFile")
        AssetUnpackUtil.unpack_asset_filtered(
            "./Assets_raw/" + self.location + "/" + _filename + ".ab",
            "./Assets_raw/" + self.location + "/text/Core/",
            data_list
        )
        JsonUtil.getTextAsset(self.location, data_list)
