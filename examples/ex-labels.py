#!/usr/bin/env python
"""Basic Donut Chart.
"""

from infographics import canvas, donuts

style = donuts.DonutStyle()

data = [ (25, "Fee", {}),
         (25, "Fi", {}),
         (25, "Fo", {}),
         (25, "Fum", {}),
         (5, "smell", {}),
]

chart1 = style.generate(data, title="Giant1")

data[4] = (5, "smell", {"rotate":True})
chart2 = style.generate(data, title="Giant2")

data[4] = (5, "smell", {"rotate":True, "dx":-0.5})
chart3 = style.generate(data, title="Giant3")

page = canvas.Canvas(width=14, height=4)
page.add_graphic(chart1, x=0, width=4)
page.add_graphic(chart2, x=5, width=4)
page.add_graphic(chart3, x=10, width=4)

page.write("ex-labels.svg")

         
