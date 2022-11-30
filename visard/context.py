# +
from __future__ import annotations

from typing import ContextManager

from ._matplotlib import plt
from .size import golden_size_from_width, journal_page

_basic_rc = {
    "font.family": "serif",
    "font.size": 10,
    "mathtext.fontset": "custom",
    "axes.labelsize": 10,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "legend.fontsize": 8,
    # 'savefig.format': 'pdf',
    "figure.figsize": golden_size_from_width(3.5),
    "axes.xmargin": 0.05,
    "axes.ymargin": 0.05,
    "figure.subplot.left": 0.15,  # 0.125
    "figure.subplot.right": 0.9,  # 0.9
    "figure.subplot.bottom": 0.25,  # .11
    "figure.subplot.top": 0.9,  # 0.88
    # 'axes.labelpad': 3.0
}


def journal(
    style: str = "fullpage",
    wide: bool = False,
    rows: int = 1,
    tex: bool = True,
    input_rc: dict | None = None,
    left: float | None = None,
    trim: bool = False,
) -> ContextManager:
    if input_rc is None:
        x = _basic_rc.copy()
    else:
        x = input_rc.copy()
    page = journal_page(style)

    # fig size
    if left:
        x["figure.subplot.left"] = left
    w, h = golden_size_from_width(page["single"])
    if wide:
        c = page["double"] / page["single"]
        w *= c
        x["figure.subplot.left"] /= c
        x["figure.subplot.right"] = 1 - (1 - x["figure.subplot.right"]) / c
        x["figure.subplot.wspace"] = 0.2 + x["figure.subplot.left"]

    if rows > 1:
        h *= rows
        x["figure.subplot.bottom"] /= rows
        x["figure.subplot.top"] = 1 - (1 - x["figure.subplot.top"]) / rows
        x["figure.subplot.hspace"] = 0.3 + x["figure.subplot.bottom"]
    x["figure.figsize"] = (w, h)

    if trim:
        x.update({"axes.xmargin": 0.0, "axes.ymargin": 0.0})

    # latex
    x["text.usetex"] = tex

    return plt.rc_context(x)
