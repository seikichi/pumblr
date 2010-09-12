#!/usr/bin/python
# -*- coding: utf-8 -*-

# 実際に通信してテストを行う

from __future__ import with_statement
from getpass import getpass

from pumblr.errors import *
from nose.tools import *


passowrd = ''
mail = ''


def setpass():
    global mail, password
    import sys
    sys.stderr.write('\nMail:')
    mail = raw_input('')
    password = getpass('Password:', sys.stderr)


@with_setup(setpass)
def test_all():
    """実際に通信をしてテストする"""
    import pumblr
    # 認証が必要な関数でエラーが出るか確認
    assert_raises(PumblrError, pumblr.api.dashboard)
    assert_raises(PumblrError, pumblr.api.like, 0, 0)
    assert_raises(PumblrError, pumblr.api.unlike, 0, 0)
    assert_raises(PumblrError, pumblr.api.reblog, 0, 0)

    assert_raises(PumblrAuthError, pumblr.api.auth, mail, '')

    read_data = pumblr.api.read('seikichi', num=3, type='quote')
    assert_equal(len(read_data.posts), 3)
    assert_equal(0, len(filter(lambda p: p.type!='quote', read_data.posts)))

    # 以下認証後のテスト
    pumblr.api.auth(mail, password)

    # dashboard
    dashboard_data = pumblr.api.dashboard(num=10)
    assert_equal(len(dashboard_data.posts), 10)
    dashboard_data = pumblr.api.dashboard(type='photo')
    assert_equal(0, len(filter(lambda p: p.type!='photo', dashboard_data.posts)))

    # reblog
    post = dashboard_data.posts[0]
    pumblr.api.reblog(post.id, post.reblog_key, group='se-kichi')
    new_post = pumblr.api.read('se-kichi', num=1).posts[0]
