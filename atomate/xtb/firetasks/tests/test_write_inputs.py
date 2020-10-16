# coding: utf-8

from __future__ import division, print_function, unicode_literals, absolute_import

import os
import unittest
import shutil

from atomate.xtb.firetasks.write_inputs import WriteBasicInput
from atomate.utils.testing import AtomateTest
from pymatgen.core import Molecule

__author__ = "Alex Epstein "
__email__ = "aepstein@lbl.gov"

module_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)))


class TestWriteInputCREST(AtomateTest):
    @classmethod
    def setUpClass(cls):

        cls.crest_in = Molecule.from_file(
            os.path.join(module_dir, "..", "..", "test_files", "crest_in.xyz"))

    def setUp(self, lpad=False):
        super(TestWriteInputCREST, self).setUp(lpad=False)

    def tearDown(self):
        shutil.rmtree(self.scratch_dir)
        for x in ["crest_in.xyz"]:
            if os.path.exists(os.path.join(module_dir, x)):
                os.remove(os.path.join(module_dir, x))

    def test_write_basic_input(self):
        ft = WriteBasicInput(
            molecule=self.crest_in)
        ft.run_task({})
        test_mol = Molecule.from_file("mol.xyz")
        self.assertEqual(self.crest_in, test_mol)


if __name__ == "__main__":
    unittest.main()
