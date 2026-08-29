import os
from typing import List
import typing

import numpy as np
from spell_writing import necklaces
from spell_writing.attributes import RANGE_FEET, RANGE_MILE, AttributesEnum, DURATION_TYPE, RANGE_TYPE, get_default_ordering_path
from spell_writing.spell import Spell

from spell_writing.attributes import DURATION_DAY, DURATION_HOUR, DURATION_INSTANTANEOUS, DURATION_MINUTE, DURATION_ROUND, DURATION_SPECIAL, AOEAttribute, Attributes, DurationAttribute, Unset

from spell_writing.attributes import DURATION_UNTIL_DISPELLED

def parse_txt_attribute_file(path):
    with open(path,"r") as f:
        data = f.readlines()
        f.close()
    data = [d.replace("\n","").lower() for d in data]
    return {value: i for i,value in enumerate(data)}


def attribute_string_unit_plural(value, units):
    if value > 1 and units != 'feet':
        unit_name = f'{units}{"s" if value > 1 else ""}'
    elif value == 1 and units == 'feet':
        unit_name = 'foot'
    else:
        unit_name = units
    return f'{value} {unit_name}'


def list_of_literal(literals: list):
    return [s.lower() for s in typing.get_args(typing.Literal[*literals])]

class AttributeOrderDatabase:
    def __init__(self, attributes_order):
        self.attributes_order = attributes_order
    
    def parse_item(self, attribute_type: AttributesEnum, attribute):
        match attribute_type:
            case AttributesEnum.AOE:
                if attribute["value"] is None:
                    return "None"
                return f'{attribute["units"]} ({attribute["value"]})'
            case AttributesEnum.DAMAGE_TYPE:
                if attribute is None:
                    return "None"
                return attribute
            case AttributesEnum.DURATION:
                if attribute["units"] in list_of_literal([DURATION_INSTANTANEOUS, DURATION_SPECIAL,DURATION_UNTIL_DISPELLED]):
                    return attribute["units"]
                elif attribute["units"] in list_of_literal([DURATION_HOUR, DURATION_DAY, DURATION_ROUND, DURATION_MINUTE]):
                    return f'{"Up to " if attribute["up_to"] else ""}{attribute_string_unit_plural(attribute["value"], attribute["units"])}'
            case AttributesEnum.LEVEL:
                return  str(attribute) if attribute is not None else "Blank"
            
            case AttributesEnum.RANGE:
                if attribute['units'] in list_of_literal([RANGE_FEET, RANGE_MILE]):
                    return attribute_string_unit_plural(attribute["value"], attribute["units"]) if attribute["value"] is not None else "Blank"
                else:
                    return attribute["units"]

            case AttributesEnum.SCHOOL:
                if attribute is None:
                    return 'Blank'
                else:
                    return attribute


    def __getitem__(self, key):
        attribute_type: AttributesEnum = key[0]
        item = key[1]
        value = self.parse_item(attribute_type, item)
        return self.attributes_order[attribute_type][value.lower() if value is not None else "none"]
    

    @classmethod
    def from_txt_directory(cls, txt_file_base=None):
        txt_file_base = txt_file_base if txt_file_base is not None else get_default_ordering_path()
        aoe_txt_file = os.path.join(txt_file_base, r"area_types.txt")
        dmg_txt_file = os.path.join(txt_file_base,r"damage_types.txt")
        dur_txt_file = os.path.join(txt_file_base,r"duration.txt")
        lvl_txt_file = os.path.join(txt_file_base,r"levels.txt")
        ran_txt_file = os.path.join(txt_file_base,r"range.txt")
        sch_txt_file = os.path.join(txt_file_base,r"school.txt")
        txt_files = {
            AttributesEnum.LEVEL: lvl_txt_file,
            AttributesEnum.SCHOOL: sch_txt_file,
            AttributesEnum.DAMAGE_TYPE: dmg_txt_file,
            AttributesEnum.AOE: aoe_txt_file,
            AttributesEnum.RANGE: ran_txt_file,
            AttributesEnum.DURATION: dur_txt_file
        }
        return cls({
            attribute: parse_txt_attribute_file(path) for attribute,path in txt_files.items()
        })

def get_attribute(current_attribute: AttributesEnum, attributes: Attributes):
    match current_attribute:
        case AttributesEnum.LEVEL:
            return attributes['level']
        case AttributesEnum.AOE:
            return attributes['aoe']
        case AttributesEnum.DAMAGE_TYPE:
            return attributes['damage_type']
        case AttributesEnum.DURATION:
            return attributes['duration']
        case AttributesEnum.SCHOOL:
            return attributes['school']
        case AttributesEnum.RANGE:
            return attributes['range']
        
class Encoding:
    DEFAULT_ORDER = [
        AttributesEnum.LEVEL,
        AttributesEnum.SCHOOL,
        AttributesEnum.DAMAGE_TYPE,
        AttributesEnum.AOE,
        AttributesEnum.RANGE,
        AttributesEnum.DURATION,
    ]

    def __init__(self, database: AttributeOrderDatabase,n=13):
        self.attribute_order_database = database
        self.n = n
        self.binary_value = necklaces.default_generation(n=n)
    
    def encode_attribute(self, attribute: AttributesEnum, value, n=13):
        if n != self.n:
            self.binary_value = necklaces.default_generation(n=n)
        i = self.attribute_order_database[attribute, value]
        return self.binary_value[i]

    def encode_spell(self, spell: Spell, order: List[AttributesEnum]=DEFAULT_ORDER):
        binary_matrix = np.zeros((spell.n_att,spell.n_pos),dtype = int)

        i = 0
        for current in order:
            value = get_attribute(current, spell.attributes)
            if value is Unset:
                continue
            binary_matrix[i] = self.encode_attribute(current, value)
            i += 1
        
        return binary_matrix