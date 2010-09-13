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

  $ python setup.py install (run as admin/root)


Usage
-----
::

  # import
  >>> import pumblr

  # read user post (/api/read)
  # to read 'seikichi.tumblr.com',
  >>> data = pumblr.api.read('seikichi')

  # authenticate (/api/authenticate)
  >>> pumblr.api.auth(email='hoge@fuga', password='password')

  # write quote (/api/write)
  >>> pumblr.api.write_quote(quote='myo---n')

  # read dashboard (/api/dashboard)
  >>> data = pumblr.api.dashboard()
  >>> p = data.posts[0]

  # liking post(/api/like) (unliking is similar)
  >>> pumblr.api.like(post_id=p.id, reblog_key=p.reblog_key)

  # reblogging post(/api/reblog)
  >>> pumblr.api.reblog(post_id=p.id, reblog_key=p.reblog_key)


Other
-----
not implemented yet
+++++++++++++++++++
* Liked posts (api/likes)
* Pages reading (api/pages)
* Editing posts (api/write)

|
| Author: seikichi
| License: MIT
| Mail: seikichi[at]kmc.gr.jp

