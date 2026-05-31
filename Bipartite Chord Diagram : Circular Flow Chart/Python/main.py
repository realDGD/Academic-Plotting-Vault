import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pycirclize import Circos

# Random seed to replicate rng(2)
np.random.seed(2)
# MATLAB rand() F-contiguous
rand_arr = np.random.rand(55)
data_mat = np.floor(rand_arr * 7).astype(int) + 1
data_mat = data_mat.reshape((11, 5), order='F')

row_names = ['Bartomella','Bradyrhizobium','Dysgomonas','Enterococcus',
           'Lactococcus','norank','others','Pseudomonas','uncultured',
           'Vibrionimonas','Wolbachia']
col_names = ['Fly','Beetle','Leaf','Soil','Waxberry']

matrix_df = pd.DataFrame(data_mat, index=row_names, columns=col_names)

# Colors
cmap = {
    'Fly': '#c6cf85',
    'Beetle': '#717862',
    'Leaf': '#943a74',
    'Soil': '#7267ac',
    'Waxberry': '#040000',
    'Bartomella': '#95afc8',
    'Bradyrhizobium': '#1c2a53',
    'Dysgomonas': '#172989',
    'Enterococcus': '#a1cb36',
    'Lactococcus': '#0a351b',
    'norank': '#040000',
    'others': '#daeddf',
    'Pseudomonas': '#635368',
    'uncultured': '#80b862',
    'Vibrionimonas': '#172f2e',
    'Wolbachia': '#d13b12'
}

# The gaps are between the two groups.
sectors_order = col_names[::-1] + row_names[::-1]
space = [1, 1, 1, 1, 6, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 6]

def link_kws_handler(r_name, c_name):
    # Chords end at r=81 to decrease the gap slightly
    return {"fc": cmap[c_name], "alpha": 0.5, "ec": "none", "r1": 81, "r2": 81}

circos = Circos.chord_diagram(
    matrix_df,
    space=space,
    cmap=cmap,
    order=sectors_order,
    r_lim=(85, 95),  # Node is thick: 85 to 95
    ticks_interval=None,
    label_kws=dict(r=105, orientation="vertical", size=15, fontname='Cambria'),
    link_kws_handler=link_kws_handler
)

for sector in circos.sectors:
    # Outer block (Node)
    track = sector.tracks[0] if sector.tracks else sector.add_track((85, 95))
    
    # Remove borders from the node patches
    for patch in track.patches:
        patch.set_edgecolor("none")
        patch.set_linewidth(0)
    
    # Separate outer track for ticks and axis line
    tick_track = sector.add_track((97, 98))
    
    # Draw tick axis line at r=98
    x = np.linspace(sector.start, sector.end, 100)
    y = np.full(100, 98)
    tick_track.line(x, y, color="black", lw=1)
    
    if sector.name in col_names:
        vals = [matrix_df.loc[r, sector.name] for r in row_names[::-1]]
    else:
        vals = [matrix_df.loc[sector.name, c] for c in col_names[::-1]]
        
    cum_vals = [0] + list(np.cumsum(vals))
    # Draw non-uniform ticks outward from r=98
    tick_track.xticks(cum_vals, labels=[""] * len(cum_vals), outer=True)

fig = circos.plotfig()
fig.savefig("/Users/dgd/Potable/Files/Code/Python/Python_Painting_Vault/Bipartite Chord Diagram : Circular Flow Chart/Python/result.png", dpi=300)
