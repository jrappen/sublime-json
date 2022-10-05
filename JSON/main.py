#!/usr/bin/env python
# coding: utf-8


from __future__ import annotations                                              # https://docs.python.org/3.8/library/__future__.html


################################################################################


import sys                                                                      # https://docs.python.org/3.8/library/sys.html

prefix = __package__ + "."
for module_name in [
    module_name
    for module_name in sys.modules
    if module_name.startswith(prefix) and module_name != __name__
]:
    del sys.modules[module_name]
prefix = None


################################################################################


from .src import *
