import re
from zbarect import ZbaRect


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

    max_um_size = 400
    default_size = [200.0, 200.0]

    def __init__(self, uf_type=None, size=(200.0, 200.0,), pos_list=None, mask_string=None, rect_list=None):
        self.ufield_type: str = uf_type
        self.size: list = list(size)
        self.pos_list: list = pos_list
        self.mask: str = mask_string
        self.rect_list: list = rect_list

    def __str__(self):
        return "UField:(size:" + str(self.size) + ", type:" + self.ufield_type + ")" + \
            "\npos:" + str(self.pos_list) + \
            "\nmask:" + str(self.mask) + \
            "\nN rects:" + str(len(self.rect_list))

    def parse_pos_string(self, pos_string: str):
        """
        Internal helper method.
        :param pos_string: 
        :return: 
        """
        # TODO parse string and make a proper generator to use later

        def from_ut_string(string: str):
            # check <UT:float,float;>
            p = re.compile(r"^UT:\d*?\.?\d+?,\d*?\.?\d+?;$")
            if not p.match(string):
                raise ValueError("Wrong UT format.")

            # fill ufield positions list
            p_list = [float(s) for s in string.strip("UT:").strip(";").split(",")]
            return p_list

        def from_ur_string(string: str):

            def pos_generator():
                for j in range(ny):
                    for i in range(nx):
                        yield [x0 + int(dx * i * 10) / 10, y0 + int(dy * j * 10) / 10]

            # check <UR:float,float,float,float,int,int;>
            p = re.compile(r"^UR:\d*?\.?\d+?,\d*?\.?\d+?,\d*?\.?\d+?,\d*?\.?\d+?,\d+?,\d+?;$")
            if not p.match(string):
                raise ValueError("Wrong UR format string:", string)

            vals = string.strip("UR:").strip(";").split(",")

            x0 = float(vals[0])
            y0 = float(vals[1])
            dx = float(vals[2])
            dy = float(vals[3])
            nx = int(vals[4])
            ny = int(vals[5])

            p_list = list()

            for p in pos_generator():
                p_list.append(p)

            return p_list

        def from_uw_string(string: str):

            def pos_generator():
                for i, x in enumerate(posstrlist):
                    if not i & 1:
                        # x
                        pair = list()
                        pair.append(float(x))
                    else:
                        # y
                        pair.append(float(x))
                        yield pair

            # check UW coordinate count, even = pass
            coord_count = string.count(",") + 1
            if coord_count & 1:
                raise ValueError("UW format coordinate count must be even:", coord_count, string)

            posstrlist = string.strip("UW:").strip(";").split(",")

            pos_list = list()

            for p in pos_generator():
                pos_list.append(p)

            return pos_list

        def from_um_string(string: str):

            def generate_filtered(filter_string: str):
                for i, s in enumerate(filter_string):
                    if s == "1":
                        row = int(i / nx)
                        col = i % nx
                        yield [x0 + dx * col, y0 + dy * row]

            def generate_full():
                for j in range(ny):
                    for i in range(nx):
                        yield [x0 + dx * i, y0 + dy * j]

            # check <UR:float,float,float,float,int,int[,array 1|0];>
            p = re.compile(r"^UM:\d*?\.?\d+?,\d*?\.?\d+?,\d*?\.?\d+?,\d*?\.?\d+?,\d*?,\d*?(,([01])+)?;$")
            if not p.match(string):
                raise ValueError("Wrong UM format string:", string)

            vals = string.strip("UM:").strip(";").split(",")

            x0 = float(vals[0])
            y0 = float(vals[1])
            dx = float(vals[2])
            dy = float(vals[3])
            nx = int(vals[4])
            ny = int(vals[5])

            matrix_size = nx * ny
            # TODO: !!! confirm this condition !!!
            if matrix_size > self.max_um_size:
                raise ValueError("Matrix cannot be bigger than 400 elements:", matrix_size)

            if len(vals) == 7:
                mstr = vals[6]
                if matrix_size != len(mstr):
                    raise ValueError("Matrix size doesn't match matrix filter string:", matrix_size, len(mstr), mstr)
                pos_generator = generate_filtered(mstr)
            else:
                mstr = ""
                pos_generator = generate_full()

            pos_list = list()
            for p in pos_generator:
                pos_list.append(p)

            return pos_list, mstr

        m_list: str = None
        uf_type: str = None
        pos_list: list = None

        if "UT" in pos_string:
            pos_list = from_ut_string(pos_string)
            uf_type = "UT"

        elif "UR" in pos_string:
            pos_list = from_ur_string(pos_string)
            uf_type = "UR"

        elif "UW" in pos_string:
            pos_list = from_uw_string(pos_string)
            uf_type = "UW"

        elif "UM" in pos_string:
            pos_list, m_list = from_um_string(pos_string)
            uf_type = "UM"

        else:
            raise ValueError("Wrong UField pos specifier:", pos_string)

        return uf_type, pos_list, m_list

    @classmethod
    def from_string(cls, ufield_as_string: str):
        """
        Makes ZbaUfield instance object from a given sanitized string.
        :param ufield_as_string: "@<UT|UW|UR|UM><position parameter list><RECT string>;@"
        :return: ZbaUfield instance object
        """
        # check ufield signature
        if (("UT" not in ufield_as_string) and ("UW" not in ufield_as_string) and ("UR" not in ufield_as_string)
                and ("UM" not in ufield_as_string)) or ufield_as_string[-1] != "@":
            raise ValueError("Wrong ufield string format:", ufield_as_string)

        # split UField header
        strlist = ufield_as_string.split(";", 1)

        # make UField pos list
        uf_type, pos_list, mstr = cls.parse_pos_string(cls, pos_string=strlist[0] + ";")

        # make RECT list
        rect_str_list = ["R" + s + ";" for s in strlist[1].strip("R").strip("@").strip(";").split(";")]
        rect_list = [ZbaRect.from_string(s) for s in rect_str_list]

        return cls(uf_type=uf_type, size=cls.default_size, pos_list=pos_list, mask_string=mstr, rect_list=rect_list)

    def print_rects(self):
        for r in self.rect_list:
            print(r)
