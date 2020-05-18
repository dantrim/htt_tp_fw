from setuptools import setup, find_packages
import os

# dantrim May 2020:
# This is a hack but it appears to work and I coudln't get anything from
# stackoverflow to work. It also does not help that the package is camelcased
# (fun fact: Unix filesystem is case-insensitive!)
# and matches in name with an existing package on PyPi...
system_sim_path = "https://:@gitlab.cern.ch:8443/atlas-tdaq-p2-firmware/tdaq-htt-firmware/system-simulation.git"
system_sim_branch = "python3_import"
os.system("pip install git+{}@{}".format(system_sim_path, system_sim_branch))

setup(
    name="tp_tb",
    version="0.1",
    description="",
    long_description="",
    url="",
    author="Daniel Joseph Antrim",
    author_email="daniel.joseph.antrim@cern.ch",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    include_package_data=True,
    python_requires=">=3.6",
    install_requires=[
        "cocotb",
        "pre-commit",
        "flake8",
        "black",
        "colorama",
        "columnar",
        "numpy",
        "Click>=6.0",
        "bitstring",
        "scipy",
        "jsonschema",
    ],
    entry_points={"console_scripts": ["tb=tp_tb.cli:cli"]},
)
