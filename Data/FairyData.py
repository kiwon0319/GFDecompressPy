# FairyData.py
from Data import TypeData


_STAT_LIST = [                  # index     name(Ko_KR)
    "pow",                      # 0         화력
    "hit",                      # 1         명중
    "dodge",                    # 2         회피
    "armor",                    # 3         장갑
    "critical_harm_rate",       # 4         치명피해
    "armor_piercing"            # 5         장갑관통
]


def _getStatKey(string):
    if string not in _STAT_LIST:
        return "Undefined"
    else:
        if string == _STAT_LIST[4]:
            return "criticalHarmRate"
        elif string == _STAT_LIST[5]:
            return "armorPiercing"
        else:
            return string


class FairyData:
    def __init__(self, fairy_obj, skill_list, skin_list):
        # basic info
        self._id = int(fairy_obj["id"])                                              # fairy id
        self._category = TypeData.get_fairy_category(int(fairy_obj["category"]))     # fairy category

        # stats
        self._stats = dict()
        for stat_name in _STAT_LIST:
            if fairy_obj[stat_name] != "0":
                self._stats[_getStatKey(stat_name)] = int(fairy_obj[stat_name])

        # skill
        self._skill = dict()
        self._skill["id"] = fairy_obj["skill_id"]       # skill id

        if self._skill["id"][0] == "*":                                                                                     # strategy fiary skill
            skill_arr = [obj for obj in skill_list[1] if int(obj["skill_group_id"]) == int(self._skill["id"][1:])]
            self._skill["codename"] = skill_arr[0]["code"]                                                                  # codename
            self._skill["initialCooldown"] = 0                                                                              # start cooldown
            self._skill["cooldownType"] = "turn"                                                                            # cooldown type
            self._skill["consumption"] = skill_arr[0]["consumption"]                                                        # support point consumption

            self._skill["dataPool"] = list()                                                                                # skill cooldown each level
            for element in skill_arr:
                skill_obj = {"level": element["level"], "cooldown": element["cd_time"]}
                self._skill["dataPool"].append(skill_obj)
        else:                                                                                                               # battle fairy skill
            skill_arr = [obj for obj in skill_list[0] if int(obj["skill_group_id"]) == int(self._skill["id"])]
            self._skill["codename"] = skill_arr[0]["code"]                                                                  # codename
            self._skill["initialCooldown"] = skill_arr[0]["start_cd_time"]                                                  # start cooldown

            if skill_arr[0]["cd_type"] == 1:                                                                                # cooldown type
                self._skill["cooldownType"] = "frame"
            else:
                self._skill["cooldownType"] = "turn"

            self._skill["consumption"] = skill_arr[0]["consumption"]                                                        # support point consumption

            self._skill["dataPool"] = list()                                                                                # skill cooldown each level
            for element in skill_arr:
                skill_obj = {"level": element["level"], "cooldown": element["cd_time"]}
                self._skill["dataPool"].append(skill_obj)

        self._grow = int(fairy_obj["grow"])                                            # build time
        self._codename = fairy_obj["code"]                                                                                                                  # grow ratio
        self._build_time = int(fairy_obj["develop_duration"])                                                                    # code name

        self.powerup = dict()                               # fiary upgrade cost
        self.powerup["mp"] = fairy_obj["powerup_mp"]        # manpower
        self.powerup["ammo"] = fairy_obj["powerup_ammo"]    # ammo
        self.powerup["mre"] = fairy_obj["powerup_mre"]      # mre
        self.powerup["part"] = fairy_obj["powerup_part"]    # part

        self._retire_exp = fairy_obj["quality_exp"]                                                                         # upgrade exp
        self._quality_exp = [int(i.split(':')[1]) for i in fairy_obj["quality_need_number"].split(',')]                     # quality exp each rank

        # skins
        self._skins = list()
        for element in skin_list["fairy_skin_info"]:
            if int(element["gift_fairy"]) == self._id:
                self._skins.append(
                            {
                                "id": element["id"],                # skin id
                                "codename": element["pic_id"]       # resource image name
                            }
                        )

    # return instance value as dictinary
    def getObject(self):
        return {
            "id": self._id,
            "category": self._category,
            "stats": self._stats,
            "skill": self._skill,
            "grow": self._grow,
            "buildTime": self._build_time,
            "codename": self._codename,
            "powerup": self.powerup,
            "retireExp": self._retire_exp,
            "qualityExp": self._quality_exp,
            "skins": self._skins
        }
