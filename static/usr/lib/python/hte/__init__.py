#! /usr/bin/env python
#
# hte/__init__.py

# Copyright 2014 John Marshall. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from __future__ import absolute_import

import string
import types
from xml.sax.saxutils import escape, quoteattr

class Elem(object):
    """Generic element with tag specified. Children are optional, as
    are id, class, and generic element attribute settings. Void
    element tags may be identified.
    """

    def __init__(self, tag, children=None, _id=None, _class=None, attrs=None, void=None, ht=None):
        self.tag = tag
        self.children = []
        self.attrs = {}
        self.ht = ht
        self.set(children, _id=_id, _class=_class, attrs=attrs, void=void)

    def set(self, *args, **kwargs):
        children = args and args[0] or None
        if children != None:
            self.children = []
            self.add(children)
        attrs = attrs or {}
        if "_id" in kwargs:
            attrs["id"] = _id
        if "_class" in kwargs:
            attrs["class"] = _class
        if "attrs" in kwargs:
            self.attrs = attrs
        if "void" in kwargs:
            self.void = kwargs["void"]
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
            elif hasattr(child, "render") and callable(child.render):
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
            l.append("<%s %s>" \
                % (self.tag,
                    self.attrs and " ".join([v != None and k+"="+quoteattr(v) or k for k, v in self.attrs.items()]) or ""))
        for child in self.children:
            if type(child) in types.StringTypes:
                l.append(escape(child))
            elif isinstance(child, Elem) or isinstance(child, Raw):
                l.extend(child.render())
            else:
                # warn?
                pass
        if self.tag and not self.void:
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

class BaseTree:
    """Dynamically supports methods named to match tags subject to
    configuration.
    """

    def __init__(self, **kwargs):
        self._top = Elem(None, ht=self)
        self._warnings = []

        # flags
        self._anytag = kwargs.get("anytag", False)
        self._attrminimize = kwargs.get("attrminimize", False)
        self._voidtags = kwargs.get("voidtags", [])
        self._ignorecase = kwargs.get("ignorecase", False)
        self._lowercase = kwargs.get("lowercase", False)

        tags = kwargs.get("tags", [])
        voidtags = kwargs.get("voidtags", [])
        if self._lowercase or self._ignorecase:
            tags = map(string.lower, tags)
            voidtags = map(string.lower, voidtags)
        self._tags = tags
        self._voidtags = voidtags
        self._tagsd = dict([(name, None) for name in self._tags])
        self._voidtagsd = dict([(name, None) for name in self._voidtags])

    def __getattr__(self, attr):
        tag = self._ignorecase and attr.lower() or attr
        isvoidtag = tag in self._voidtagsd
        if tag in self._tagsd or self._anytag:
            if not self._lowercase:
                tag = attr
            return Elem(tag, void=isvoidtag, ht=self).set
        raise AttributeError(attr)

    def __str__(self):
        return str(self._top)

    def _elem(self, *args, **kwargs):
        return Elem(*args, **kwargs)
