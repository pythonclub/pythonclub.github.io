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

from docutils import nodes
from docutils.parsers.rst import directives, Directive


class YouTube(Directive):
    """ Embed YouTube video in posts.

    Based on the YouTube directive by Brian Hsu:
    https://gist.github.com/1422773

    VIDEO_ID is required, other arguments are optional

    Usage:
    .. youtube:: VIDEO_ID
    """

    def boolean(argument):
        """Conversion function for yes/no True/False."""
        value = directives.choice(argument, ("yes", "True", "no", "False"))
        return value in ("yes", "True")

    required_arguments = 1
    optional_arguments = 6
    option_spec = {
        "class": directives.unchanged,
        "width": directives.positive_int,
        "height": directives.positive_int,
        "allowfullscreen": boolean,
        "seamless": boolean,
        "nocookie": boolean,
    }

    final_argument_whitespace = False
    has_content = False

    def run(self):
        videoID = self.arguments[0].strip()
        # Choose whether to use the YouTube nocookie domain for reduced
        # tracking.
        youtube_domain = (
            "youtube-nocookie" if "nocookie" in self.options else "youtube"
        )
        url = "https://www.{}.com/embed/{}".format(youtube_domain, videoID)

        width = self.options.get("width", None)
        height = self.options.get("height", None)
        fullscreen = self.options.get("allowfullscreen", True)
        seamless = self.options.get("seamless", True)
        css_classes = "youtube"
        if "class" in self.options:
            css_classes += " {}".format(self.options["class"])
        elif height is None:
            # use responsive design with 16:9 aspect ratio by default
            css_classes += " {}".format("youtube-16x9")
        # no additional classes if dimensions (height/width) are specified

        iframe_arguments = [
            (width, 'width="{}"'),
            (height, 'height="{}"'),
            (fullscreen, "allowfullscreen"),
            (seamless, 'seamless frameBorder="0"'),
        ]

        div_block = '<div class="{}">'.format(css_classes)
        embed_block = '<iframe src="{}" '.format(url)

        for value, format in iframe_arguments:
            embed_block += (format + " ").format(value) if value else ""

        embed_block = embed_block[:-1] + "></iframe>"

        return [
            nodes.raw("", div_block, format="html"),
            nodes.raw("", embed_block, format="html"),
            nodes.raw("", "</div>", format="html"),
        ]


def register():
    directives.register_directive("youtube", YouTube)
