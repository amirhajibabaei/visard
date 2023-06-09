# +
import nglview as ngl
import numpy as np
from ase import Atoms
from ase.io import read


def trajectory(traj, radiusScale=0.7, focus=None, axes=False, wrap=False):
    if type(traj) == str:
        traj = read(traj, ":")
    elif type(traj) == Atoms:
        traj = [traj]

    # wrap
    if wrap:
        for atoms in traj:
            atoms.wrap()

    #
    if focus:
        split = [[], []]
        for a in range(len(traj[0])):
            if a in focus:
                split[0].append(a)
            else:
                split[1].append(a)
        view = ngl.show_asetraj([atoms[split[0]] for atoms in traj])
        view.add_component(ngl.ASETrajectory([atoms[split[1]] for atoms in traj]))
        components = [view.component_0, view.component_1]
    else:
        view = ngl.show_asetraj(traj)
        components = [view.component_0]

    # spacefill
    for i, comp in enumerate(components):
        comp.add_spacefill()
        comp.remove_ball_and_stick()
        comp.update_spacefill(
            radiusType="covalent", radiusScale=radiusScale, color_scale="rainbow"
        )
        if i > 0:
            comp.update_spacefill(opacity=0.3)

    # global
    view.add_unitcell()
    view.camera = "orthographic"
    view.parameters = {"clipDist": 0}

    # directions
    if axes:
        add_directions(view, traj[0].cell)
    return view


def add_directions(view, cell, arrowsize=1.0, textsize=1.0):
    # TODO: it is not working for non-orthogonal!
    scale = cell.cellpar()[:3].min() / 50
    radius = arrowsize * scale
    _textsize = textsize * scale * 20
    #
    arrow_a = -np.ones(3) * 2
    names = "a b c".split()
    shapes = []
    for i, vec in enumerate(cell):
        color = [0, 0, 0]
        color[i] = 1
        arrow_b = arrow_a + vec / 3
        arrow = ("arrow", arrow_a, arrow_b, color, radius)
        label = ("label", arrow_b, color, _textsize, names[i])
        shapes.extend([arrow, label])
    view._add_shape(shapes, name="axes")
