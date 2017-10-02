#!/usr/bin/env python3
"""Rank documents with TF-IDF via xapian"""

import logging
import numpy as np
import scipy.sparse as sp
import time
import xapian

from multiprocessing.pool import ThreadPool
from functools import partial

from . import utils
from . import DEFAULTS
from .. import tokenizers

logger = logging.getLogger(__name__)

class XapianRanker(object):
    def __init__(self, tfidf_path, strict=True):
        self.db = xapian.Database(tfidf_path)

        queryparser = xapian.QueryParser()
        queryparser.set_stemmer(xapian.Stem("en"))
        queryparser.set_stemming_strategy(queryparser.STEM_SOME)
        # Start of prefix configuration.
        queryparser.add_prefix("title", "S")
        queryparser.add_prefix("description", "XD")

        self.queryparser = queryparser
        self.enquire = xapian.Enquire(self.db)

    def closest_docs(self, query, k=1):
        """Closest docs by dot product between query and documents
        in tfidf weighted word vector space.
        """
        query = self.queryparser.parse_query(str(query))
        self.enquire.set_query(query)
        matches = []
        #t0 =time.time()
        offset = 0
        pagesize = k
        docids = []
        docs = []
        for i, match in enumerate(self.enquire.get_mset(offset, pagesize)):
            text = match.document.get_data()
            docs.append(text.lower())
            docids.append(unicode(str(match.docid)))
        #print(time.time() - t0)
        return docids, docs

    def batch_closest_docs(self, queries, k=1, num_workers=None):
        """Process a batch of closest_docs requests multithreaded."""
        # get highest scoring document for multiple queries
        batch = []
        for i, q in enumerate(queries):
            if i % 100 == 0:
                print(i)
            docids, docs = self.closest_docs(q, k)
            batch.append((docids, docs))
        #print(len(batch))
        return batch

    def parse(self, query): return None
    def text2spvec(self, query): return None
    def get_doc_index(self, doc_id): return 0
    def get_doc_id(self, doc_index): return 0
    def __exit__(self, *args):
        pass
