import json
from typing import Dict, Union, List, Optional


class NoSuchData(Exception):
    pass


def get_data(datatype) -> Optional[Dict]:
    try:
        with open(f"res/buildings/{datatype}.json") as data_file:
            data: Dict = json.load(data_file)
        return data
    except FileNotFoundError:
        print("Wrong data type!")


def get_amount(lvl: int, building: str) -> int:
    star_base_data: Dict[str, int] = get_data("amount")[str(lvl)]
    amount: Union[int, List[int]] = star_base_data[building.title()]
    if isinstance(amount, list):
        amount: int = amount[0]
    return amount


def get_building_lvl(lvl: int, building: str) -> int:
    star_base_data: Dict[str, int] = get_data("amount")[str(lvl)]
    data: Union[int, List[int]] = star_base_data[building.title()]
    if isinstance(data, list):
        max_lvl: int = data[1]
        return max_lvl
    else:
        raise NoSuchData(f"Information about maximum level is not provided for {building.title()}")


def get_radius(building: str, lvl: int) -> int:
    radius_data: Dict[str, int] = get_data("radius")[building.title()]
    radius: int = radius_data[str(lvl)]
    return radius


def get_surface_area(building: str) -> int:
    area: int = get_data("surface")[building.title()]
    return area
