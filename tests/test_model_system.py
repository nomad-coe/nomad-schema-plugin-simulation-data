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

from simulationdataschema.model_system import AtomicCell


class TestAtomicCell:
    @pytest.fixture(autouse=True)
    def atomic_cell(self):
        return AtomicCell(
            lattice_vectors=[[1, 0, 0], [0, 1, 0], [0, 0, 1]],
            positions=[[0, 0, 0], [0.5, 0.5, 0.5]],
            species=['H', 'O'],
        )