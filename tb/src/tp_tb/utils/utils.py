from pathlib import Path

from cocotb import binary


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


def allowed_schema_types():

    return ["test_config", "test_results_summary"]


def tp_fw_path():

    cwd = Path.cwd()
    for p in cwd.parents:
        if str(p.parts[-1]).replace("-", "_") == "tp_fw":
            if p.exists():
                return p
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
