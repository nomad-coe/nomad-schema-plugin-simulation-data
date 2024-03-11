#
# Copyright The NOMAD Authors.
#
# This file is part of NOMAD. See https://nomad-lab.eu for further info.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import pytest
from typing import List

from nomad.units import ureg

from . import logger
from nomad_simulations.model_system import AtomicCell
from nomad_simulations.atoms_state import AtomsState


def get_template_atomic_cell(
    lattice_vectors: List = [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
    positions=None,
    periodic_boundary_conditions: List = [False, False, False],
    chemical_symbols: List = ['H', 'H', 'O'],
    atomic_numbers: List = [1, 1, 8],
) -> AtomicCell:
    # Define positions if not provided
    if positions is None and chemical_symbols is not None:
        n_atoms = len(chemical_symbols)
        positions = [[i / n_atoms, i / n_atoms, i / n_atoms] for i in range(n_atoms)]
    # Define the atomic cell
    atomic_cell = AtomicCell()
    if lattice_vectors:
        atomic_cell.lattice_vectors = lattice_vectors * ureg('angstrom')
    if positions:
        atomic_cell.positions = positions * ureg('angstrom')
    if periodic_boundary_conditions:
        atomic_cell.periodic_boundary_conditions = periodic_boundary_conditions

    # Add the elements information
    for index, atom in enumerate(chemical_symbols):
        atom_state = AtomsState()
        setattr(atom_state, 'chemical_symbol', atom)
        atomic_number = atom_state.resolve_atomic_number(logger)
        assert atomic_number == atomic_numbers[index]
        atom_state.atomic_number = atomic_number
        atomic_cell.atoms_state.append(atom_state)
    return atomic_cell


@pytest.fixture(scope='session')
def atomic_cell() -> AtomicCell:
    return get_template_atomic_cell()
