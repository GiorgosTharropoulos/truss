from dataclasses import dataclass, field

from models.truss import Truss


@dataclass
class Spacing:
    __truss: Truss
    spacing_map: dict[int, float] = field(init=False)

    def __get_longest_elements_length(self) -> float:
        """
        Returns the length of the longest element of the truss.
        """
        element_lengths = [
            float(element.get_length()) for element in self.__truss.elements
        ]
        return max(element_lengths)

    def __percentage_to_longest(self, percentage: float) -> float:
        """
        Returns the absolute units of the longest element's length.
        """
        return percentage * self.__get_longest_elements_length()

    def __post_init__(self) -> None:
        """
        Initializes the spacing map.
        """
        self.spacing_map = {
            percentage: self.__percentage_to_longest(percentage) / 100
            for percentage in range(0, 210, 10)
        }
