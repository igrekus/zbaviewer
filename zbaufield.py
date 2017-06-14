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

    def __init__(self, size, pos_list, mask_list, rect_list):
        self.size = size
        self.pos_list = pos_list
        self.mask = mask_list
        self.rect_list = rect_list

    @classmethod
    def from_string(cls, ufield_as_string):
        if (("UT" not in ufield_as_string) and ("UW" not in ufield_as_string) and ("UW" not in ufield_as_string)
                and ("UM" not in ufield_as_string)) or ufield_as_string[-1] != ";" or "R" not in ufield_as_string:
            raise ValueError("Wrong ufield string format.")

        pos = ufield_as_string.index(";") + 1
        posstr = ufield_as_string[:pos]
        rectstr = ufield_as_string[pos:]

        # fill ufield's rect list
        # TODO: use previous rect if no rect specified for this ufield?
        rect_str_list = ["R" + s for s in rectstr.replace("@", "").replace("R", "").split(";")[:-1]]
        print(rect_str_list)

        r_list = []
        for s in rect_str_list:
            r_list.append(zbarect.ZbaRect.from_string(s))

        for r in r_list:
            r.dump()

        # return cls(200.0, 200.0, pos_list, rect_list)


        #
        # # poslist = posstr.strip("UW:").strip(";").split(",")
        # pos_list = []
        # if "UW:" in posstr:
        #     if not posstr.count(",") & 1:
        #         raise ValueError("Wrong UW format coordinate count.")
        #
        #     # TODO: refactor into a generator
        #     for i, x in enumerate(posstr.strip("UW:").strip(";").split(",")):
        #         if not i & 1:
        #             # x
        #             pair = []
        #             pair.append(float(x))
        #         else:
        #             # y
        #             pair.append(float(x))
        #             pos_list.append(pair)
        #
        # elif "UR:" in posstr:
        #     # match "UR:float,float,float,float,int,int;
        #     p = re.compile(r"^UR:\d*?\.?\d+?,\d*?\.?\d+?,\d*?\.?\d+?,\d*?\.?\d+?,\d*?\.?\d+?,\d*?\.?\d+?;$")
        #     if not p.match(posstr):
        #         raise ValueError("Wrong UR format.")
        #
        #     vals = posstr.strip("UR:").strip(";").split(",")
        #
        #     x0 = float(vals[0])
        #     y0 = float(vals[1])
        #     dx = float(vals[2])
        #     dy = float(vals[3])
        #     nx = int(vals[4])
        #     ny = int(vals[5])
        #
        #     for j in range(ny):
        #         for i in range(nx):
        #             pos_list.append([x0 + int(dx * i * 10)/10, y0 + int(dy * j * 10)/10])
        #
        # elif "UG:" in posstr:
        #     p = re.compile(r"^UG:\d*?\.?\d+?,\d*?\.?\d+?;$")
        #     if not p.match(posstr):
        #         raise ValueError("Wrong UT format.")
        #
        #     vals = [float(s) for s in posstr.strip("UG:").strip(";").split(",")]
        #
        #     pos_list.append(vals)
        #
        # elif "UM:" in posstr:
        #     # TODO: from mask
        #     print("From matrix")
        #
        # else:
        #     raise ValueError("Wrong Ufield specifier")

    def dump_rects(self):
        for r in self.rect_list:
            r.dump()

    def dump(self):
        print("UField:(size:", self.size, ")")
        print("pos:", self.pos_list)
        print("mask:", self.mask)
        print("N rects:", len(self.rect_list))
