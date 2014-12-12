#! /usr/bin/env python
#
# hte/__init__.py

# Copyright 2014 John Marshall. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import types
from xml.sax.saxutils import escape, quoteattr

class Elem(object):
    """Generic element with tag specified. Children are optional, as
    are id, class, and generic element attribute settings. Empty
    tags may be identified.
    """

    def __init__(self, tag, children=None, _id=None, _class=None, attrs=None, empty=None, ht=None):
        self.tag = tag
        self.children = []
        self._id = None
        self._class = None
        self.attrs = {}
        self.ht = ht
        self.set(children, _id=_id, _class=_class, attrs=attrs, empty=empty)

    def set(self, *args, **kwargs):
        children = args and args[0] or None
        if children != None:
            self.children = []
            self.add(children)
        if "_id" in kwargs:
            self._id = kwargs["_id"]
        if "_class" in kwargs:
            self._class = kwargs["_class"]
        if "empty" in kwargs:
            self.empty = kwargs["empty"]
        if "attrs" in kwargs:
            self.attrs = kwargs["attrs"] or {}
        return self

    def add(self, children):
        """Add zero/one or more children.
        """
        if type(children) != types.ListType:
            children = [children]
        for child in children:
            if isinstance(child, Elem):
                if type(self.ht) != type(child.ht):
                    # dissimilar builders
                    self.ht.warnings.append("mismatched tree type for child (%s)" % child)
                self.children.append(child)
            elif type(child) in types.StringTypes \
                or isinstance(child, Raw):
                self.children.append(child)
            else:
                # warn?
                pass
        return children and children[0]

    def render(self):
        """Render the current element and its children, returning
        them in a flat list.
        """
        l = []
        if self.tag:
            l.append("<%s %s %s %s>" \
                % (self.tag,
                    self._id != None and ("id=%s" % quoteattr(v)) or "",
                    self._class != None and ("class=%s" % quoteattr(v)) or "",
                    self.attrs and " ".join([v != None and k+"="+quoteattr(v) or k for k, v in self.attrs.items()]) or ""))
        for child in self.children:
            if type(child) in types.StringTypes:
                l.append(escape(child))
            elif isinstance(child, Elem) or isinstance(child, Raw):
                l.extend(child.render())
            else:
                # warn?
                pass
        if self.tag and not self.empty:
            l.append("</%s>" % self.tag)
        return l

    def __str__(self):
        """Return the rendered list as a "joined" string.
        """
        return "".join(self.render())

class Raw:
    """Raw/unprocessed text.
    """

    def __init__(self, txt):
        self.txt = txt

    def render(self):
        return self.txt
