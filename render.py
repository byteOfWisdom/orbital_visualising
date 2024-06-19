#!/usr/bin/env python3

from sys import argv
import numpy as np
from matplotlib import pyplot as plt
import plotly.graph_objects as go
import numba


def main():
    data = np.transpose(np.loadtxt(argv[1]))

    upper = max(data[3])
    lower = min(data[3])
    diff = upper - lower

    fig = go.Figure(data=go.Isosurface(
        x=data[0],
        y=data[1],
        z=data[2],
        value=data[3],
        opacity=0.6,
        surface_count = 4,
        colorscale="teal",
#        isomin=0.005,
        isomin=lower + 0.1 * diff,
        isomax=upper - 0.2 * diff,
        caps=dict(x_show=False, y_show=False)
    ))

    camera = dict(
        eye=dict(x=0.8, y=0.8, z=1.9 )if int(argv[3]) != 0 else dict(x=1.3, y=1.3, z=0.6),
        center=dict(x=0, y=0, z=0)
    )
    title = argv[2]
    fig.update_layout(scene_camera=camera, title=title)
    #fig.show()
    fig.write_image(argv[1].split('.')[0] + ".png", scale=2)


if __name__ == "__main__":
    main()
