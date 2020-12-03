# coding: utf-8

from __future__ import division, print_function, unicode_literals, absolute_import

import os
import unittest

from atomate.xtb.firetasks.write_inputs import WriteBasicInput
from atomate.xtb.firetasks.run_calc import RunCRESTDirect
from atomate.xtb.firetasks.parse_outputs import CRESTToDb
from atomate.xtb.fireworks.core import ConformersFW
from atomate.utils.testing import AtomateTest
from pymatgen.io.xtb.outputs import CRESTOutput

__author__ = "Alex Epstein"
__copyright__ = "Copyright 2018, The Materials Project"
__version__ = "0.1"
__maintainer__ = "Alex Epstein"
__email__ = "aepstein@lbl.gov"
__status__ = "Alpha"
__date__ = ""
__credits__ = "Sam Blau"

module_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)))
db_dir = os.path.join(module_dir, "..", "..", "..", "common", "test_files")


class TestCore(AtomateTest):
    def setUp(self, lpad=False):
        out_path = os.path.join(module_dir, "..", "..", "test_files",
                                "conformer_search")
        crest_out = CRESTOutput(path=out_path, output_filename='crest_out.out')
        self.act_mol = crest_out.input_structure
        super(TestCore, self).setUp(lpad=False)

    def tearDown(self):
        pass

    def test_conformersFW(self):
        firework = ConformersFW(molecule=self.act_mol)
        self.assertEqual(firework.tasks[0].as_dict(),
                         WriteBasicInput(
                             molecule=self.act_mol,
                         ).as_dict())
        self.assertEqual(firework.tasks[1].as_dict(),
                         RunCRESTDirect(
                             crest_cmd="crest",
                             input_file="crest_in.xyz",
                             crest_flags={}
                         ).as_dict())
        self.assertEqual(firework.tasks[2].as_dict(),
                         CRESTToDb(
                             db_file=None,
                             input_file="crest_in.xyz",
                             output_file="crest_out.out",
                             additional_fields={"task_label": 'conformer search'}
                         ).as_dict())
        self.assertEqual(firework.parents, [])
        self.assertEqual(firework.name, "conformer search")


if __name__ == "__main__":
    unittest.main()
