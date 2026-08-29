from enum import StrEnum
import os
from pathlib import Path
from typing import Literal, Union, TypedDict
from typing_extensions import NotRequired

# TODO: Add a better way to use attributes
# 1. Creating an attribute and attaching a value should be easy in code
# 2. Looking up the value's order should be easy 
# 3. This should integrate to the Spell object

def get_default_ordering_path():
    return Path(os.path.dirname(__file__)) / "attribute_ordering"

class Unset:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    def __repr__(self):
        return "<UNSET>"

# Attributes
class AttributesEnum(StrEnum):
    LEVEL = "level"
    SCHOOL = "school"
    RANGE = "range"
    DURATION = "duration"
    DAMAGE_TYPE = "damage_type"
    AOE = "aoe"

# Schools
SCHOOL_ABJURATION = Literal["abjuration"]
SCHOOL_CONJURATION = Literal["conjuration"]
SCHOOL_DIVINATION = Literal["divination"]
SCHOOL_ENCHANTMENT = Literal["enchantment"]
SCHOOL_EVOCATION = Literal["evocation"]
SCHOOL_ILLUSION = Literal["illusion"]
SCHOOL_NECROMANCY = Literal["necromancy"]
SCHOOL_TRANSMUTATION = Literal["transmutation"]

SCHOOL_TYPE = Literal[
    SCHOOL_ABJURATION,
    SCHOOL_CONJURATION,
    SCHOOL_DIVINATION,
    SCHOOL_ENCHANTMENT,
    SCHOOL_EVOCATION,
    SCHOOL_ILLUSION,
    SCHOOL_NECROMANCY,
    SCHOOL_TRANSMUTATION,
]


# Ranges
RANGE_FEET=Literal['feet']
RANGE_MILE=Literal['mile']
RANGE_SELF=Literal['self']
RANGE_TOUCH=Literal['touch']
RANGE_UNLIMITED=Literal['unlimited']
RANGE_SPECIAL=Literal['special']
RANGE_SIGHT=Literal['sight']

RANGE_TYPE = Literal[RANGE_FEET, RANGE_MILE, RANGE_SELF, RANGE_TOUCH, RANGE_UNLIMITED, RANGE_SPECIAL, RANGE_SIGHT]

# Durations
DURATION_HOUR=Literal["hour"]
DURATION_MINUTE=Literal["minute"]
DURATION_DAY=Literal["day"]
DURATION_ROUND=Literal["round"]
DURATION_SPECIAL=Literal["special"]
DURATION_INSTANTANEOUS=Literal['Instantaneous']
DURATION_UNTIL_DISPELLED = Literal['until dispelled']

DURATION_TYPE = Literal[
    DURATION_HOUR,
    DURATION_MINUTE,
    DURATION_DAY,
    DURATION_ROUND,
    DURATION_SPECIAL,
    DURATION_INSTANTANEOUS,
    DURATION_UNTIL_DISPELLED
]

# Damage
DAMAGE_ACID=Literal["acid"]
DAMAGE_BLUDGEONING=Literal["bludgeoning"]
DAMAGE_COLD=Literal["cold"]
DAMAGE_FIRE=Literal["fire"]
DAMAGE_FORCE=Literal["force"]
DAMAGE_LIGHTNING=Literal["lightning"]
DAMAGE_NECROTIC=Literal["necrotic"]
DAMAGE_PIERCING=Literal["piercing"]
DAMAGE_POISON=Literal["poison"]
DAMAGE_PSYCHIC=Literal["psychic"]
DAMAGE_RADIANT=Literal["radiant"]
DAMAGE_SLASHING=Literal["slashing"]
DAMAGE_THUNDER=Literal["thunder"]

DAMAGE_TYPE = Literal[
    DAMAGE_ACID,
    DAMAGE_BLUDGEONING,
    DAMAGE_COLD,
    DAMAGE_FIRE,
    DAMAGE_FORCE,
    DAMAGE_LIGHTNING,
    DAMAGE_NECROTIC,
    DAMAGE_PIERCING,
    DAMAGE_POISON,
    DAMAGE_PSYCHIC,
    DAMAGE_RADIANT,
    DAMAGE_SLASHING,
    DAMAGE_THUNDER,
]

AOE_CONE=Literal['cone']
AOE_CUBE=Literal['cube']
AOE_CYLINDER=Literal['cylinder']
AOE_LINE=Literal['line']
AOE_SPHERE=Literal['sphere']

AOE_TYPE = Literal[
    AOE_CONE,
    AOE_CUBE,
    AOE_CYLINDER,
    AOE_LINE,
    AOE_SPHERE,
]
class RangeAttribute(TypedDict):
    value: Union[None, int]
    units: RANGE_TYPE

class DurationAttribute(TypedDict):
    value: Union[None, int]
    up_to: NotRequired[bool] = False
    units: DURATION_TYPE

class AOEAttribute(TypedDict):
    value: Union[None, int]
    units: AOE_TYPE | None

class Attributes(TypedDict):
    level: NotRequired[int | None | Unset] = Unset()
    school: NotRequired[SCHOOL_TYPE | None | Unset] = Unset()
    range: NotRequired[RangeAttribute | Unset] = Unset()
    duration: NotRequired[DurationAttribute | Unset] = Unset()
    damage_type: NotRequired[DAMAGE_TYPE | None | Unset] = Unset()
    aoe: NotRequired[AOEAttribute | Unset] = Unset()