#! /usr/bin/env python
#
# hte/xml.py

# Copyright 2014 John Marshall. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from hte import Elem, Raw, BaseTree

def XmlTree():
    attrs = {
        "anytag": True,
        "ignorecase": False,
        "lowercase": False,
        "attrminimize": False,
        "tags": [],
        "voidtags": [],
    }
    return BaseTree(**attrs)
