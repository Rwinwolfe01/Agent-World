def can_move(world_map, x, y):

    # خارج شدن از نقشه
    if not world_map.is_inside_world(x, y):

        return False

    # برخورد با ساختمان
    if world_map.is_blocked(x, y):

        return False

    return True