# -*- coding: utf-8 -*-

# Copyright (c) 2013 Kura
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from __future__ import unicode_literals

from urllib.parse import urlencode, quote

from docutils import nodes
from docutils.parsers.rst import directives, Directive


class Vimeo(Directive):
    """ Embed Vimeo video in posts.

    Based on the YouTube directive by Brian Hsu:
    https://gist.github.com/1422773

    VIDEO_ID is required, width / height are optional integer,
    and align could be left / center / right.

    Usage:
    .. vimeo:: VIDEO_ID
        :width: 640
        :height: 480
        :align: center

    Additionally, this plugin allows to specify the following `Vimeo
    player URL parameters
    <https://vimeo.zendesk.com/hc/en-us/articles/360001494447>`__
    as options (values are passed through):

    * autopause
    * autoplay
    * background
    * byline
    * color
    * controls
    * dnt
    * fun
    * loop
    * muted
    * playsinline
    * portrait
    * quality
    * speed
    * t
    * texttrack
    * title
    * transparent

    If you encounter Vimeo player URL parameters not supported by this
    plugin, you can also specify those appended to the video ID
    (e.g., ``.. vimeo:: 37818131?some_option=some_value&foo=bar``).
    """

    # all except "#t" (since this is a fragment identifier, not an URL
    # parameter):
    url_options = (
        "autopause",
        "autoplay",
        "background",
        "byline",
        "color",
        "controls",
        "dnt",
        "fun",
        "loop",
        "muted",
        "playsinline",
        "portrait",
        "quality",
        "speed",
        "texttrack",
        "title",
        "transparent",
    )

    def align(argument):
        """Conversion function for the "align" option."""
        return directives.choice(argument, ("left", "center", "right"))

    required_arguments = 1
    option_spec = {
        "width": directives.positive_int,
        "height": directives.positive_int,
        "align": align,
        "t": directives.unchanged,
    }
    option_spec.update(
        {option: directives.unchanged for option in url_options}
    )

    final_argument_whitespace = False
    has_content = False

    def run(self):
        videoID = self.arguments[0].strip()

        width = self.options.get("width", 420)
        height = self.options.get("height", 315)
        align = self.options.get("align", "left")

        url = "https://player.vimeo.com/video/{}".format(videoID)

        url_params = {
            option: self.options[option]
            for option in self.url_options
            if option in self.options
        }

        if url_params:
            url += "?" + urlencode(url_params)

        if "t" in self.options:
            url += "#t=" + quote(self.options["t"])

        div_block = '<div class="vimeo" align="{}">'.format(align)
        embed_block = (
            '<iframe width="{}" height="{}" src="{}" '
            'frameborder="0" webkitAllowFullScreen '
            "mozallowfullscreen allowFullScreen></iframe>"
            "".format(width, height, url)
        )

        return [
            nodes.raw("", div_block, format="html"),
            nodes.raw("", embed_block, format="html"),
            nodes.raw("", "</div>", format="html"),
        ]


def register():
    directives.register_directive("vimeo", Vimeo)
