#!/usr/bin/python
# -*- coding: utf-8 -*-

import utils
from urllib import urlencode
import urllib2

json = utils.import_json()
from models import ApiRead
from errors import PumblrError, PumblrAuthError, PumblrRequestError


class API(object):
    """Tumblr API"""

    def __init__(self, email=None, password=None):
        self._authenticated = False
        if email is not None and password is not None:
            self.auth(email, password)

    def auth(self, email, password):
        self._email = email
        self._password = password
        url = 'http://www.tumblr.com/api/authenticate'
        query = dict(
            email=self._email,
            password=self._password,
        )
        try:
            req = urllib2.urlopen(url, urlencode(query))
            text = req.read()
        except urllib2.HTTPError, e:
            if e.code == 403:
                raise PumblrAuthError(str(e))
            if e.code == 400:
                raise PumblrRequestError(str(e))
        except Exception, e:
            raise PumblrError(str(e))

        self._check_we_ll_be_back(text)
        self._authenticated = True


    def _check_we_ll_be_back(self, text): # ;-p
        if text.startswith('<!DOCTYPE html PUBLIC'): #TODO: これ微妙すぎるだろ
            raise PumblrError('We\'ll be back shortly!')

    def _auth_check(self):
        if not self._authenticated:
            raise PumblrError("You are not authenticated yet.")

    def dashboard(self, start=0, num=20, type=None, likes=0):
        """
        Dashboard reading.
        Arguments:
        - `start`: The post offset to start from. The default is 0.
        - `num`: The number of posts to return. The default is 20, and the maximum is 50.
        - `type`: The type of posts to return. If unspecified or empty, all types of posts are returned. Must be one of text, quote, photo, link, chat, video, or audio.
        """
        self._auth_check()

        url = 'http://www.tumblr.com/api/dashboard/json'
        query = dict(
            email=self._email,
            password=self._password,
            start=start,
            num=num,
            likes=likes
        )
        if type is not None:
            query['type'] = type

        req = urllib2.urlopen(url, urlencode(query))
        text = req.read()
        self._check_we_ll_be_back(text)
        return ApiRead.parse(json.loads(utils.extract_dict(text)))

    def read(self, name, start=0, num=20, type=None, id=None, search=None, tagged=None):
        """
        Reading Tumblr data.
        Arguments:
        - `name`: username
        - `start`: The post offset to start from. The default is 0.
        - `num`: The number of posts to return. The default is 20, and the maximum is 50.
        - `type`: The type of posts to return. If unspecified or empty, all types of posts are returned. Must be one of text, quote, photo, link, chat, video, or audio.
        - `id`: A specific post ID to return. Use instead of start, num, or type.
        - `search`: Search for posts with this query.
        - `tagged`: Return posts with this tag in reverse-chronological order (newest first).
        """
        if id is not None:
            query = dict(id=id)
        else:
            query = dict(
                start=start,
                num=num
            )
            if type is not None:
                query['type'] = type
            if search is not None:
                query['search'] = search
            if tagged is not None:
                query['tagged'] = tagged

        url = "http://%s.tumblr.com/api/read/json?%s" % (name, urlencode(query))
        req = urllib2.urlopen(url)
        text = req.read()
        self._check_we_ll_be_back(text)
        return ApiRead.parse(json.loads(utils.extract_dict(text)))

    def like(self, post_id, reblog_key):
        """
        Liking post.
        Arguments:
        - `post_id`: The integer ID of the post to reblog.
        - `reblog_key`: The corresponding reblog_key value from the post's read data.
        """
        self._like_unlike(post_id, reblog_key, like=True)

    def unlike(self, post_id, reblog_key):
        """
        Un-Liking post.
        Arguments:
        - `post_id`: The integer ID of the post to reblog.
        - `reblog_key`: The corresponding reblog_key value from the post's read data.
        """
        self._like_unlike(post_id, reblog_key, like=False)

    def _like_unlike(self, post_id, reblog_key, like):
        self._auth_check()
        url = 'http://www.tumblr.com/api/%s' % ('like' if like else 'unlike')
        query = {
            'email':self._email,
            'password':self._password,
            'post-id':post_id,
            'reblog-key':reblog_key
        }
        try:
            urllib2.urlopen(url, urlencode(query))
        except urllib2.HTTPError, e:
            if e.code == 404:
                raise PumblrError('incorrect reblog-key')
            if e.code == 403:
                raise PumblrAuthError(str(e))
            if e.code == 400:
                raise PumblrRequestError(str(e))
        except Exception, e:
            raise PumblrError(str(e))


    def reblog(self, post_id, reblog_key, comment=None, reblog_as=None, group=None):
        """
        Reblogging post.
        Arguments:
        - `post_id`: The integer ID of the post to reblog.
        - `reblog_key`: The corresponding reblog_key value from the post's read data.
        - `comment`: Text, HTML, or Markdown string (see format) of the commentary added to the reblog.
        - `reblog_as`: Reblog as a different format from the original post.
        - `group`: Post this to a secondary blog on your account.
        """

        self._auth_check()

        url = 'http://www.tumblr.com/api/reblog'
        query = {
            'email':self._email,
            'password':self._password,
            'post-id':post_id,
            'reblog-key':reblog_key
        }
        if comment is not None:
            query['comment'] = comment
        if reblog_as is not None:
            query['as'] = reblog_as
        if group is not None:
            query['group'] = '%s.tumblr.com' % group

        try:
            urllib2.urlopen(url, urlencode(query))
        except urllib2.HTTPError, e:
            if e.code == 201:
                return
            if e.code == 403:
                raise PumblrAuthError(str(e))
            if e.code == 400:
                raise PumblrRequestError(str(e))
        except Exception, e:
            raise PumblrError(str(e))
        raise PumblrError('reblog failed.')
