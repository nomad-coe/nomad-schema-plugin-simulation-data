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
#
# Copyright The NOMAD Authors.
#
# This file is part of NOMAD.
# See https://nomad-lab.eu for further info.
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

import numpy as np

from nomad.units import ureg
from nomad.metainfo import SubSection, Quantity, MEnum, Section, Datetime
from nomad.datamodel.metainfo.annotations import ELNAnnotation
from nomad.datamodel.data import EntryData
from nomad.datamodel.metainfo.basesections import Entity, Activity

from .model_system import ModelSystem
from .model_method import ModelMethod
from .outputs import Outputs


class Program(Entity):
    """
    A base section used to specify a well-defined program used for computation.

    Synonyms:
     - code
     - software
    """

    name = Quantity(
        type=str,
        description="""
        The name of the program.
        """,
        a_eln=ELNAnnotation(component='StringEditQuantity'),
    )

    version = Quantity(
        type=str,
        description="""
        The version label of the program.
        """,
        a_eln=ELNAnnotation(component='StringEditQuantity'),
    )

    link = Quantity(
        type=str,
        description="""
        Website link to the program in published information.
        """,
        a_eln=ELNAnnotation(component='URLEditQuantity'),
    )

    version_internal = Quantity(
        type=str,
        description="""
        Specifies a program version tag used internally for development purposes.
        Any kind of tagging system is supported, including git commit hashes.
        """,
        a_eln=ELNAnnotation(component='StringEditQuantity'),
    )

    compilation_host = Quantity(
        type=str,
        description="""
        Specifies the host on which the program was compiled.
        """,
        a_eln=ELNAnnotation(component='StringEditQuantity'),
    )

    def normalize(self, archive, logger) -> None:
        pass


class BaseSimulation(Activity):
    """
    A computational simulation that produces output data from a given input model system
    and methodological parameters.

    Synonyms:
     - computation
     - calculation
    """

    m_def = Section(
        links=['https://liusemweb.github.io/mdo/core/1.1/index.html#Calculation']
    )

    datetime_end = Quantity(
        type=Datetime,
        description="""
        The date and time when this computation ended.
        """,
        a_eln=ELNAnnotation(component='DateTimeEditQuantity'),
    )

    cpu1_start = Quantity(
        type=np.float64,
        unit='second',
        description="""
        The starting time of the computation on the (first) CPU 1.
        """,
        a_eln=ELNAnnotation(component='NumberEditQuantity'),
    )

    cpu1_end = Quantity(
        type=np.float64,
        unit='second',
        description="""
        The end time of the computation on the (first) CPU 1.
        """,
        a_eln=ELNAnnotation(component='NumberEditQuantity'),
    )

    wall_start = Quantity(
        type=np.float64,
        unit='second',
        description="""
        The internal wall-clock time from the starting of the computation.
        """,
        a_eln=ELNAnnotation(component='NumberEditQuantity'),
    )

    wall_end = Quantity(
        type=np.float64,
        unit='second',
        description="""
        The internal wall-clock time from the end of the computation.
        """,
        a_eln=ELNAnnotation(component='NumberEditQuantity'),
    )

    program = SubSection(sub_section=Program.m_def, repeats=False)

    def normalize(self, archive, logger) -> None:
        pass


class Simulation(BaseSimulation, EntryData):
    """ """

    # m_def = Section(extends_base_section=True)

    model_system = SubSection(sub_section=ModelSystem.m_def, repeats=True)

    model_method = SubSection(sub_section=ModelMethod.m_def, repeats=True)

    outputs = SubSection(sub_section=Outputs.m_def, repeats=True)

    def _set_system_branch_depth(
        self, system_parent: ModelSystem, branch_depth: int = 0
    ):
        for system_child in system_parent.model_system:
            system_child.branch_depth = branch_depth + 1
            self._set_system_branch_depth(system_child, branch_depth + 1)

    def normalize(self, archive, logger) -> None:
        super(EntryData, self).normalize(archive, logger)

        # Finding which is the representative system of a calculation: typically, we will
        # define it as the last system reported (TODO CHECK THIS!).
        # TODO extend adding the proper representative system extraction using `normalizer.py`
        if self.model_system is None:
            logger.error('No system information reported.')
            return
        system_ref = self.model_system[-1]
        # * We define is_representative in the parser
        # system_ref.is_representative = True
        self.m_cache['system_ref'] = system_ref

        # Setting up the `branch_depth` in the parent-child tree
        for system_parents in self.model_system:
            system_parents.branch_depth = 0
            if len(system_parents.model_system) == 0:
                continue
            self._set_system_branch_depth(system_parents)
