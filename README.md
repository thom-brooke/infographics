# Infographics

A Python package for generating basic infographic charts.

This is by no means a complete implementation.  In fact, it's rather limited.  How limited?  At this point it only generates Pie and Donut charts.  That's ... pretty limited -- especially considering the broad range of data visualization representations that most people expect in an infographic.

It all started with Donut charts, because there was a pressing need for them.  But it was obvious early on that more chart types _might_ be coming, and that establishing a foundation which could support multiple charts and graphics made sense.

So that's why there's all this infrastructure around one simple chart type.

In a nutshell:

* An infographic is a `Canvas` on which various charts (and other drawing objects) are placed.
* A Chart is a self-contained graphic, typically representing some data in an intuitive way.
* Charts are generated for specific datasets based on some _style_, in order to maintain consistency.
* A Donut chart is a circular Pie chart with a title in the middle.
* (A Pie chart is a Donut chart with no hole)

All of this happens in SVG.

The canvas and charts are expected to be generated programmatically. While it is possible to add pre-rendered elements to a canvas, it's probably easier to just create the desired graphic in an SVG editor, like [Inkscape](https://inkscape.org), in the first place.

## Installation

At this point, it's source-based only.

So, either run your scripts from a location containing the `infographics` package (e.g., from the same place as this README file), or download and install using `pip` locally:
```
$ pip install -e infographics
```
Omit the `-e` option if you don't need to edit the modules.

Run tests from the project directory (i.e., here):
```
$ python -m unittest
```


## Usage

All of the examples here may be found in the `examples` directory.

For clarity, the following examples always refer to the infographics through their modules:
```
from infographics import canvas, donuts
```
You may, of course, choose to import 

### Basics
Charts are based on a _style_, so that multiple charts can be created with a consistent look and feel:
```
style = donuts.DonutStyle()
```

A chart is _generated_ from the style, using a dataset containing, well, the data:
```
data = [ (25, "Fee", {}), (25, "Fi", {}), (25, "Fo", {}), (25, "Fum", {}) ]

chart = style.generate(data, title="Giant")
```

For a donut chart, the dataset is a list-like object containing one element for each wedge.  Each element is a list-like object consisting of a _weight_, a _label_ (which may be blank), and a presentation _options_ dict (which usually is blank).

The above chart has four wedges, each with a weight of 25.  The size of each wedge is relative to the total weight of all the data items.  In this case, the total weight is 100, and each wedge is then 25/100 of the whole donut/pie -- or 1/4.  If one wedge were, say, 50 instead, it would be twice as large as the others: 2/5 of the donut (50/125).

Each label is centered in its wedge, and adjusted by the presentation options.  Here, none of the labels have presentation options, so they are rendered horizontally and centered.

So how do you see the results?

A chart is just an `xml.etree.ElementTree` containing a single `svg` element.  You can use any library or tool that can render the svg element.  Setting up such a toolchain in python, however, is a fiddly business, and if you don't have one in place already, it's probably not worth the effort.

Fortunately, a chart may be saved directly to a file:
```
donuts.make_graphic(chart, "ex-basic.svg", width_cm=10)
```

The resulting file can be viewed with any reasonable SVG library or application: Chrome, Firefox, Inkscape, gThumb -- even emacs. Note that you need to provide the actual graphic size, in cm; here's what it looks like:

![ex-basic](docs/figures/ex-basic.svg)

What about those "presentation options"?

Suppose the data had a skinny slice:
```
data.append( (5, "smell", {}) )
chart = style.generate(data, title="Giant")
donuts.make_graphic(chart, "ex-labels.svg", width_cm=10)
```

The label here is a little long, and extends beyond the thin wedge.  That's ugly; one presentation option is to _rotate_ the label:
```
data[4] = (5, "smell", {"rotate": True})
chart = style.generate(data, title="Giant")
donuts.make_graphic(chart, "ex-labels.svg", width_cm=10)
```

Better, but the label is a little crowded towards the center of the chart.  Other presentation options let you "nudge" the label a little bit in the x or y directions.  Note that the axes are relative to the text, not the chart.  So +x is to the right _along the text baseline_, and -x is to the left; +y is "down", perpendicular to the text baseline, and -y is "up".  Here, we'd like to slide the label a little closer to the outer edge:
```
data[4] = (5, "smell", {"rotate": True, "dx":-0.5})
chart = style.generate(data, title="Giant")
donuts.make_graphic(chart, "ex-labels.svg", width_cm=10)
```

A nudge is relative to the font size.  So, a nudge of "1" is roughly 1 em.
And the whole progression looks something like this:

![ex-labels](docs/figures/ex-labels.svg)

Remembering how to format the data items with their presentation options can be ... tedious.  There is a convenience function for that:
```
item1 = donuts.mk_wedge(25, "Fred")
item2 = donuts.mk_wedge(5, "Barney", rotate=True, dx=-0.5)
```


### Customization
The default style is reasonable, but some attributes may be tailored, if desired:

* `border_size` (default 0.01)
* `hole_size` (default 0.3)
* `title_size` (default 0.08)
* `label_size` (default 0.08)
* `border_color` (default "white")
* `hole_color` (default "silver")
* `title_color` (default "black")
* `label_color` (default "white")
* `wedge_colors` (default ("red", "blue", "green", "orange", "teal", "brown", "magenta", "cyan"))
* `start_angle` (default -pi/2)

All sizes are relative to the overall chart size, so a hole size of 0.25 would be 1/4 of the chart width; a title size of 0.1 would be 1/10 the chart height, etc. (Donut charts are square: width = height)

In general, colors are "CSS2 colors" (<https://www.w3.org/TR/2008/REC-CSS2-20080411/syndata.html#color-units>); in practice they may be any of the 147 SVG color names (see <https://www.december.com/html/spec/colorsvg.html>), or an RGB representation, as used in HTML or CSS.  for example: `rgb(100, 100, 0)` or `#A9A9A9`.

The start angle is where the first wedge starts.  Normally, this is straight up (due North, noon, +y axis, etc.), but it may be more pleasing to start at 0 -- especially with thin wedges towards the end of the dataset.

For example:
```
style = donuts.DonutStyle(hole_size=0.4,
                          hole_color="darkseagreen",
                          title_color="yellow",
                          label_size=0.06,
                          label_color="black",
                          wedge_colors=("#909090", "#a0a0a0", "#b0b0b0", "#c0c0c0", "#d0d0d0", "#e0e0e0"),
                          start_angle=0
)

data = [ donuts.mk_wedge(25, "Fee"),
         donuts.mk_wedge(25, "Fi"),
         donuts.mk_wedge(25, "Fo"),
         donuts.mk_wedge(25, "Fum"),
         donuts.mk_wedge(5, "smell", rotate=True, dx=0.5),
]

chart = style.generate(data, title="Giants")
donuts.make_graphic(chart, "ex-custom.svg", width_cm=10)
```

![ex-custom](docs/figures/ex-custom.svg)

Pie charts are just donut charts with a hole size of zero.

### Composition
Sometimes, one chart (or one graphic element) isn't enough.  For those situations, there's a `Canvas`.

The canvas is the page on which several elements will be placed. For example, see the triple-chart above, illustrating the use of label rotation and position.  In fact, the `make_graphic` function, used in the earlier examples, simply creates a canvas the same size as the chart, places the chart on it, and saves the canvas.

First create the overall page:
```
page = canvas.Canvas(width=10, height=5, units="cm")
```

Then place graphics or charts on it:
```
page.add_graphic(chart, width=5)
page.add_graphic(chart, x=7, y=2, width=3)
```

The x/y offset is from the top left corner (default is 0/0), and the width and/or height is in canvas units.  By default, the canvas units are the same as the canvas size (here: width 10 and height 5), but they may be scaled, if convenient.

Finally, write it to a file when finished:
```
page.write("ex-canvas.svg")
```

![ex-canvas](docs/figures/ex-canvas.svg)


### Annotations
A chart itself is just an XML "svg" element; a canvas has a `svg` field which is also just an XML "svg" element.  These can be manipulated directly -- for example, to add annotations or to further customize their appearance.

This is not for the faint of heart; programmatically generating SVG is a fiddly business, better suited to automation than to one-off tweaks.  If you just want to add a little something to a chart or a canvas, use an SVG editor, instead.

Still, it's just XML:
```
import xml.etree.ElementTree as ET

chart = style.generate(data, title="Giant")

bg = ET.Element("rect")
bg.set("width", str(style.size))
bg.set("height", str(style.size))
bg.set("fill", "lavender")
# don't cover up the chart with the background:
chart.insert(0, bg)
```
Annotating the canvas is similar:
```
page = canvas.Canvas(width=10, height=5, units="cm", px_scale=100)
page.add_graphic(chart, width=page.width/2)
page.add_graphic(chart, x=(0.7*page.width), y=(0.4*page.height), width=(0.3*page.width))

tag = ET.Element("text")
tag.set("font-family", "sans-serif")
tag.set("font-size", str(0.2*page.height))
tag.set("fill", "red")
tag.set("x", str(0.6*page.width))
tag.set("y", str(0.25*page.height))
tag.text = "Fancy"
page.svg.append(tag)

page.write("ex-annotate.svg")
```
Be careful:  by default, the canvas' user units are 1-to-1 with the given `width` and `height`.  Not all SVG libraries can handle this well for large display units (such as "cm").  The `px_scale` argument is an expansion factor for the width and height in user units.

![ex-annotate](docs/figures/ex-annotate.svg)


## Considerations

Different SVG rendering libraries work differently.

For example, some do not support the "dominant-baseline" attribute for text elements.  Which means that a label which is _supposed_ to be centered vertically on a reference line is instead aligned on its baseline (making it appear slightly "higher" than it should).

Inkscape does not handle "untagged" nested SVG elements well.

A `Canvas` adds graphics as nested "svg" elements.  This is convenient, and perfectly valid.  However, Inkscape cannot modify these elements unless they have some magic attributes (which the `infographics` scripts don't provide).  Charts on a canvas, or a chart inserted into another Inkscape document, can't be moved or scaled or anything.  Inkscape will report that it "cannot transform an embedded SVG".  The solution is to double-click the chart, which will cause Inkscape to add the magic tags.  Then it can be edited just any other drawing object.

