from yaml_utils import (
    get_ident_level,
    get_yaml_line_field_name_and_value,
    yaml_line_has_val,
)
from yaml_parsing import APPENDED_FIELD_NAME


def convert_miniyaml_to_yaml(mini_yaml, spaces_per_indent):
    return _convert_miniyaml_lists_to_yaml(mini_yaml, 0, len(mini_yaml) - 1, spaces_per_indent)


def _convert_miniyaml_lists_to_yaml(mini_yaml, start_idx, end_idx, spaces_per_indent):
    i = start_idx

    while i < end_idx:
        curr_indent_level = get_ident_level(mini_yaml[i], spaces_per_indent)

        if _curr_line_is_mini_yaml_list(mini_yaml[i], mini_yaml[i + 1], curr_indent_level, spaces_per_indent):
            spaces_for_next_indent_level = int(spaces_per_indent * (curr_indent_level + 1))
            field_name, field_val = get_yaml_line_field_name_and_value(mini_yaml[i])
            mini_yaml[i] = "{}:".format(field_name)
            mini_yaml.insert(
                i + 1,
                "{}{}: {}".format(" " * spaces_for_next_indent_level, APPENDED_FIELD_NAME, field_val),
            )
            i += 1
            end_idx += 1

        i += 1

    return mini_yaml


def _curr_line_is_mini_yaml_list(curr_line, next_line, curr_ident_level, spaces_per_indent):
    next_line_indent_level = get_ident_level(next_line, spaces_per_indent)

    if curr_ident_level >= next_line_indent_level:
        return False

    # The current line has children. Is it using the special MiniYaml format?
    return yaml_line_has_val(curr_line)
