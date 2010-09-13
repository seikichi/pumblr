==========
pumblr
==========

What's this?
------------
Tumblr APIのためのライブラリ．


Requirements
------------
| python 2.5 or later
| simplejson (python 2.5)

How to Install?
---------------

setuptools
++++++++++
::

  $ python setup.py install (run as admin/root)


Usage
-----
::

  # モジュールのインポート
  >>> import pumblr

  # 特定のユーザーのpostを読む (/api/read)
  # seikichi.tumblr.comの場合は
  >>> data = pumblr.api.read('seikichi')

  # 認証を行う (/api/authenticate)
  >>> pumblr.api.auth(email='hoge@fuga', password='password')

  # quoteを書き込む (/api/write)
  >>> pumblr.api.write_quote(quote='myo---n')

  # dashboardを読む (/api/dashboard)
  >>> data = pumblr.api.dashboard()
  >>> p = data.posts[0]

  # likeを付ける (/api/like) (unlikeも同様)
  >>> pumblr.api.like(post_id=p.id, reblog_key=p.reblog_key)

  # reblogする (/api/reblog)
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

