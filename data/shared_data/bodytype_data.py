# class BodyType(Enum):
#     NORMAL = auto()
#     SCRAWNY = auto()
#     OBESE = auto()
#     TINY = auto()
#     SMALL = auto()
#     LARGE = auto()
#     GARGANTUAN = auto()
#
from data.shared_data.types_data import BodyType

bodytype_data = {
    'normal': {
        'type': BodyType.NORMAL
    },
    'weak_1': {
        'type': BodyType.SCRAWNY,
        'dmg_mod_multipl': 0.6,
        'av_mod_multipl': 0.8
    },
    'weak_2': {
        'type': BodyType.TINY,
        'hp_mod_multipl': 0.5,
        'dmg_mod_multipl': 0.5
    },
    'weak_3': {
        'type': BodyType.SMALL,
        'hp_mod_multipl': 0.9,
        'dmg_mod_multipl': 0.9
    },
    'strong_1': {
        'type': BodyType.LARGE,
        'hp_mod_multipl': 1.2,
        'dmg_mod_multipl': 1.2
    },
    'strong_2': {
        'type': BodyType.OBESE,
        'hp_mod_multipl': 1.5
    },
    'super_1': {
        'type': BodyType.GARGANTUAN,
        'dmg_mod_multipl': 2,
        'hp_mod_multipl': 2.5
    }
}