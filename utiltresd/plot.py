# 3d draw function
import numpy as np
#import plotly.plotly as py
import chart_studio.plotly as py
import plotly.graph_objects as go
from plotly.offline import init_notebook_mode, iplot
init_notebook_mode(connected=True)

# https://stackoverflow.com/questions/47230817/plotly-notebook-mode-with-google-colaboratory
# by Pratik Parmar

def enable_plotly_in_cell():
  import IPython
  from plotly.offline import init_notebook_mode
  display(IPython.core.display.HTML('''<script src="/static/components/requirejs/require.js"></script>'''))
  init_notebook_mode(connected=False)


# c=(105,127,155)
def plot_vol(vol, s=10, c=(106, 217, 158), show_grid=False):
    if vol.dtype != np.bool:
        vol = vol > 0

    pc = volume_to_point_cloud(vol)
    plot3d(pc, s, c, show_grid)

def plot3d(verts, s=10, c=(106, 217, 158), show_grid=False):
    enable_plotly_in_cell()
    x, y, z = zip(*verts)
    color = f'rgb({c[0]}, {c[1]}, {c[2]})'
    trace = go.Scatter3d(
        x=x, y=y, z=z,
		mode='markers',
        marker=dict(
            size=s,
            color=color,
            line=dict(
                #color='rgba(217, 217, 217, 0.14)',
				color='rgba(125, 128, 137, 1)',
                width=0.5
            ),
            opacity=1
        )
    )
    data = [trace]
    layout = go.Layout(
        margin=dict(l=0, r=0, b=0, t=0),
        scene=dict(
          xaxis=dict(visible=False),
          yaxis=dict(visible=False),
          zaxis=dict(visible=False),),
    )
    fig = go.Figure(data=data, layout=layout)
    iplot(fig)



def volume_to_point_cloud(vol):
    """ vol is occupancy grid (value = 0 or 1) of size vsize*vsize*vsize
        return Nx3 numpy array.
    """
    vsize = vol.shape[0]
    assert(vol.shape[1] == vsize and vol.shape[1] == vsize)
    points = []
    for a in range(vsize):
        for b in range(vsize):
            for c in range(vsize):
                if vol[a,b,c] == 1:
                    points.append(np.array([a,b,c]))
    if len(points) == 0:
        return np.zeros((0,3))
    points = np.vstack(points)
    
    return points
	
	
def plot_reconstruction(vol1, vol2, s=10, c1=(106, 217, 158), c2=(182,49,62), show_grid=False):
    enable_plotly_in_cell()

    if vol1.dtype != np.bool:
        vol1 = vol1 > 0
    if vol2.dtype != np.bool:
        vol2 = vol2 > 0
        
    color1 = f'rgb({c1[0]}, {c1[1]}, {c1[2]})'
    color2 = f'rgb({c2[0]}, {c2[1]}, {c2[2]})'
    vol2 = np.logical_xor(vol2, vol1)
    pc1 = volume_to_point_cloud(vol1)
    pc2 = volume_to_point_cloud(vol2)
    x1, y1, z1 = zip(*pc1)
    x2, y2, z2 = zip(*pc2)
    trace1 = go.Scatter3d(
        x=x1, y=y1, z=z1,
        mode='markers',
        marker=dict(
            size=s,
            color=color1,
            line=dict(
                color='rgba(125, 128, 137, 1)',
                width=0.5
            ),
            opacity=1
        )
    )
    trace2 = go.Scatter3d(
        x=x2, y=y2, z=z2,
        mode='markers',
        marker=dict(
            size=9,
            color=color2,
            line=dict(
                color='rgba(113, 166, 33, .9)',
                width=0.5
            ),
            opacity=1
        )
    )
    data = [trace1, trace2]
    layout = go.Layout(margin=dict(l=0, r=0, b=0, t=0), 
                       scene = dict(
                               xaxis=dict(visible=False),
                               yaxis=dict(visible=False),
                               zaxis=dict(visible=False)),
                       showlegend=False)
    fig = go.Figure(data=data, layout=layout)
    iplot(fig)