import re
import zbarect
import zbaufield


class ZbaTfield:
    """
    ZBA subfield class:
    list[x, y] list[height, width]
    init: (list float x, list float y, float w, float h)
    from_string: accepts string format "T[A|R|W]:list(float x,float y);list(ufield);list(rect);"
    """
    size = [200.0, 200.0]  # default size

    def __init__(self, tf_type, size, p_list, u_list, r_list):
        self.tfield_type = tf_type
        self.size = size
        self.pos_list = p_list
        self.ufield_list = u_list
        self.rect_list = r_list

    @classmethod
    def from_string(cls, tfield_as_string):
        if (("TA" not in tfield_as_string) and ("TR" not in tfield_as_string) and ("TW" not in tfield_as_string)) \
                or tfield_as_string[-1] != ";" or "R" not in tfield_as_string or "U" not in tfield_as_string:
            raise ValueError("Wrong ufield string format.")

        # split tfield header
        pos = tfield_as_string.index(";", 1) + 1
        posstr = tfield_as_string[:pos]
        ufstr = tfield_as_string[pos:]

        ufstrlist = ["U" + s for s in ufstr.split("U")[1:]]

        u_list = []
        r_list = []
        for s in ufstrlist:
            if not ";@R" in s:
                u_list.append(zbaufield.ZbaUfield.from_string(s.strip("@")))
            else:
                tmp = s.split("@")
                u_list.append(zbaufield.ZbaUfield.from_string(tmp[0]))

                rectstrlist = ["R" + s for s in tmp[1].split("R")[1:]]
                for r in rectstrlist:
                    r_list.append(zbarect.ZbaRect.from_string(r.strip(";")))

        for u in u_list:
            u.dump()

        for r in r_list:
            r.dump()

        # u_list = []
        # for s in ufstrlist:
        #     u_list.append(zbaufield.ZbaUfield.from_string(s))

        #
        # pos_list = []
        #
        # if "TW:" in posstr:
        #     if not posstr.count(",") & 1:
        #         raise ValueError("Wrong TW format coordinate count.")
        #
        #     # TODO: refactor to a generator
        #     for i, x in enumerate(posstr.strip("TW:").strip(";").split(",")):
        #         if not i & 1:
        #             # x
        #             pair = []
        #             pair.append(float(x))
        #         else:
        #             # y
        #             pair.append(float(x))
        #             pos_list.append(pair)
        #
        # elif "TR:" in posstr:
        #     # # match "TR:float,float,float,float,int,int;
        #     p = re.compile(r"^TR:\d*?\.?\d+?,\d*?\.?\d+?,\d*?\.?\d+?,\d*?\.?\d+?,\d*?\.?\d+?,\d*?\.?\d+?;$")
        #     if not p.match(posstr):
        #         raise ValueError("Wrong TR format.")
        #
        #     vals = posstr.strip("TR:").strip(";").split(",")
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
        #             pos_list.append([x0 + int(dx * i * 10) / 10, y0 + int(dy * j * 10) / 10])
        #
        # elif "TA:" in posstr:
        #     p = re.compile(r"^TA:\d*?\.?\d+?,\d*?\.?\d+?;$")
        #     if not p.match(posstr):
        #         raise ValueError("Wrong TA format.")
        #
        #     vals = [float(s) for s in posstr.strip("TA:").strip(";").split(",")]
        #
        #     pos_list.append(vals)
        #
        # else:
        #     raise ValueError("Wrong TA field specifier.")
        #
        # uf_list = [zbaufield.ZbaUfield.from_string("U" + s) for s in ufstr.split("U")[1:]]
        #
        # return cls(cls.size[0], cls.size[1], pos_list, uf_list)

    def dump_ufields(self):
        for uf in self.ufield_list:
            uf.dump()

    def dump(self):
        print("TField(size:", self.size, ")")
        print("pos:", self.pos_list)
        print("N Ufields:", len(self.ufield_list))
        print("N rects:", len(self.rect_list))
