=============
Pelican Vimeo
=============

Pelican Vimeo is a plugin to enabled you to embed Vimeo videos in your pages
and articles.

Installation
============

To install pelican-vimeo, simply install it from PyPI:

.. code-block:: bash

    $ pip install pelican-vimeo

Then enabled it in your pelicanconf.py

.. code-block:: python

    PLUGINS = [
        # ...
        'pelican_vimeo',
        # ...
    ]

Usage
=====

In your article or page, you simply need to add a line to embed you video.

.. code-block:: rst

    .. vimeo:: VIDEO_ID

Which will result in:

.. code-block:: html

    <div class="vimeo" align="left">
    <iframe width="420" height="315" src="https://player.vimeo.com/video/VIDEO_ID" frameborder="0"
    webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe>
    </div>

Additional arguments
--------------------

You can also specify a `width`, `height` and `alignment`

.. code-block:: rst

    .. vimeo:: 37818131
            :width: 800
            :height: 500
            :align: center

Which will result in:

.. code-block:: html

    <div class="vimeo" align="center">
    <iframe width="800" height="500" src="https://player.vimeo.com/video/37818131" frameborder="0"
    webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe>
    </div>

Additionally, this plugin allows to specify the following `Vimeo
player URL parameters
<https://vimeo.zendesk.com/hc/en-us/articles/360001494447>`__
as options (values are passed through):

* ``autopause``
* ``autoplay``
* ``background``
* ``byline``
* ``color``
* ``controls``
* ``dnt``
* ``fun``
* ``loop``
* ``muted``
* ``playsinline``
* ``portrait``
* ``quality``
* ``speed``
* ``t``
* ``texttrack``
* ``title``
* ``transparent``

If you encounter Vimeo player URL parameters not supported by this
plugin, you can also specify those appended to the video ID
(e.g., ``.. vimeo:: 37818131?another_option=another_value&foo=bar``).

License
=======

`MIT`_ license.

.. _MIT: http://opensource.org/licenses/MIT


