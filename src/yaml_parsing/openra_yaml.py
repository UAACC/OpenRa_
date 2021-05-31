import yaml

from yaml_parsing.miniyaml_to_yaml_conv import convert_miniyaml_to_yaml
from common.types import Vector2

MP_SPAWN_ACTOR_NAME = "mpspawn"
APPENDED_FIELD_NAME = "MINIYAML_PARENT_IDENTIFIER"


class MapYamlInfo:
    def __init__(self, map_yaml_path):
        map_yaml = _load_and_convert_miniyaml_to_yaml(map_yaml_path)
        spawn_positions, other_actor_data = _extract_spawn_pos_and_actor_data(map_yaml)

        self.global_data = MapYamlGlobal(map_yaml)
        self.actors = other_actor_data
        self.faction_info = _extract_faction_info(map_yaml)
        self.player_start_positions = spawn_positions


class MapYamlGlobal:
    def __init__(self, map_yaml):
        self.map_format = map_yaml["MapFormat"]
        self.requires_mod = map_yaml["RequiresMod"]
        self.title = map_yaml["Title"]
        self.author = map_yaml["Author"]
        self.tileset = map_yaml["Tileset"]
        self.map_size = _extract_location_attrib_from_yaml(map_yaml["MapSize"])
        self.bounds = map_yaml["Bounds"]
        self.visibility = map_yaml["Visibility"]
        self.categories = map_yaml["Categories"]


def _load_and_convert_miniyaml_to_yaml(map_yaml_path):
    with open(map_yaml_path, "r") as f:
        mini_yaml_str = f.read()
        mini_yaml_lines = mini_yaml_str.replace("\t", "    ").split("\n")
        yaml_lines = convert_miniyaml_to_yaml(mini_yaml_lines, 4)
        yaml_str = "\n".join(yaml_lines)

        return yaml.load(yaml_str, Loader=yaml.FullLoader)


def _extract_spawn_pos_and_actor_data(rules_yaml):
    player_spawn_positions = []
    other_actor_yaml = {}

    for actor_name, actor_attribs in rules_yaml["Actors"].items():
        actor_type = actor_attribs[APPENDED_FIELD_NAME]

        if actor_type == MP_SPAWN_ACTOR_NAME:
            spawn_location = _extract_location_attrib_from_yaml(actor_attribs["Location"])
            player_spawn_positions.append(spawn_location)
            continue

        # Otherwise just lump it with the other actors
        other_actor_yaml[actor_name] = actor_attribs

    return player_spawn_positions, other_actor_yaml


def _extract_faction_info(map_yaml):
    return map_yaml["Players"]


def _extract_location_attrib_from_yaml(yaml_line):
    x, y = yaml_line.split(",")
    return Vector2(x, y)
