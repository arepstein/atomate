# coding: utf-8

from __future__ import division, print_function, unicode_literals, absolute_import

# This module defines tasks that support running QChem in various ways.


import shutil
import os
import subprocess
from pymatgen.io.qchem.inputs import QCInput

from fireworks import explicit_serialize, FiretaskBase

from atomate.utils.utils import env_chk, get_logger
import numpy as np

__author__ = "Alex Epstein"
__copyright__ = "Copyright 2020, The Materials Project"
__version__ = "0.1"
__maintainer__ = "Alex Epstein"
__email__ = "aepstein@lbl.gov"
__status__ = "Alpha"
__date__ = ""
__credits__ = "Ryan Kingsbury"

logger = get_logger(__name__)


@explicit_serialize
class RunCRESTDirect(FiretaskBase):
    """
    Execute a command directly (no custodian).

    Required params:
        crest_cmd (str): The name of the full command line call to run.

    Optional params:
        charge (int): The total charge of the structure
        uhf (int): N_alpha - N_Beta for unrestricted Hartree Fock calculations
        gbsa (str): The name of the gbsa solvent
        speed (str): Methods for a crude conformer search: norotmd, quick, squick, -mquick
    """

    required_params = ["crest_cmd"]
    optional_params = ["input_file", "output_file", "crest_flags"]

    def run_task(self, fw_spec):
        cmd = env_chk(self["crest_cmd"], fw_spec)
        input_file = self.get("input_file", "crest_in.xyz")
        output_file = self.get("output_file", "crest_out.out")
        crest_flags = self.get("crest_flags", "")
        full_cmd = cmd + " " + input_file + " " + crest_flags + ">" + output_file

        logger.info("Running command: {}".format(full_cmd))
        return_code = subprocess.call(full_cmd, shell=True)
        logger.info("Command {} finished running with return code: {}".format(
            full_cmd, return_code))


@explicit_serialize
class RunNoCREST(FiretaskBase):
    """
    Do NOT run CREST. Do nothing.
    """

    def run_task(self, fw_spec):
        pass
