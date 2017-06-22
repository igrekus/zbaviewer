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
    size = [200.0, 200.0]  # default size

    def __init__(self, tf_type, size, p_list, u_list, r_list):
        self.tfield_type = tf_type
        self.size = size
        self.pos_list = p_list
        self.ufield_list = u_list
        self.rect_list = r_list

    @classmethod
    def from_string(cls, tfield_as_string):
        # check tfield signature
        if (("TA" not in tfield_as_string) and ("TR" not in tfield_as_string) and ("TW" not in tfield_as_string)) \
                or tfield_as_string[-1] != ";" or "R" not in tfield_as_string:
            raise ValueError("Wrong ufield string format:", tfield_as_string)

        # split tfield header
        delim = tfield_as_string.index(";") + 1
        posstr = tfield_as_string[:delim]
        ufstr = tfield_as_string[delim:]

        # make ufield string list
        ufstrlist = []
        if "U" in ufstr:
            ufstrlist = ["U" + s for s in ufstr.split("U")[1:]]
        else:
            ufstrlist.append(ufstr)

        u_list = []
        r_list = []
        for s in ufstrlist:
            # empty ufield list, fill rects
            if "U" not in s:
                rectstrlist = ["R" + r for r in s.split("R")[1:]]
                for r in rectstrlist:
                    r_list.append(zbarect.ZbaRect.from_string(r.strip(";")))
            else:
                # fill ufield list
                if ";@R" not in s:
                    u_list.append(zbaufield.ZbaUfield.from_string(s.strip("@")))
                else:
                    tmp = s.split("@")
                    u_list.append(zbaufield.ZbaUfield.from_string(tmp[0]))

                    rectstrlist = ["R" + s for s in tmp[1].split("R")[1:]]
                    for r in rectstrlist:
                        r_list.append(zbarect.ZbaRect.from_string(r.strip(";")))

        # fill position coordinate list
        pos_list = []
        if "TW:" in posstr:
            # check TW coordinate count, even = pass
            coord_count = posstr.count(",") + 1
            if coord_count & 1:
                raise ValueError("Wrong TW format coordinate count:", coord_count, posstr)

            # TODO: refactor to a generator
            for i, x in enumerate(posstr.strip("TW:").strip(";").split(",")):
                if not i & 1:
                    # x
                    pair = []
                    pair.append(float(x))
                else:
                    # y
                    pair.append(float(x))
                    pos_list.append(pair)
            tf_type = "TW"

        elif "TR:" in posstr:
            # check <TR:float,float,float,float,int,int;>
            p = re.compile(r"^TR:\d*?\.?\d+?,\d*?\.?\d+?,\d*?\.?\d+?,\d*?\.?\d+?,\d*?\.?\d+?,\d*?\.?\d+?;$")
            if not p.match(posstr):
                raise ValueError("Wrong TR format.")

            vals = posstr.strip("TR:").strip(";").split(",")

            x0 = float(vals[0])
            y0 = float(vals[1])
            dx = float(vals[2])
            dy = float(vals[3])
            nx = int(vals[4])
            ny = int(vals[5])

            for j in range(ny):
                for i in range(nx):
                    pos_list.append([x0 + int(dx * i * 10) / 10, y0 + int(dy * j * 10) / 10])
            tf_type = "TR"

        elif "TA:" in posstr:
            # check <TA:float,float;>
            p = re.compile(r"^TA:\d*?\.?\d+?,\d*?\.?\d+?;$")
            if not p.match(posstr):
                raise ValueError("Wrong TA format.")

            vals = [float(s) for s in posstr.strip("TA:").strip(";").split(",")]
            pos_list.append(vals)

            tf_type = "TA"

        else:
            raise ValueError("Wrong TA field specifier.")

        return cls(tf_type, cls.size, pos_list, u_list, r_list)

    def dump_ufields(self):
        for uf in self.ufield_list:
            uf.dump()

    def dump(self):
        print("TField(size:", self.size, "| type:", self.tfield_type, ")")
        print("pos:", self.pos_list)
        print("N Ufields:", len(self.ufield_list))
        print("N rects:", len(self.rect_list))
