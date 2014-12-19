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

class Node(object):

    def __init__(self, children=None, ht=None):
        self.children = children or []
        self.ht = ht

    def _render(self):
        """Render all children to a flat list and return.
        """
        l = []
        for child in self.children:
            if isinstance(child, Node) or isinstance(child, Raw):
                l.extend(child._render())
            elif type(child) in types.StringTypes:
                l.append(escape(child))
            else:
                # warn?
                pass
        return l

    def add(self, children):
        """Add zero/one or more children.
        """
        if type(children) != types.ListType:
            children = [children]
        for child in children:
            if isinstance(child, Node):
                if type(self.ht) != type(child.ht):
                    # dissimilar builders
                    self.ht.warnings.append("mismatched tree type for child (%s)" % child)
                self.children.append(child)
            elif type(child) in types.StringTypes \
                or isinstance(child, Raw):
                self.children.append(child)
            elif hasattr(child, "_render") and callable(child._render):
                self.children.append(child)
            else:
                # warn?
                pass
        return children and children[0]

    def find(self, node, matchfn=None, **kwargs):
        l = self.findn(node, 1, matchfn, **kwargs)
        return l and l[0] or None

    def findall(self, node, matchfn=None, **kwargs):
        return self.findn(node, 1<<31, matchfn, **kwargs)

    def findn(self, node, count, matchfn, **kwargs):
        l = []
        for i, child in enumerate(self.children):
            if matchfn(child, node, **kwargs):
                l.append((self, i))
                if len(l) >= count:
                    break
            if isinstance(child, Node):
                l.extend(child.findn(node, count, matchfn))
                if len(l) >= count:
                    break
        return l

class Elem(Node):
    """Generic element with tag specified. Children are optional, as
    are id, class, and generic element attribute settings. Void
    element tags may be identified.
    """

    def __init__(self, tag, children=None, _id=None, _class=None, attrs=None, void=None, ht=None):
        Node.__init__(self, children, ht=ht)
        self.tag = tag
        self.attrs = {}
        self.set(children, _id=_id, _class=_class, attrs=attrs, void=void)

    def _render(self):
        """Render the current element and its children, returning
        them in a flat list.
        """
        l = []
        if self.tag:
            l.append("<%s %s>" \
                % (self.tag,
                    self.attrs and " ".join([v != None and k+"="+quoteattr(v) or k for k, v in self.attrs.items()]) or ""))
        l.extend(Node._render(self))
        if self.tag and not self.void:
            l.append("</%s>" % self.tag)
        return l

    def set(self, *args, **kwargs):
        children = args and args[0] or None
        if children != None:
            self.children = []
            self.add(children)
        attrs = kwargs.get("attrs") or {}
        if "_id" in kwargs and kwargs["_id"] != None:
            attrs["id"] = kwargs["_id"]
        if "_class" in kwargs and kwargs["_class"] != None:
            attrs["class"] = kwargs["_class"]
        if "attrs" in kwargs:
            self.attrs = attrs
        if "void" in kwargs:
            self.void = kwargs["void"]
        return self

    def render(self):
        """Return the rendered list as a "joined" string.
        """
        return "".join(self._render())

class Raw:
    """Raw/unprocessed text.
    """

    def __init__(self, txt):
        self.txt = txt

    def _render(self):
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

    def _elem(self, *args, **kwargs):
        return Elem(*args, **kwargs)

    def render(self):
        return self._top.render()
