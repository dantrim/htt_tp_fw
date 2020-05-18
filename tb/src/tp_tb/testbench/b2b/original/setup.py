from setuptools import setup

setup(
    name="tb_b2b",
    version="0.1",
    description="CocoTB testbench for TP B2B block",
    url="https://gitlab.cern.ch/atlas-tdaq-p2-firmware/tdaq-htt-firmware/tp-fw.git",
    author="Daniel Joseph Antrim",
    author_email="daniel.joseph.antrim@cern.ch",
    packages=["tb_b2b"],
    zip_safe=False,
    install_requires=["bitstring", "bitarray", "Columnar", "scipy"],
)
