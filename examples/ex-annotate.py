#!/usr/bin/env python
"""Chart and Canvas Annotations
"""

from infographics import canvas, donuts
from infographics.donuts import mk_wedge
import xml.etree.ElementTree as ET

style = donuts.DonutStyle(start_angle=0)

data = [ mk_wedge(25, "Fee"),
         mk_wedge(25, "Fi"),
         mk_wedge(25, "Fo"),
         mk_wedge(25, "Fum"),
         mk_wedge(5, "smell", rotate=True, dx=0.5),
]

chart = style.generate(data, title="Giant")
# add a background (_beneath_ the chart):
bg = ET.Element("rect")
bg.set("width", str(style.size))
bg.set("height", str(style.size))
bg.set("fill", "lavender")
chart.insert(0, bg)

page = canvas.Canvas(width=10, height=5, units="cm", px_scale=100)
page.add_graphic(chart, width=page.width/2)
page.add_graphic(chart, x=(0.7*page.width), y=(0.4*page.height), width=(0.3*page.width))
# add a title
tag = ET.Element("text")
tag.set("font-family", "sans-serif")
tag.set("font-size", str(0.2*page.height))
tag.set("fill", "red")
tag.set("x", str(0.6*page.width))
tag.set("y", str(0.25*page.height))
tag.text = "Fancy"
page.svg.append(tag)

page.write("ex-annotate.svg")


         
