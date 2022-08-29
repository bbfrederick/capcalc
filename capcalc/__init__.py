from ._gittag import __gittag__
from .version import __version__  # noqa

from . import _version
__version__ = _version.get_versions()['version']
