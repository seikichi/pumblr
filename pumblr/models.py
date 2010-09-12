#!/usr/bin/python
# -*- coding: utf-8 -*-

class Model(object):

    def __init__(self):
        pass

    @classmethod
    def parse(kls, json):
        """Parse a JSON object into a model instance"""
        raise NotImplementedError


class ApiRead(Model):

    @classmethod
    def parse(kls, json):
        apiread = kls()
        for key, value in json.iteritems():
            if key == 'tumblelog':
                setattr(apiread, key, TumbleLog.parse(value))
            elif key == 'posts':
                setattr(apiread, key, [Post.parse(p) for p in value])
            else:
                setattr(apiread, key, value)
        return apiread


class TumbleLog(Model):

    @classmethod
    def parse(kls, json):
        tumblelog = kls()
        for key, value in json.iteritems():
            setattr(tumblelog, key, value)
        return tumblelog


class Post(Model):

    @classmethod
    def parse(kls, json):
        post = kls()
        for key, value in json.iteritems():
            if key == 'tumblelog':
                setattr(post, key, TumbleLog.parse(value))
            else:
                setattr(post, key, value)
        return post
