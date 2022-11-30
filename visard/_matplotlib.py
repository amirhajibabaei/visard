# +
import matplotlib as mpl
import pylab as plt

preamble = r"""
\usepackage[per-mode=symbol]{siunitx}
\DeclareSIUnit{\calorie}{cal}
\DeclareSIUnit{\atmosphere}{atm}
"""

# latex preamble doesn't work with context managers so we set it globally
mpl.rcParams.update({"text.latex.preamble": preamble})


def _get_plt_attr(attr):
    try:
        f = getattr(plt, attr)
    except AttributeError:
        raise NotImplementedError(attr)
    return f
