from dataclasses import dataclass, field

import numpy as np
from numpy.typing import NDArray

from .element import Element
from .node import Dofs, NodalDisplacement, Node
from utils.flatten import flatten


@dataclass
class _ImposeBoundaryConditionsResults:
    stiffness: NDArray[np.float64]
    force: NDArray[np.float64]


@dataclass
class Truss:
    """2D Truss"""

    elements: list[Element]
    nodes: list[Node]
    dof_to_nodal_displacements_map: dict[Dofs, NodalDisplacement] = field(
        init=False
    )

    def get_number_of_dofs(self) -> int:
        """Get the total degrees of freedom of the truss."""

        return len(self.nodes) * Node.number_of_dofs

    def get_force_vector(self) -> NDArray:
        """Arrange the force vector. Returns a column force vector"""

        forces = flatten(
            [[node.force.fx, node.force.fy] for node in self.nodes]
        )
        return np.array(forces, dtype=np.float64).reshape(
            self.get_number_of_dofs(), 1
        )

    def get_free_dofs(self) -> list[int]:
        """Get the free moving dofs of the truss."""

        return flatten([node.get_free_dofs() for node in self.nodes])

    def get_supported_dofs(self) -> list[int]:
        """Get the dofs of the truss that are supported."""

        return flatten([node.get_restrained_dofs() for node in self.nodes])

    def __get_nodal_displacements(self) -> NDArray[np.float64]:
        """Get the nodal displacements vector of truss."""

        return np.array(
            flatten(
                [
                    [
                        node.nodal_displacements.x,
                        node.nodal_displacements.y,
                    ]
                    for node in self.nodes
                ]
            ),
            dtype=np.float64,
        )

    def get_stiffness_matrix(self) -> NDArray:
        """Get the global stiffness matrix of the truss."""

        number_of_dofs = self.get_number_of_dofs()
        stiffness = np.zeros(
            (number_of_dofs, number_of_dofs), dtype=np.float64
        )

        for element in self.elements:
            dofs = element.get_node_dofs()
            element_global_stiffness = element.get_global_stiffness_matrix()
            stiffness[np.ix_(dofs, dofs)] += element_global_stiffness

        return stiffness

    def impose_boundary_conditions(self) -> _ImposeBoundaryConditionsResults:
        """Impose boundary conditions to the stiffness matrix and the force vector"""

        stiffness = self.get_stiffness_matrix()
        force_vector = self.get_force_vector()

        restrained_dofs = self.get_supported_dofs()

        for axis in range(2):
            stiffness = np.delete(
                stiffness,
                [dof for dof in restrained_dofs],
                axis=axis,
            )

        force_vector = np.delete(
            force_vector,
            [dof for dof in restrained_dofs],
            axis=0,
        )

        return _ImposeBoundaryConditionsResults(
            stiffness=stiffness,
            force=force_vector,
        )

    def solve_for_displacements(self) -> NDArray:
        """Return the displacement of the free moving dofs."""
        imposed_system = self.impose_boundary_conditions()
        return np.linalg.solve(imposed_system.stiffness, imposed_system.force)

    def set_nodal_displacements(self) -> None:
        """Set the computed nodal displacements to each node."""

        displacements = self.solve_for_displacements().flatten()
        for free_dof, displacement in zip(self.get_free_dofs(), displacements):
            if free_dof % 2 == 0:
                # dof in x direction
                node_idx = int(free_dof / 2)
                node = self.nodes[node_idx]
                node.nodal_displacements.x = displacement
            else:
                # dof in y direction
                node_idx = int((free_dof - 1) / 2)
                node = self.nodes[node_idx]
                node.nodal_displacements.y = displacement

    def set_element_stresses(self) -> None:
        """Set elements' stress"""

        for element in self.elements:
            element.set_stress()

    def get_reactions(self) -> NDArray[np.float64]:
        """Get the reaction forces for each supported node."""

        stiffness_at_supported_dofs = self.get_stiffness_matrix()[
            np.ix_(self.get_supported_dofs())
        ]
        nodal_displacements = self.__get_nodal_displacements().T
        return stiffness_at_supported_dofs @ nodal_displacements

    def __post_init__(self) -> None:
        self.dof_to_nodal_displacements_map = {}
        for node in self.nodes:
            self.dof_to_nodal_displacements_map[
                node.dofs
            ] = node.nodal_displacements
