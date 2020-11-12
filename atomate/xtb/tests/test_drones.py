# coding: utf-8
# Copyright (c) Materials Virtual Lab.
# Distributed under the terms of the BSD License.

from __future__ import division, print_function, unicode_literals, absolute_import

import os
import unittest
from atomate.xtb.drones import CRESTDrone
import numpy as np

__author__ = "Alex Epstein "
__copyright__ = "Copyright 2018, The Materials Project"
__version__ = "0.1"
__maintainer__ = "Alex Epstein "
__email__ = "aepstein@lbl.gov"
__status__ = "Alpha"
__date__ = "4/29/18"
__credits__ = "Sam Blau"

module_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)))


class CRESTDroneTest(unittest.TestCase):
    def test_assimilate_opt(self):
        drone = CRESTDrone()
        doc = drone.assimilate(
            path=os.path.join(module_dir, "..", "test_files", "conformer_search"),
            input_file="crest_in.xyz",
            output_file="crest_out.out",
            multirun=False)
        self.assertIn("calcs_reversed", doc)
        self.assertIn("initial_molecule", doc["input"])
        self.assertIn("lowest_energy_structure", doc["output"])
        self.assertIn("sorted_structures_energies", doc["output"])
        self.assertIn("state", doc)
        self.assertIn("dir_name", doc)
        self.assertEqual(len(doc["calcs_reversed"]), 1)

if __name__ == "__main__":
    unittest.main()
