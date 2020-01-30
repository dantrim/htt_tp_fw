# This enables the 'tptest' cocotb package
# to be installed into a virtual environment.
# Ben Rosser <bjr@sas.upenn.edu>

from setuptools import setup

setup(name='tptest',
      version='0.1',
      description='Cocotb Testbench for the TP',
      url='https://gitlab.cern.ch/atlas-tdaq-ph2upgrades/atlas-tdaq-htt/tdaq-htt-firmware/tp-fw',
      author='Ben Rosser',
      author_email='bjr@sas.upenn.edu',
      license='MIT',
      packages=['tptest'],
      zip_safe=False)

