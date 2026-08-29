from typing import Callable

import numpy as np
from spell_writing import bases, line_shapes
from spell_writing.spell import Spell
from spell_writing.rotationally_symmetric_encoding import Encoding, AttributeOrderDatabase

def default_encoding():
    return Encoding(database=AttributeOrderDatabase.from_txt_directory())

def to2d(vals):
    x_vals, y_vals = vals
    return np.hstack([
        np.array(x_vals).reshape(-1,1),
        np.array(y_vals).reshape(-1,1)]
    ).reshape(-1,2)

class Glyph:
    def __init__(
        self,
        spell: Spell,
        encoding: Encoding = None,
        base_fn=None,
        base_kwargs=None,
        lines_fn=None,
        lines_kwargs=None
    ):
        # Spell Graph:
        self.spell = spell
        self.encoding = encoding if encoding is not None else default_encoding()
        self.adjacency_matrix = self.encoding.encode_spell(self.spell)

        # Coordinates:
        self.base_fn = base_fn if base_fn is not None else bases.polygon
        self.lines_fn = lines_fn if lines_fn is not None else line_shapes.straight
        self.base_kwargs = base_kwargs if base_kwargs is not None else {}
        self.lines_kwargs = lines_kwargs if lines_kwargs is not None else {}

        self.base = None
        self.lines = None

        self.init_glyph()
    
    def init_glyph(self,):
        self.base = to2d(
            self.base_fn(
                self.spell.n_pos,
                **self.base_kwargs
            )) #
        
        
        all_lines = []
        for i in range(self.spell.n_att):
            k = i + 1
            attr_lines = []
            for j, elem in enumerate(self.adjacency_matrix[i]):
                if elem == 1:
                    P = self.base[j]
                    Q = self.base[(j+k) % self.spell.n_pos]
                    attr_lines.append(to2d(self.lines_fn(P,Q,*self.lines_kwargs)))
            all_lines.append(attr_lines)

        self.lines = all_lines

        
    