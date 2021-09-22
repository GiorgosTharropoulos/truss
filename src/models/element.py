from dataclasses import dataclass
from math import sqrt
from typing import Union

import numpy as np
from numpy.typing import NDArray

from .node import Node
from utils.flatten import flatten


@dataclass
class Element:
    node1: Node
    node2: Node
    youngs_modulus: Union[np.float64, float]
    area: Union[np.float64, float]
    __stress: Union[np.float64, float] = np.float64(0)

    def get_length(self) -> np.float64:
        """Returns the length of the element."""

        return np.float64(
            sqrt(
                (self.node1.x - self.node2.x) ** 2
                + (self.node1.y - self.node2.y) ** 2
            )
        )

    def cos(self) -> np.float64:
        """Returns the cosine of the element with respect to the x axis."""

        return (self.node2.x - self.node1.x) / self.get_length()

    def sin(self) -> np.float64:
        """Returns the sine of the element with the respect to the x axis."""

        return (self.node2.y - self.node1.y) / self.get_length()

    def get_global_stiffness_matrix(self) -> NDArray[np.float64]:
        """Returns the global stiffness matrix of the element"""

        s = self.sin()
        c = self.cos()
        matrix_helper = [
            c ** 2,
            c * s,
            -(c ** 2),
            -c * s,
            c * s,
            s ** 2,
            -c * s,
            -(s ** 2),
            -(c ** 2),
            -c * s,
            c ** 2,
            c * s,
            -c * s,
            -(s ** 2),
            c * s,
            s ** 2,
        ]
        return (
            self.youngs_modulus
            * self.area
            / self.get_length()
            * np.array(matrix_helper, dtype=np.float64).reshape(4, 4)
        )

    def get_node_dofs(self) -> list[int]:
        """Returns a list with the indices that correspond to the degrees of
        freedoms of each of the two nodes."""

        x1, y1 = self.node1.dofs
        x2, y2 = self.node2.dofs
        return [x1, y1, x2, y2]

    def get_transformation_matrix(self):
        """Get the transformation matrix of the element from the local
        coordinate system to the global one."""

        s = self.sin()
        c = self.cos()
        return np.array(
            [
                c ** 2,
                c * s,
                -(c ** 2),
                -c * s,
                c * s,
                s ** 2,
                -c * s,
                -(s ** 2),
                -(c ** 2),
                -c * s,
                c ** 2,
                c * s,
                -c * s,
                -(s ** 2),
                c * s,
                s ** 2,
            ],
            dtype=np.float64,
        ).reshape(4, 4)

    def __get_arranged_nodal_displacements(self) -> NDArray[np.float64]:
        """Get the nodal displacements vector of element's nodes."""

        nodes = (self.node1, self.node2)
        nodal_displacements = flatten(
            [node.nodal_displacements.x, node.nodal_displacements.y]
            for node in nodes
        )
        return np.array(nodal_displacements, dtype=np.float64)

    def set_stress(self) -> None:
        """Compute the stress of the element and set in the private __stress member."""

        c = self.cos()
        s = self.sin()
        transformation_matrix = np.array([-c, -s, c, s], dtype=np.float64)
        nodal_displacements = self.__get_arranged_nodal_displacements()
        self.__stress = (
            self.youngs_modulus  # type: ignore
            / self.get_length()
            * (transformation_matrix @ nodal_displacements.T)
        )

    def get_stress(self) -> Union[np.float64, float]:
        """Return the stress of the element."""

        return self.__stress
