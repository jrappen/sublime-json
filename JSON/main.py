#!/usr/bin/env python
# coding: utf-8

#   This file is being maintained at:
#       https://github.com/sublimehq/Packages/blob/master/JSON/main.py


from __future__ import annotations                                              # https://docs.python.org/3.8/library/__future__.html

import sublime

from .src import *


def plugin_loaded() -> None:
    json_prettify.plugin_loaded()


def plugin_unloaded() -> None:
    json_prettify.plugin_unloaded()
