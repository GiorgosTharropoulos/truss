from models.element import Element
from models.node import NodalForce, Node
from visualization.plotter import Plotter
from models.truss import Truss
from models.boundary_conditions import (
    FreeMoving,
    FullyRestricted,
    RestrictedInY,
)


class Main:
    def run(self) -> None:
        n1 = Node(0, 0, FullyRestricted())
        n2 = Node(4, 0, RestrictedInY())
        n3 = Node(4, 6, FreeMoving(), NodalForce(100e3))
        el1 = Element(n1, n2, 2e11, 2300e-6)
        el2 = Element(n2, n3, 2e11, 2300e-6)
        el3 = Element(n1, n3, 2e11, 2300e-6)
        truss = Truss([el1, el2, el3], [n1, n2, n3])
        truss.set_nodal_displacements()
        print(truss.solve_for_displacements())
        plotter = Plotter(truss=truss)
        plotter.plot_truss()
        # print(truss.get_stiffness_matrix())
        # print("*******")
        # print(truss.get_free_dofs())
        # print(truss.dof_to_nodal_displacements_map)
        # truss.set_nodal_displacements()
        # truss.set_element_stresses()
        # print(truss.get_reactions())


if __name__ == "__main__":
    Main().run()
