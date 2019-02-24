import re
import attr
from zbarect import ZbaRect

max_um_size = 400
default_uf_size = (200.0, 200.0)

@attr.s
class ZbaUfield(object):
    """
    ZBA UField class.

    properties:

    max_um_size: int - maximum UM matrix size
    default_size: [float, float] - default UField size, microns
    ufield_type: str [UT, UR, UW, UM] - UField type
    size: [float, float] - actual UField size, microns
    pos_list: list[float, float] - UField position list, microns
    mask: str - mask string
    rect_list: list[ZbaRect] - list of rectangles, defined inside current UField

    from_string: parses UField string and makes UField object.
    """

    uf_type = attr.ib(type=str)
    size = attr.ib(type=tuple)
    positions = attr.ib(type=list)
    mask = attr.ib(type=str)
    rects = attr.ib(type=list)

    def __str__(self):
        return f'ZbaUfield(type={self.uf_type}, size={self.size}, poss={len(self.positions)}, rects={len(self.rects)})'

    @classmethod
    def from_uw_string_list(cls, params):
        ps, *rs = params.asList()

        lst = list()
        poss = list()
        for val in ps:
            lst.append(float(val))
            if len(lst) == 2:
                poss.append(lst)
                lst = list()

        rects = [ZbaRect.from_string_list(vals) for vals in rs]
        return cls('UW', default_uf_size, poss, '', rects)

    @classmethod
    def from_ut_string_list(cls, params):
        ps, *rs = params.asList()

        rects = [ZbaRect.from_string_list(vals) for vals in rs]
        return cls('UT', default_uf_size, [ps], '', rects)

    @classmethod
    def from_ur_string_list(cls, params):
        ps, *rs = params.asList()

        x0, y0, dx, dy, nx, ny = map(float, ps)
        nx, ny = int(nx), int(ny)

        def pos_generator():
            for j in range(ny):
                for i in range(nx):
                    yield [x0 + int(dx * i * 10) / 10, y0 + int(dy * j * 10) / 10]

        rects = [ZbaRect.from_string_list(vals) for vals in rs]
        return cls('UR', default_uf_size, list(pos_generator()), '', rects)

    @classmethod
    def from_um_string_list(cls, params):
        ps, mat, *rs = params

        x0, y0, dx, dy, nx, ny = map(float, ps)
        nx, ny = int(nx), int(ny)

        if mat == 'full':
            mat = ''.join(['1'] * (nx * ny))
            print(mat)

        if nx * ny != len(mat):
            raise ValueError('Matrix pattern does not cover all positions.')

        # TODO verify matrix matches

        def pos_generator(mat):
            for j in range(ny):
                for i in range(nx):
                    if mat[i + j * nx] == '1':
                        yield [x0 + int(dx * i * 10) / 10, y0 + int(dy * j * 10) / 10]

        rects = [ZbaRect.from_string_list(vals) for vals in rs]
        return cls('UM', default_uf_size, [pos for pos, flag in zip(pos_generator(mat), mat)], '', rects)

    @classmethod
    def form_uw_string_list(cls, params):
        ps, *rs = params.asList()

        print(ps)
        print(rs)
