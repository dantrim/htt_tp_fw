from pathlib import Path
import json
import struct
from jsonschema import validate

from cocotb import binary

from tp_tb.utils import events

# from tp_tb.utils import
from DataFormat import DataFormat, BitField


def transaction_to_data_word(transaction):

    # at this point "transaction" is a 65-bit word with the MSB the meta-flag,
    # so we have 9-bytes (72-bits) per data word

    transaction = int(transaction)

    endian = "little"  # hard-code, not sure this is ever going to change
    fmt = {"little": "<Q?", "big": ">?Q"}[endian]
    data = transaction.to_bytes(9, endian)
    contents, is_metadata = struct.unpack(fmt, data)
    word = events.DataWord(contents, is_metadata)
    return word


def l0id_from_data_word(data_word):
    if data_word.is_start_of_event():
        header = DataFormat.BitFieldWordValue(DataFormat.EVT_HDR1, data_word.contents)
        l0id = header.getField("L0ID")
        return l0id
    return None


# taken from: https://gitlab.cern.ch/atlas-tdaq-p2-firmware/tdaq-htt-firmware/tp-fw/-/blob/master/tb/tptest/tptest/util.py
class BinaryValue(binary.BinaryValue):
    def __init__(
        self,
        value=None,
        n_bits=None,
        bigEndian=False,
        binaryRepresentation=binary.BinaryRepresentation.UNSIGNED,
        bits=None,
    ):
        super().__init__(
            value,
            n_bits=n_bits,
            bigEndian=bigEndian,
            binaryRepresentation=binaryRepresentation,
            bits=bits,
        )


def validate_against_schema(instance, schema_type):
    """
    Validate the input \"instance\" against a known schema type.

    inputs:
        instance -> (str, dict): The JSON instance to be validated (can be a python dictionary or a string representing a path to afile
        schema_type -> str: A known schema type (see allowed_schema_types())

    returns:
        bool -> True: valid, False: invalid
    """

    instance_data = instance
    if isinstance(instance, str):
        # assume it is a filepath
        p_instance = Path(instance)
        path_ok = p_instance.is_file() and p_instance.exists()
        if not path_ok:
            raise Exception(
                "Could not find path to instance file provided (={instance})"
            )
        if p_instance.is_file() and p_instance.exists():
            with open(instance, "r") as infile:
                instance_data = json.load(infile)

    schema_file = get_schema_file(schema_type=schema_type)
    if schema_file is None:
        raise Exception(f"Could not find schema file of type={schema_type}")

    with open(schema_file, "r") as infile:
        schema_data = json.load(infile)

    try:
        validate(instance=instance_data, schema=schema_data)
    except Exception as ex:
        return False, f"Provided JSON instance fails schema check:\n{ex}"
    return True, None


def allowed_schema_types():

    all_schema_files = get_schema_files()
    allowed_types = []
    for sf in all_schema_files:
        sf = str(sf).split("/")[-1]
        sf = sf.replace(".json", "")
        sf = sf.replace("schema_", "")
        allowed_types.append(sf)
    return allowed_types


def tp_fw_path():

    cwd = Path.cwd()
    for p in cwd.parents:
        if str(p.parts[-1]).replace("-", "_") == "tp_fw":
            if p.exists():
                return p
    return None


def tb_test_config_directory():

    p_tp_fw = tp_fw_path()
    if not p_tp_fw:
        return None

    p_config = p_tp_fw / "tb" / "test_config"
    if p_config.exists():
        return p_config
    else:
        return None


def tb_schema_directory():

    p_tp_fw = tp_fw_path()
    if not p_tp_fw:
        return None

    p_schema = p_tp_fw / "tb" / "schema"
    if p_schema.exists():
        return p_schema
    else:
        return None


def get_schema_file(schema_type=""):

    if schema_type not in allowed_schema_types():
        print(
            f"ERROR Invalid schema_type (={schema_type}) provided, allowed ones are: {allowed_schema_types()}"
        )
        return None

    found_schema = []
    for schema_file in get_schema_files():
        if schema_type in str(schema_file).split("/")[-1]:
            found_schema.append(schema_file)
    if len(found_schema) != 1:
        print(
            f'ERROR Found invalid number of schema files of type "{schema_type}", found {len(found_schema)}: {found_schema}'
        )
        return None
    return found_schema[0]


def get_schema_files():

    p_schema = tb_schema_directory()
    schema_files = list(p_schema.glob("schema*.json"))
    return schema_files
