import zbatfield


class ZbaAfield:
    """
    ZBA field class:
    x, y list[height, width]
    init: (list float x, list float y, float w, float h)
    from_string: accepts string format "T[A|R|W]:list(float x,float y);list(ufield);list(rect);"
    """
    pos = [0.0, 0.0]
    size = [200.0, 200.0]  # default size
    tfield_list = []

    def __init__(self, x, y, w, h, t_list):
        self.pos = [x, y]
        self.size = [w, h]
        self.tfield_list = t_list

    @classmethod
    def from_string(cls, afield_as_string):
        # TODO: make a validator
        print(afield_as_string)
        if afield_as_string[0] != "A" \
                or ";T" not in afield_as_string \
                or ";U" not in afield_as_string \
                or ";R" not in afield_as_string:
            raise ValueError("Wrong tfield string format.")

        delim = afield_as_string.index(";T") + 1
        posstr = afield_as_string[:delim]
        tfstr = afield_as_string[delim:]

        vals = posstr.strip("AF:").strip(";").split(",")
        pos = [float(vals[0]), float(vals[1])]

        t_list = [zbatfield.ZbaTfield.from_string("T" + s.strip("@")) for s in tfstr.split("T")[1:]]

        return cls(pos[0], pos[1], cls.size[0], cls.size[1], t_list)

    def dump(self):
        print("AF(", self.pos, self.size, ")")
        print("N Tfields:", len(self.tfield_list))

    def dump_tfields(self):
        for tf in self.tfield_list:
            tf.dump()
