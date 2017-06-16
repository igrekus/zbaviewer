import zbarect
import re


class ZbaUfield:
    """
    ZBA sub-subfield class:
    list[x, y] list[height, width]
    init: (float w, float h, list pos[[float x, float y]] list rect[zbarect])
    from_string: accepts string format "U[T|R|W]:list(float x,float y);list(rect);"
    """

    size = [200.0, 200.0]  # default size
    max_matrix_size = 400

    def __init__(self, uf_type, size, pos_list, mask_list, rect_list):
        self.ufield_type = uf_type
        self.size = size
        self.pos_list = pos_list
        self.mask = mask_list
        self.rect_list = rect_list

    @classmethod
    def from_string(cls, ufield_as_string):
        if (("UT" not in ufield_as_string) and ("UW" not in ufield_as_string) and ("UR" not in ufield_as_string)
                and ("UM" not in ufield_as_string)) or ufield_as_string[-1] != ";" or "R" not in ufield_as_string:
            raise ValueError("Wrong ufield string format:", ufield_as_string)

        pos = ufield_as_string.index(";") + 1
        posstr = ufield_as_string[:pos]
        rectstr = ufield_as_string[pos:]
        mstr = ""

        # fill ufield's rect list
        # TODO: use previous rect if no rect specified for this ufield?
        rect_str_list = ["R" + s for s in rectstr.replace("@", "").replace("R", "").split(";")[:-1]]
        r_list = []
        for s in rect_str_list:
            r_list.append(zbarect.ZbaRect.from_string(s))

        # fill ufield's positions list
        p_list = []
        if "UT" in posstr:
            p = re.compile(r"^UT:\d*?\.?\d+?,\d*?\.?\d+?;$")
            if not p.match(posstr):
                raise ValueError("Wrong UT format string:", posstr)
            vals = [float(s) for s in posstr.strip("UT:").strip(";").split(",")]
            p_list.append(vals)
            uftype = "UT"

        elif "UR" in posstr:
            # match "UR:float,float,float,float,int,int;
            p = re.compile(r"^UR:\d*?\.?\d+?,\d*?\.?\d+?,\d*?\.?\d+?,\d*?\.?\d+?,\d*?\.?\d+?,\d*?\.?\d+?;$")
            if not p.match(posstr):
                raise ValueError("Wrong UR format string:", posstr)

            vals = posstr.strip("UR:").strip(";").split(",")

            x0 = float(vals[0])
            y0 = float(vals[1])
            dx = float(vals[2])
            dy = float(vals[3])
            nx = int(vals[4])
            ny = int(vals[5])

            # TODO: make generator
            for j in range(ny):
                for i in range(nx):
                    p_list.append([x0 + int(dx * i * 10)/10, y0 + int(dy * j * 10)/10])

            uftype = "UR"

        elif "UW" in posstr:
            num_coords = posstr.count(",")
            if not num_coords & 1:
                raise ValueError("UW format coordinate count must be even:", num_coords + 1)

            posstrlist = posstr.strip("UW:").strip(";").split(",")

            # TODO: refactor into a generator
            for i, x in enumerate(posstrlist):
                if not i & 1:
                    # x
                    pair = []
                    pair.append(float(x))
                else:
                    # y
                    pair.append(float(x))
                    p_list.append(pair)
            uftype = "UW"

        elif "UM" in posstr:
            vals = posstr.strip("UM:").strip(";").split(",")

            x0 = float(vals[0])
            y0 = float(vals[1])
            dx = float(vals[2])
            dy = float(vals[3])
            nx = int(vals[4])
            ny = int(vals[5])
            mstr = vals[6]

            if nx * ny > cls.max_matrix_size:
                raise ValueError("Matrix cannot be bigger than 400 elements:", nx * ny)

            for i, s in enumerate(mstr):
                row = int(i / nx)
                col = i % nx

                if s == "1":
                    p_list.append([x0 + dx * col, y0 + dy * row])

            # l2 = []
            # for j in range(ny):
            #     for i in range(nx):
            #         l2.append([i, j, mstr[j*nx + i]])
            uftype = "UM"

        else:
            raise ValueError("Wrong Ufield specifier:", posstr)

        return cls(uftype, cls.size, p_list, mstr, r_list)

    def dump_rects(self):
        for r in self.rect_list:
            r.dump()

    def dump(self):
        print("UField:(size:", self.size, " type:", self.ufield_type, ")")
        print("pos:", self.pos_list)
        print("mask:", self.mask)
        print("N rects:", len(self.rect_list))
