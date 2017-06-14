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
    pos_list = []
    mask = []
    rect_list = []

    def __init__(self, w, h, p_list, r_list):
        self.size = [w, h]
        self.pos_list = p_list
        self.rect_list = r_list

    @classmethod
    def from_string(cls, ufield_as_string):
        # TODO: make the validator
        if ufield_as_string[0] != "U" or ufield_as_string[-1] != ";" or ";R" not in ufield_as_string:
            raise ValueError("Wrong ufield string format.")

        pos = ufield_as_string.index(";R") + 1
        posstr = ufield_as_string[:pos]
        rectstr = ufield_as_string[pos:].replace("R", "")

        # poslist = posstr.strip("UW:").strip(";").split(",")
        pos_list = []
        if "UW:" in posstr:
            if not posstr.count(",") & 1:
                raise ValueError("Wrong UW format coordinate count.")

            # TODO: refactor into a generator
            for i, x in enumerate(posstr.strip("UW:").strip(";").split(",")):
                if not i & 1:
                    # x
                    pair = []
                    pair.append(float(x))
                else:
                    # y
                    pair.append(float(x))
                    pos_list.append(pair)

        elif "UR:" in posstr:
            # match "UR:float,float,float,float,int,int;
            p = re.compile(r"^UR:\d*?\.?\d+?,\d*?\.?\d+?,\d*?\.?\d+?,\d*?\.?\d+?,\d*?\.?\d+?,\d*?\.?\d+?;$")
            if not p.match(posstr):
                raise ValueError("Wrong UR format.")

            vals = posstr.strip("UR:").strip(";").split(",")

            x0 = float(vals[0])
            y0 = float(vals[1])
            dx = float(vals[2])
            dy = float(vals[3])
            nx = int(vals[4])
            ny = int(vals[5])

            for j in range(ny):
                for i in range(nx):
                    pos_list.append([x0 + int(dx * i * 10)/10, y0 + int(dy * j * 10)/10])

        elif "UG:" in posstr:
            p = re.compile(r"^UG:\d*?\.?\d+?,\d*?\.?\d+?;$")
            if not p.match(posstr):
                raise ValueError("Wrong UT format.")

            vals = [float(s) for s in posstr.strip("UG:").strip(";").split(",")]

            pos_list.append(vals)

        elif "UM:" in posstr:
            # TODO: from mask
            print("From matrix")

        else:
            raise ValueError("Wrong Ufield specifier")

        # rlist = rectstr.split(";")
        # rect_list = [zbarect.ZbaRect.from_string(s) for s in rlist[:-1]]
        rect_list = [zbarect.ZbaRect.from_string(s) for s in rectstr.split(";")[:-1]]
        return cls(cls.size[0], cls.size[1], pos_list, rect_list)

    def dump_rects(self):
        for r in self.rect_list:
            r.dump()

    def dump(self):
        print("UField:(size:", self.size, ")")
        print("pos:", self.pos_list)
        print("mask:", self.mask)
        print("N rects:", len(self.rect_list))
