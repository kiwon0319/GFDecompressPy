# GunData.py
from Data import TypeData, Grid


class GunData:
    def __init__(self, gun_list, skin_list, skill_list):
        # basic info
        self.id = gun_list["id"]                                    # gun id
        self.rank = gun_list["rank_display"]                        # gun rank(star)
        self.type = TypeData.get_doll_type(gun_list["type"])        # gun type
        self.buildtime = gun_list["develop_duration"]               # build time

        # skin info
        self.skins = list()
        for element in skin_list:
            if int(element["fit_gun"]) == self.id:
                self.skins.append(element["id"])

        # stat
        self.stats = dict()
        self.stats["hp"] = gun_list["ratio_life"]                   # HP
        self.stats["pow"] = gun_list["ratio_pow"]                   # pow
        self.stats["hit"] = gun_list["ratio_hit"]                   # hit
        self.stats["dodge"] = gun_list["ratio_dodge"]               # dodge
        self.stats["speed"] = gun_list["ratio_speed"]               # speed
        self.stats["rate"] = gun_list["ratio_rate"]                 # rate
        self.stats["armorPiercing"] = gun_list["armor_piercing"]    # armor piercing
        self.stats["criticalPercent"] = gun_list["crit"]            # critical percent
        self.stats["armor"] = gun_list["ratio_armor"]               # armor

        # grid effect
        self.effect = dict()
        try:
            self.effect["effectType"] = TypeData.get_doll_type(int(gun_list["effect_guntype"]))                             # grid effect target
        except ValueError:
            self.effect["effectType"] = [TypeData.get_doll_type(int(i)) for i in gun_list["effect_guntype"].split(',')]     # grid effect target (buff more than 2 types except buff all)
        self.effect["effectCenter"] = Grid.grid_center(gun_list["effect_grid_center"])                                      # effect center position
        self.effect["effectPos"] = [Grid.read_pos(int(i)) for i in gun_list["effect_grid_pos"].split(',')]                  # effect position
        self.effect["gridEffect"] = dict()                                                                                  # buff effect
        for element in gun_list["effect_grid_effect"].split(';'):
            tmp = element.split(',')
            self.effect["gridEffect"][Grid.get_effect_type(int(tmp[0]))] = int(tmp[1])

        # grow ratio
        self.grow = gun_list["eat_ratio"]
        # codename
        self.codename = gun_list["code"]

        # skill 1
        self.skill1 = dict()
        self.skill1["id"] = str(gun_list["skill1"])                                                                         # skill id

        skill1_arr = [obj for obj in skill_list if int(obj["skill_group_id"]) == int(self.skill1["id"])]
        self.skill1["codename"] = skill1_arr[0]["code"]                                                                     # skill codename
        self.skill1["initialCooldown"] = skill1_arr[0]["start_cd_time"]                                                     # start cooldown
        if skill1_arr[0]["cd_type"] == 1:                                                                                   # cooldown type (frame/turn)
            self.skill1["cooldownType"] = "frame"
        else:
            self.skill1["cooldownType"] = "turn"

        self.skill1["dataPool"] = list()                                                                                    # skill cooldown for each level
        for element in skill1_arr:
            skill1_obj = {"level": element["level"], "cooldown": element["cd_time"]}
            self.skill1["dataPool"].append(skill1_obj)

        # skill 2
        if self.id > 20000:
            self.skill2 = dict()
            self.skill2["id"] = str(gun_list["skill2"])                                                                     # skill2 id

            skill2_arr = [obj for obj in skill_list if int(obj["skill_group_id"]) == int(self.skill2["id"])]
            self.skill2["codename"] = skill2_arr[0]["code"]                                                                 # skill2 codename
            self.skill2["initialCooldown"] = skill2_arr[9]["start_cd_time"]                                                 # start cooldown
            if skill2_arr[0]["cd_type"] == 1:                                                                               # cooldown type (frame/turn)
                self.skill2["cooldownType"] = "frame"
            else:
                self.skill2["cooldownType"] = "turn"

            self.skill2["dataPool"] = list()                                                                                # skill cooldwon each level
            for element in skill1_arr:
                skill2_obj = {"level": element["level"], "cooldown": element["cd_time"]}
                self.skill2["dataPool"].append(skill2_obj)
        else:
            self.skill2 = "locked"

        # gun obtain
        self.obtain = [int(i) for i in gun_list["obtain_ids"].split(',')]

        # equip slot 1
        self.equip1 = [TypeData.get_equip_type(int(i)) for i in gun_list["type_equip1"].split(';')[1].split(',')]
        # equipt slot 2
        self.equip2 = [TypeData.get_equip_type(int(i)) for i in gun_list["type_equip2"].split(';')[1].split(',')]
        # equipt slot 3
        self.equip3 = [TypeData.get_equip_type(int(i)) for i in gun_list["type_equip3"].split(';')[1].split(',')]

        # minde update consume resource
        if gun_list["mindupdate_consume"] != "":
            cnt = 0
            consume = gun_list["mindupdate_consume"].split(';')
            self.mindupdate = list()
            for string in consume:
                self.mindupdate.append(dict())
                self.mindupdate[cnt]["core"] = int(string.split(',')[0].split(':')[1])
                self.mindupdate[cnt]["mempiece"] = int(string.split(',')[1].split(':')[1])
                cnt += 1
        else:
            self.mindupdate = "locked"

        # nation or team tag
        if gun_list["tag"] == "" or gun_list["tag"] is None:
            self.tag = "team_griffin"
        else:
            self.tag = gun_list["tag"]

    # return instance value as dictionary
    def getObject(self):
        if self.id > 20000:
            return {
                "id": self.id,
                "rank": self.rank,
                "type": self.type,
                "buildTime": self.buildtime,
                "skins": self.skins,
                "stats": self.stats,
                "effect": self.effect,
                "grow": self.grow,
                "codename": self.codename,
                "skill1": self.skill1,
                "skill2": self.skill2,
                "obtain": self.obtain,
                "equip1": self.equip1,
                "equip2": self.equip2,
                "equip3": self.equip3,
                "mindupdate": self.mindupdate,
                "tag": self.tag
            }
        else:
            return {
                "id": self.id,
                "rank": self.rank,
                "type": self.type,
                "buildTime": self.buildtime,
                "skins": self.skins,
                "stats": self.stats,
                "effect": self.effect,
                "grow": self.grow,
                "codename": self.codename,
                "skill1": self.skill1,
                "obtain": self.obtain,
                "equip1": self.equip1,
                "equip2": self.equip2,
                "equip3": self.equip3,
                "tag": self.tag
            }
