#!/usr/bin/env python3.8
# coding: utf-8


from __future__ import annotations

import sublime
import sublime_plugin

import collections
import decimal
import json
import typing

if typing.TYPE_CHECKING:
    import sublime_types


BASE_SCOPE: typing.Final[str] = 'source.json - (source.json.hjson | source.json.json5 | source.json.jsonc), source.json.geojson, source.json.jsondotnet'
BASE_SETTINGS: typing.Final[str] = 'Preferences.sublime-settings'
PKG_NAME: typing.Final[str] = __package__.split('.')[0]

settings: typing.Optional[sublime.Settings] = None


def status_msg(msg: str = '') -> None:
    if msg == '': return
    sublime.status_message(msg=f'{PKG_NAME}: {msg}')


def print_msg(msg_header: str = '', msg_body: str = '') -> None:
    if msg_body == '': return
    print(f'JSON: {msg_header}:\n\n{msg_body}\n\n')


def json2py(view: sublime.View) -> typing.Optional[sublime_types.Value]:
    OLD_CONTENTS: typing.Final[str] = view.substr(x=whole_view(view))
    try:
        # https://docs.python.org/3.8/library/json.html#json.loads
        return json.loads(
            s=OLD_CONTENTS,
            object_pairs_hook=collections.OrderedDict,
            parse_float=decimal.Decimal
        )
    except Exception as e:
        print_msg(msg_header='Conversion failed due to error:', msg_body=f'{e}')
    return None


def whole_view(view: sublime.View) -> sublime.Region:
    return sublime.Region(a=0, b=view.size())


def is_json(view: sublime.View) -> bool:
    return view.match_selector(pt=0, selector=BASE_SCOPE)


def plugin_loaded(reload: typing.Optional[bool] = False) -> None:
    try:
        global settings
        settings = sublime.load_settings(base_name=BASE_SETTINGS)
        settings.clear_on_change(tag='reload')
        settings.add_on_change(
            tag='reload',
            callback=lambda: plugin_loaded(reload=True)
        )
    except Exception as e:
        print_msg(
            msg_header=f'Loading "{BASE_SETTINGS}" failed due to error',
            msg_body=f'{e}'
        )

    if reload:
        status_msg(msg='Reloaded settings on change.')


def plugin_unloaded() -> None:
    global settings
    settings = None


class JsonToggleAutoPrettify(sublime_plugin.WindowCommand):

    __is_checked: bool = False
    __KEY: typing.Final[str] = 'json.auto_prettify'

    def __init__(self, window: sublime.Window) -> None:
        try:
            if settings is None:
                return
            self.__is_checked = settings.get(key=self.__KEY, default=False)
        except Exception:
            pass

    def run(self) -> None:
        try:
            global settings
            if settings is None:
                return
            if self.__is_checked:
                # remove the override (true) of the default (false)
                settings.erase(key=self.__KEY)
            else:
                settings.set(key=self.__KEY, value=True)
            sublime.save_settings(base_name=BASE_SETTINGS)
            # toggle
            self.__is_checked = not self.__is_checked
        except Exception:
            pass

    def is_checked(self) -> bool:
        return self.__is_checked


class JsonAutoPrettifyListener(sublime_plugin.EventListener):

    __KEY: typing.Final[str] = 'json.auto_prettify'

    def on_pre_save_async(self, view) -> None:
        if settings is None or not is_json(view):
            return
        if not settings.get(key=self.__KEY, default=False):
            return
        view.run_command(cmd='json_prettify')


class JsonPrettify(sublime_plugin.TextCommand):

    def run(self, edit_token: sublime.Edit) -> None:
        try:
            JSON_PY_OBJ: typing.Final[typing.Optional[sublime_types.Value]] = json2py(view=self.view)
            if JSON_PY_OBJ is None: return
            self.view.replace(
                edit=edit_token,
                region=whole_view(view=self.view),
                # https://docs.python.org/3.8/library/json.html#json.dumps
                text=json.dumps(
                    obj=JSON_PY_OBJ,
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
        try:
            JSON_PY_OBJ: typing.Final[typing.Optional[sublime_types.Value]] = json2py(view=self.view)
            if JSON_PY_OBJ is None: return
            self.view.replace(
                edit=edit_token,
                region=whole_view(view=self.view),
                # https://docs.python.org/3.8/library/json.html#json.dumps
                text=json.dumps(
                    obj=JSON_PY_OBJ,
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
