"""SVG "container" for charts.

This module is written in/for Python3, although it can probably be used in Python2
with little modification.  The biggest incompatibility is string formatting.

All dependencies are available in the standard distribution:

  * copy
  * xml.etree.ElementTree
  * xml.dom

"""

import copy
import xml.etree.ElementTree as ET
from xml.dom import minidom

# make this a class (derived from ET.Element) for introspection (TBR).
# (e.g., examining the width/height/view-box/etc. after it's created)
class Canvas:
    """An extent (e.g., page) to hold charts and things.

    A Canvas is really just a container to keep all your charts from falling on the floor.  
    Once you have a Canvas, you can add charts (or other drawing objects) to it, and you
    can save it to a file, and an SVG drawing.

    Members:
    width  -- the overall canvas width, in user coordinates.
    height -- the overall canvas height, in user coordinates.
    svg    -- an "svg" root element, containing all the drawing objects on the canvas.

    Methods:
    add_graphic -- place an SVG sub-object onto the canvas.
    write       -- save the canvas to a file, as SVG.
    """

    def __init__(self, width, height, units="cm", px_scale=1):
        """Create an empty top-level SVG element, on which to place other drawing elements.
    
        Arguments:  
        width  -- the width of the canvas (in `units`)  
        height -- the height of the canvas (in `units`)
        
        Keyword Arguments:  
        px_scale -- the px-per-unit scale (default 1)
        units    -- SVG dimension for `width` and `height` (default "cm:")

        The constructed `svg` element includes the `xmlns` attribute,
        along with the canvas physical size (from `width`, `height`, and `units`), 
        and the `viewBox` coordinates (from `width`, `height`, and `px_scale`).

        Valid SVG dimensions are:
        * "cm" -- Centimeters
        * "in" -- Inches
        * "mm" -- Millimeters
        * "pc" -- Picas (1/6 inch)
        * "pt" -- [Big] Points (1/72 inch)
        * "px" -- Pixels

        Also valid, but likely not very useful (since no font is defined) are:
        * "em" -- One 'em', or about the size of the font.
        * "ex" -- One 'ex`, or about the width of a lower case 'x' in the font.
        """
        # in "user" units:
        self.width = px_scale*width
        self.height = px_scale*height
        # create the XML tree and root svg element:
        self.svg = ET.Element("svg")
        self.svg.set("xmlns", "http://www.w3.org/2000/svg")
        self.svg.set("version", "1.1")
        self.svg.set("width", f"{width}{units}")
        self.svg.set("height", f"{height}{units}")
        self.svg.set("viewBox", f"0 0 {self.width} {self.height}")

    def __repr__(self):
        return "Canvas(width=%r,height=%r,svg=%r)" % (self.width, self.height, self.svg)

    def __str__(self):
        content = ET.tostring(self.svg, 'utf-8')
        parsed = minidom.parseString(content)
        return parsed.toprettyxml(indent="  ")
    
    def add_graphic(self, svg, x=0, y=0, width=None, height=None):
        """Insert an SVG object onto the canvas, with position and size.

        Arguments:  
        svg -- An xml.etree.ElementTree.Element denoting an SVG object

        Keyword Arguments:  
        x      -- Offset from canvas left edge, in user coordinates (default 0)  
        y      -- Offset from canvas top edge, in user coordinates (default 0)  
        width  -- Width of object, in user coordinates (default None)
        height -- Height of object, in user coordinates (default None)

        This will create a copy of the `svg` argument (which must be an
        `svg` element, not some other SVG drawing object, like a group
        (`g`) or rectangle (`rect`) etc.), and add it to the canvas at
        the specified location and size.

        If both `width` and `height` are provided, both will be used.
        If neither are provided (i.e., both are `None`), then the full
        extent of the canvas will be used -- but be aware of
        stretching issues, based on the `preserveAspectRatio`
        attribute.  If only one is provided, the other will be derived
        from the `viewBox` of the object, such that the aspect ratio
        is maintained.  This prevents [mis]alignment artifacts.
        """
        if svg.tag != 'svg':
            raise ValueError("Non-SVG argument")

        # we don't want to alter the original element, so make a copy
        graphic = copy.deepcopy(svg)
        graphic.set("x", str(x))
        graphic.set("y", str(y))
        if width is not None:
            graphic.set("width", str(width))
            if height is None:
                viewbox = [int(i) for i in svg.attrib['viewBox'].split()]
                graphic.set("height", str(width * viewbox[3] / viewbox[2]))
        if height is not None:
            graphic.set("height", str(height))
            if width is None:
                viewbox = [int(i) for i in svg.attrib['viewBox'].split()]
                graphic.set("width", str(height * viewbox[2] / viewbox[3]))
        # if both are None, don't set either; full canvas will be used.
        self.svg.append(graphic)
    
    def write(self, filename, doctype=False):

        """Write the canvas, with all its content, to a file.

        Arguments:
        filename -- the name of the file to write the canvas XML to

        Keyword Arguments:
        doctype -- whether to include a "DOCTYPE" declaration (default False)

        By default, this just writes the straight XML, without a DOCTYPE declaration.
        If you need a DOCTYPE, set `doctype` to `True`.  You'll get uglier output, however.
        """
        # we need the XML tree, no matter what:
        content = ET.tostring(self.svg, 'utf-8')
        if doctype:
            xmldecl = '<?xml version="1.0" standalone="no"?>'
            doctype = '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">'
            with open(filename, 'w') as f:
                f.write(xmldecl)
                f.write(doctype)
                f.write(content)
        else:
            # pretty-print it; this will include the "xml" directive (but no DOCTYPE)
            parsed = minidom.parseString(content)
            with open(filename, 'w') as f:
                f.write(parsed.toprettyxml(indent="  "))
 



          

    

