#! /usr/bin/env python
#
# hte/xml.py

# Copyright 2014 John Marshall. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from __future__ import absolute_import

from hte.base import BaseTree

class XmlTree(BaseTree):

    def __init__(self, **kwargs):
        attrs = {
            "anytag": True,
            "ignorecase": False,
            "lowercase": False,
            "attrminimize": False,
            "tags": [],
            "voidtags": [],
        }
        attrs.update(**kwargs)
        BaseTree.__init__(self, **attrs)
