#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import string

def extract_dict(json):
    """
    'var hoge={...}' -> '{...}'

    >>> extract_dict('var hoge = {\"fuga\":1}')
    '{\"fuga\":1}'
    """
    return re.match("^.*?({.*}).*$", json, re.DOTALL | re.MULTILINE | re.UNICODE).group(1)


def make_variable_name(name):
    """
    replace invalide character

    example:
    >>> make_variable_name('hoge-fuga-piyo')
    'hoge_fuga_piyo'
    >>> make_variable_name('Love & Peace')
    'Love___Peace'
    >>> make_variable_name('12abc23')
    'i12abc23'
    """
    if name[0] in string.digits:
        name = 'i' + name # ここどうしよう
    return re.sub('[^A-Za-z0-9_]', '_', name)


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
