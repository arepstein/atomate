# coding: utf-8

from __future__ import division, print_function, unicode_literals, absolute_import

import os
import unittest
import shutil

try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

from atomate.xtb.firetasks.run_calc import RunCRESTDirect
from atomate.utils.testing import AtomateTest
from pymatgen.io.xtb.outputs import CRESTOutput
import numpy as np

__author__ = "Alex Epstein"
__email__ = "aepstein@lbl.gov"
__credits__ = "Sam Blau"
module_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)))


class TestRunCalcCREST(AtomateTest):
    def setUp(self, lpad=False):
        super(TestRunCalcCREST, self).setUp(lpad=False)

    def tearDown(self):
        pass

    def test_RunCrestDirect_Basic(self):
        with patch("atomate.xtb.firetasks.run_calc.subprocess.call"
                   ) as subprocess_patch:
            firetask = RunCRESTDirect(
                crest_cmd="crest crest_in.xyz -mquick> crest_out.out")
            firetask.run_task(fw_spec={})
            subprocess_patch.assert_called_once()
            self.assertEqual(subprocess_patch.call_args[0][0],
                             "crest crest_in.xyz -mquick> crest_out.out")


    # def test_RunQChemCustodian_using_fw_spec_defaults(self):
    #     with patch("atomate.qchem.firetasks.run_calc.Custodian"
    #                ) as custodian_patch:
    #         firetask = RunQChemCustodian(
    #             qchem_cmd=">>qchem_cmd<<",
    #             scratch_dir=">>scratch_dir<<",
    #             input_file=os.path.join(module_dir, "..", "..", "test_files",
    #                                     "co_qc.in"))
    #         firetask.run_task(
    #             fw_spec={
    #                 "_fw_env": {
    #                     "qchem_cmd": "qchem -slurm",
    #                     "scratch_dir": "/this/is/a/test"
    #                 }
    #             })
    #         custodian_patch.assert_called_once()
    #         self.assertEqual(custodian_patch.call_args[0][0][0].as_dict(),
    #                          QChemErrorHandler(
    #                              input_file=os.path.join(
    #                                  module_dir, "..", "..", "test_files",
    #                                  "co_qc.in"),
    #                              output_file="mol.qout").as_dict())
    #         self.assertEqual(custodian_patch.call_args[0][1][0].as_dict(),
    #                          QCJob(
    #                              qchem_command="qchem -slurm",
    #                              multimode="openmp",
    #                              input_file=os.path.join(
    #                                  module_dir, "..", "..", "test_files",
    #                                  "co_qc.in"),
    #                              output_file="mol.qout",
    #                              scratch_dir="/this/is/a/test").as_dict())
    #         self.assertEqual(custodian_patch.call_args[1], {
    #             "max_errors": 5,
    #             "gzipped_output": True
    #         })

if __name__ == "__main__":
    unittest.main()
