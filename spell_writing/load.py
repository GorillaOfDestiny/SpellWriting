import json
import re
from typing import Literal, get_args
import pandas

from spell_writing.spell import Spell
from .attributes import DURATION_DAY, DURATION_HOUR, DURATION_INSTANTANEOUS, DURATION_MINUTE, DURATION_ROUND, DURATION_SPECIAL, DURATION_UNTIL_DISPELLED, RANGE_FEET, RANGE_MILE, AOEAttribute, Attributes, DurationAttribute, RangeAttribute

def _resolve_typing_literal(literal,index=0) -> str:
    return get_args(literal)[index].lower()

def range_to_attribute(range_string: str):
    range_string = range_string.lower()
    value = None
    if _resolve_typing_literal(RANGE_FEET) in range_string:
        units = _resolve_typing_literal(RANGE_FEET)
        value = int(range_string.split(' ')[0])
    elif _resolve_typing_literal(RANGE_MILE) in range_string:
        units = _resolve_typing_literal(RANGE_MILE)
        value = int(range_string.split(' ')[0])
    else:
        units = range_string
        
    return RangeAttribute(
        {
            'units': units,
            'value': value
        }
    )

def aoe_to_attribute(aoe_dict: dict):
    if aoe_dict is None:
        return AOEAttribute(
            {
                'value': None,
                'units': None
            }
        )
    return AOEAttribute({
        'units': aoe_dict['type'],
        'value': aoe_dict['size']
    })
    

def duration_to_attribute(duration_string: str):
    duration_string = duration_string.lower()
    up_to = False
    units = None
    value = None
    if 'up to' in duration_string:
        up_to=True
    if _resolve_typing_literal(DURATION_SPECIAL) in duration_string:
        units = _resolve_typing_literal(DURATION_SPECIAL)
    elif _resolve_typing_literal(DURATION_INSTANTANEOUS) in duration_string:
        units = _resolve_typing_literal(DURATION_INSTANTANEOUS)
    elif _resolve_typing_literal(DURATION_UNTIL_DISPELLED) in duration_string:
        units = _resolve_typing_literal(DURATION_UNTIL_DISPELLED)
    else:
        for duration_type in [DURATION_HOUR, DURATION_MINUTE, DURATION_DAY, DURATION_ROUND]:
            if _resolve_typing_literal(duration_type) not in duration_string:
                continue
            units = _resolve_typing_literal(duration_type)
            value = int(re.sub("[^0-9]", "", duration_string))
            break
    return DurationAttribute(
        {
            'units': units,
            'up_to': up_to,
            'value': value
        }
    )

def get_damage_type(spell_json):
    if 'damage' not in spell_json:
        return None

    if 'damage_type' not in spell_json['damage']:
        print(spell_json['name'], 'does not have damage_type', spell_json['damage'])
        return None
    
    return spell_json['damage']['damage_type']['index']

def parse_attributes(spell_json):
    return Attributes(
        {
            'level': spell_json['level'],
            'damage_type': get_damage_type(spell_json),
            'range': range_to_attribute(spell_json['range']),
            'aoe': aoe_to_attribute(spell_json.get('area_of_effect')),
            'duration': duration_to_attribute(spell_json['duration']),
            'school': spell_json['school']['index']
        }
    )


def parse_spell(spell_json):
    attributes = parse_attributes(spell_json)
    return Spell(attributes=attributes, name=spell_json['name'])

class SpellsJson:
    def __init__(self, json_path, transform=None):
        self.spells = []
        with open(json_path, encoding="utf-8") as f:
            for line in f.readlines():
                spell = json.loads(line)
                self.spells.append(spell)


    def __len__(self):
        return len(self.samples)

    def __getitem__(self, i):
        return self.spells[i]
    
    def get_dataframe(self,):
        return pandas.DataFrame.from_records(self.spells)


