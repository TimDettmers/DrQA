#!/usr/bin/env python3
# Copyright 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.

import os
from ..tokenizers import CoreNLPTokenizer
from ..retriever import TfidfDocRanker, whoosh_ranker, lucene_ranker#, xapian_ranker
from ..retriever import DocDB
from .. import DATA_DIR

DEFAULTS = {
    'tokenizer': CoreNLPTokenizer,
    #'ranker': TfidfDocRanker,
    #'ranker': whoosh_ranker.WhooshRanker,
    #'ranker': xapian_ranker.XapianRanker,
    'ranker': lucene_ranker.LuceneRanker,
    'db': DocDB,
    'reader_model': os.path.join(DATA_DIR, 'reader/multitask.mdl'),
}


def set_default(key, value):
    global DEFAULTS
    DEFAULTS[key] = value


from .drqa import DrQA
