from dataclasses import dataclass
from typing import Union

import matplotlib
import matplotlib.lines as mlines
import matplotlib.pyplot as plt
from models.node import Node
from models.truss import Truss

from .annotate_helper import AnnotateHelper
from .spacing import Spacing

matplotlib.use("TkAgg")


@dataclass
class MinMax:
    min: float
    max: float


class Plotter:
    def __init__(
        self,
        truss: Truss,
        arrowprops: dict[str, Union[str, tuple[float, float], float]] = {
            "arrowstyle": "-|>",
            "connectionstyle": "arc3",
            "relpos": (0.0, 0.0),
            "color": "r",
            "lw": 1.5,
        },
    ) -> None:
        self.truss = truss
        self.arrowprops = arrowprops
        self.fig, self.ax = plt.subplots()
        self.minmaxes: dict[str, MinMax] = {
            "x": MinMax(0, 0),
            "y": MinMax(0, 0),
        }
        self.space_map = Spacing(truss).spacing_map
        self.legend_handlers: list[mlines.Line2D] = []

    @staticmethod
    def __line2d_for_legend(label: str, **kwargs) -> mlines.Line2D:
        """
        Static helper method that returns Line2D to be used as an Actor
        to be displayed in the legend of the plot.
        """

        return mlines.Line2D([], [], label=label, **kwargs)

    def __set_min_max(self, key: str, value: float) -> None:
        if key not in self.minmaxes:
            return

        if value < self.minmaxes[key].min:
            self.minmaxes[key].min = value

        if value > self.minmaxes[key].max:
            self.minmaxes[key].max = value

    def plot_nodal_forces(self, node: Node) -> None:
        """
        Plots the nodal forces for the node specified.
        """

        helper = AnnotateHelper(arrow_scale=self.space_map[10])
        x_offset, y_offset = helper.offset_from_node(node)
        if node.force.fx != 0:
            self.ax.annotate(
                f"Fx{node.id}",
                xy=(x_offset, node.y),
                xytext=(node.x, node.y),
                arrowprops=self.arrowprops,
            )
            self.__set_min_max("x", x_offset)

        if node.force.fy != 0:
            self.ax.annotate(
                f"Fy{node.id}",
                xy=(node.x, y_offset),
                xytext=(node.x, node.y),
                arrowprops=self.arrowprops,
            )
            self.__set_min_max("y", y_offset)

    def plot_nodes(self) -> None:
        """
        Plots the nodes of the truss using, the forces applied to each node
        are also plotted by calling the plot_nodal_forces method.
        """
        marker = "o"
        color = "red"
        linestyle = "None"

        for node in self.truss.nodes:
            self.plot_nodal_forces(node)
            self.ax.plot(node.x, node.y, color=color, marker=marker)
        node_legend = Plotter.__line2d_for_legend(
            label="Nodes", marker=marker, color=color, linestyle=linestyle
        )
        self.legend_handlers.append(node_legend)

    def plot_undeformed_elements(self) -> None:
        """
        Plot the undeformed elements of the truss.
        """
        color = "black"
        linestyle = "--"

        for element in self.truss.elements:
            self.ax.plot(
                [element.node1.x, element.node2.x],
                [element.node1.y, element.node2.y],
                color=color,
                linestyle=linestyle,
            )
        undeformed_legend = Plotter.__line2d_for_legend(
            color=color, linestyle=linestyle, label="Undeformed elements"
        )
        self.legend_handlers.append(undeformed_legend)

    def plot_deformed_elements(self) -> None:
        """
        Plot the deformed elements of the truss.
        """

        color = "blue"
        linestyle = "-"
        for element in self.truss.elements:
            self.ax.plot(
                [
                    element.node1.x
                    + element.node1.nodal_displacements.x
                    * self.space_map[200],
                    element.node2.x
                    + element.node2.nodal_displacements.x
                    * self.space_map[200],
                ],
                [
                    element.node1.y
                    + element.node1.nodal_displacements.y
                    * self.space_map[200],
                    element.node2.y
                    + element.node2.nodal_displacements.y
                    * self.space_map[200],
                ],
                color=color,
                linestyle=linestyle,
            )
        deformed_legend = Plotter.__line2d_for_legend(
            color=color, linestyle=linestyle, label="Deformed elements"
        )
        self.legend_handlers.append(deformed_legend)

    def plot_legend(self) -> None:
        """
        Adds the handles of the instance to the legend.
        """

        self.ax.legend(handles=self.legend_handlers)

    def set_axis_limits(self) -> None:
        """
        Sets the x and y limits of the axis.
        """
        if self.minmaxes["x"].min != 0 or self.minmaxes["x"].max != 0:
            self.ax.set_xlim(self.minmaxes["x"].min, self.minmaxes["x"].max)

        if self.minmaxes["y"].min != 0 or self.minmaxes["y"].max != 0:
            self.ax.set_ylim(self.minmaxes["y"].min, self.minmaxes["y"].max)

    def plot_truss(self):
        self.plot_nodes()
        self.plot_undeformed_elements()
        self.plot_deformed_elements()
        self.set_axis_limits()
        self.plot_legend()

        plt.show()
