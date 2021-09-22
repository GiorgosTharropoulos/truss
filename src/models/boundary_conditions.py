class BoundaryCondition:
    def __init__(self, is_free_in_x: bool, is_free_in_y: bool) -> None:
        self.is_free_in_x = is_free_in_x
        self.is_free_in_y = is_free_in_y

    def __repr__(self) -> str:
        return (
            f"BoundaryCondition(is_free_in_x={self.is_free_in_x},"
            f" is_free_in_y={self.is_free_in_y})"
        )


class FreeMoving(BoundaryCondition):
    def __init__(self) -> None:
        super().__init__(True, True)

    def __repr__(self) -> str:
        return (
            f"FreeMoving(is_free_in_x={self.is_free_in_x},"
            f" is_free_in_y={self.is_free_in_y})"
        )


class RestrictedInX(BoundaryCondition):
    def __init__(self) -> None:
        super().__init__(False, True)

    def __repr__(self) -> str:
        return (
            f"RestrictedInX(is_free_in_x={self.is_free_in_x},"
            f" is_free_in_y={self.is_free_in_y})"
        )


class RestrictedInY(BoundaryCondition):
    def __init__(self) -> None:
        super().__init__(True, False)

    def __repr__(self) -> str:
        return (
            f"RestrictedInY(is_free_in_x={self.is_free_in_x},"
            f" is_free_in_y={self.is_free_in_y})"
        )


class FullyRestricted(BoundaryCondition):
    def __init__(self) -> None:
        super().__init__(False, False)

    def __repr__(self) -> str:
        return (
            f"FullyRestricted(is_free_in_x={self.is_free_in_x},"
            f" is_free_in_y={self.is_free_in_y})"
        )
