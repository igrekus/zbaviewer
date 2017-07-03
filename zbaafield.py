from zbatfield import ZbaTfield
import re


class ZbaAfield:
    """
    ZBA AF field class:
    x, y list[height, width]
    init: (list float x, list float y, float w, float h)
    from_string: accepts string format "T[A|R|W]:list(float x,float y);list(ufield);list(rect);"
    """

    def __init__(self, pos=(0, 0,), size=(3200.0, 3200.0,), tf_list=None, uf_list=None, rect_list=None):
        self.pos = list(pos)
        self.size = list(size)
        self.tfield_list = tf_list
        self.ufield_list = uf_list
        self.rect_list = rect_list

    def pos_list_from_string(self, pos_string=None):
        if pos_string is None:
            raise ValueError("Pos string is None.")

        # check pos_string format
        r = re.compile(r"^AF:\d*?\.?\d+?,\d*?\.?\d+?;$")
        if not r.match(pos_string):
            raise ValueError("Wrong AF position format:", pos_string)

        return [float(x) for x in pos_string.strip("AF:").strip(";").split(",")]


    @classmethod
    def from_string(cls, afield_as_string="", af_size=None, tf_size=None):
        """
        Parses input AF string to make an AF object. Checks AF pos format, checks TF formats for presens of UF.
        :param afield_as_string: prepared AF string, must have TF and RECT specifiers 
        :param af_size: AF size, passed from header
        :return: AF object
        """

        # split Afield header
        strlist = afield_as_string.split(";", 1)

        # make AF pos list
        pos_list = cls.pos_list_from_string(cls, pos_string=strlist[0] + ";")

        tlist = ["T" + s.replace("UG", "UT") for s in strlist[1].replace("UT", "UG").split("T")[1:]]

        # make TF list
        for s in tlist:
            tf = ZbaTfield.from_string(tfield_as_string=s, tf_size=tf_size)
            break

        # TODO return class
        # for s in tfstrlist:
        #     t_list.append(zbatfield.ZbaTfield.from_string(s.replace("UG", "UT").strip("@")))
        #
        # return cls(pos_list, cls.size, t_list, [], [])

    def dump(self):
        print("AF(", self.pos, self.size, ")")
        print("N Tfields:", len(self.tfield_list))

    def dump_tfields(self):
        for tf in self.tfield_list:
            tf.dump()
