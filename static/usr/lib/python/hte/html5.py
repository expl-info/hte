#! /usr/bin/env python
#
# hte/html5.py

# Copyright 2014 John Marshall. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from . import Elem, Raw

TAGS = [
    "a", "abbr", "acronym", "address", "applet", "area", "article", "aside", "audio",
    "b", "base", "basefont", "bdi", "bdo", "big", "blockquote", "body", "br", "button",
    "canvas", "caption", "center", "cite", "code", "col", "colgroup",
    "datalist", "dd", "del", "details", "dfn", "dialog", "dir", "div", "dl", "dt",
    "em", "embed",
    "fieldset", "figcaption", "figure", "font", "footer", "form", "frame", "frameset",
    "head", "header", "hgroup", "h1", "h2", "h3", "h4", "h5", "h6","hr", "html",
    "i", "iframe", "img", "input", "ins",
    "kbd", "keygen",
    "label", "legend", "li", "link",
    "main", "map", "mark", "menu", "menuitem", "meta", "meter",
    "nav", "noframes", "noscript",
    "object", "ol", "optgroup", "option", "output",
    "p", "param", "pre", "progress",
    "q",
    "rp", "rt", "ruby",
    "s", "samp", "script", "section", "select", "small", "source", "span", "strike",
        "strong", "style", "sub", "summary", "sup",
    "table", "tbody", "td", "textarea", "tfoot", "th", "thead", "time", "title", "tr", "track", "tt",
    "u", "ul",
    "var", "video",
    "wbr",
]
TAG_METHODS = dict([(name.capitalize(), name) for name in TAGS])

EMPTY_TAGS = [ "area", "base", "basefont", "br", "col", "frame", "hr", "img", "input",
    "isindex", "link", "meta", "param"
]
EMPTY_TAGS = dict([(name, None) for name in EMPTY_TAGS])

class Html5Tree:

    def __init__(self):
        self.top = Elem(None, ht=self)
        self.warnings = []

    def __getattr__(self, attr):
        tag = TAG_METHODS.get(attr)
        if tag:
            # Return "set" method on new Elem object.
            return Elem(tag, empty=tag in EMPTY_TAGS, ht=self).set
        raise AttributeError(attr)

    def __str__(self):
        return str(self.top)

    def render(self):
        return self.top.render()

    def raw(self, *args, **kwargs):
        return Raw(*args, **kwargs)
