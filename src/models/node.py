import itertools
from dataclasses import dataclass
from typing import NamedTuple

from .boundary_conditions import BoundaryCondition, FreeMoving


class Dofs(NamedTuple):
    x: int
    y: int


@dataclass
class NodalForce:
    fx: float = 0
    fy: float = 0


@dataclass
class Reaction:
    fx: float = 0
    fy: float = 0


@dataclass
class NodalDisplacement:
    x: float = 0
    y: float = 0


class Node:
    id_iter = itertools.count()
    number_of_dofs = 2

    def __init__(
        self,
        x: float,
        y: float,
        boundary_condition: BoundaryCondition = FreeMoving(),
        force: NodalForce = NodalForce(),
    ) -> None:
        self.x = x
        self.y = y
        self.id: int = next(self.id_iter)
        self.dofs: Dofs = Dofs(x=2 * self.id, y=2 * self.id + 1)
        self.boundary_condition = boundary_condition
        self.force = force
        self.nodal_displacements = NodalDisplacement(0, 0)
        self.reaction: Reaction = Reaction(0, 0)

    def is_supported(self) -> bool:
        """Check if the node is supported."""
        return (
            not self.boundary_condition.is_free_in_x
            or not self.boundary_condition.is_free_in_y
        )

    def get_restrained_dofs(self) -> list[int]:
        """Get the node's dofs that are supported.
        If there aren't any, an empty list is returned."""
        res: list[int] = []
        if self.is_supported():
            if not self.boundary_condition.is_free_in_x:
                res.append(self.dofs.x)
            if not self.boundary_condition.is_free_in_y:
                res.append(self.dofs.y)
        return res

    def get_free_dofs(self) -> list[int]:
        """Get the node's dofs that are free to move.
        If there aren't any, an empty list is returned."""
        res: list[int] = []
        if self.boundary_condition.is_free_in_x:
            res.append(self.dofs.x)
        if self.boundary_condition.is_free_in_y:
            res.append(self.dofs.y)
        return res

    def __key(
        self,
    ) -> tuple[float, float, int, Dofs, BoundaryCondition, NodalForce]:
        return (
            self.x,
            self.y,
            self.id,
            self.dofs,
            self.boundary_condition,
            self.force,
        )

    def __hash__(self) -> int:
        return hash(self.__key())

    def __eq__(self, o: object) -> bool:
        if isinstance(o, Node):
            return self.__key() == o.__key()
        return NotImplemented

    def __repr__(self) -> str:
        return (
            f"Node(x={self.x}, y={self.y},"
            f" boundary_condition={self.boundary_condition},"
            f" force={self.force}"
        )
