#!/usr/bin/env python
# coding: utf-8

#   This file is being maintained at:
#       https://github.com/sublimehq/Packages/blob/master/JSON/src/prettify_json.py


import sublime
import sublime_plugin

import json
#   Compare the docs for these methods:
#       https://docs.python.org/3.8/library/json.html#json.loads
#       https://docs.python.org/3.8/library/json.html#json.dumps


PKG_NAME: str = __package__.split('.')[0]


def status_msg(msg: str = '') -> None:

    if msg == '':
        return

    sublime.status_message(f'{PKG_NAME}: {msg}')


class JsonPrettify(sublime_plugin.TextCommand):

    def run(self, edit):
        """
        Attempt to prettify the current view's JSON contents. Print errors to
        the console when it fails.
        """
        try:
            old_contents: str = self.view.substr(
                x=sublime.Region(
                    a=0,
                    b=self.view.size()
                )
            )
            json_to_python = json.loads(
                s=old_contents
            )
            self.view.replace(
                edit,
                r=sublime.Region(
                    a=0,
                    b=self.view.size()
                ),
                text=json.dumps(
                    obj=json_to_python,
                    allow_nan=False,
                    indent=4,
                    sort_keys=True
                )
            )
            status_msg('Prettified.')
        except Exception as e:
            print(f'JSON: Conversion failed due to error: \n\n\n{e}')
            status_msg('Prettifying failed. See console for details.')
            pass

    def is_enabled(self) -> bool:
        return self.view.match_selector(
            pt=0,
            selector='source.json - (source.json.jsonc | source.json.json5)'
        )


class JsonMinify(sublime_plugin.TextCommand):

    def run(self, edit):
        """
        Attempt to minify the current view's JSON contents. Print errors to
        the console when it fails.
        """
        try:
            old_contents: str = self.view.substr(
                x=sublime.Region(
                    a=0,
                    b=self.view.size()
                )
            )
            json_to_python = json.loads(
                s=old_contents
            )
            self.view.replace(
                edit,
                r=sublime.Region(
                    a=0,
                    b=self.view.size()
                ),
                text=json.dumps(
                    obj=json_to_python,
                    allow_nan=False,
                    indent=None,
                    separators=(',', ':'),
                    sort_keys=True
                )
            )
            status_msg('Minified.')
        except Exception as e:
            print(f'JSON: Conversion failed due to error: \n\n\n{e}')
            status_msg('Minifying failed. See console for details.')
            pass

    def is_enabled(self) -> bool:
        return self.view.match_selector(
            pt=0,
            selector='source.json - (source.json.jsonc | source.json.json5)'
        )
