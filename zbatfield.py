import re
from zbarect import ZbaRect
from zbaufield import ZbaUfield


class ZbaTfield(object):
    """
    ZBA TField class.
    
    properties: 
    default_size: [float, float] - default TField size, microns
    tfield_type: str [TA, TR, TW] - TField type
    size: [float, float] - actual TField size, microns
    pos_list: list[float, float] - TField position list, microns
    ufield_list: list[ZbaUfield] - list of UFields, defined inside current TField
    rect_list: list[ZbaRect] - list of rectangles, defined inside current TField

    from_string: parses UField string and makes UField object.
    """

    default_size = [200.0, 200.0]

    def __init__(self, tf_type=None, size=(200.0, 200.0, ), p_list=None, u_list=None, r_list=None):
        self.tfield_type: str = tf_type
        self.size: list = list(size)
        self.pos_list: list = p_list
        self.ufield_list: list = u_list
        self.rect_list: list = r_list

    def __str__(self):
        return "TField(size:" + str(self.size) + ", type:" + self.tfield_type + ")" + \
            "\npos:" + str(self.pos_list) + \
            "\nN UFileds:" + str(len(self.ufield_list)) + \
            "\nN RECTs:" + str(len(self.rect_list))

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
        # TODO: make generator
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

        # TODO !!! assume Ufield before rects --- confirm this!!!
        # if strlist[1][0] != "U": # TODO check any rects before UField
        ustrlist = ["U" + s for s in tmpstr.split("U")[1:]]

        uf_list = list()
        rect_list = list()

        for u in ustrlist:
            if "UT" not in u and "UR" not in u and "UW" not in u and "UM" not in u:
                # TODO !!! parse uf-less TField !!!
                print("no Ufield found, make rects")

            elif "@R" not in u:
                if u[0] != "U":
                    raise ValueError("Uf string doesn't start with an U! Does it have preceding rect?")

                uf = ZbaUfield.from_string(u)

            else:
                strlist = u.split("@")
                uf = ZbaUfield.from_string(strlist[0]+"@")
                rect_str_list = ["R" + s for s in (strlist[1] + ";").split("R")[1:]]

                for r in rect_str_list:
                    rect_list.append(ZbaRect.from_string(r))

                for r in rect_list:
                    print(r)
                print("Ufield with stray rects, separate")
            break


        # return cls(tf_type, cls.size, pos_list, u_list, r_list)

    def print_ufields(self):
        for uf in self.ufield_list:
            print(uf)
