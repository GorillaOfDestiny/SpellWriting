from matplotlib import pyplot as plt
from spell_writing.glyph import Glyph

def matplotlib_draw(
        glyph: Glyph,
        ax=None,
        dot_color='k',
        dot_size=50,
        annotate_lines=False,
        line_color='darkred',
        cmap = 'magma',
        legend_fontsize = 10,
        legend_anchor = (1,0.75),
        show_name=False
    ):
    if ax is None:
        fig, ax = plt.subplots(1,1)
    else:
        fig = ax.figure
    
    ax.scatter(
        glyph.base[0,0],
        glyph.base[0,1],
        color = dot_color,
        marker = "o",
        s = dot_size
    )
    ax.scatter(
        glyph.base[1:,0],
        glyph.base[1:,1],
        color = dot_color,
        marker = "o",
        s = dot_size,
        facecolors='none'
    )
    for i, attr_lines in enumerate(glyph.lines):
        if annotate_lines:
            color = cmap(0.9*i/(glyph.spell.n_att))
        else:
            color = line_color
        labelled = False
        for j, line in enumerate(attr_lines):
            label = list(glyph.spell.attributes.keys())[i] if (labelled is False) and annotate_lines else None
            ax.plot(
                line[:,0],
                line[:,1],
                ls='-',
                lw=2,
                color=color,
                label=label
            )
    if annotate_lines:
        ax.legend(fontsize = legend_fontsize,bbox_to_anchor = legend_anchor)
    if show_name:
        ax.set_title(glyph.spell.__name__)


