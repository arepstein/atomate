# coding: utf-8

from __future__ import division, print_function, unicode_literals, absolute_import

# This module defines firetasks for writing QChem input files

import os

from atomate.utils.utils import load_class
from fireworks import FiretaskBase, explicit_serialize
from pymatgen.core.structure import Molecule

__author__ = "Brandon Wood"
__copyright__ = "Copyright 2018, The Materials Project"
__version__ = "0.1"
__maintainer__ = "Brandon Wood"
__email__ = "b.wood@berkeley.edu"
__status__ = "Alpha"
__date__ = "5/20/18"
__credits__ = "Sam Blau, Shyam Dwaraknath"


@explicit_serialize
class WriteBasicInput(FiretaskBase):
    """
    CREST only requires one structure file as input.
        """
    # TODO: implement constraints

    # molecule not required because can be inherited from prev_calc_molecule
    required_params = []
    optional_params = ["molecule", "constraints"]

    def run_task(self, fw_spec):
        input_file = os.path.join(self.get("write_to_dir", ""), self.get("input_file", "crest_in.xyz"))
        # these if statements might need to be reordered at some point
        if "molecule" in self:
            molecule = self["molecule"]
        elif fw_spec.get("prev_calc_molecule"):
            molecule = fw_spec.get("prev_calc_molecule")
        else:
            raise KeyError(
                "No molecule present, add as an optional param or check fw_spec"
            )
        molecule.to(fmt='xyz', filename=input_file)
