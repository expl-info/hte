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

FIND_PATH = 1
FIND_ELEM = 2

class Node(object):

    def __init__(self, children=None, tb=None):
        self.children = children or []
        self.tb = tb

    def _findn(self, count, matcher, parent, path, findtype):
        """A generator to return matches according to the provided
        matcher. Returned values are matched elements or the full
        path to the element (relative to the base element).
        """
        path = path or [parent]
        for i, child in enumerate(parent.children):
            if matcher.match(child):
                if findtype == FIND_PATH:
                    yield path+[child]
                    count -= 1
                else:
                    yield child
                    count -= 1
                if count <= 0:
                    return
            if isinstance(child, Node):
                for val in self._findn(count, matcher, child, path+[child], findtype):
                    yield val
                    count -= 1
                    if count <= 0:
                        return

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

    def add(self, *children):
        """Add zero/one or more children.
        """
        if children and type(children[0]) != types.ListType:
            children = [children]
        for child in children:
            if isinstance(child, Node):
                if type(self.tb) != type(child.tb):
                    # dissimilar builders
                    self.tb.warnings.append("mismatched tree type for child (%s)" % child)
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

    def find(self, matcher, findtype=FIND_ELEM):
        """Return a generator to find a single/first match.
        """
        return self._findn(1, matcher, self, None, findtype)

    def findall(self, matcher, findtype=FIND_ELEM):
        """Return a generator to find all matches.
        """
        return self.findn(1<<31, matcher, findtype)

    def findn(self, count, matcher, findtype=FIND_ELEM):
        """Return a generator to find n matches.
        """
        return self._findn(count, matcher, self, None, findtype)

class Elem(Node):
    """Generic element with tag specified. Children are optional, as
    are id, class, and generic element attribute settings. Void
    element tags may be identified.
    """

    def __init__(self, tag, children=None, _id=None, _class=None, attrs=None, void=None, tb=None):
        Node.__init__(self, children, tb=tb)
        self.tag = tag
        self.attrs = {}
        self.set(children, _id=_id, _class=_class, attrs=attrs, void=void)

    def __str__(self):
        return "<Elem tag=%s nattrs=%s nchildren=%s>" % (self.tag, len(self.attrs), len(self.children))

    def __repr__(self):
        return self.__str__()

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
        """Render raw text as is (no escaping).
        """
        return self.txt

class Text(Node):

    def __init__(self, txt):
        """Text node.
        """
        Node.__init__(self)
        self.txt = txt

    def _render(self):
        """Return the text string.
        """
        return escape(self.txt)

class TreeBuilder:
    """Dynamically supports methods named to match tags subject to
    configuration.

    All top-level (i.e., non-prefixed) methods are reserved for
    element names (determined by the configuration). At
    instantiation, the following keyword arguments are supported:
    * anytag - allow any tag (bool)
    * attrminimize - automatically minimize attribute names (bool)
    * ignorecase - ignore tag case (bool)
    * lowercase - automatically lowercase tag name (bool)
    * voidtags - list of void tags (i.e., do not need closing tag)

    They affect handling and rendering.
    """

    def __init__(self, **kwargs):
        self._warnings = []

        # flags
        self._anytag = kwargs.get("anytag", False)
        self._attrminimize = kwargs.get("attrminimize", False)
        self._ignorecase = kwargs.get("ignorecase", False)
        self._lowercase = kwargs.get("lowercase", False)
        self._voidtags = kwargs.get("voidtags", [])

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
        """Return a special object which can be instatiated to an
        Elem object with the tag corresponding to the method name
        used and according to the configuration.
        """
        tag = self._normtag(attr)
        if tag == None:
            raise AttributeError(attr)
        def _Elem(*args, **kwargs):
            return self._elem(tag, *args, **kwargs)
        return _Elem

    def _normtag(self, tag):
        """Normalize tag according to the configuration.
        """
        _tag = self._ignorecase and tag.lower() or tag
        if _tag in self._tagsd or self._anytag:
            if not self._lowercase:
                _tag = tag
            return _tag
        return None

    def _elem(self, tag, *args, **kwargs):
        """Return instatiated Elem object according to the
        configuration.
        """
        isvoidtag = tag in self._voidtagsd
        tag = self._normtag(tag)
        if tag == None:
            raise AttributeError(tag)
        return Elem(tag, *args, void=isvoidtag, tb=self, **kwargs)
