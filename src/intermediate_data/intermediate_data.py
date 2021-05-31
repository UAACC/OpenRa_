from glob import glob
import os.path
import warnings

from yaml_parsing.openra_yaml import MapYamlInfo
from map_bin_data import MapBinData, load_map_binary_data


class IntermediateData:
    def __init__(self, bin_data, map_yaml_data):
        self.bin_data = bin_data
        self.map_yaml_data = map_yaml_data

    def __repr__(self):
        # Decided to just lump all of the printing stuff here to unclutter the rest of the codebase

        out = []

        out.append("Bin Data:")
        out.append("tile format: {}".format(self.bin_data.header.tile_format))
        out.append("map size: {}".format(self.bin_data.header.map_size))

        out.append("tiles_offset: {}".format(self.bin_data.header.block_offsets.tiles_offset))
        out.append("resources_offset: {}".format(self.bin_data.header.block_offsets.resources_offset))

        out.append("Num tiles: {}".format(len(self.bin_data.data_blocks.tiles) / MapBinData.BYTES_PER_TILE))
        out.append("Num resources: {}".format(len(self.bin_data.data_blocks.resources) / MapBinData.BYTES_PER_RESOURCE))

        out.append("\nMap Yaml:")
        out.append("Actor info: {}".format(self.map_yaml_data.actors))
        out.append("\nFaction Info: {}".format(self.map_yaml_data.faction_info))
        out.append("\nSpawn positions: {}".format(self.map_yaml_data.player_start_positions))
        out.append("\nGlobal data: {}".format(self.map_yaml_data.global_data.__dict__))

        return "\n".join(out)

    def create_inter_data_from_map(self, map_dir):
        bin_path = glob("{}/*.bin".format(map_dir))[0]
        map_yaml_data_path = "{}/map.yaml".format(map_dir)

        if os.path.isfile(map_yaml_data_path):
            map_yaml_data = MapYamlInfo(map_yaml_data_path)
        else:
            warnings.warn('No map.yaml found for map "{}"! (Is this a multiplayer map?)')
            map_yaml_data = None

        bin_data = load_map_binary_data(bin_path)

        return IntermediateData(bin_data, map_yaml_data)

    def convert_to_openra_map(self, map_dir):
        pass
