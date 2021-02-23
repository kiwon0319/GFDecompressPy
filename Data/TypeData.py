# TypeData.py
def get_doll_type(code):
    if code == 0:
        return "all"
    elif code == 1:
        return "hg"
    elif code == 2:
        return "smg"
    elif code == 3:
        return "rf"
    elif code == 4:
        return "ar"
    elif code == 5:
        return "mg"
    elif code == 6:
        return "sg"
    else:
        return "undefined"


def get_equip_type(code):
    if code == 0:
        return "none"
    elif code == 1:
        return "optical"
    elif code == 2:
        return "holo"
    elif code == 3:
        return "reddot"
    elif code == 4:
        return "nightvision"
    elif code == 5:
        return "apAmmo"
    elif code == 6:
        return "hpAmmo"
    elif code == 7:
        return "shotgunShell"
    elif code == 8:
        return "hvAmmo"
    elif code == 9:
        return "chip"
    elif code == 10:
        return "exoSkeleton"
    elif code == 11:
        return "armorPlate"
    elif code == 12:
        return "medal"
    elif code == 13:
        return "suppressor"
    elif code == 14:
        return "ammunitionBox"
    elif code == 15:
        return "cloak"
    elif code == 16:
        return "spPart"
    elif code == 17:
        return "spClip"
    else:
        return "undefined"


def get_equip_category(code):
    if code == 1:
        return "accessory"
    elif code == 2:
        return "ammo"
    elif code == 3:
        return "doll"
    else:
        return "undefined"


def get_fairy_category(category):
    if category == 1:
        return "battle"
    elif category == 2:
        return "strategy"
    else:
        return "dummy"


def get_squad_type(code):
    if code == 1:
        return "ATW"
    elif code == 2:
        return "MTR"
    elif code == 3:
        return "AGL"
    else:
        return "undefined"
