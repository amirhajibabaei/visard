# +
import nglview as ngl
import numpy as np
from ase import Atoms


def trajectory(traj, radiusScale=0.7, focus=None):
    if type(traj) == Atoms:
        traj = [traj]

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
    add_directions(view, traj[0].cell)
    return view


def add_directions(view, cell, radius=0.2, textsize=4):
    arrow_a = -np.ones(3) * 2
    names = "a b c".split()
    shapes = []
    for i, vec in enumerate(cell):
        color = [0, 0, 0]
        color[i] = 1
        arrow_b = arrow_a + vec / 3
        arrow = ("arrow", arrow_a, arrow_b, color, radius)
        label = ("label", arrow_b, color, textsize, names[i])
        shapes.extend([arrow, label])
    view._add_shape(shapes, name="axes")
