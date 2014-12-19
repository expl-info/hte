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

def matchtext(child, node, **kwargs):
	return type(child) in StringTypes \
		and type(node) in StringTypes \
		and child == node

def matchelem(child, node, **kwargs):
	if type(child) == type(node) \
		and isinstance(child, Elem) \
		and child.tag == node.tag \
		and len(child.attrs) == len(node.attrs):
		for k, v in child.attrs.items():
			if k not in node.attrs or v != node[attrs]:
				return False
		return True
	return False

def matchany(child, node, **kwargs):
	if type(child) in StringTypes:
		return matchtext(child, node)
	elif isinstance(child, Elem):
		return matchelem(child, node)
