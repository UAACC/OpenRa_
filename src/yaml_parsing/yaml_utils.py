def yaml_line_has_val(line):
    res = line.split(":")
    if len(res) == 1 or res[1] == "":
        return False

    return True


def get_yaml_line_field_name_and_value(line):
    res = line.split(":")
    return res[0], res[1].strip()


def count_spaces_at_start(line):
    return len(line) - len(line.lstrip())


def get_ident_level(line, ident_level):
    return count_spaces_at_start(line) / ident_level
