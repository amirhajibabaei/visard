# +
from ._matplotlib import _get_plt_attr
from .context import journal

__all__ = ["journal"]

__getattr__ = _get_plt_attr
