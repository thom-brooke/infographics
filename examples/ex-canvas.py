#!/usr/bin/env python
"""Canvas with Charts.
"""

from infographics import canvas, donuts
from infographics.donuts import mk_wedge

style = donuts.DonutStyle(hole_size=0.4,
                          hole_color="darkseagreen",
                          title_color="yellow",
                          label_size=0.06,
                          label_color="black",
                          wedge_colors=("#909090", "#a0a0a0", "#b0b0b0", "#c0c0c0", "#d0d0d0", "#e0e0e0"),
                          start_angle=0,
)

data = [ mk_wedge(25, "Fee"),
         mk_wedge(25, "Fi"),
         mk_wedge(25, "Fo"),
         mk_wedge(25, "Fum"),
         mk_wedge(5, "smell", rotate=True, dx=0.5),
]

chart = style.generate(data, title="Giants")

page = canvas.Canvas(width=10, height=5, units="cm")
page.add_graphic(chart, width=5)
page.add_graphic(chart, x=7, y=2, width=3)
page.write("ex-canvas.svg")


         
