import numpy as np
import pytest
from src.models.element import Element
from src.models.node import Node


@pytest.fixture
def default_rod():
    node1 = Node(x=0, y=0)
    node2 = Node(x=12 * 16, y=12 * 12)
    return Element(node1=node1, node2=node2, area=10, youngs_modulus=3e4)


def test_rod_length(default_rod: Element):
    assert default_rod.get_length() == 240.0


def test_rod_sin(default_rod: Element):
    assert default_rod.sin() == 0.6


def test_rod_cos(default_rod: Element):
    assert default_rod.cos() == 0.8


def test_rod_stiffness_matrix(default_rod: Element):
    matrix = [
        800.0,
        600.0,
        -800.0,
        -600.0,
        600.0,
        450.0,
        -600.0,
        -450.0,
        -800.0,
        -600.0,
        800.0,
        600.0,
        -600.0,
        -450.0,
        600.0,
        450.0,
    ]
    assert np.allclose(
        default_rod.get_global_stiffness_matrix(),
        np.array(matrix).reshape(4, 4),
    )
