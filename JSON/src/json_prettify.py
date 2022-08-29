#!/usr/bin/env python
# coding: utf-8

#   This file is being maintained at:
#       https://github.com/sublimehq/Packages/blob/master/JSON/src/json_prettify.py


from __future__ import annotations                                              # https://docs.python.org/3.8/library/__future__.html

import sublime
import sublime_plugin

import collections                                                              # https://docs.python.org/3.8/library/collections.html
import decimal                                                                  # https://docs.python.org/3.8/library/decimal.html
import json                                                                     # https://docs.python.org/3.8/library/json.html
import typing                                                                   # https://docs.python.org/3.8/library/typing.html


PKG_NAME: typing.Final[str] = __package__.split('.')[0]
settings: typing.Union[sublime.Settings, None] = None
base_settings: typing.Final[str] = 'Preferences.sublime-settings'
base_scope: typing.Final[str] = 'source.json - (source.json.hjson | source.json.json5 | source.json.jsonc), source.json.geojson, source.json.jsondotnet'


def status_msg(msg: str = '') -> None:
    """
    Prefixes status messages in the status bar with the package name.

    :param msg:
        The message.
    """

    if msg == '': return
    sublime.status_message(msg=f'{PKG_NAME}: {msg}')


def print_msg(msg_header: str = '', msg_body: str = '') -> None:
    """
    Prefixes messages for the built-in Sublime Console with the package name.

    :param msg_header:
        Header for the first line of the message.

    :param msg_body:
        Message body.
    """

    if msg_body == '': return
    print(f'JSON: {msg_header}:\n\n{msg_body}\n\n')


def json2py(view: sublime.View) -> sublime.Value:
    """
    Converts JSON to a Python object.

    :param view:
        The view from which to extract the contents.

    :return:
        A Python object with the same contents.
    """

    old_contents: typing.Final[str] = view.substr(
        x=whole_view(view)
    )
    try:
        return json.loads(                                                      # https://docs.python.org/3.8/library/json.html#json.loads
            s=old_contents,
            object_pairs_hook=collections.OrderedDict,
            parse_float=decimal.Decimal
        )
    except Exception as e:
        print_msg(
            msg_header='Conversion failed due to error:',
            msg_body=f'{e}'
        )
    return None


def whole_view(view: sublime.View) -> sublime.Region:
    """
    Get the whole view as a region.

    :param view:
        The view from which to get the region.

    :return:
        The whole view as a region.
    """

    return sublime.Region(
        a=0,
        b=view.size()
    )


def is_json(view: sublime.View) -> bool:
    """
    Checks a match against a JSON base scope.

    :param view:
        The view to match.

    :return:
        A match against a JSON base scope.
    """

    return view.match_selector(
        pt=0,
        selector=base_scope
    )


def plugin_loaded(reload: typing.Optional[bool] = False) -> None:
    try:
        global settings
        settings = sublime.load_settings(base_name=base_settings)
        settings.clear_on_change(tag='reload')
        settings.add_on_change(
            tag='reload',
            callback=lambda: plugin_loaded(reload=True)
        )
    except Exception as e:
        print_msg(
            msg_header=f'Loading "{base_settings}" failed due to error',
            msg_body=f'{e}'
        )

    if reload:
        status_msg(msg='Reloaded settings on change.')


def plugin_unloaded() -> None:
    global settings
    settings = None


class JsonToggleAutoPrettify(sublime_plugin.WindowCommand):

    __is_checked: bool = False
    __key: typing.Final[str] = 'json.auto_prettify'

    def __init__(self, window: sublime.Window) -> None:
        try:
            if settings is None:
                return
            self.__is_checked = settings.get(key=self.__key, default=False)
        except Exception:
            pass

    def run(self) -> None:
        try:
            global settings
            if settings is None:
                return
            if self.__is_checked:
                settings.erase(key=self.__key)                                  # remove the override (true) of the default (false)
            else:
                settings.set(key=self.__key, value=True)
            sublime.save_settings(base_name=base_settings)
            self.__is_checked = not self.__is_checked                           # toggle
        except Exception:
            pass

    def is_checked(self) -> bool:
        return self.__is_checked


class JsonAutoPrettifyListener(sublime_plugin.EventListener):

    __key: typing.Final[str] = 'json.auto_prettify'

    def on_pre_save_async(self, view) -> None:
        if not is_json(view):
            return
        if settings is None:
            return
        if not settings.get(key=self.__key, default=False):
            return
        view.run_command(cmd='json_prettify')


class JsonPrettify(sublime_plugin.TextCommand):

    def run(self, edit_token: sublime.Edit) -> None:
        """
        Attempt to prettify the current view's JSON contents. Print errors to
        the console when it fails.
        """

        try:
            json_as_python: typing.Final[sublime.Value] = json2py(view=self.view)
            if json_as_python is None: return
            self.view.replace(
                edit=edit_token,
                region=whole_view(view=self.view),
                text=json.dumps(                                                # https://docs.python.org/3.8/library/json.html#json.dumps
                    obj=json_as_python,
                    allow_nan=False,
                    indent=4,
                    sort_keys=True
                )
            )
            status_msg(msg='Prettified.')
        except Exception as e:
            print_msg(
                msg_header='Conversion failed due to error',
                msg_body=f'{e}'
            )
            status_msg(msg='Prettifying failed. See console for details.')
            pass

    def is_enabled(self) -> bool:
        return is_json(view=self.view)

    def is_visible(self) -> bool:
        return is_json(view=self.view)

    def description(self) -> str:
        return 'Prettify JSON'


class JsonMinify(sublime_plugin.TextCommand):

    def run(self, edit_token: sublime.Edit) -> None:
        """
        Attempt to minify the current view's JSON contents. Print errors to the
        console when it fails.
        """

        try:
            json_as_python: typing.Final[sublime.Value] = json2py(view=self.view)
            if json_as_python is None: return
            self.view.replace(
                edit=edit_token,
                region=whole_view(view=self.view),
                text=json.dumps(                                                # https://docs.python.org/3.8/library/json.html#json.dumps
                    obj=json_as_python,
                    allow_nan=False,
                    indent=None,
                    separators=(',', ':'),
                    sort_keys=True
                )
            )
            status_msg(msg='Minified.')
        except Exception as e:
            print_msg(
                msg_header='Conversion failed due to error',
                msg_body=f'{e}'
            )
            status_msg(msg='Minifying failed. See console for details.')
            pass

    def is_enabled(self) -> bool:
        return is_json(view=self.view)

    def is_visible(self) -> bool:
        return is_json(view=self.view)

    def description(self) -> str:
        return 'Minify JSON'
