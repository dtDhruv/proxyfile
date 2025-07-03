"""proxyfile: download files through random free proxies"""

from importlib import metadata as _md
from .core import download_via_proxy

__all__ = ["download_via_proxy", "__version__"]
__version__ = _md.version(__package__ or "proxyfile")
# SPDX-License-Identifier: MIT
