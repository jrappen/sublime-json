#!/usr/bin/env python
# coding: utf-8


from .json_prettify import *
from .jsonc_prettify import *


def plugin_loaded() -> None:
    json_prettify.plugin_loaded(reload=False)


def plugin_unloaded() -> None:
    json_prettify.plugin_unloaded()
