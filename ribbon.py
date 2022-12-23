from chart_studio import plotly as py
#import plotly.express as py# load data
from plotly.offline import iplot
import plotly.graph_objs as go

import urllib.request
import numpy as np


url = "https://raw.githubusercontent.com/plotly/datasets/master/spectral.csv"
f = urllib.request.urlopen(url)
#f = open("log_20221218_2000.txt", "r")
spectra=np.loadtxt(f, delimiter=',')

traces = []
y_raw = spectra[:, 0] # wavelength
sample_size = spectra.shape[1]-1
for i in range(1, sample_size):
    z_raw = spectra[:, i]
    x = []
    y = []
    z = []
    ci = int(255/sample_size*i) # ci = "color index"
    for j in range(0, len(z_raw)):
        z.append([z_raw[j], z_raw[j]])
        y.append([y_raw[j], y_raw[j]])
        x.append([i*2, i*2+1])
    traces.append(dict(
        z=z,
        x=x,
        y=y,
        colorscale=[ [i, 'rgb(%d,%d,255)'%(ci, ci)] for i in np.arange(0,1.1,0.1) ],
        showscale=False,
        type='surface',
    ))

fig = { 'data':traces, 'layout':{'title':'Ribbon Plot'} }
py.iplot(fig, filename='ribbon-plot-python')
