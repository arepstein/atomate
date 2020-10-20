# coding: utf-8

from __future__ import division, print_function, unicode_literals, absolute_import

import os
from fnmatch import fnmatch
from collections import OrderedDict
import traceback
from itertools import chain

from monty.json import jsanitize
from pymatgen.io.xtb.outputs import CRESTOutput
from pymatgen.core.structure import Molecule
from pymatgen.apps.borg.hive import AbstractDrone

from atomate.utils.utils import get_logger
from atomate import __version__ as atomate_version

__author__ = "Alex Epstein"
__copyright__ = "Copyright 2018, The Materials Project"
__version__ = "0.1"
__maintainer__ = "Alex Epstein"
__email__ = "aepstein@lbl.gov"
__status__ = "Alpha"
__date__ = "10/01/19"
__credits__ = "Sam Blau, Ryan Kingsbury, Evan Spotte-Smith"

logger = get_logger(__name__)


class CRESTDrone(AbstractDrone):
    """
    A CREST drone to parse CREST calculations and insert an organized, searchable entry into the database.
    """

    __version__ = atomate_version  # note: the version is inserted into the task doc

    # Schema def of important keys and sub-keys; used in validation
    # I haven't worried about this yet
    schema = {
        "root": {
            "dir_name", "input", "output", "smiles",
            "walltime", "cputime", "formula_pretty", "formula_anonymous",
            "chemsys", "pointgroup"
        },
        "input": {"initial_molecule", "job_type"},
        "output": {"initial_molecule", "job_type"}
    }

    def __init__(self, runs=None, additional_fields=None):
        """
        Initialize a CREST drone to parse CREST calculations
        Args:
            runs (list): Naming scheme for multiple calculations in one folder. Copied from QChemDrone
                for consistency, but will probably never be used for CREST parsing
            additional_fields (dict): dictionary of additional fields to add to output document
        """
        self.runs = runs or list(
            chain.from_iterable([["csearch_" + str(ii)]
                                 for ii in range(9)]))
        self.additional_fields = additional_fields or {}

    def assimilate(self, path, input_file, output_file, multirun=False):
        """
        Parses CREST input and output files and insert the result into the db.

        Args:
            path (str): Path to the directory containing output file
            input_file (str): base name of the input file(s)
            output_file (str): base name of the output file(s)
            multirun (bool): Whether the job to parse includes multiple
                            calculations in one i/o pair. Likely unused here.

        Returns:
            d (dict): a task dictionary
        """
        logger.info("Getting task doc for base dir :{}".format(path))
        crestinput_files = self.filter_files(path, file_pattern=input_file)
        crestoutput_files = self.filter_files(path, file_pattern=output_file)
        if len(crestinput_files) != len(crestoutput_files):
            raise AssertionError("Inequal number of input and output files!")
        if len(crestinput_files) > 0 and len(crestoutput_files) > 0:
            d = self.generate_doc(path, crestinput_files, crestoutput_files,
                                  multirun)
            self.post_process(path, d)
        else:
            raise ValueError("Either input or output not found!")
        self.validate_doc(d)
        return jsanitize(d, strict=True, allow_bson=True)

    def filter_files(self, path, file_pattern):
        """
        Find the files that match the pattern in the given path and
        return them in an ordered dictionary. The searched for files are
        filtered by the run types defined in self.runs.

        Args:
            path (string): path to the folder
            file_pattern (string): base files to be searched for

        Returns:
            OrderedDict of the names of the files to be processed further.
            The key is set from list of run types: self.runs
        """
        processed_files = OrderedDict()
        files = os.listdir(path)
        for r in self.runs:
            # try subfolder schema
            if r in files:
                for f in os.listdir(os.path.join(path, r)):
                    if fnmatch(f, "{}*".format(file_pattern)):
                        processed_files[r] = os.path.join(r, f)
            # try extension schema
            else:
                for f in files:
                    if fnmatch(f, "{}.{}*".format(file_pattern, r)):
                        processed_files[r] = f
        if len(processed_files) == 0:
            # get any matching file from the folder
            for f in files:
                if fnmatch(f, "{}*".format(file_pattern)):
                    processed_files["standard"] = f
        return processed_files

    def generate_doc(self, dir_name, crestinput_files, crestoutput_files, multirun):
        #Deleted a lot of this because assuming only one run
        try:
            fullpath = os.path.abspath(dir_name)
            d = jsanitize(self.additional_fields, strict=True)
            d["schema"] = {
                "code": "atomate",
                "version": CRESTDrone.__version__
            }
            d["dir_name"] = fullpath
            if multirun:
                d["calcs_reversed"] = self.process_crestrun(
                    dir_name, crestinput_files, crestoutput_files)
            else:
                d["calcs_reversed"] = [
                    self.process_crestrun(dir_name, taskname,
                                          crestinput_files.get(taskname),
                                          output_filename)
                    for taskname, output_filename in crestoutput_files.items()
                ]
            d["calcs_reversed"].reverse()
            d_calc_init = d["calcs_reversed"][-1]
            d_calc_final = d["calcs_reversed"][0]
            d["state"] = "successful" if d_calc_final[
                "properly_terminated"] else "unsuccessful"
            return d

        except Exception:
            logger.error(traceback.format_exc())
            logger.error("Error in " + os.path.abspath(dir_name) + ".\n" +
                         traceback.format_exc())
            raise

    @staticmethod
    def process_crestrun(dir_name, taskname, input_file, output_file):
        """
        Process a CREST calculation, aka an input/output pair.
        """
        crest_input_file = os.path.join(dir_name, input_file)
        crest_output_file = os.path.join(dir_name, output_file)
        CO = CRESTOutput(crest_output_file)
        d = {}
        d["input"] = CO.cmd_options
        d["input"]["molecule"] = Molecule.from_file(crest_input_file)
        d["output"] = {}
        d["output"]["lowest_energy_structure"] = CO.lowest_energy_structure
        d["input"]["sorted_structures_energies"] = CO.sorted_structures_energies
        d["task"] = {"type": taskname, "name": taskname}
        return d

    def validate_doc(self, d):
        """
        Sanity check, aka make sure all the important keys are set. Note that a failure
        to pass validation is unfortunately unlikely to be noticed by a user.
        """
        for k, v in self.schema.items():
            diff = v.difference(set(d.get(k, d).keys()))
            if diff:
                logger.warn("The keys {0} in {1} not set".format(diff, k))

    @staticmethod
    def get_valid_paths(self, path):
        return [path]
