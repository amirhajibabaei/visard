import numpy as np
from ase import Atom, Atoms
from ase.geometry import Cell
from ase.neighborlist import NeighborList

RangeType = dict[int, tuple[float, float]]


def _in_range(
    p: tuple[float, float, float],
    xrange: RangeType | None = None,
) -> bool:
    if xrange is None:
        return True
    for i, r in xrange.items():
        if not r[0] <= p[i] <= r[1]:
            return False
    return True


def _get_positions(
    atoms: Atoms,
    wrap: bool = True,
) -> np.ndarray:
    # positions
    if wrap:
        c = Cell(atoms.cell)
        scaled = c.scaled_positions(atoms.positions)
        # images = np.floor(scaled).astype("int")
        positions = c.cartesian_positions(scaled % 1.0)  # wrapped positions
    else:
        positions = atoms.positions
    return positions


def extract_range(
    atoms: Atoms,
    wrap: bool = True,
    xrange: RangeType | None = None,
) -> tuple[Atoms, Atoms]:
    """
    Extract atoms from a given structure.

    Args:
        atoms: The structure to extract atoms from.
        wrap: Whether to wrap the atoms into the unit cell.
        xrange: The range of positions to extract.

    Returns:
        A tuple of two structures. The first structure contains the extracted
        atoms, the second structure contains the residual atoms.

    Notes:
        The residual atoms are not wrapped with wrap = True.

    """
    # positions
    positions = _get_positions(atoms, wrap=wrap)
    # extract atoms
    extracted = Atoms()
    residual = Atoms(cell=atoms.cell, pbc=atoms.pbc)
    for a, (x, y, z) in zip(atoms, positions):
        if _in_range((x, y, z), xrange):
            extracted += Atom(a.symbol, (x, y, z))
        else:
            residual += Atom(a.symbol, tuple(a.position))
    return extracted, residual


def extract_symbols(
    atoms: Atoms,
    symbols: list[str],
    wrap: bool = True,
    xrange: RangeType | None = None,
) -> tuple[Atoms, Atoms]:
    """
    Extract atoms from a given structure.

    Args:
        atoms: The structure to extract atoms from.
        symbols: The symbols of the atoms to extract.
        wrap: Whether to wrap the atoms into the unit cell.
        xrange: The range of positions to extract.

    Returns:
        A tuple of two structures. The first structure contains the extracted
        atoms, the second structure contains the residual atoms.

    Notes:
        The residual atoms are not wrapped with wrap = True.
    """
    # positions
    positions = _get_positions(atoms, wrap=wrap)
    # extract atoms
    extracted = Atoms()
    residual = Atoms(cell=atoms.cell, pbc=atoms.pbc)
    for a, (x, y, z) in zip(atoms, positions):
        if a.symbol in symbols:
            if _in_range((x, y, z), xrange):
                extracted += Atom(a.symbol, (x, y, z))
        else:
            residual += Atom(a.symbol, tuple(a.position))
    return extracted, residual


def extract_water(
    atoms: Atoms,
    bond: float,
    wrap: bool = True,
    xrange: RangeType | None = None,
) -> tuple[Atoms, Atoms]:
    """
    Extract water molecules from a given structure.

    Args:
        atoms: The structure to extract water molecules from.
        bond: The maximum bond length between atoms in a water molecule.
        wrap: Whether to wrap the atoms into the unit cell.
        xrange: The range of positions to extract.

    Returns:
        A tuple of two structures. The first structure contains the water
        molecules, the second structure contains the residual atoms.

    Notes:
        The residual atoms are not wrapped with wrap = True.

    """
    # neighbor list
    cutoffs = [bond / 2 if a.symbol in ("O", "H") else 0.0 for a in atoms]
    nl = NeighborList(
        cutoffs,
        skin=0.0,
        sorted=False,
        self_interaction=False,
        bothways=True,
    )
    nl.update(atoms)

    # positions
    positions = _get_positions(atoms, wrap=wrap)

    # extract water molecules
    water = Atoms()
    residual = Atoms(cell=atoms.cell, pbc=atoms.pbc)
    hydrogens = []
    _hydrogens = []
    for a, p in zip(atoms, positions):
        x, y, z = p
        if a.symbol == "O":
            nei, off = nl.get_neighbors(a.index)
            assert (
                len(nei) == 2 and a.index not in nei and (atoms[nei].numbers == 1).all()
            ), "Not a water molecule."
            _hydrogens.extend(nei)
            if not _in_range((x, y, z), xrange):
                continue
            v1, v2 = atoms.get_distances(a.index, nei, mic=True, vector=True)
            water += Atom("O", p)
            water += Atom("H", p + v1)
            water += Atom("H", p + v2)
        elif a.symbol == "H":
            hydrogens.append(a.index)
        else:
            residual += Atom(a.symbol, tuple(a.position))
    assert sorted(_hydrogens) == sorted(hydrogens)
    return water, residual
