from enum import Enum
from typing import Union, Dict


class AttributePercentage(Enum):
    FULL = 100
    THREE_QUARTER = 75
    HALF = 50
    ONE_QUARTER = 25
    VERY_LOW = 1
    EMPTY = 0

class DamagePercentage(Enum):
    VERY_HIGH = 60
    HIGH = 40
    MODERATE = 20
    LIGHT = 5
    VERY_LIGHT = 1
    NONE = 0

def get_gui_data(percentage:float, dictionary:Dict,category: Union[AttributePercentage, DamagePercentage]):
    for enum in list(category):
        if enum.value <= percentage:
            value = dictionary[enum]
            return value