#!/usr/bin/python
# -*- coding: utf-8 -*-

import utils
from urllib import urlencode
import urllib2

json = utils.import_json()
from models import ApiRead


class API(object):
    """Tumblr API"""

    def __init__(self):
        pass

    def read(self, user, start=0, num=20, type=None, id=None, search=None, tagged=None):
        """
        Arguments:
        - `user`: username
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

        url = "http://%s.tumblr.com/api/read/json" % user
        req = urllib2.urlopen(url+'?'+urlencode(query))
        return ApiRead.parse(json.loads(utils.extract_dict(req.read())))
