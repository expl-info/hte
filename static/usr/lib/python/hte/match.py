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

def matchany(child, x, **kwargs):
	"""Match against text or element.
	"""
	if type(child) in StringTypes:
		return matchtext(child, x)
	elif isinstance(child, Elem):
		return matchelem(child, x)

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
	if isinstance(child, Elem) \
		and child.tag == x.tag \
		and len(child.attrs) == len(x.attrs):
		for k, v in child.attrs.items():
			if k not in x.attrs or v != x[attrs]:
				return False
		return True
	return False

def matchregexp(child, x, **kwargs):
	"""Match against a compiled regexp.
	"""
	return type(child) in StringTypes \
		and x.match(child)

def matchtext(child, x, **kwargs):
	"""Match against text.
	"""
	return type(child) in StringTypes \
		and child == x
