#! /usr/bin/env python
#
# hte/match.py

# Copyright 2014 John Marshall. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

"""Collection of match functions for use with the Node.find()
methods.
"""

from __future__ import absolute_import

from types import StringTypes

from hte.base import Elem

class Matcher:

    def __init__(self, x, matchfn):
        self.x = x
        self.matchfn = matchfn

    def match(self, child):
        if self.matchfn == None:
            return True
        return self.matchfn(child, self.x)

def matchall(child, x, **kwargs):
    """Match all. Simple iterator.
    """
    return True

def matchany(child, x, **kwargs):
    """Match against text or element.
    """
    return isinstance(child, Node) and child == x

def matchanytext(child, x, **kwargs):
    """Match against text (Text or Raw).
    """
    return (isinstance(child, Text) or isinstance(child, Raw)) and child == x

def matchchildregexp(child, x, **kwargs):
    """Match against element with a child that matches against a
    compiled regexp.
    """
    return isinstance(child, Elem) \
        and child.children \
        and matchregexp(child.children[0], x)

def matchchildtext(child, x, **kwargs):
    """Match against element with a child that matches against text.
    """
    return isinstance(child, Elem) \
        and child.children \
        and matchtext(child.children[0], x)

def matchelem(child, x, **kwargs):
    """Match against an element.
    """
    return isinstance(child, Elem) and child == x

def matchregexp(child, x, **kwargs):
    """Match against a compiled regexp.
    """
    return (isinstance(child, Text) or isinstance(child, Raw)) \
        and x.match(child.txt)

def matchtext(child, x, **kwargs):
    """Match against text.
    """
    return isinstance(child, Text) and child == x
