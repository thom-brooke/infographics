#!/usr/bin/env python
"""Basic Donut Chart.
"""

from infographics import canvas, donuts

style = donuts.DonutStyle()

data = [ (25, "Fee", {}),
         (25, "Fi", {}),
         (25, "Fo", {}),
         (25, "Fum", {}),
         (5, "smell", {"rotate":True, "dx":-0.5}),
]

chart = style.generate(data, title="Giant")

donuts.make_graphic(chart, "ex-labels.svg", width_cm=10)

         
