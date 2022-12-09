#!/usr/bin/env python3.8
# coding: utf-8


from __future__ import annotations

import sublime
import sublime_plugin

import json
import typing

if typing.TYPE_CHECKING:
    import sublime_types


PKG_NAME: typing.Final[str] = __package__.split('.')[0]
BASE_SCOPE: typing.Final[str] = 'source.json.jsonc'


def status_msg(msg: str = '') -> None:
    if msg == '':
        return
    sublime.status_message(msg=f'{PKG_NAME}: {msg}')


def print_msg(msg_header: str = '', msg_body: str = '') -> None:
    if msg_body == '':
        return
    print(f'JSONC: {msg_header}:\n\n{msg_body}\n\n')


def json2py(view: sublime.View) -> sublime_types.Value:
    OLD_CONTENTS: typing.Final[str] = view.substr(x=whole_view(view))
    return sublime.decode_value(data=OLD_CONTENTS)


def whole_view(view: sublime.View) -> sublime.Region:
    return sublime.Region(a=0, b=view.size())


def is_jsonc(view: sublime.View) -> bool:
    return view.match_selector(pt=0, selector=BASE_SCOPE)


class JsoncPrettify(sublime_plugin.TextCommand):

    def run(self, edit_token: sublime.Edit, force: typing.Optional[bool] = False) -> None:
        try:
            if not force and not sublime.ok_cancel_dialog(
                msg='Prettifying JSONC will remove included comments and trailing commas.',
                ok_title='Continue',
                # only shown on Windows
                title='JSONC: Prettify'
            ):
                return
            JSON_PY_OBJ: typing.Final[sublime_types.Value] = json2py(view=self.view)
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
            # status_msg('Prettified.')
        except Exception as e:
            print_msg(
                msg_header='Conversion failed due to error',
                msg_body=f'{e}'
            )
            status_msg(msg='Prettifying failed. (Main menu -> View -> Show console)')

    def is_enabled(self) -> bool:
        return is_jsonc(view=self.view)

    def is_visible(self) -> bool:
        return is_jsonc(view=self.view)

    def description(self) -> str:
        return 'Prettify'


class JsoncMinify(sublime_plugin.TextCommand):

    def run(self, edit_token: sublime.Edit, force: typing.Optional[bool] = False) -> None:
        try:
            if not force and not sublime.ok_cancel_dialog(
                msg='Minifying JSONC will remove included comments and trailing commas.',
                ok_title='Continue',
                # only shown on Windows
                title='JSONC: Minify'
            ):
                return
            JSON_PY_OBJ: typing.Final[sublime_types.Value] = json2py(view=self.view)
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
            # status_msg(msg='Minified.')
        except Exception as e:
            print_msg(
                msg_header='Conversion failed due to error',
                msg_body=f'{e}'
            )
            status_msg(msg='Minifying failed. (Main menu -> View -> Show console)')

    def is_enabled(self) -> bool:
        return is_jsonc(view=self.view)

    def is_visible(self) -> bool:
        return is_jsonc(view=self.view)

    def description(self) -> str:
        return 'Minify'
