import nglview
import numpy as np

from ..analysis import extract
from ..trajectory import add_directions
from .orientation import orient


# +
class MetaData:
    def __init__(self, view):
        self.view = view
        self.keys = {}
        self.index = -1

    def add_to_keys(self, key):
        self.index += 1
        if key not in self.keys:
            self.keys[key] = []
        self.keys[key].append(self.index)

    def last(self):
        return getattr(self.view, f"component_{self.index}")


def _add_component(view, key, atoms):
    if view is None:
        view = nglview.show_ase(atoms)
        view._metadata = MetaData(view)
    else:
        view.add_structure(nglview.ASEStructure(atoms))
    view._metadata.add_to_keys(key)
    return view


def _last_component(view):
    return view._metadata.last()


def slab(
    atoms,
    *,
    wrap=True,
    xrange=None,
    force_slab_bonds=False,
    force_water_bonds=False,
    show_water=True,
    water_opacity=1.0,
    show_solutes=True,
    show_cell: bool = False,
):
    water, rest = extract.extract_water(atoms, 1.5, wrap=wrap, xrange=xrange)
    solute, rest = extract.extract_symbols(rest, ("Na", "Cl"), wrap=wrap, xrange=xrange)
    slab, rest = extract.extract_range(rest, xrange=xrange)  # no wrap

    view = None
    # slab
    if True:
        if show_cell:
            slab.cell = atoms.cell
            slab.pbc = atoms.pbc
        view = _add_slab(view, slab, force_slab_bonds=force_slab_bonds)

    # solute
    if show_solutes:
        view = _add_component(view, "solute", solute)
        _last_component(view).add_spacefill()
        _last_component(view).update_spacefill(radiusScale=0.5)

    # water
    if show_water:
        if force_water_bonds:
            chunksize = 128
            water_chunks = []
            i = 0
            while True:
                chunk = water[i : i + 3 * chunksize]
                if len(chunk) == 0:
                    break
                water_chunks.append(chunk)
                i += 3 * chunksize
        else:
            water_chunks = [water]
        for chunk in water_chunks:
            view = _add_component(view, "water", chunk)
            _last_component(view).update_ball_and_stick(opacity=water_opacity)
    #
    view.camera = "orthographic"
    # view.component_1.update_spacefill(color="yellow")
    orient(view, "yz")
    if show_cell:
        view.add_unitcell()
        add_directions(view, atoms.cell)
    view.center()
    return view


def _add_slab(view, slab, force_slab_bonds=False):
    # sort by z
    z = slab.positions[:, 2]
    idx = z.argsort()
    z = z[idx]
    slab = slab[idx]
    if not force_slab_bonds:
        return _add_component(view, "slab", slab)
    breaks = []
    for i, d in enumerate(np.diff(z)):
        if d > 1.1:
            breaks.append(i)
    breaks.append(len(z))
    a = 0
    for i, b in enumerate(breaks):
        if b - a > 4 * 64 or i == len(breaks) - 1:
            view = _add_component(view, "slab", slab[a:b])
            a = breaks[i - 1]
    return view
