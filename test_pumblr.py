#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import with_statement
import os
import urllib2

from pumblr.api import *
from pumblr.errors import *
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
        self._error = False

    def set_data(self, filename):
        class _Ret(object):
            def __init__(self, data):
                self._data = data

            def read(self, *args, **kw):
                return self._data

        self._ret = _Ret(read_data(filename))

    def set_error_code(self, code):
        self._error = True
        self._code = code

    def __call__(self, *args, **kw):
        if self._error:
            raise urllib2.HTTPError('', self._code, '', None, None)
        return self._ret


def patch_urllib2():
    urllib2._urlopen = urllib2.urlopen
    urllib2.urlopen = StubURLOpen()


def unpatch_urllib2():
    urllib2.urlopen = urllib2._urlopen
    delattr(urllib2, '_urlopen')


@with_setup(patch_urllib2, unpatch_urllib2)
def test_api_read():
    """test for pumblr/api.py"""
    api = API()
    urllib2.urlopen.set_data('read.json') # fake
    api_read = api.read('seikichi')
    assert_equal(api_read.tumblelog.description, u'わしの取得単位は108まであるぞ')

    urllib2.urlopen.set_data('dashboard.json')
    api.auth(email='seikichi@localhost', password='password') # ;-p
    dashboard = api.dashboard()
    assert_equal(dashboard.posts[0].id, 1104344180)

    urllib2.urlopen.set_data('error.xhtml')
    assert_raises(PumblrError, api.dashboard)


@with_setup(patch_urllib2, unpatch_urllib2)
def test_api_auth():
    api = API()
    assert_raises(PumblrError, api.dashboard)
    assert_raises(PumblrError, api.like, 0, 0)
    assert_raises(PumblrError, api.unlike, 0, 0)
    assert_raises(PumblrError, api.reblog, 0, 0)
    assert_raises(PumblrError, api.write_quote, {'quote':'hoge'})
    assert_raises(PumblrError, api.write_regular, {'title':'hoge', 'body':'fuga'})
    assert_raises(PumblrError, api.write_link, {'url':'http://localhost', 'name':'見ろ人がゴミのようだ', 'description':'うおー'})


@with_setup(patch_urllib2, unpatch_urllib2)
def test_error_code():
    api = API()
    urllib2.urlopen.set_data('dashboard.json') # dummy
    api.auth(email='seikichi@localhost', password='password') # ;-p
    urllib2.urlopen.set_error_code(403)
    assert_raises(PumblrAuthError, api.like, 0, 0)
    urllib2.urlopen.set_error_code(400)
    assert_raises(PumblrRequestError, api.like, 0, 0)
    urllib2.urlopen.set_error_code(403)
    assert_raises(PumblrAuthError, api.unlike, 0, 0)
    urllib2.urlopen.set_error_code(400)
    assert_raises(PumblrRequestError, api.unlike, 0, 0)
    urllib2.urlopen.set_error_code(404)
    assert_raises(PumblrError, api.reblog, 0, 0)


@with_setup(patch_urllib2, unpatch_urllib2)
def test_api_delete():
    api = API()
    urllib2.urlopen.set_data('dashboard.json') # dummy
    api.auth(email='seikichi@localhost', password='password') # ;-p
    urllib2.urlopen.set_error_code(201)
    api.delete(123456789)


@with_setup(patch_urllib2, unpatch_urllib2)
def test_api_write():
    api = API()
    urllib2.urlopen.set_data('dashboard.json') # dummy
    api.auth(email='seikichi@localhost', password='password') # ;-p

    urllib2.urlopen.set_error_code(201)
    api.write_quote(quote='ほげふがー', source='pyo------')
    api.write_regular(title='みょーーん', body='はいはいワロスワロス')
    api.write_quote(quote='hoge')
    api.write_regular(title='hoge', body='fuga')
    api.write_link(url='http://localhost', name='見ろ人がゴミのようだ', description='うおー')
    api.write_conversation(conversation='うおー', title='書くの飽きてきた')
    api.write_audio(externally_hosted_url='書く意味あるのかなーと思わんでもない', caption='壁殴り代行始めました')
    api.write_video(embed='<object width="640" height="385"><param name="movie" value="http://www.youtube.com/v/Pqisib2bAb8?fs=1&amp;hl=ja_JP"></param><param name="allowFullScreen" value="true"></param><param name="allowscriptaccess" value="always"></param><embed src="http://www.youtube.com/v/Pqisib2bAb8?fs=1&amp;hl=ja_JP" type="application/x-shockwave-flash" allowscriptaccess="always" allowfullscreen="true" width="640" height="385"></embed></object>', caption='あらぶるてんしんらんまんの何とか')
