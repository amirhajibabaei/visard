# +
import nglview as ngl
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
    return view
