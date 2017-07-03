import re
import zbarect
import zbaufield


class ZbaTfield(object):
    """
    ZBA subfield class:
    list[x, y] list[height, width]
    init: (list float x, list float y, float w, float h)
    from_string: accepts string format "T[A|R|W]:list(float x,float y);list(ufield);list(rect);"
    """

    def __init__(self, tf_type=None, size = (200.0, 200.0, ), p_list=None, u_list=None, r_list=None):
        self.tfield_type = tf_type
        self.size = list(size)
        self.pos_list = p_list
        self.ufield_list = u_list
        self.rect_list = r_list

    def pos_list_from_ta_string(self, pos_string=None):
        # check <TA:float,float;>
        p = re.compile(r"^TA:\d*?\.?\d+?,\d*?\.?\d+?;$")
        if not p.match(pos_string):
            raise ValueError("Wrong TA format.")

        pos_list = list()
        vals = [float(s) for s in pos_string.strip("TA:").strip(";").split(",")]
        pos_list.append(vals)

        return pos_list

    def pos_list_from_tr_string(self, pos_string=None):
        # check <TR:float,float,float,float,int,int;>
        p = re.compile(r"^TR:\d*?\.?\d+?,\d*?\.?\d+?,\d*?\.?\d+?,\d*?\.?\d+?,\d*?\.?\d+?,\d*?\.?\d+?;$")
        if not p.match(pos_string):
            raise ValueError("Wrong TR format.")

        vals = pos_string.strip("TR:").strip(";").split(",")

        x0 = float(vals[0])
        y0 = float(vals[1])
        dx = float(vals[2])
        dy = float(vals[3])
        nx = int(vals[4])
        ny = int(vals[5])

        pos_list = list()

        for j in range(ny):
            for i in range(nx):
                pos_list.append([x0 + int(dx * i * 10) / 10, y0 + int(dy * j * 10) / 10])

        return pos_list

    def pos_list_from_tw_string(self, pos_string=None):
        # TODO: regex format check
        # check TW coordinate count, even = pass
        coord_count = pos_string.count(",") + 1
        if coord_count & 1:
            raise ValueError("Wrong TW format coordinate count:", coord_count, pos_string)

        pos_list = list()
        # TODO: refactor to a generator
        for i, x in enumerate(pos_string.strip("TW:").strip(";").split(",")):
            if not i & 1:
                # x
                pair = []
                pair.append(float(x))
            else:
                # y
                pair.append(float(x))
                pos_list.append(pair)

        return pos_list

    def parse_pos_string(self, pos_string=None):
        if pos_string is None:
            raise ValueError("Pos string is None.")

        if "TA" in pos_string:
            tf_type = "TA"
            pos_list = self.pos_list_from_ta_string(self, pos_string=pos_string)
        elif "TR" in pos_string:
            tf_type = "TR"
            pos_list = self.pos_list_from_tr_string(self, pos_string=pos_string)
        elif "TW" in pos_string:
            tf_type = "TW"
            pos_list = self.pos_list_from_tw_string(self, pos_string=pos_string)
        else:
            raise ValueError("Wrong pos string format:", pos_string)

        return tf_type, pos_list

    @classmethod
    def from_string(cls, tfield_as_string=None, tf_size=None):
        if tfield_as_string is None or tf_size is None:
            raise ValueError("TF string and tf_size must not be None.")

        # split TField header
        strlist = tfield_as_string.split(";", 1)

        # make Tfield pos list
        tf_type, pos_list = cls.parse_pos_string(cls, pos_string=strlist[0] + ";")

        # check data string for Ufield presence
        tmpstr = strlist[1]

        # TODO assume Ufield before rects --- check this!!!
        ustrlist = ["U" + s for s in tmpstr.split("U")[1:]]

        for u in ustrlist:
            if "UT" not in u and "UR" not in u and "UW" not in u and "UM" not in u:
                print("no Ufield found, make rects")
            elif "@R" not in u:
                if u[0] != "U":
                    raise ValueError("Uf string doesn't start from u! Does it have preceding rect?")

                print(u)
                print("Ufield detected, stray rects not detected. Parse UF")
            else:
                print("Ufield with stray rects, separate")


        # # make ufield string list
        # ufstrlist = []
        # if "U" in ufstr:
        #     ufstrlist = ["U" + s for s in ufstr.split("U")[1:]]
        # else:
        #     ufstrlist.append(ufstr)
        #
        # u_list = []
        # r_list = []
        # for s in ufstrlist:
        #     # empty ufield list, fill rects
        #     if "U" not in s:
        #         rectstrlist = ["R" + r for r in s.split("R")[1:]]
        #         for r in rectstrlist:
        #             r_list.append(zbarect.ZbaRect.from_string(r.strip(";")))
        #     else:
        #         # fill ufield list
        #         if ";@R" not in s:
        #             u_list.append(zbaufield.ZbaUfield.from_string(s.strip("@")))
        #         else:
        #             tmp = s.split("@")
        #             u_list.append(zbaufield.ZbaUfield.from_string(tmp[0]))
        #
        #             rectstrlist = ["R" + s for s in tmp[1].split("R")[1:]]
        #             for r in rectstrlist:
        #                 r_list.append(zbarect.ZbaRect.from_string(r.strip(";")))
        #
        # return cls(tf_type, cls.size, pos_list, u_list, r_list)

    def dump_ufields(self):
        for uf in self.ufield_list:
            uf.dump()

    def dump(self):
        print("TField(size:", self.size, "| type:", self.tfield_type, ")")
        print("pos:", self.pos_list)
        print("N Ufields:", len(self.ufield_list))
        print("N rects:", len(self.rect_list))
