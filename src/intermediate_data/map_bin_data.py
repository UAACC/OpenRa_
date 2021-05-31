from common.types import Vector2


class MapBinData:
    BYTES_PER_TILE = 3
    BYTES_PER_RESOURCE = 2

    def __init__(self, header, data_blocks):
        self.header = header
        self.data_blocks = data_blocks


class Header:
    def __init__(self, tile_format, map_size, block_offsets):
        self.tile_format = tile_format
        self.map_size = map_size
        self.block_offsets = block_offsets


class DataBlocks:
    def __init__(self, tiles, resources):
        self.tiles = tiles
        self.resources = resources


class BlockOffsets:
    def __init__(self, tiles_offset, resources_offset):
        self.tiles_offset = tiles_offset
        self.resources_offset = resources_offset


def load_map_binary_data(bin_data_path):
    f = open(bin_data_path, "rb")

    tile_format = _read_int_bytes_from_file(f, 1)
    map_x = _read_int_bytes_from_file(f, 2)
    map_y = _read_int_bytes_from_file(f, 2)

    tiles_offset = _read_int_bytes_from_file(f, 4, signed=False)
    resources_offset = _read_int_bytes_from_file(f, 4, signed=False)

    block_elems = map_x * map_y

    tile_bytes = _read_block_at_offset(f, tiles_offset, block_elems * MapBinData.BYTES_PER_TILE)
    resources_bytes = _read_block_at_offset(f, resources_offset, block_elems * MapBinData.BYTES_PER_RESOURCE)

    offsets = BlockOffsets(tiles_offset, resources_offset)
    header = Header(tile_format, Vector2(map_x, map_y), offsets)
    blocks = DataBlocks(tile_bytes, resources_bytes)

    return MapBinData(header, blocks)


def _read_block_at_offset(fin, offset, num_bytes):
    fin.seek(offset)
    return fin.read(num_bytes)


def _read_int_bytes_from_file(fin, num_bytes, signed=True):
    return int.from_bytes(fin.read(num_bytes), "little", signed=signed)
