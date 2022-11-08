#!/usr/bin/env python3.8
# coding: utf-8


from .json_prettify import *
from .jsonc_prettify import *


def plugin_loaded() -> None:
    json_prettify.plugin_loaded(reload=False)


def plugin_unloaded() -> None:
    json_prettify.plugin_unloaded()
