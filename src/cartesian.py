import random


def contains(a, pt):
    """
    Returns True if the two rectangles `a` and `b` intersect.
    """
    left, top, width, height = a
    right = left + width
    bottom = top + height
    x, y = pt

    return left <= x <= right and top <= y <= bottom


def random_coords(area, exclude_region=(0, 0, 0, 0), exclude_margin=0):
    """
    Generates random points in the (x,y) space defined by `area`, while making
    sure the generated coordinate is at least `exclude_margin` distance away
    from intersecting with the `exclude_region`.

    NOTE: This is a randomized algorithm that relies on the exclude region being
    rather small comapred to the total area, making the "probability" of the
    exclude region small. If the intersection of the target area and the exclude
    region is large, this function will likely hang.
    """
    w, h = area
    m = exclude_margin
    exclude_region = tuple(sum(x)
                           for x in zip(exclude_region, (-m, -m, 2*m, 2*m)))

    while True:
        x = random.randint(0, w)
        y = random.randint(0, h)

        if contains(exclude_region, (x, y)):
            continue

        return x, y
