===============
Pelican YouTube
===============

Pelican YouTube is a plugin to enabled you to embed YouTube videos in your pages
and articles.

Installation
============

To install pelican-youtube, simply install it from PyPI:

.. code-block:: bash

    $ pip install pelican-youtube

Then enable it in your pelicanconf.py

.. code-block:: python

    PLUGINS = [
        # ...
        'pelican_youtube',
        # ...
    ]

Usage
=====

In your article or page, you simply need to add a line to embed your video.

.. code-block:: rst

    .. youtube:: VIDEO_ID

Which will result in:

.. code-block:: html

    <div class="youtube youtube-16x9">
    <iframe src="https://www.youtube.com/embed/VIDEO_ID" allowfullscreen seamless frameBorder="0"></iframe>
    </div>

.. note::

    This code will render you a fully responsive YouTube video, spanning the
    whole available container width.  Note that you will need to integrate the
    code from `youtube.css`_ in your project or template style sheet.
    Alternatively, you can specify `width` and `height` as detailed below.


.. _youtube.css: https://github.com/kura/pelican_youtube/blob/master/youtube.css

Additional arguments
--------------------

+-------------------+------------------+---------------------------------------------------------+
| Attribute         | default          |                                                         |
+===================+==================+=========================================================+
| `allowfullscreen` | ``yes``          | allow video to be displayed full-screen                 |
+-------------------+------------------+---------------------------------------------------------+
| `seamless`        | ``yes``          | no borders around iframe                                |
+-------------------+------------------+---------------------------------------------------------+
| `class`           | ``youtube-16x9`` | additional CSS classes, usually for responsive behavior |
+-------------------+------------------+---------------------------------------------------------+
|                   | empty°           | (° when `width` or `height` are specified)              |
+-------------------+------------------+---------------------------------------------------------+
| `width`, `height` | empty            | video dimensions when responsive design is not desired  |
+-------------------+------------------+---------------------------------------------------------+

Example 1: (responsive design)

.. code-block:: rst

    .. youtube:: 4_X6EyqXa2s
        :class: youtube-4x3
        :allowfullscreen: no
        :seamless: no

Will result in:

.. code-block:: html

    <div class="youtube youtube-4x3">
    <iframe src="https://www.youtube.com/embed/4_X6EyqXa2s"></iframe>
    </div>

Example 2: (non-responsive design)

.. code-block:: rst

    .. youtube:: 4_X6EyqXa2s
        :width: 800
        :height: 500
        :allowfullscreen: no

Will result in:

.. code-block:: html

    <div class="youtube">
    <iframe width="800" height="500" src="https://www.youtube.com/embed/4_X6EyqXa2s" seamless frameBorder="0"></iframe>
    </div>

More Control of YouTube Video Player
------------------------------------

YouTube offers more control via player parameters, which you simply attach to the VIDEO_ID
as query parameters.  See `YouTube documentation`_ for a list of possible parameters.

Example: (start video at time 00:20, start playing automatically, don't show related content at end of video)

.. code-block:: rst

    .. youtube:: 4_X6EyqXa2s?start=20&amp;autoplay=1&amp;rel=0


.. _YouTube documentation: https://developers.google.com/youtube/player_parameters#Parameters

Known Issues
------------

The presence of the ``frameBorder`` attribute causes an HTML5 validation error.  Unfortunately,
this attribute is still necessary for supporting older versions of Internet Explorer.

License
=======

`MIT`_ license.

.. _MIT: http://opensource.org/licenses/MIT


