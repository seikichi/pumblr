#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import with_statement
import os
import urllib2

from pumblr.api import *
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


class StubURLOpen(object):
    """Stub for urlopen"""

    def __init__(self, *args, **kw):
        """don't care"""
        pass

    def set_data(self, filename):
        class _Ret(object):
            def __init__(self, data):
                self._data = data

            def read(self, *args, **kw):
                return self._data

        self._ret = _Ret(read_data(filename))

    def __call__(self, *args, **kw):
        return self._ret


def patch_urllib2():
    urllib2._urlopen = urllib2.urlopen
    urllib2.urlopen = StubURLOpen()


def unpatch_urllib2():
    urllib2.urlopen = urllib2._urlopen
    delattr(urllib2, '_urlopen')


@with_setup(patch_urllib2, unpatch_urllib2)
def test_api():
    """test for pumblr/api.py"""
    api = API()
    urllib2.urlopen.set_data('read.json') # fake
    api_read = api.read('seikichi.tumblr.com')
    assert_equal(api_read.tumblelog.description, u'わしの取得単位は108まであるぞ')
