"""Module  to generate 'donut' (and 'pie') charts as SVG.

A donut chart is just a pie chart with a central "hole".  We treat the pie chart
as a degenerate case -- a donut chart with a zero-width hole -- which is kind of 
backwards.

This module is written in/for Python3, although it can probably be used in Python2
with little modification.  The biggest incompatibility is string formatting.

All depenedencies are available in the standard distribution:

  * math
  * xml.dom
  * xml.etree.ElementTree

"""

import xml.etree.ElementTree as ET
from math import sin, cos, pi, degrees

from .chart import Point, progression
from .canvas import Canvas

class DonutStyle:
    """Class to create "donut" charts -- pie charts with a hole in the middle.

    A `DonutStyle` object defines the _style_ of a chart, not an actual chart.
    Create an actual chart (as an SVG element) from some data using `generate()`.

    In general, `DonutStyle` has reasonable defaults for charts with 5 - 10 wedges, 
    and labels/titles of one word (not too long).  Much of this can be tailored
    in the constructor.
    """

    def __init__(self, **kwargs):
        """Create a style for donut charts.

        Keyword Arguments:
        border_size  -- relative thickness of wedge/hole/chart borders (default 0.01)
        hole_size    -- relative width of central "donut hole" (default 0.3)
        title_size   -- relative size (em-space) of title font (default 0.08)
        label_size   -- relative size (em-space) of label font (default 0.08)
        border_color -- stroke for wedge, hole, and boundary outlines (default "white")
        hole_color   -- fill for donut hole (default "silver")
        title_color  -- for title font (default "black")
        label_color  -- for label font (default "white")
        wedge_colors -- list-like for wedge fill color sequence
        init_angle   -- start angle for first wedge, in radians. (0 is "East"; -pi/2 is "North")

        The "size" arguments are relative to the overall chart size.  So, for example, 
        a hole_size of 0.25 would be 1/4 of the chart width (or height; it's square).  
        A title_size of 0.1 would be 1/10 of the chart width (which may be a little big).

        The "color" arguments are absolute.  The safest choice is to use one of the 147 SVG 
        names (e.g., "white", "pink").  But you should also be able to other HTML and CSS mechanisms; 
        for example, by rgb (e.g., "rgb(100, 0, 0)" or by hex value (e.g., "#A9A9A9").

        The wedge_colors is the color progression for each subsequent wedge in the chart,
        starting with the first.  If there are more wedges than colors, the cycle will repeat.
        The default wedge colors are: ("red", "blue", "green", "orange", "teal", "brown", "magenta", "cyan").

        The init_angle sets the position of the first wedge in the chart.  By default this is 
        due North (or noon): -pi/2.  It may be more pleasing to start due East (at 0).
        """
        # The overall chart _size is arbitrary, for internal convenience.
        # All customization is relative to this, so its actual value is immaterial.
        self._size = 1000 # units, width and height

        # Sizes relative to self.size
        self.border_size = 0.01
        self.hole_size = 0.3
        self.title_size = 0.08
        self.label_size = 0.08

        # absolute values
        self.border_color = "white"
        self.hole_color = "silver"
        self.title_color = "black"
        self.label_color = "white"
        self.wedge_colors = ("red", "blue", "green", "orange", "teal", "brown", "magenta", "cyan")
        self.init_angle = -pi/2 # radians. 0 = East, so -pi/2 = North/noon
        
        for k,v in kwargs.items():
            if hasattr(self, k):
                setattr(self, k, v)
            # perhaps we should warn about use of undefined settings?

        # librsvg (what GNOME and gThumb and others use to render SVG) is picky about the font class string.
        # It _doesn't_ like a composite "font" attribute (it wants it broken up into -family, -weight, etc.).
        #
        # Also, librsvg doesn't process the "dominant-baseline" at all.  Which means the labels will all be
        # 1/2 ex too "high".  Inkscape, emacs, chrome, and other SVG renderers don't seem to have this problem.
        # This is probably okay for previews, but when using librsvg for final rendering, you may want
        # to add some x/y nudge to the labels.
        #
        # @todo: Alternatively, don't use the dominant-baseline at all, and compute the label center
        # point manually, based on label font size and the rotation angle.  What a PITA.
        # Since virtually _everyone_ else does it right, this is pretty low on the priority list.
        
        self.fontspec = ".{cls} {{font-family:sans-serif;font-weight:bold;font-size:{size}px;dominant-baseline:middle;text-anchor:middle;stroke:none;fill:{color};}}"
        return

    # __repr__

    # __str__
    
    def generate(self, dataset, title=""):
        """Make a chart in this style using the given `dataset` of values.
        
        Arguments:
        dataset -- A list-like object consisting of one "wedge" per element

        Keyword Arguments:
        title -- The title of the chart, placed in the donut "hole" (default "")

        This will create an SVG element (as xml.etree.ElementTree.Element) 
        containing the donut (or pie) chart for the `dataset`, based on the style
        parameters of this object.

        Each element in the `dataset` defines one "wedge" in the chart.
        The element contains, in turn, a list/tuple consisting of:

        * The weight of the wedge (numeric)
        * The label for the wedge (string)
        * A dict with label presentation options:
            - "dx" (px): nudge the label location a little on the x-axis
            - "dy" (px): nudge the label location a little on the y-axis
            - "rotate" (boolean): Align the label along the center radial through the wedge.
        
        By default, labels are aligned horizontally and centered within the wedge 
        (where "centered" here means midway along the center radial, between the 
        hole and the edge). The nudge values (dx, dy) are relative to the chart size 
        (so 0.01 would be 1%).

        For example, a single wedge element might be: `(25, "fred", {'rotate': True})'
        Which means the wedge has a weight of 25, with the label "fred", which is rotated 
        to match the angle of the wedge.

        Wedge sizes are proportional to the total weight of all wedges.  
        A chart consisting of 4 wedges, with weights 50, 25, 10, and 5, has a total weight
        of 50 + 25 + 10 + 5 = 90.  The size of the first wedge would be 50/90 of the donut,
        or 200 degrees of arc; the second wedge would be 25/90 (100 degrees); and so forth.

        The easiest (well, safest) way to format wedge elements is the `mk_wedge` function.
        """
        wedges = progression(self.wedge_colors)
            
        r = int(self._size/2)
        center = Point(r, r)

        total = sum([item[0] for item in dataset])

        r_hole = (self.hole_size * self._size)/2
        r_text = (r + r_hole)/2 # halfway between hole and edge

        svg = ET.Element("svg")
        svg.set("viewBox", f"0 0 {self._size} {self._size}")

        chart = ET.Element("g")
        chart.set("stroke", self.border_color)
        chart.set("stroke-width", str(self.border_size * self._size))

        styles = ET.Element("style")
        font_title = self.fontspec.format(cls="title", size=(self.title_size * self._size), color=self.title_color)
        font_label = self.fontspec.format(cls="label", size=(self.label_size * self._size), color=self.label_color)
        styles.text = "\n".join((font_title, font_label))
        chart.append(styles)
        
        # calculate the points from the origin; offset when generating shapes.
        init_angle = self.init_angle
        prior_angle = init_angle
        start = Point(center.x + r*cos(init_angle), center.y + r*sin(init_angle))
        cum_weight = 0 # avoid rounding errors by accumulating values, not angles.
        
        path_data = "M {c.x},{c.y} L {p1.x},{p1.y} A {r},{r} 0 {large},1 {p2.x},{p2.y} Z"

        for weight, name, opts in dataset:
            # Group wedge + label
            item = ET.Element("g")
            
            cum_weight += weight
            angle = init_angle + (cum_weight/total) * 2*pi
            finish = Point(center.x + r*cos(angle), center.y + r*sin(angle))
            if weight > total/2:
                lg = 1
            else:
                lg = 0
            wedge = ET.Element("path")
            wedge.set("d", path_data.format(c=center, r=r, large=lg, p1=start, p2=finish))
            wedge.set("fill", next(wedges))
            item.append(wedge)

            # The label goes in the center: halfway along the mid-angle between the hole and the edge.
            bisect = (prior_angle + angle)/2

            # ... but "nudged" a little by the opts
            dx = center.x + r_text*cos(bisect) + (opts.get("dx", 0) * self._size)
            dy = center.y + r_text*sin(bisect) + (opts.get("dy", 0) * self._size)
            # ... and rotated along the center line by the opts
            rotate = opts.get('rotate', False)
            text_angle = degrees(bisect) if rotate else 0
            if not (-90 < text_angle < 90):
                text_angle -= 180 
            
            label = ET.Element("text")
            label.set("x", "0")
            label.set("y", "0")
            label.set("class", "label")
            label.set("transform", f"translate({str(dx)} {str(dy)}) rotate({text_angle})")
            label.text = name
            item.append(label)

            chart.append(item)
            start = finish
            prior_angle = angle
            
        if self.hole_size > 0:
            item = ET.Element("g")
            
            hole = ET.Element("circle")
            hole.set("cx", str(center.x))
            hole.set("cy", str(center.y))
            hole.set("r", str(int((self.hole_size * self._size)/2)))
            hole.set("fill", self.hole_color)
            item.append(hole)
        
            label = ET.Element("text")
            label.set("x", str(center.x))
            label.set("y", str(center.y))
            label.set("class", "title")
            label.text = title
            item.append(label)
            chart.append(item)

        svg.append(chart)
        return svg

def mk_wedge(weight, name="", dx=0, dy=0, rotate=False):
    """Construct a donut/pie chart dataset "wedge".

    Arguments:
    weight -- Size of the wedge (relative to total weight of all wedges)

    Keyword Arguments:
    name   -- Label text for the wedge (default is "")
    dx     -- X-axis label adjustment, as a fraction of chart width (default 0)
    dy     -- Y-axis label adjustment, as a fraction of chart width (default 0)
    rotate -- Whether label should be rotated to lie on wedge angle (default False)
    """
    return (weight, name, {'dx':dx, 'dy':dy, 'rotate':rotate})


def make_graphic(chart, filename, width_cm):
    """Create a graphic from the given SVG chart, and save it to a file.
    
    Arguments:
    chart    -- The generated donut/pie chart to output
    filename -- File to save it to
    width_cm -- Graphic size, in cm

    This is a convenience function to implicitly create an infographics.canvas.Canvas
    of the given size, put the `chart` in it, and save it to the `filename`.

    You have to create the `chart` first (e.g., from DonutStyle.generate()).

    As donut/pie charts are square, the height is implied.
    """
    page = Canvas(width_cm=width_cm, height_cm=width_cm)
    page.add_graphic(chart)
    page.write(filename)
