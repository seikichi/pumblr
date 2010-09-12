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
        """
        """
        pass

    def read(self, url):
        url = "http://%s/api/read/json" % url
        return ApiRead.parse(json.loads(utils.extract_dict(urllib2.urlopen(url).read())))
