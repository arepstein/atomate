# coding: utf-8

from __future__ import division, print_function, unicode_literals, absolute_import

import os
import unittest

from fireworks import FWorker
from fireworks.core.rocket_launcher import rapidfire
from atomate.utils.testing import AtomateTest
from pymatgen.core import Molecule
from atomate.xtb.workflows.base.conformer_search import get_wf_simpleConformerSearch

__author__ = "Alex Epstein"
__copyright__ = "Copyright 2018, The Materials Project"
__version__ = "0.1"
__maintainer__ = "Alex Epstein"
__email__ = "aepstein@lbl.gov"
__status__ = "Alpha"
__date__ = "6/1/18"
__credits__ = "Sam Blau"

module_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)))
db_dir = os.path.join(module_dir, "..", "..", "..", "common", "test_files")


class TestSimpleConformerSearch(AtomateTest):
    def test_simple_conformer_search(self):
        # location of test files
        test_csearch_files = os.path.join(module_dir, "..", "..",
                                            "test_files", "conformer_search")
        # define starting molecule
        initial_mol = Molecule.from_file(os.path.join(test_csearch_files, "crest_in.xyz"))

        real_wf = get_wf_simpleConformerSearch(
            molecule=initial_mol
            )
        # use powerup to replace run with fake run
        ref_dirs = {
            "first_FF_no_pcm":
                os.path.join(test_double_FF_files, "block", "launcher_first"),
            "second_FF_with_pcm":
                os.path.join(test_double_FF_files, "block", "launcher_second")
        }
        fake_wf = use_fake_qchem(real_wf, ref_dirs)
        self.lp.add_wf(fake_wf)
        rapidfire(
            self.lp,
            fworker=FWorker(env={"db_file": os.path.join(db_dir, "db.json")}))

        wf_test = self.lp.get_wf_by_fw_id(1)
        self.assertTrue(
            all([s == "COMPLETED" for s in wf_test.fw_states.values()]))

        first_FF = self.get_task_collection().find_one({
            "task_label":
                "first_FF_no_pcm"
        })
        self.assertEqual(first_FF["calcs_reversed"][0]["input"]["solvent"],
                         None)
        self.assertEqual(first_FF["num_frequencies_flattened"], 1)
        first_FF_final_mol = Molecule.from_dict(
            first_FF["output"]["optimized_molecule"])

        second_FF = self.get_task_collection().find_one({
            "task_label":
                "second_FF_with_pcm"
        })
        self.assertEqual(second_FF["calcs_reversed"][0]["input"]["solvent"],
                         {"dielectric": "10.0"})
        self.assertEqual(second_FF["num_frequencies_flattened"], 1)
        second_FF_initial_mol = Molecule.from_dict(
            second_FF["input"]["initial_molecule"])

        self.assertEqual(first_FF_final_mol, second_FF_initial_mol)


if __name__ == "__main__":
    unittest.main()
