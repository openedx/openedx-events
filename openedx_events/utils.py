"""
Utilities for Open edX events usage.
"""

import traceback
from pprint import PrettyPrinter
from typing import Any


class ResponsePrettyPrinter(PrettyPrinter):
    """
    Custom printer for Open edX Events responses.

    This class pretty-prints the response of common Django Signals.
    """

    # This overrides a standard library function, these problems are inherited
    # from it.
    # pylint: disable=too-many-positional-arguments, redefined-builtin
    def _format(
        self,
        object: Any,
        stream: Any,
        indent: int,
        allowance: int,
        context: dict[int, int],
        level: int,
    ) -> None:
        """
        Override format method exposing more information about functions/exceptions.

        When formatting a function this method will return the function path.
        When formatting an exception this method will return the stack trace of the
        exception.
        With other objects has the same behavior.
        """
        if isinstance(object, Exception):
            exc_type, exc_value, exc_traceback = (
                type(object),
                object,
                object.__traceback__,
            )
            exc_traceback_formatted = traceback.format_exception(
                exc_type, exc_value, exc_traceback
            )
            object = "".join(exc_traceback_formatted)
        if callable(object):
            object = "{func_module}.{func_name}".format(
                func_module=object.__module__,
                func_name=object.__name__,
            )
        return super()._format(object, stream, indent, allowance, context, level)


def format_responses(
    obj: Any,
    indent: int = 1,
    width: int = 80,
    depth: int | None = None,
    *,
    compact: bool = False,
    sort_dicts: bool = True,
) -> str:
    """
    Format a Django Signal response object into a pretty-printed representation.

    Example usage::

        log.info(
                "Responses of the Open edX Event <%s>: %s",
                self.event_type,
                format_responses(responses, depth=2),
        )

    Will result in:

    .. code-block:: none

        [
            (
                'openedx_basic_hooks.receivers.login_receiver',
                'Traceback (most recent call last):'
                '  File '
                '"/edx/app/edxapp/venvs/edxapp/lib/python3.8/site-packages/django/dispatch/dispatcher.py", '
                'line 207, in send_robust'
                '    response = receiver(signal=self, sender=sender, **named)'
                '  File "/edx/src/openedx-basic-hooks/openedx_basic_hooks/receivers.py", '
                'line 18, in login_receiver'
                '    m = 1/0'
                'ZeroDivisionError: division by zero'
            )
        ]

    Arguments:
        - obj (tuple): response object to be formatted.
        - indent (int): specifies the amount of indentation added to each recursive level.
        - width (int): desired output width.
        - depth (int): number of levels to represent.
        - compact (bool): when true, will format as many items as will fit within the width
          on each output line.
        - sort_dicts (bool): dictionaries will be formatted with their keys sorted.

    Same as in https://docs.python.org/3/library/pprint.html#pprint.PrettyPrinter

    Returns:
        (str) string representation of Open edX events responses.
    """
    return ResponsePrettyPrinter(
        indent=indent,
        width=width,
        depth=depth,
        compact=compact,
        sort_dicts=sort_dicts,
    ).pformat(obj)
