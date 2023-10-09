# +
from ._matplotlib import _get_plt_attr
from .context import journal
try:
    from .trajectory import trajectory
except ImportError:
    pass

__all__ = ["journal", "trajectory", "view"]
view = trajectory

__getattr__ = _get_plt_attr
