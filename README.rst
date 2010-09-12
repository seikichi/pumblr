==========
pumblr
==========

| ※ 激しく書きかけ
| ※ 現状でできること: read, dashboar, like, unlike, reblog

What's this?
------------
A python library for The Tumblr API.


Requirements
------------
| python 2.5 or later
| simplejson(python 2.5)

How to Install?
---------------

setuptools
++++++++++
::

  $ python setup.py install (run as admin/root)


Usage
++++++++++
::

  >>> import pumblr
  >>> data = pumblr.api.read('seikichi') # seikichi.tumblr.com
  >>> print data.posts[0].type


|
|
| Author: seikichi
| License: MIT
| Mail: seikichi[at]kmc.gr.jp

