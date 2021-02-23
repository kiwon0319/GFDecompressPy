# Grid.py

def read_pos(client_value):
    if client_value == 7:
        return 1
    elif client_value == 8:
        return 4
    elif client_value == 9:
        return 7
    elif client_value == 12:
        return 2
    elif client_value == 13:
        return 5
    elif client_value == 14:
        return 8
    elif client_value == 17:
        return 3
    elif client_value == 18:
        return 6
    elif client_value == 19:
        return 9
    else:
        return -1


def grid_center(value):
    if value == 7:
        return 9
    elif value == 8:
        return 6
    elif value == 9:
        return 3
    elif value == 12:
        return 8
    elif value == 13:
            return 5
    elif value == 14:
        return 2
    elif value == 17:
        return 7
    elif value == 18:
        return 8
    elif value == 19:
        return 1
    else:
        return -1


def get_effect_type(value):
    if value == 1:
        return "pow"
    elif value == 2:
        return "rate"
    elif value == 3:
        return "hit"
    elif value == 4:
        return "dodge"
    elif value == 5:
        return "criticalPercent"
    elif value == 6:
        return "cooldown"
    elif value == 7:
        return "bullet"
    elif value == 8:
        return "armor"
    elif value == 9:
        return "nightview"
    else:
        return "undefined"