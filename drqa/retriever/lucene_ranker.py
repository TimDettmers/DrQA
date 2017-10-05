#!/usr/bin/env python3
"""Rank documents with TF-IDF via xapian"""

import logging
import numpy as np
import scipy.sparse as sp
import time
import uuid

from multiprocessing.pool import ThreadPool
from functools import partial

from . import utils
from . import DEFAULTS
from .. import tokenizers

logger = logging.getLogger(__name__)

import lucene
from java.nio.file import Paths
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.index import IndexReader, DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import SimpleFSDirectory


class LuceneRanker(object):
    def __init__(self, tfidf_path, strict=True):
        lucene.initVM()
        analyzer = StandardAnalyzer()
        reader = DirectoryReader.open(SimpleFSDirectory(Paths.get(tfidf_path)))
        self.searcher = IndexSearcher(reader)

        self.parser = QueryParser("text", analyzer)
        self.parser.setDefaultOperator(QueryParser.Operator.OR)

    def closest_docs(self, query, k=1):
        """Closest docs by dot product between query and documents
        in tfidf weighted word vector space.
        """
        query = self.parser.parse(query.replace('/', '//').replace('?', '').replace('"', ''))
        hits = self.searcher.search(query, k)
        docids = []
        docs = []
        for i, hit in enumerate(hits.scoreDocs):
            doc = self.searcher.doc(hit.doc)
            docs.append(unicode(doc['text']))
            docids.append(unicode(doc['title']))
        return docids, docs

    def batch_closest_docs(self, queries, k=1, num_workers=None):
        """Process a batch of closest_docs requests multithreaded."""
        # get highest scoring document for multiple queries
        batch = []
        for i, q in enumerate(queries):
            if i % 100 == 0:
                print(i)

            t0 = time.time()
            docids, docs = self.closest_docs(q, k)
            batch.append((docids, docs))
        return batch

    def parse(self, query): return None
    def text2spvec(self, query): return None
    def get_doc_index(self, doc_id): return 0
    def get_doc_id(self, doc_index): return 0
    def __exit__(self, *args):
        pass
