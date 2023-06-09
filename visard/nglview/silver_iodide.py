import nglview

from ..analysis import extract
from .orientation import orient


def slab(atoms, *, wrap=True, xrange=None):
    water, rest = extract.extract_water(atoms, 1.5, wrap=wrap, xrange=xrange)
    solute, slab = extract.extract_symbols(rest, ("Na", "Cl"), wrap=wrap, xrange=xrange)
    #
    view = nglview.show_ase(slab)
    view.add_structure(nglview.ASEStructure(solute))
    view.add_structure(nglview.ASEStructure(water))
    #
    view.component_1.add_spacefill()
    view.component_1.update_spacefill(radiusScale=0.5)
    view.component_2.update_ball_and_stick(opacity=1.0)
    #
    view.camera = "orthographic"
    # view.component_1.update_spacefill(color="yellow")
    orient(view, "yz")
    return view
