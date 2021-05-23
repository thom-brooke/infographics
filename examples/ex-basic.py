#!/usr/bin/env python
"""Basic Donut Charts.
"""

from infographics import canvas, donuts

style = donuts.DonutStyle()

data = [ (25, "Fee", {}),
         (25, "Fi", {}),
         (25, "Fo", {}),
         (25, "Fum", {}),
]

chart = style.generate(data, title="Giant")

donuts.make_graphic(chart, "ex-basic.svg", width_cm=10)

         
