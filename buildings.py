from math import sqrt
from typing import Tuple
from starbase_data import *


class Building:
    def __init__(self, building_type: str, amount: int, surface_area: int):
        self.building_type: str = building_type.title()
        self.amount: int = amount
        self.surface_area: int = surface_area

    def get_size(self) -> Tuple[int, int]:
        side_length: int = int(sqrt(self.surface_area))
        size: Tuple[int, int] = (side_length, side_length)
        return size


class Defence(Building):
    def __init__(self, building_type, amount, surface_area, radius):
        super().__init__(building_type, amount, surface_area)
        self.radius: int = radius


buildings: Dict[str, List[str]] = get_data("types")


def create_buildings(sb_lvl) -> Optional[Dict[str, Union[Building, Defence]]]:
    objects: Optional[Dict[str, Union[Building, Defence]]] = {}

    for type_of_building in buildings:
        for building in buildings[type_of_building]:
            if type_of_building == "building":
                try:
                    obj: Building = Building(building_type=building,
                                             amount=get_amount(lvl=sb_lvl,
                                                               building=building),
                                             surface_area=get_surface_area(building))
                    objects[building] = obj
                except KeyError:
                    pass
            else:
                try:
                    obj: Defence = Defence(building_type=building,
                                           amount=get_amount(lvl=sb_lvl,
                                                             building=building),
                                           surface_area=get_surface_area(building),
                                           radius=get_radius(building=building,
                                                             lvl=get_building_lvl(lvl=sb_lvl,
                                                                                  building=building)))
                    objects[building] = obj
                except KeyError:
                    pass
    return objects
