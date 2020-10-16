# coding: utf-8

from __future__ import absolute_import, division, print_function, \
    unicode_literals

from fireworks import Workflow
from atomate.xtb.fireworks.core import conformersFW
from atomate.utils.utils import get_logger

__author__ = "Alex Epstein"
__copyright__ = "Copyright 2018, The Materials Project"
__version__ = "0.1"
__maintainer__ = "Alex Epstein "
__email__ = "aepstein@lbl.gov"
__status__ = "Alpha"
__date__ = "5/23/18"
__credits__ = "Sam Blau"

logger = get_logger(__name__)


def get_wf_simpleConformerSearch(molecule,
                         name="simple_conf_search",
                         crest_cmd=">>crest_cmd<<",
                         db_file=">>db_file<<",
                         **kwargs):
    """
    Returns a workflow to the torsion potential for a molecule.

    Firework 1 : run CREST conformer search conformerFW
                 parse directory and insert into db,

    Args:
        molecule (Molecule): input molecule to be optimized and run.
        crest_cmd (str): Command to run CREST.
        db_file (str): path to file containing the database credentials.
        kwargs (keyword arguments): additional kwargs to be passed to Workflow

    Returns:
        Workflow
    """

    # Optimize the molecule in vacuum
    fw1 = conformersFW(
        molecule=molecule,
        name="simple_conformer_search",
        crest_cmd=crest_cmd,
        db_file=db_file)

    # Optimize the molecule in PCM

    wfname = "{}:{}".format(molecule.composition.reduced_formula, name)

    return Workflow([fw1], name=wfname, **kwargs)
