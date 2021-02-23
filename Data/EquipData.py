# EquipData.py
from Data import TypeData

_STAT_LIST = [                  # index     name(Ko_KR)
    "pow",                      # 0         화력
    "hit",                      # 1         명중
    "dodge",                    # 2         회피
    "speed",                    # 3         이동속도
    "rate",                     # 4         사격속도
    "critical_harm_rate",       # 5         치명 피해
    "critical_percent",         # 6         치명률
    "armor_piercing",           # 7         장갑관통
    "armor",                    # 8         장갑
    "shield",                   # 9         보호막
    "damage_amplify",           # 10        공격 피해증가
    "damage_reduction",         # 11        피격 피해감소
    "night_view_percent",       # 12        야시능력
    "bullet_number_up"          # 13        장탄수 증가
]


def _getStatKey(string):
    if string not in _STAT_LIST:
        return "Undefined"
    else:
        if string == _STAT_LIST[5]:
            return "criticalHarmRate"
        elif string == _STAT_LIST[6]:
            return "criticalPercent"
        elif string == _STAT_LIST[7]:
            return "armorPiercing"
        elif string == _STAT_LIST[10]:
            return "damageAmplify"
        elif string == _STAT_LIST[11]:
            return "damageReduction"
        elif string == _STAT_LIST[12]:
            return "nightview"
        elif string == _STAT_LIST[13]:
            return "bullet"
        else:
            return string


class EquipData:
    def __init__(self, obj):
        # basic info
        self._id = obj["id"]                                                # id
        self._codename = obj["code"]                                        # resource image name
        self._rank = obj["rank"]                                            # rank(star)
        self._category = TypeData.get_equip_category(obj["category"])       # equip category
        self._type = TypeData.get_equip_type(obj["type"])                   # equip type
        self._company = obj["company"]                                      # manufacturer company

        # exclusive equip fit gun
        if str(obj["fit_guns"]) != "":
            self._fit_guns = [int(i) for i in obj["fit_guns"].split(',')]
        else:
            self._fit_guns = None

        self._exclusive_rate = obj["exclusive_rate"]                        # equip exp ratio (normal 1.0, exclusive 3.0)
        self._max_level = obj["max_level"]                                  # max level
        self._build_time = obj["develop_duration"]                          # build time

        # stats
        self._stats = dict()
        for stat_name in _STAT_LIST:
            if obj[stat_name] != "":
                self._stats[_getStatKey(stat_name)] = {
                    "min": obj[stat_name].split(',')[0],                    # min calibrated value
                    "max": obj[stat_name].split(',')[1]                     # max calibrated value
                }
                if not obj["bonus_type"] == "":
                    for bonus in obj["bonus_type"].split(','):
                        if bonus.split(':')[0] == stat_name:
                            self._stats[_getStatKey(stat_name)]["upgrade"] = bonus.split(':')[1]

        self.powerup = dict()                                               # equip upgrade cost
        self.powerup["mp"] = obj["powerup_mp"]                              # manpower
        self.powerup["ammo"] = obj["powerup_ammo"]                          # ammo
        self.powerup["mre"] = obj["powerup_mre"]                            # mre
        self.powerup["part"] = obj["powerup_part"]                          # part

    # return instance value as dictinary
    def getObject(self):
        return{
            "id": self._id,
            "codename": self._codename,
            "rank": self._rank,
            "category": self._category,
            "type": self._type,
            "company": self._company,
            "fitGuns": self._fit_guns,
            "exclusiveRate": self._exclusive_rate,
            "maxLevel": self._max_level,
            "buildTime": self._build_time,
            "stats": self._stats,
            "powerup": self.powerup,
        }