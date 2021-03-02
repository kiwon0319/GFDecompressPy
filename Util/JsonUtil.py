# JsonUtil.py
import json
import os
from Data import TypeData
from Data.GunData import GunData
from Data.EquipData import EquipData
from Data.FairyData import FairyData


def getDollJson(arr, skin_list, skill_list):
    print("인형 데이터 추출 시작")
    result = list()

    for obj in arr:
        # filtering data
        if 2000 < obj["id"] < 20000:
            continue
        if obj["id"] > 30000:
            continue

        print(str(obj["id"]) + "번 인형 변환 중...")
        # parse data
        data = GunData(obj, skin_list, skill_list)
        result.append(data.getObject())

    # save json
    with open("./results/doll.json", 'wt', encoding='UTF-8') as output:
        json.dump(result, output, indent=4)

    print("\n")


def getFairyJson(battle_skill_list, mission_skill_list):
    print("요정 데이터 추출 시작")
    result = list()

    fairy_data = json.load(open("./output/catchdata/fairy_info.json"))              # fairy data
    fairy_skin_data = json.load(open("output/catchdata/fairy_skin_info.json"))      # fairy skin data

    for obj in fairy_data["fairy_info"]:
        # filtering data
        if TypeData.get_fairy_category(int(obj["category"])) == "dummy":
            continue

        print(str(obj["id"]) + "번 요정 변환 중...")
        # parse data
        data = FairyData(obj, [battle_skill_list, mission_skill_list], fairy_skin_data)
        result.append(data.getObject())

    with open("./results/fairy.json", "wt", encoding='UTF-8') as output:
        json.dump(result, output, indent=4)

    print("\n")


def getEquiptJson(arr):
    print("장비 데이터 추출 시작")
    result = list()

    for obj in arr:
        # filtering data
        if str(obj["id"]) == obj["code"] or obj["id"] == 97 or obj["id"] == 98:
            continue

        print(str(obj["id"]) + "번 장비 변환 중...")
        # parse data
        data = EquipData(obj)
        result.append(data.getObject())

    with open("./results/equip.json", 'wt', encoding='UTF-8') as output:
        json.dump(result, output, indent=4)

    print("\n")


def getTextAsset(_location: str, _list: list):
    src_path = "./Assets_raw/" + _location + "/text/Core/"
    output_path = "./results/text/" + _location + "/"
    os.makedirs(output_path, exist_ok= True)
    for files in os.listdir(src_path):
        file_name = os.path.basename(files)
        data = dict()
        if file_name.split(".")[0] in _list:
            with open(src_path + file_name, "r", encoding='utf-8') as f:
                lines = f.readlines()
                for line in lines:
                    string = line.split(",")
                    if len(string) == 1:
                        string.append("")

                    tmp = dict()
                    tmp[string[0]] = string[1].replace("\n", "").replace("//c", ",").replace("//n", "\n")

                    data.update(tmp)

            file_name = file_name.split(".")[0] + ".json"
            with open(output_path + file_name, "wt", encoding='UTF-8') as output:
                json.dump(data, output, indent=4, ensure_ascii= False)


def getDialogueText(_locatoin: str, _list: list):
    src_path = "./Assets_raw/" + _locatoin + "/text/Extra/"
    output_path = "./results/extra_text/" + _locatoin + "/"

    os.makedirs(output_path, exist_ok= True)
    for files in os.listdir(src_path):
        file_name = os.path.basename(files)
        data = dict()
        if file_name.split(".")[0] in _list:
            with open(src_path + file_name, "r", encoding= 'utf-8') as f:
                lines = f.readlines()
                for line in lines:
                    string = line.split("|")
                    string[1] = string[1].lower()

                    if string[0] not in data.keys():
                        data[string[0]] = {}

                    data[string[0]].update({string[1] : [string[2].replace("\n", "")]})

            file_name = file_name.split(".")[0] + ".json"
            with open(output_path + file_name, "wt", encoding='UTF-8') as output:
                json.dump(data, output, indent=4, ensure_ascii= False)