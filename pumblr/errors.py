#!/usr/bin/python
# -*- coding: utf-8 -*-

class PumblrError(Exception):
    """Pumblr exception"""
    
    def __init__(self, msg):
        self._msg = msg

    def __str__(self):
        return self._msg


class PumblrAuthError(PumblrError):
    """403 Forbidden exception"""
    pass


class PumblrReqestError(PumblrError):
    """400 Bad Request exception"""
    pass

