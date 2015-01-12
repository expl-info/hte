#! /usr/bin/env python
#
# hte/__init__.py

# Copyright 2014 John Marshall. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

"""HTE (HTML Tree Engine) Provides an easy way to programatically
build HTML (and similar) document trees.

For example:
	import hte
	tb = hte.Html5Tree()
	doc = tb.html()
	doc.add([tb.body(tb.h1("Hello"), tb.p("This is a story ..."))])
	print doc.render()

produces (after pretty printed):
	<html>
		<body>
			<h1>Hello</h1>
			<p>This is a story ...</p>
		</body>
	</html>

The tree builder (e.g., Html5Tree) provides methods corresponding to
the element tags (e.g., tb.h1(), tb.table(), tb.br()). The final
product is generated at render time, with case, void elements, and
quoting/escaping handled according to the tree builder
configuration.
"""

from __future__ import absolute_import

from hte.base import *
from hte.html5 import Html5Tree, XHtml5Tree
from hte.xml import XmlTree
