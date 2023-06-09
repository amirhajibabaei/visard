# +
from ._matplotlib import _get_plt_attr
from .context import journal
from .trajectory import trajectory

__all__ = ["journal", "trajectory", "view"]
view = trajectory

__getattr__ = _get_plt_attr
