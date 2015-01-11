#! /usr/bin/env python
#
# hte/parse.py

"""Parsers that produce HTE trees.
"""

from __future__ import absolute_import

import xml.parsers.expat
try:
    from HTMLParser import HTMLParser
except:
    from html.parser import HTMLParser

from hte import Elem

class LocalHtmlParser(HTMLParser):
    pass

    #def handle_starttag(self, tag, attrs):
        #pass

    #def handle_endtag(self, tag):
        #pass

    #def handle_data(self, text):
        #pass

class BaseParser:
    """Base parser with element handlers.
    """

    def __init__(self, ht, ignorevoiderrors=False):
        self._ht = ht
        self._top = Elem(None, ht=self._ht)
        self.stack = []

    def start_element(self, name, attrs):
        last = self.stack[-1]
        el = self._ht._elem(name, attrs=dict(attrs))
        last.add(el)
        if not el.void:
            self.stack.append(el)

    def end_element(self, name):
        last = self.stack[-1]
        if last.tag != name:
            raise Exception("error: end tag expected (%s) got (%s)" % (last.tag, name))
        self.stack.pop()

    def char_data(self, text):
        last = self.stack[-1]
        last.add(text)

    def load(self, s):
        """Parse ML from string.
        """
        self.stack = [self._top]
        self.parse(s)
        return self.stack[0]

    def loadf(self, f):
        """Parse ML from file.
        """
        self.stack = [self._top]
        self.parsef(f)
        return self.stack[0]

class HtmlParser(BaseParser):
    """Base parser for HTML.
    """

    def __init__(self, ht):
        BaseParser.__init__(self, ht)
        self.p = LocalHtmlParser()
        self.p.handle_starttag = self.start_element
        self.p.handle_endtag = self.end_element
        self.p.handle_data = self.char_data

    def parse(self, s):
        self.p.feed(s)

    def parsef(self, f):
        self.p.feed(f.read())

class XmlParser(BaseParser):
    """Base parser for XML.
    """

    def __init__(self, ht):
        BaseParser.__init__(self, ht)
        self.p = xml.parsers.expat.ParserCreate()
        self.p.StartElementHandler = self.start_element
        self.p.EndElementHandler = self.end_element
        self.p.CharacterDataHandler = self.char_data

    def parse(self, s):
        self.p.Parse(s)

    def parsef(self, f):
        self.p.ParseFile(f)