import pkg_resources
import sys
import warnings

if (3, 5) <= sys.version_info < (3, 6):
    warnings.warn(
        "Support for Python 3.5 will be removed in web3fsnpy v5",
        category=DeprecationWarning,
        stacklevel=2)

if sys.version_info < (3, 5):
    raise EnvironmentError(
        "Python 3.5 or above is required. "
        "Note that support for Python 3.5 will be removed in web3fsnpy v5")

from eth_account import Account  # noqa: E402
from web3fsnpy.main import Web3Fsn  # noqa: E402
from web3fsnpy.providers.rpc import (  # noqa: E402
    HTTPProvider,
)
from web3fsnpy.providers.eth_tester import (  # noqa: E402
    EthereumTesterProvider,
)
from web3fsnpy.providers.ipc import (  # noqa: E402
    IPCProvider,
)
from web3fsnpy.providers.websocket import (  # noqa: E402
    WebsocketProvider,
)

#__version__ = pkg_resources.get_distribution("web3fsnpy").version
__version__ = 1.0

__all__ = [
    "__version__",
    "Web3Fsn",
    "HTTPProvider",
    "IPCProvider",
    "WebsocketProvider",
    "TestRPCProvider",
    "EthereumTesterProvider",
    "Account",
]
