#!/usr/bin/python
# -*- coding: utf-8 -*-

import utils
import urllib2
import functools

json = utils.import_json()
from models import ApiRead
from errors import PumblrError, PumblrAuthError, PumblrRequestError


class API(object):
    """Tumblr API"""

    def __init__(self, email=None, password=None):
        self._authenticated = False
        if email is not None and password is not None:
            self.auth(email, password)

    def _check_we_ll_be_back(self, text): # ;-p
        if text.startswith('<!DOCTYPE html PUBLIC'): #TODO: これ微妙すぎるだろ
            raise PumblrError('We\'ll be back shortly!')

    def _auth_check(func):
        """check authenticate"""
        @functools.wraps(func)
        def wrapper(self, *args, **kw):
            if not self._authenticated:
                raise PumblrError("You are not authenticated yet.")
            return func(self, *args, **kw)
        return wrapper

    def _check_status_code(self, url, data):
        """POST to url(with data) and check HTTP status code"""
        try:
            req = urllib2.urlopen(url, data)
            return req.read()
        except urllib2.HTTPError, e:
            if e.code == 200 or e.code == 201:
                return # OK
            if e.code == 404:
                raise PumblrError('incorrect reblog-key')
            if e.code == 403:
                raise PumblrAuthError(str(e))
            if e.code == 400:
                raise PumblrRequestError(str(e))
        except Exception, e:
            raise PumblrError(str(e))
        raise PumblrError('')

    def _read_json_data(self, url, data=None):
        """open url  and return json instance"""
        text = urllib2.urlopen(url, data).read()
        self._check_we_ll_be_back(text)
        return json.loads(utils.extract_dict(text))

    def auth(self, email, password):
        """validate credentials"""
        self._email = email
        self._password = password
        url = 'http://www.tumblr.com/api/authenticate'
        query = dict(
            email=self._email,
            password=self._password,
        )
        text = self._check_status_code(url, utils.urlencode(query))
        self._check_we_ll_be_back(text)
        self._authenticated = True

    @_auth_check
    def dashboard(self, start=0, num=20, type=None, likes=0):
        """
        Dashboard reading.
        Arguments:
        - `start`: The post offset to start from. The default is 0.
        - `num`: The number of posts to return. The default is 20, and the maximum is 50.
        - `type`: The type of posts to return. If unspecified or empty, all types of posts are returned. Must be one of text, quote, photo, link, chat, video, or audio.
        """
        url = 'http://www.tumblr.com/api/dashboard/json'
        query = dict(
            email=self._email,
            password=self._password,
            start=start,
            num=num,
            likes=likes,
            type=type
        )
        return ApiRead.parse(self._read_json_data(url, utils.urlencode(query)))

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
                num=num,
                type=type,
                search=search,
                tagged=tagged
            )
        url = "http://%s.tumblr.com/api/read/json?%s" % (name, utils.urlencode(query))
        return ApiRead.parse(self._read_json_data(url))

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

    @_auth_check
    def _like_unlike(self, post_id, reblog_key, like):
        url = 'http://www.tumblr.com/api/%s' % ('like' if like else 'unlike')
        query = {
            'email':self._email,
            'password':self._password,
            'post-id':post_id,
            'reblog-key':reblog_key
        }
        self._check_status_code(url, utils.urlencode(query))

    @_auth_check
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
        if group is not None:
            group = '%s.tumblr.com' % group
        url = 'http://www.tumblr.com/api/reblog'
        query = {
            'email':self._email,
            'password':self._password,
            'post-id':post_id,
            'reblog-key':reblog_key,
            'group':group,
            'comment':comment,
            'as':reblog_as,
        }
        self._check_status_code(url, utils.urlencode(query))

    def _write(f):
        def _wrapper(self, generator='pumblr', group=None, **kw):
            """
        Write API.
        Arguments:
        - `generator`: A short description of the application
        - `group`: Post this to a secondary blog on your account
        \n\n
            """
            url = 'http://www.tumblr.com/api/write'
            if group is not None: group = '%s.tumblr.com' % group
            query = dict(
                email=self._email,
                password=self._password,
                generator=generator,
                group=group
            )
            query.update(f(self, **kw))
            if not 'type' in query.keys():
                raise PumblrError('post type is needed!')
            self._check_status_code(url, utils.urlencode(query))

        _wrapper.__doc__ += f.__doc__
        return _wrapper

    @_write
    @_auth_check
    def write_quote(self, quote, source=None):
        """
        Quote Arguments:
        - `quote`:
        - `source`:
        """
        return dict(type='quote', quote=quote, source=source)

    @_write
    @_auth_check
    def write_regular(self, title, body):
        """
        Regular Arguments:
        - `title`:
        - `body`:
        """
        return dict(type='regular', title=title, body=body)
