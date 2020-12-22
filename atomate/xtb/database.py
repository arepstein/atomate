# coding: utf-8

from __future__ import division, print_function, unicode_literals, absolute_import

# This module defines the database classes.

from atomate.utils.database import CalcDb
from atomate.utils.utils import get_logger

__author__ = "Alex Epstein"
__credits__ = "Sam Blau, Brandon Wood"
__email__ = "aepstein@lbl.gov"

logger = get_logger(__name__)


class CRESTCalcDb(CalcDb):
    """
    Class to help manage database insertions of CREST drones
    """

    def __init__(self,
                 host="localhost",
                 port=27017,
                 database="CREST",
                 collection="tasks",
                 user=None,
                 password=None,
                 **kwargs):
        super(CRESTCalcDb, self).__init__(host, port, database, collection,
                                          user, password, **kwargs)

    def build_indexes(self, indexes=None, background=True):
        """
        Build the indexes.

        Args:
            indexes (list): list of single field indexes to be built.
            background (bool): Run in the background or not.

        TODO: make sure that the index building is sensible and check for
            existing indexes.
        """
        _indices = indexes or [
            "formula_pretty", "formula_anonymous", "dir_name", "smiles",
            "last_updated"
        ]
        self.collection.create_index(
            "task_id", unique=True, background=background)
        # build single field indexes
        for ii in _indices:
            self.collection.create_index(ii, background=background)
        # TODO: build compound indexes

    def reset(self):
        self.collection.delete_many({})
        self.db.counter.delete_one({"_id": "taskid"})
        self.db.counter.insert_one({"_id": "taskid", "c": 0})
        self.build_indexes()
