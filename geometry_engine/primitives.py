import cadquery as cq

def build_polyline(points, closed=True):
    wp = cq.Workplane("XY").polyline(points)
    if closed:
        wp = wp.close()
    return wp

def build_rectangle(position, width, height):
    x, y = position
    return (
        cq.Workplane("XY")
        .transformed(offset=(x, y, 0))
        .rect(width, height)
    )

def build_circle(center, radius):
    x, y = center
    return (
        cq.Workplane("XY")
        .transformed(offset=(x, y, 0))
        .circle(radius)
    )
