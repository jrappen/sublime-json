#!/usr/bin/env python
# coding: utf-8

#   This file is being maintained at:
#       https://github.com/sublimehq/Packages/blob/master/JSON/src/json_prettify.py


import sublime
import sublime_plugin

import json
#   Compare the docs for these methods:
#       https://docs.python.org/3.8/library/json.html#json.loads
#       https://docs.python.org/3.8/library/json.html#json.dumps


PKG_NAME: str = __package__.split('.')[0]


def status_msg(msg: str = '') -> None:
    if msg == '': return
    sublime.status_message(f'{PKG_NAME}: {msg}')


def json2py(view: sublime.View):
    old_contents: str = view.substr(
        x=whole_view(view)
    )
    return json.loads(
        s=old_contents
    )


def whole_view(view: sublime.View):
    return sublime.Region(
        a=0,
        b=view.size()
    )


def is_json(view: sublime.View):
    return view.match_selector(
        pt=0,
        selector='source.json - (source.json.jsonc | source.json.json5)'
    )


class JsonPrettify(sublime_plugin.TextCommand):

    def run(self, edit):
        """
        Attempt to prettify the current view's JSON contents. Print errors to
        the console when it fails.
        """
        try:
            json_as_python = json2py(self.view)
            self.view.replace(
                edit,
                r=whole_view(self.view),
                text=json.dumps(
                    obj=json_as_python,
                    allow_nan=False,
                    indent=4,
                    sort_keys=True
                )
            )
            status_msg('Prettified.')
        except Exception as e:
            print(f'JSON: Conversion failed due to error:\n\n\n{e}')
            status_msg('Prettifying failed. See console for details.')
            pass

    def is_enabled(self) -> bool:
        return is_json(self.view)

    def is_visible(self) -> bool:
        return is_json(self.view)

    def description(self) -> str:
        return """
        Attempt to prettify the current view's JSON contents. Print errors to
        the console when it fails.
        """


class JsonMinify(sublime_plugin.TextCommand):

    def run(self, edit):
        """
        Attempt to minify the current view's JSON contents. Print errors to
        the console when it fails.
        """
        try:
            json_as_python = json2py(self.view)
            self.view.replace(
                edit,
                r=whole_view(self.view),
                text=json.dumps(
                    obj=json_as_python,
                    allow_nan=False,
                    indent=None,
                    separators=(',', ':'),
                    sort_keys=True
                )
            )
            status_msg('Minified.')
        except Exception as e:
            print(f'JSON: Conversion failed due to error:\n\n\n{e}')
            status_msg('Minifying failed. See console for details.')
            pass

    def is_enabled(self) -> bool:
        return is_json(self.view)

    def is_visible(self) -> bool:
        return is_json(self.view)

    def description(self) -> str:
        return """
        Attempt to minify the current view's JSON contents. Print errors to
        the console when it fails.
        """
