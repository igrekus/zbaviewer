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

        # poss = [pos for pos, flag in zip(pos_generator(), mat) if flag == '1']
        rects = [ZbaRect.from_string_list(vals) for vals in rs]
        return cls('UM', default_uf_size, [pos for pos, flag in zip(pos_generator(mat), mat)], '', rects)

#     def parse_pos_string(self, pos_string: str):
#         """
#         Internal helper method.
#         :param pos_string:
#         :return: uf_type, pos_list, m_list
#         """
#
#         def from_ur_string(string: str):
#
#             def pos_generator():
#                 for j in range(ny):
#                     for i in range(nx):
#                         yield [x0 + int(dx * i * 10) / 10, y0 + int(dy * j * 10) / 10]
#
#             # check <UR:float,float,float,float,int,int;>
#             p = re.compile(r"^UR:\d*?\.?\d+?,\d*?\.?\d+?,\d*?\.?\d+?,\d*?\.?\d+?,\d+?,\d+?;$")
#             if not p.match(string):
#                 raise ValueError("Wrong UR format string:", string)
#
#             vals = string.strip("UR:").strip(";").split(",")
#
#             x0 = float(vals[0])
#             y0 = float(vals[1])
#             dx = float(vals[2])
#             dy = float(vals[3])
#             nx = int(vals[4])
#             ny = int(vals[5])
#
#             p_list = [p for p in pos_generator()]
#             return p_list
#
#         def from_uw_string(string: str):
#
#             def pos_generator():
#                 for i, x in enumerate(string.strip("UW:").strip(";").split(",")):
#                     if not i & 1:
#                         # x
#                         pair = list()
#                         pair.append(float(x))
#                     else:
#                         # y
#                         pair.append(float(x))
#                         yield pair
#
#             # check UW coordinate count, even = pass
#             # TODO: make regex check
#             coord_count = string.count(",") + 1
#             if coord_count & 1:
#                 raise ValueError("UW format coordinate count must be even:", coord_count, string)
#
#             p_list = [p for p in pos_generator()]
#             return p_list
#
#         def from_um_string(string: str):
#
#             def generate_filtered(filter_string: str):
#                 for i, s in enumerate(filter_string):
#                     if s == "1":
#                         row = int(i / nx)
#                         col = i % nx
#                         yield [x0 + dx * col, y0 + dy * row]
#
#             def generate_full():
#                 for j in range(ny):
#                     for i in range(nx):
#                         yield [x0 + dx * i, y0 + dy * j]
#
#             # check <UM:float,float,float,float,int,int[,array 1|0];>
#             p = re.compile(r"^UM:\d*?\.?\d+?,\d*?\.?\d+?,\d*?\.?\d+?,\d*?\.?\d+?,\d*?,\d*?(,([01])+)?;$")
#             if not p.match(string):
#                 raise ValueError("Wrong UM format string:", string)
#
#             vals = string.strip("UM:").strip(";").split(",")
#
#             x0 = float(vals[0])
#             y0 = float(vals[1])
#             dx = float(vals[2])
#             dy = float(vals[3])
#             nx = int(vals[4])
#             ny = int(vals[5])
#
#             matrix_size = nx * ny
#             # TODO: !!! confirm this condition !!!
#             if matrix_size > self.max_um_size:
#                 raise ValueError("Matrix cannot be bigger than 400 elements:", matrix_size)
#
#             if len(vals) == 7:
#                 mstr = vals[6]
#                 if matrix_size != len(mstr):
#                     raise ValueError("Matrix size doesn't match matrix filter string:", matrix_size, len(mstr), mstr)
#                 pos_generator = generate_filtered(mstr)
#             else:
#                 mstr = ""
#                 pos_generator = generate_full()
#
#             p_list = [p for p in pos_generator]
#             return p_list, mstr
#
#         m_list: str = None
#         uf_type: str = None
#         pos_list: list = None
#
#         if "UT" in pos_string:
#             pos_list = from_ut_string(pos_string)
#             uf_type = "UT"
#
#         elif "UR" in pos_string:
#             pos_list = from_ur_string(pos_string)
#             uf_type = "UR"
#
#         elif "UW" in pos_string:
#             pos_list = from_uw_string(pos_string)
#             uf_type = "UW"
#
#         elif "UM" in pos_string:
#             pos_list, m_list = from_um_string(pos_string)
#             uf_type = "UM"
#
#         else:
#             raise ValueError("Wrong UField pos specifier:", pos_string)
#
#         return uf_type, pos_list, m_list
#
#     @classmethod
#     def from_string(cls, ufield_as_string: str):
#         """
#         Makes ZbaUfield instance object from a given sanitized string.
#         :param ufield_as_string: "<UT|UW|UR|UM>:<position parameter list><RECT string>;@"
#         :return: ZbaUfield instance object
#         """
#
#         # check ufield signature
#         if (("UT" not in ufield_as_string) and ("UW" not in ufield_as_string) and ("UR" not in ufield_as_string)
#             and ("UM" not in ufield_as_string)) or ufield_as_string[-1] != "@":
#             raise ValueError("Wrong ufield string format:", ufield_as_string)
#
#         # split UField header
#         strlist = ufield_as_string.split(";", 1)
#
#         # make UField pos list
#         uf_type, pos_list, mstr = cls.parse_pos_string(cls, pos_string=strlist[0] + ";")
#
#         # make RECT list
#         rect_str_list = ["R" + s + ";" for s in strlist[1].strip("R").strip("@").strip(";").replace("R", "").split(";")]
#         rect_list = [ZbaRect.from_string(s) for s in rect_str_list]
#
#         return cls(uf_type=uf_type, size=cls.default_size, pos_list=pos_list, mask_string=mstr, rect_list=rect_list)
