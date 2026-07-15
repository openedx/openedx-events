"""
Package where Open edX Events and the necessary tooling are implemented.

These definitions are part of the Hooks Extension Framework, see OEP-50 for
more information about the project.
"""
from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("openedx-events")
except PackageNotFoundError:
    # Package isn't installed (e.g. running from a source checkout with no
    # editable install) -- data.EventData.sourcelib parses this into a tuple
    # of ints, so it must stay a valid, minimal version string.
    __version__ = "0.0.0"
