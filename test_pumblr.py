#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import with_statement
import os

from pumblr.models import *
from pumblr.utils import *
from nose.tools import *

json = import_json()


def read_data(filename):
    """return the data of testdata/${filename}"""
    filename = os.path.join(os.path.dirname(__file__), 'testdata', filename)
    with open(filename) as f:
        return f.read()


def test_models():
    """test for pumblr/models.py"""
    data = json.loads(extract_dict(read_data('read.json')))
    api_read = ApiRead.parse(data)
    assert_equal(api_read.tumblelog.description, u'わしの取得単位は108まであるぞ')
