# coding: utf-8

from __future__ import absolute_import, division, print_function, \
    unicode_literals

# Defines standardized Fireworks that can be chained easily to perform various
# sequences of QChem calculations.


from fireworks import Firework

from atomate.xtb.firetasks.parse_outputs import *
from atomate.xtb.firetasks.run_calc import *
from atomate.xtb.firetasks.write_inputs import *

__author__ = "Samuel Blau"
__copyright__ = "Copyright 2018, The Materials Project"
__version__ = "0.1"
__maintainer__ = "Samuel Blau"
__email__ = "samblau1@gmail.com"
__status__ = "Alpha"
__date__ = "5/23/18"
__credits__ = "Brandon Wood, Shyam Dwaraknath"


class ConformersFW(Firework):
    def __init__(self,
                 molecule=None,
                 name="conformer search",
                 crest_cmd="crest",
                 input_file="crest_in.xyz",
                 output_file="crest_out.out",
                 crest_flags=None,
                 db_file=None,
                 parents=None,
                 **kwargs):
        """
        Optimize the given structure.

        Args:
            molecule (Molecule): Input molecule.
            name (str): Name for the Firework.
            crest_cmd (str): Command to run QChem. Defaults to qchem.
            input_file (str): Name of the QChem input file. Defaults to mol.qin.
            crest_flags (dict): Specify kwargs for instantiating the input set parameters.
                                       For example, if you want to change
                                       the solvent to water, you should
                                       provide: {"gbsa": "H2O"}. Defaults to
                                       None.
            db_file (str): Path to file specifying db credentials to place output parsing.
            parents ([Firework]): Parents of this particular Firework.
            **kwargs: Other kwargs that are passed to Firework.__init__.
        """

        crest_flags = crest_flags or {}
        if molecule.charge != 0:
            crest_flags["c"] = molecule.charge

        t = []
        t.append(
            WriteBasicInput(
                molecule=molecule,
            )
        )
        t.append(
            RunCRESTDirect(
                crest_cmd=crest_cmd,
                input_file=input_file,
                crest_flags=crest_flags,
                output_file=output_file
            )
        )
        t.append(
            CRESTToDb(
                db_file=db_file,
                input_file=input_file,
                output_file=output_file,
                additional_fields={"task_label": name}))
        super(ConformersFW, self).__init__(
            t,
            parents=parents,
            name=name,
            **kwargs)


class CRESTtoQChemFW(Firework):
    def __init__(self,
                 molecule=None,
                 name="crest_to_qchem",
                 crest_cmd=">>crest_cmd<<",
                 input_file="crest_in.xyz",
                 output_file="crest_out.out",
                 crest_flags=None,
                 db_file=None,
                 parents=None,
                 **kwargs):
        """
        Optimize the given structure.

        Args:
            molecule (Molecule): Input molecule.
            name (str): Name for the Firework.
            crest_cmd (str): Command to run QChem. Defaults to qchem.
            input_file (str): Name of the QChem input file. Defaults to mol.qin.
            crest_flags (dict): Specify kwargs for instantiating the input set parameters.
                                       For example, if you want to change
                                       the solvent to water, you should
                                       provide: {"gbsa": "H2O"}. Defaults to
                                       None.
            db_file (str): Path to file specifying db credentials to place output parsing.
            parents ([Firework]): Parents of this particular Firework.
            **kwargs: Other kwargs that are passed to Firework.__init__.
        """

        crest_flags = crest_flags or {}
        if molecule.charge != 0:
            crest_flags["c"] = molecule.charge

        t = []
        t.append(
            WriteBasicInput(
                molecule=molecule,
            )
        )
        t.append(
            RunCRESTDirect(
                crest_cmd=crest_cmd,
                input_file=input_file,
                crest_flags=crest_flags,
                output_file=output_file
            )
        )
        t.append(
            CRESTToDb(
                db_file=db_file,
                input_file=input_file,
                output_file=output_file,
                spawn_qchem_max=5,
                additional_fields={"task_label": name}))

        super(CRESTtoQChemFW, self).__init__(
            t,
            parents=parents,
            name=name,
            **kwargs)
