import re


class ZbaRect:
    """
    ZBA rectangle class:
    x, y, height, width, doseid
    init: (float x, float y, float w, float h, int d)
    from_string: accepts string format "float x,float y,float w,float h[,int doseid]"
    """
    pos = [0.0, 0.0]
    size = [0.0, 0.0]
    doseid = 0

    def __init__(self, x, y, w, h, d=None):
        self.pos = [x, y]
        self.size = [w, h]
        self.doseid = d

    @classmethod
    def from_string(cls, rect_as_string):
        # (regex matches both R forms: float,float,float,float | float,float,float,float,[1-8])
        # TODO: check dose range [0-7] or [1-8]
        # p = re.compile(r"^\d*?\.?\d+?,\d*?\.?\d+?,\d*?\.?\d+?,\d*?\.?\d+?(,[1-8])?;$")
        p = re.compile(r"^\d*?\.?\d+?,\d*?\.?\d+?,\d*?\.?\d+?,\d*?\.?\d+?(,[1-8])?$")
        if not p.match(rect_as_string):
            raise ValueError("Wrong rect string format.")

        tmp = rect_as_string.split(",")
        if len(tmp) == 4:
            return cls(float(tmp[0]), float(tmp[1]), float(tmp[2]), float(tmp[3]))
        elif len(tmp) == 5:
            return cls(float(tmp[0]), float(tmp[1]), float(tmp[2]), float(tmp[3]), int(tmp[4]))
        else:
            raise ValueError("Wrong rect parameter list.")

    def dump(self):
        print("rect(", self.pos, self.size, self.doseid, ")")
