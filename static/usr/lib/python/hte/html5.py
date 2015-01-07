#! /usr/bin/env python
#
# hte/html5.py

# Copyright 2014 John Marshall. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from __future__ import absolute_import

from hte.base import Elem, Raw, BaseTree

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

VOIDTAGS = [ "area", "base", "basefont", "br", "col", "frame", "hr", "img", "input",
    "isindex", "link", "meta", "param"
]

def Html5Tree(overrides=None):
    attrs = {
        "anytag": False,
        "attrminimize": True,
        "ignorecase": True,
        "lowercase": True,
        "tags": TAGS,
        "voidtags": VOIDTAGS,
    }
    if overrides != None:
        attrs.update(overrides)
    return BaseTree(**attrs)

def XHtml5Tree(overrides=None):
    attrs = {
        "anytag": False,
        "ignorecase": False,
        "lowercase": True,
        "attrminimize": False,
        "tags": TAGS,
        "voidtags": VOIDTAGS,
    }
    if overrides != None:
        attrs.update(overrides)
    return BaseTree(**attrs)