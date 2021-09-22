import sys
from dataclasses import dataclass

from models.node import Node


@dataclass
class AnnotateHelper:
    """
    Helper class to get the offset from the nodes location to plot
    arrow annotations to visualize the nodal forces.

    arrow_scale: int is arbitrarily chosen to magnify the resulting vector.
    """

    eps = sys.float_info.min

    arrow_scale: float

    def offset_from_node(self, node: Node) -> tuple[float, float]:
        """
        Returns the absolute coordinates at the end of the force vector.

        The two coordinates should not be used to represent a single point in
        space. X is used only for the force that is present in the x
        direction. Whether y is used only for the force that is present in
        the y direction. They both refer to the same node though.

        To avoid division by zero the eps variable is utilized which is the
        minimum float of the system
        """
        x_origin, y_origin = node.x, node.y
        fx_magnitude, fy_magnitude = node.force.fx, node.force.fy
        fx_direction = fx_magnitude / (abs(fx_magnitude + self.eps))
        fy_direction = fy_magnitude / (abs(fy_magnitude + self.eps))
        x = x_origin + fx_direction * self.arrow_scale
        y = y_origin + fy_direction * self.arrow_scale
        return x, y
