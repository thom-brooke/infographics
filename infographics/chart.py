"""Utility classes and functions for infographics and charts."""

class Point:
    """Convenience class to hold a cartesian point.

    It doesn't _do_ anything; just holds a cartesian coordinate pair 
    in its `x` and `y` attributes.
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

# TBD:
# class Chart:
#    bare outline of charts, with size (for viewBox), and whatever other
#    general attributes the Canvas needs.


def progression(domain):
    """Return a _generator_ to circularly step through a list of values.
    
    Arguments:
    domain -- list-like sequence of values to cycle through.

    This returns a _generator_, not an object, where the first value
    produced is the first value in `domain`, and subsequent values are
    sequential.  The sequence wraps at the end such that the value
    returned after the last is the first again.

    Note that the generator is infinite; it will _never_ end.

    **Warning:** 
    The `domain` argument is _global_.  Changing it _after_ creating 
    the progression will affect the generated sequence and may have 
    unpredictable results.  So be careful; it's probably safest to use 
    anonymous expressions.  Or a tuple.

    >>> foo = infographics.chart.progression(['round', 'and'])
    >>> next(foo)
    'round'
    >>> next(foo)
    'and'
    >>> next(foo)
    'round'
    >>> next(foo)
    'and'

    """
    current = 0
    while True:
        yield domain[current]
        current = (current + 1) % len(domain)
    
