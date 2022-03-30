import pandas as pd
import networkx
import numpy as np
import json
import os
import sys
from bokeh.io import save
from bokeh.models import Range1d, Circle, MultiLine, NodesAndLinkedEdges, TapTool, Plot, HoverTool, OpenURL
from bokeh.plotting import figure, from_networkx, output_file
from bokeh.events import Tap
import warnings
warnings.filterwarnings("ignore")

os.chdir(os.path.dirname(__file__))
current_dir = os.getcwd()
f = open(current_dir + "/" + 'output.json', encoding='utf-8')
data = json.load(f)
dt = pd.DataFrame(columns=list('AB'))

for i in data:
    if len(i['friends']) == 0:
        pass
    else:
        for j in i['friends']:
            dt = dt.append({'A': i['_id'], 'B' : j}, ignore_index=True)

G = networkx.from_pandas_edgelist(dt, 'A', 'B')
degrees = dict(networkx.degree(G))
networkx.set_node_attributes(G, name='degree', values=degrees)

names = {}
ids = {}
link = {}

for i in data:
    names[i["_id"]] = str(i['firstName'] + " " + i['lastName'])
    ids[i["_id"]] = i['id']
    link[i["_id"]] = "https://vk.com/id" + str(i['id'])

# attributes
networkx.set_node_attributes(G, name='name', values=names)
networkx.set_node_attributes(G, name='ids', values=ids)
networkx.set_node_attributes(G, name='link', values=link)

#Title
title = 'График связей'

#Establish which categories will appear when hovering over each node
TOOLTIPS = [
        ('Имя', "@name"),
        ("ID", "@ids"),
        ("Кол-во связей", "@degree")
]

#Choose colors for node and edge highlighting
node_highlight_color = 'white'
edge_highlight_color = 'red'

#Create a plot — set dimensions, toolbar, and title
plot = figure(x_range=Range1d(-100.1, 100.1), y_range=Range1d(-100.1, 100.1), title=title, plot_width=800, plot_height=800, tools="pan,wheel_zoom,save,reset", active_scroll='wheel_zoom')

#Tap
plot.add_tools(HoverTool(tooltips=TOOLTIPS), TapTool())
url = "@link"
taptool = plot.select(type=TapTool)
taptool.callback = OpenURL(url=url)

#Create a network graph object with spring layout
network_graph = from_networkx(G, networkx.spring_layout, scale=100, center=(0, 0))

#Set node size and color
network_graph.node_renderer.glyph = Circle(size=5, fill_color='skyblue')

#Set edge opacity and width
network_graph.edge_renderer.glyph = MultiLine(line_alpha=0.05, line_width=1)

#Set edge highlight colors
network_graph.edge_renderer.selection_glyph = MultiLine(line_color=edge_highlight_color, line_width=2)
network_graph.edge_renderer.hover_glyph = MultiLine(line_color=edge_highlight_color, line_width=2)

#Set node highlight colors
network_graph.node_renderer.hover_glyph = Circle(fill_color=node_highlight_color, line_width=2)
network_graph.node_renderer.selection_glyph = Circle(fill_color=node_highlight_color, line_width=2)

#Highlight nodes and edges
network_graph.selection_policy = NodesAndLinkedEdges()
network_graph.inspection_policy = NodesAndLinkedEdges()

#Add network graph to the plot
plot.renderers.append(network_graph)

output_file("plot.html")
save(plot, title='Connections')
print('End')