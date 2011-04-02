==========
pumblr
==========

What's this?
------------
A python library for The Tumblr API.

Requirements
------------
| python 2.5 or later
| simplejson (python 2.5)

How to Install?
---------------

easy_install
++++++++++++
::

  $ easy_install pumblr


setuptools
++++++++++
::

  $ python setup.py install # (run as admin/root)


Usage
-----
::

  # import
  >>> import pumblr

  # read user post (/api/read)
  # to read 'seikichi.tumblr.com',
  >>> data = pumblr.api.read('seikichi') # 'seikichi.tumblr.com' is also valid

  # authenticate (/api/authenticate)
  >>> api = pumblr.API(email='hoge@fuga', password='password') # or try pumblr.api.auth

  # write quote (/api/write)
  >>> api.write_quote(quote='myo---n')

  # read dashboard (/api/dashboard)
  >>> data = api.dashboard()
  >>> p = data.posts[0]

  # liking post (/api/like) (unliking is similar)
  >>> api.like(post_id=p.id, reblog_key=p.reblog_key)

  # reblogging post (/api/reblog)
  >>> api.reblog(post_id=p.id, reblog_key=p.reblog_key)

not implemented yet
-------------------
* Liked posts (api/likes)
* Pages reading (api/pages)
* Editing posts (api/write)

Other
-----
* Author: seikichi
* License: MIT
* Mail: seikichi[at]kmc.gr.jp

