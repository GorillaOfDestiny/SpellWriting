from typing import Dict, List, TypedDict
from spell_writing.attributes import Attributes

class Spell:
    def __init__(self, attributes: Attributes, name="Unknown Spell"):
        self.attributes: Attributes = Attributes(attributes)
        self.__name__ = name
    
    @property
    def n_att(self,):
        return len(self.attributes)
    
    @property
    def n_pos(self,):
        return 2*len(self.attributes) + 1