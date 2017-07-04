import re


class ZbaRect(object):
    """
    ZBA rectangle class:
    x, y, height, width, doseid
    init: (float x, float y, float w, float h, int d)
    from_string: accepts string format "float x,float y,float w,float h[,*int dose_id[0-7]]"
    """

    def __init__(self, pos, size, d=0):
        self.pos = pos
        self.size = size
        self.dose_id = d

    def __str__(self):
        return "Rect(pos:" + str(self.pos) + ", size:" + str(self.size) + ", dose id:" + str(self.dose_id) + ")"

    @classmethod
    def from_string(cls, rect_as_string):
        # (regex matches both R forms: Rfloat,float,float,float; | Rfloat,float,float,float,*[1-8];)
        p = re.compile(r"^R\d*?\.?\d+?,\d*?\.?\d+?,\d*?\.?\d+?,\d*?\.?\d+?(,\*[0-7])?;$")
        if not p.match(rect_as_string):
            raise ValueError("Wrong rect string format:", rect_as_string)

        tmp = rect_as_string.strip("R").strip(";").split(",")

        if len(tmp) == 4:
            return cls([float(tmp[0]), float(tmp[1])], [float(tmp[2]), float(tmp[3])], 0)
        elif len(tmp) == 5:
            dose = int(tmp[4].strip("*"))
            if dose not in range(8):
                raise ValueError("Wrong dose specifier:", dose)

            return cls([float(tmp[0]), float(tmp[1])], [float(tmp[2]), float(tmp[3])], dose)
        else:
            raise ValueError("Wrong rect parameter list:", tmp)
