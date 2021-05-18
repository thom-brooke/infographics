# Infographics

A Python package for generating basic infographic charts.

This is by no means a complete implementation.  In fact, it's rather limited.  How limited?  At this point it only generates Pie and Donut charts.  That's ... pretty limited -- especially considering the broad range of data visualization tools that most people expect in an infographic.

It all started with Donut charts, because there was a pressing need for them.  But it was obvious early on that more chart types _might_ be coming, and that establishing a foundation which could support multiple charts and graphics made sense.

So that's why there's all this infrastructure around one simple chart type.

In a nutshell:

* An infographic is a `Canvas` on which various charts (and other drawing objects) are placed.
* A Chart is a self-contained graphic, typically representing some data in an intuitive way.
* Charts are generated for specific datasets based on some _style_, in order to maintain consistency.
* A Donut chart is a circular Pie chart with a title in the middle.
* (A Pie chart is a Donut chart with no hole)

All of this happens in SVG.

The canvas and charts are expected to be generated programmatically. While it is possible to add pre-rendered elements to a canvas, it's probably easier to just create the desired graphic in an SVG editor, like [Inkscape](https://inkscape.org).

## Installation

At this point, it's source-based only.

So, either run your scripts from a location containing the `infographics` package (e.g., from the same place as this README file), or download and install using `pip` locally:
```
$ pip install -e infographics
```
Omit the `-e` option if you don't need to edit the modules.

## Examples

TBS.

## Considerations

Different SVG rendering libraries work differently.

For example, some do not support the "dominant-baseline" attribute for text elements.  Which means that a label which is _supposed_ to be centered vertically on a reference line is instead aligned on its baseline (making it appear slightly "higher" than it should).

## Usage

### Canvas
The "canvas" is the sheet/page/container into which charts (etc.) are placed.

construction

add_graphic

write. with or without DOCTYPE.

### Charts

TBS.

generic considerations for all chart types (even though there's currently only one).

style vs. object

strategy for tailoring (sizes relative to "full").

labels and how to adjust them (dx, dy "nudges")

#### Pie and Donut Charts

TBS.

a pie chart is a donut chart with no hole.

constructing a style

generating a chart.  datasets.  labels and text.

convenience function to fit and write a canvas to a chart

Here's an example:  
![generated](./docs/figures/test-chart.svg)