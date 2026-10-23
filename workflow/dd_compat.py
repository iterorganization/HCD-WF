"""Data Dictionary names (DD 3.42 vs DD 4.x) used by workflow/extend_equilibrium.py.

The target DD is the one of the IMAS environment, with the same rule as
workflow.ids_prep._get_target_dd_version(): IMAS_VERSION when set, else the DD
version reported by the IMAS installation. Input IDSs are converted to it by
ids_prep._smart_convert before the equilibrium fix-ups run.
"""

import os

import imas


def _target_dd_version():
    configured_version = os.getenv("IMAS_VERSION")
    if configured_version:
        return configured_version
    if hasattr(imas, "al_dd_version"):
        return imas.al_dd_version
    return imas.dd_zip.dd_xml_versions()[-1]


DD_VERSION = _target_dd_version()
DD_MAJOR = int(str(DD_VERSION).split(".")[0])
DD3 = DD_MAJOR < 4

# equilibrium time_slice.global_quantities poloidal flux on the magnetic axis:
# psi_axis (DD3), psi_magnetic_axis (DD4; psi_axis is obsolescent in DD4)
PSI_MAGNETIC_AXIS = "psi_axis" if DD3 else "psi_magnetic_axis"

# equilibrium profiles_2d toroidal field (b_field_phi exists in DD 3.42 and DD 4)
B_FIELD_PHI = "b_field_phi"

# poloidal flux sign with respect to COCOS 17: DD3 is COCOS 11, DD4 is COCOS 17
COCOS_PSI = -1.0 if DD3 else 1.0


def psi_boundary(time_slice):
    """Poloidal flux at the plasma boundary of an equilibrium time_slice: time_slice.boundary.psi
    when filled, else time_slice.global_quantities.psi_boundary (obsolescent in DD 3.42 and DD 4)."""
    if time_slice.boundary.psi.has_value:
        return time_slice.boundary.psi
    return time_slice.global_quantities.psi_boundary
