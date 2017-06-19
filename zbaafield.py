import zbatfield


class ZbaAfield:
    """
    ZBA field class:
    x, y list[height, width]
    init: (list float x, list float y, float w, float h)
    from_string: accepts string format "T[A|R|W]:list(float x,float y);list(ufield);list(rect);"
    """
    pos = [0.0, 0.0]
    size = [3200.0, 3200.0]  # default size

    def __init__(self, pos, size, t_list, u_list, r_list):
        self.pos = pos
        self.size = size
        self.tfield_list = t_list
        self.ufield_list = u_list
        self.rect_list = r_list

    @classmethod
    def from_string(cls, afield_as_string):
        # check afield format
        if afield_as_string.index("AF") != 0 or ";R" not in afield_as_string:
            raise ValueError("Wrong afield string format:", afield_as_string)

        # split afield header
        delim = afield_as_string.index(";") + 1
        posstr = afield_as_string[:delim]
        tfstr = afield_as_string[delim:]

        # fill position list
        pos_list = [float(x) for x in posstr.strip("AF:").strip(";").split(",")]

        # fill tfield list
        tfstrlist = ["T" + s for s in tfstr.replace("UT", "UG").split("T")[1:]]
        t_list = []
        for s in tfstrlist:
            t_list.append(zbatfield.ZbaTfield.from_string(s.replace("UG", "UT").strip("@")))

        # TODO: add ufield list and rect list if needed
        return cls(pos_list, cls.size, t_list, [], [])

    def dump(self):
        print("AF(", self.pos, self.size, ")")
        print("N Tfields:", len(self.tfield_list))

    def dump_tfields(self):
        for tf in self.tfield_list:
            tf.dump()
