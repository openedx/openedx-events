"""
Utilities for Open edX events usage.
"""
import collections
import traceback
from pprint import PrettyPrinter


class ResponsePrettyPrinter(PrettyPrinter):
    """
    Custom printer for Open edX Events responses.

    This class pretty-prints the response of common Django Signals.
    """

    def _format(self, obj, stream, indent, allowance, context, level):  # pylint: disable=arguments-renamed
        """
        Override format method exposing more information about functions/exceptions.

        When formatting a function this method will return the function path.
        When formatting an exception this method will return the stack trace of the
        exception.
        With other objects has the same behavior.
        """
        if isinstance(obj, Exception):
            exc_type, exc_value, exc_traceback = type(obj), obj, obj.__traceback__
            exc_traceback_formatted = traceback.format_exception(
                exc_type, exc_value, exc_traceback
            )
            obj = "".join(exc_traceback_formatted)
        if isinstance(obj, collections.abc.Callable):
            obj = "{func_module}.{func_name}".format(
                func_module=obj.__module__,
                func_name=obj.__name__,
            )
        return super()._format(obj, stream, indent, allowance, context, level)


def format_responses(obj, indent=1, width=80, depth=None, *, compact=False, sort_dicts=True):
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
