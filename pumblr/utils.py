#!/usr/bin/python
# -*- coding: utf-8 -*-

import re

def extract_dict(json):
    """ 'var hoge={...}' -> '{...}' """
    return re.match("^.*?({.*}).*$", json, re.DOTALL | re.MULTILINE | re.UNICODE).group(1)


def import_json():
    try:
        import simplejson as json
    except ImportError:
        try:
            import json # Python 2.6+
        except ImportError:
            try:
                from django.utils import simplejson as json # Google App Engine
            except ImportError:
                raise ImportError, "Can't load a json library"
    return json
