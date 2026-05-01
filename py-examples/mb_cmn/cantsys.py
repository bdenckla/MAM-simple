def mk_cantsys_struct(prose_val, poetic_val):
    return {"cant-sys-prose": prose_val, "cant-sys-poetic": poetic_val}


def get_cantsys_from_is_poetcant(is_poetcant):
    return "cant-sys-poetic" if is_poetcant else "cant-sys-prose"
