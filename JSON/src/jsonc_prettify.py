#!/usr/bin/env python
# coding: utf-8


from __future__ import annotations                                              # https://docs.python.org/3.8/library/__future__.html

import sublime                                                                  # EXECUTABLE_DIR/Lib/python38/sublime.py
import sublime_plugin                                                           # EXECUTABLE_DIR/Lib/python38/sublime_plugin.py

import json                                                                     # https://docs.python.org/3.8/library/json.html
import typing                                                                   # https://docs.python.org/3.8/library/typing.html

if typing.TYPE_CHECKING:
    import sublime_types                                                        # EXECUTABLE_DIR/Lib/python38/sublime_types.py


PKG_NAME: typing.Final[str] = __package__.split('.')[0]
BASE_SCOPE: typing.Final[str] = 'source.json.jsonc'


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
    print(f'JSONC: {msg_header}:\n\n{msg_body}\n\n')


def json2py(view: sublime.View) -> sublime_types.Value:
    """
    Converts JSONC to a Python object, removing comments.

    :param view:
        The view from which to extract the contents.

    :return:
        A Python object with the same contents but without comments.
    """

    OLD_CONTENTS: typing.Final[str] = view.substr(
        x=whole_view(view)
    )
    return sublime.decode_value(
        data=OLD_CONTENTS
    )


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


def is_jsonc(view: sublime.View) -> bool:
    """
    Checks a match against a JSONC base scope.

    :param view:
        The view to match.

    :return:
        A match against a JSONC base scope.
    """

    return view.match_selector(
        pt=0,
        selector=BASE_SCOPE
    )


class JsoncPrettify(sublime_plugin.TextCommand):

    def run(self, edit_token: sublime.Edit, auto: typing.Optional[bool] = False) -> None:
        """
        Attempt to prettify the current view's JSONC contents. Print errors to
        the console when it fails.
        """

        try:
            if not auto and not sublime.ok_cancel_dialog(
                msg='Prettifying JSONC will remove included comments and trailing commas.',
                ok_title='Continue',
                title='JSONC: Prettify'                                         # only shown on Windows
            ):
                return
            JSON_PY_OBJ: typing.Final[sublime_types.Value] = json2py(view=self.view)
            self.view.replace(
                edit=edit_token,
                region=whole_view(view=self.view),
                text=json.dumps(                                                # https://docs.python.org/3.8/library/json.html#json.dumps
                    obj=JSON_PY_OBJ,
                    allow_nan=False,
                    indent=4,
                    sort_keys=True
                )
            )
            status_msg('Prettified.')
        except Exception as e:
            print_msg(
                msg_header='Conversion failed due to error',
                msg_body=f'{e}'
            )
            status_msg(msg='Prettifying failed. See console for details.')
            pass

    def is_enabled(self) -> bool:
        return is_jsonc(view=self.view)

    def is_visible(self) -> bool:
        return is_jsonc(view=self.view)

    def description(self) -> str:
        return 'Prettify JSONC'


class JsoncMinify(sublime_plugin.TextCommand):

    def run(self, edit_token: sublime.Edit, auto: typing.Optional[bool] = False) -> None:
        """
        Attempt to minify the current view's JSONC contents. Print errors to the
        console when it fails.
        """

        try:
            if not auto and not sublime.ok_cancel_dialog(
                msg='Minifying JSONC will remove included comments and trailing commas.',
                ok_title='Continue',
                title='JSONC: Minify'                                           # only shown on Windows
            ):
                return
            JSON_PY_OBJ: typing.Final[sublime_types.Value] = json2py(view=self.view)
            self.view.replace(
                edit=edit_token,
                region=whole_view(view=self.view),
                text=json.dumps(                                                # https://docs.python.org/3.8/library/json.html#json.dumps
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
        return is_jsonc(view=self.view)

    def is_visible(self) -> bool:
        return is_jsonc(view=self.view)

    def description(self) -> str:
        return 'Minify JSONC'
