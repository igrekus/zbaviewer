import re
from zbarect import ZbaRect


class ZbaUfield(object):
    """
    ZBA sub-subfield class:
    list[x, y] list[height, width]
    init: (float w, float h, list pos[[float x, float y]] list rect[zbarect])
    from_string: accepts string format "U[T|R|W]:list(float x,float y);list(rect);"
    """

    max_matrix_size = 400
    default_size = [200.0, 200.0]

    def __init__(self, uf_type=None, size=(200.0, 200.0,), pos_list=None, mask_string=None, rect_list=None):
        self.ufield_type = uf_type
        self.size = list(size)
        self.pos_list = pos_list
        self.mask = mask_string
        self.rect_list = rect_list

    def __str__(self):
        return "UField:(size:" + str(self.size) + ", type:" + self.ufield_type + ")" + \
            "\npos:" + str(self.pos_list) + \
            "\nmask:" + str(self.mask) + \
            "\nN rects:" + str(len(self.rect_list))

    def pos_list_from_ut_string(self, pos_string=None):
        # check <UT:float,float;>
        p = re.compile(r"^UT:\d*?\.?\d+?,\d*?\.?\d+?;$")
        if not p.match(pos_string):
            raise ValueError("Wrong UT format.")

        # fill ufield positions list
        pos_list = [float(s) for s in pos_string.strip("UT:").strip(";").split(",")]
        return pos_list

    def pos_list_from_ur_string(self, pos_string=None):
        # check <UR:float,float,float,float,int,int;>
        p = re.compile(r"^UR:\d*?\.?\d+?,\d*?\.?\d+?,\d*?\.?\d+?,\d*?\.?\d+?,\d+?,\d+?;$")
        if not p.match(pos_string):
            raise ValueError("Wrong UR format string:", pos_string)

        vals = pos_string.strip("UR:").strip(";").split(",")

        x0 = float(vals[0])
        y0 = float(vals[1])
        dx = float(vals[2])
        dy = float(vals[3])
        nx = int(vals[4])
        ny = int(vals[5])

        p_list = list()
        # TODO: make generator
        for j in range(ny):
            for i in range(nx):
                p_list.append([x0 + int(dx * i * 10) / 10, y0 + int(dy * j * 10) / 10])

        return p_list

    def pos_list_from_uw_string(self, pos_string=None):
        # check UW coordinate count, even = pass
        coord_count = pos_string.count(",") + 1
        if coord_count & 1:
            raise ValueError("UW format coordinate count must be even:", coord_count, pos_string)

        posstrlist = pos_string.strip("UW:").strip(";").split(",")

        pos_list = list()
        # TODO: refactor into a generator
        for i, x in enumerate(posstrlist):
            if not i & 1:
                # x
                pair = []
                pair.append(float(x))
            else:
                # y
                pair.append(float(x))
                pos_list.append(pair)

        return pos_list

    def pos_list_from_um_string(self, pos_string=None):
        # check <UR:float,float,float,float,int,int,[array 1|0];>
        p = re.compile(r"^UM:\d*?\.?\d+?,\d*?\.?\d+?,\d*?\.?\d+?,\d*?\.?\d+?,\d*?,\d*?,([01])+;$")
        if not p.match(pos_string):
            raise ValueError("Wrong UM format string:", pos_string)

        vals = pos_string.strip("UM:").strip(";").split(",")

        x0 = float(vals[0])
        y0 = float(vals[1])
        dx = float(vals[2])
        dy = float(vals[3])
        nx = int(vals[4])
        ny = int(vals[5])
        mstr = vals[6]

        if nx * ny > self.max_matrix_size:
            # TODO: --- check this!!!
            raise ValueError("Matrix cannot be bigger than 400 elements:", nx * ny)

        pos_list = list()

        # TODO: process empty matix list
        for i, s in enumerate(mstr):
            row = int(i / nx)
            col = i % nx
            if s == "1":
                pos_list.append([x0 + dx * col, y0 + dy * row])

        # l2 = []
        # for j in range(ny):
        #     for i in range(nx):
        #         l2.append([i, j, mstr[j*nx + i]])

        return pos_list, mstr

    def parse_pos_string(self, pos_string):
        # TODO: make nested functions?
        if "UT" in pos_string:
            pos_list = self.pos_list_from_ut_string(self, pos_string=pos_string)
            uf_type = "UT"
            m_list = None

        elif "UR" in pos_string:
            pos_list = self.pos_list_from_ur_string(self, pos_string=pos_string)
            uf_type = "UR"
            m_list = None

        elif "UW" in pos_string:
            pos_list = self.pos_list_from_uw_string(self, pos_string=pos_string)
            uf_type = "UW"
            m_list = None

        elif "UM" in pos_string:
            pos_list, m_list = self.pos_list_from_um_string(self, pos_string=pos_string)
            uf_type = "UM"
        else:
            raise ValueError("Wrong UField pos specifier:", pos_string)

        return uf_type, pos_list, m_list

    @classmethod
    def from_string(cls, ufield_as_string):
        # check ufield signature
        if (("UT" not in ufield_as_string) and ("UW" not in ufield_as_string) and ("UR" not in ufield_as_string)
                and ("UM" not in ufield_as_string)) or ufield_as_string[-1] != "@":
            raise ValueError("Wrong ufield string format:", ufield_as_string)

        # split UField header
        strlist = ufield_as_string.split(";", 1)

        # make UField pos list
        uf_type, pos_list, mstr = cls.parse_pos_string(cls, pos_string=strlist[0] + ";")

        rect_str_list = ["R" + s + ";" for s in strlist[1].strip("R").strip("@").strip(";").split(";")]
        rect_list = list()
        for s in rect_str_list:
            rect_list.append(ZbaRect.from_string(rect_as_string=s))

        return cls(uf_type=uf_type, size=cls.default_size, pos_list=pos_list, mask_string=mstr, rect_list=rect_list)

    def print_rects(self):
        for r in self.rect_list:
            print(r)
