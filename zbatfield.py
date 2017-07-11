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
            "\nN UFields:" + str(len(self.ufield_list)) + \
            "\nN RECTs:" + str(len(self.rect_list))

    def parse_pos_string(self, pos_string=None):
        """
        Internal helper method.
        :param pos_string: str - "<TA|TW|TR><position parameter list>[UField list][RECT list]" 
        :return: 
        """
        # TODO parse string and make a proper generator to use later
        def from_ta_string(string: str):
            # check <TA:float,float;>
            p = re.compile(r"^TA:\d*?\.?\d+?,\d*?\.?\d+?;$")
            if not p.match(string):
                raise ValueError("Wrong TA format.")

            p_list = [float(s) for s in string.strip("TA:").strip(";").split(",")]
            return p_list

        def from_tr_string(string: str):

            def pos_generator():
                for j in range(ny):
                    for i in range(nx):
                        yield [x0 + int(dx * i * 10) / 10, y0 + int(dy * j * 10) / 10]

            # check <TR:float,float,float,float,int,int;>
            p = re.compile(r"^TR:\d*?\.?\d+?,\d*?\.?\d+?,\d*?\.?\d+?,\d*?\.?\d+?,\d*?\.?\d+?,\d*?\.?\d+?;$")
            if not p.match(string):
                raise ValueError("Wrong TR format.")

            vals = string.strip("TR:").strip(";").split(",")

            x0 = float(vals[0])
            y0 = float(vals[1])
            dx = float(vals[2])
            dy = float(vals[3])
            nx = int(vals[4])
            ny = int(vals[5])

            p_list = [p for p in pos_generator()]
            return p_list

        def from_tw_string(string: str):

            def pos_generator():
                for i, x in enumerate(string.strip("TW:").strip(";").split(",")):
                    if not i & 1:
                        # x
                        pair = list()
                        pair.append(float(x))
                    else:
                        # y
                        pair.append(float(x))
                        yield pair

            # check <TW:float,float[,float,float];>
            p = re.compile(r"^TW:\d*?\.?\d+?,\d*?\.?\d+?(,\d*?\.?\d+?,\d*?\.?\d+?)*?;$")
            if not p.match(string):
                raise ValueError("Wrong TW format (may be coordinate count?):", string)

            p_list = [p for p in pos_generator()]
            return p_list

        if "TA" in pos_string:
            tf_type = "TA"
            pos_list = from_ta_string(pos_string)

        elif "TR" in pos_string:
            tf_type = "TR"
            pos_list = from_tr_string(pos_string)

        elif "TW" in pos_string:
            tf_type = "TW"
            pos_list = from_tw_string(pos_string)

        else:
            raise ValueError("Wrong pos string format:", pos_string)

        return tf_type, pos_list

    @classmethod
    def from_string(cls, tfield_as_string=None, tf_size=None):
        """
        Makes ZbaTfield instance object from a given sanitized string.
        :param tfield_as_string: str - "@<TA|TA|TA>:<position parameter list>[UField string][RECT string]"
        :param tf_size: [float, float] - TField size
        :return: ZbaUfield instance object
        """
        if tfield_as_string is None or tf_size is None:
            raise ValueError("TF string and tf_size must not be None.")

        # split TField header
        strlist = tfield_as_string.split(";", 1)

        # make TField pos list
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
                # no UField, make RECTs
                rect_str_list = ["R" + s for s in u.split("R")[1:]]
                rect_list = [ZbaRect.from_string(r) for r in rect_str_list]

            elif "@R" not in u:
                # no stray RECTs, make UField
                uf_list.append(ZbaUfield.from_string(u))

            else:
                # UField + stray RECTs
                # split UField string from stray RECT string
                strlist = u.split("@")

                # make UField
                uf_list.append(ZbaUfield.from_string(strlist[0] + "@"))

                # prepare RECT strings
                rect_str_list = ["R" + s for s in (strlist[1]).split("R")[1:]]

                # make RECTs
                rect_list = [ZbaRect.from_string(r) for r in rect_str_list]

        return cls(tf_type, cls.default_size, pos_list, uf_list, rect_list)

    def print_ufields(self):
        for uf in self.ufield_list:
            print(uf)
