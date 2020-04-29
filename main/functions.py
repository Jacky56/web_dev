def to_square(x, y, w, h):
    if h > w:
        diff1 = max((h - w) // 2, 0)
        nx = max(x - diff1, 0)
        nxw = (h )

        return nx, y, nxw, h
    else:
        diff1 = max((w - h) // 2, 0)
        ny = max(y - diff1, 0)
        nyh = (w)

        return x, ny, w, nyh

