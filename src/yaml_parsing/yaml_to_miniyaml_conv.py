from yaml_parsing.yaml_utils import get_yaml_line_field_name_and_value, yaml_line_has_val
from yaml_parsing.openra_yaml import APPENDED_FIELD_NAME


def convert_yaml_to_miniyaml(mini_yaml):
    i = 0
    end_idx = len(mini_yaml)

    while i < end_idx:

        if _curr_line_is_split_miniyaml_list(mini_yaml[i]):
            # Place value back list start at previous line
            _, split_val = get_yaml_line_field_name_and_value(mini_yaml[i])
            mini_yaml[i - 1] = "{} {}".format(mini_yaml[i - 1], split_val)
            mini_yaml.pop(i)

            end_idx -= 1
            continue

        i += 1

    # This is really yaml by the time we are done
    return mini_yaml


def _curr_line_is_split_miniyaml_list(line):
    if yaml_line_has_val(line):
        field_name, _ = get_yaml_line_field_name_and_value(line)
        print("IN: {}".format(line))
        return field_name == APPENDED_FIELD_NAME

    return False
