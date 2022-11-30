# +
from math import sqrt

inches_per_pt = 1 / 72.27
inches_per_cm = 0.393701
golden_ratio = (sqrt(5) - 1) / 2  # 0.618


def pt_to_inches(pt):
    return inches_per_pt * pt


def cm_to_inches(cm):
    return inches_per_cm * cm


def golden_size_from_width(width):
    return width, golden_ratio * width


def square_size(width):
    return width, width


def journal_page(style):
    name = style.lower()
    if name in ("nat", "nature"):
        size = {
            "columns": 2,
            "single": cm_to_inches(8.9),
            "double": cm_to_inches(18.3),
            "single-double": None,
            "page": cm_to_inches(24.7),
        }
    elif name in ("prl", "prx", "prb", "pre", "pr"):
        size = {
            "columns": 2,
            "single": cm_to_inches(8.6),
            "double": cm_to_inches(17.8),
            "single-double": None,
            "page": None,
        }
    elif name in ("sciadv",):
        size = {
            "columns": 2,
            "single": 3.5,
            "double": 7.3,
            "single-double": 5.0,
            "page": None,
        }
    elif name in ("rsc",):
        size = {
            "columns": 2,
            "single": pt_to_inches(255.22),
            "double": pt_to_inches(528.93),
            "single-double": None,
            "page": None,
        }
    elif name in ("geo", "geometry"):
        size = {
            "columns": 1,
            "single": pt_to_inches(210.0),
            "double": pt_to_inches(430.0),
            "single-double": pt_to_inches(320.0),
            "page": None,
        }
    elif name in ("full", "fullpage"):
        size = {
            "columns": 1,
            "single": pt_to_inches(230.0),
            "double": pt_to_inches(469.75),
            "single-double": pt_to_inches(330.0),
            "page": None,
        }
    else:
        size = None
    return size
