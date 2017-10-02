#!/usr/bin/env python3
"""Documents, in a redisk database."""
from . import utils
from redisk.core import Redisk, Table


class RediskDB(object):
    def __init__(self, db_name=None):
        self.path = db_name or 'wiki_data'
        self.db = Redisk(Table(self.path))

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.db.close()

    def path(self):
        """Return the path to the file that backs this database."""
        return self.path

    def close(self):
        """Close the connection to the database."""
        self.connection.close()

    def get_doc_ids(self):
        """Fetch all ids of docs stored in the db."""
        return None

    def get_doc_text(self, doc_id):
        """Fetch the raw text of the doc for 'doc_id'."""
        return self.db.get(doc_id)

    def batched_get_doc_text(self, doc_ids):
        """Fetch the raw text of the doc for 'doc_id'."""
        return self.db.batched_get(doc_ids)
