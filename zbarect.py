import re
import attr


@attr.s
class ZbaRect:
    """
    Represents ZBA rectangle
    
    attrs:
    x, y: float, float - rectangle position, microns
    w, h: float, float - rectangle width, microns
    d: int             - dose table ID

    from_string: makes RECT object from RECT string
    """
    x = attr.ib(type=float, default=0.0)
    y = attr.ib(type=float, default=0.0)
    w = attr.ib(type=float, default=0.0)
    h = attr.ib(type=float, default=0.0)
    d = attr.ib(type=int, default=1)

    # def scaleRect(self, scale):
    #     self.posx *= scale
    #     self.posy *= scale
    #     rect = self.rect()
    #     rect.adjust(0, 0, rect.width() * scale, rect.height() * scale)
    #     self.setRect(rect)
    #
    # @classmethod
    # def fromCopy(cls, src):
    #     return cls(src.posx, src.posy, src.rect().width(), src.rect().height(), src.dose_id)
    #
    # @classmethod
    # def from_string(cls, rect_as_string: str):
    #     """
    #     Makes ZbaRect instance object from a given sanitized string.
    #     :param rect_as_string: "Rx,y,w,h,*[1-8];"
    #     :return: ZbaRect instance object
    #     """
    #     # (regex matches both R forms: Rfloat,float,float,float; | Rfloat,float,float,float,*[1-8];)
    #     p = re.compile(r"^R\d*?\.?\d+?,\d*?\.?\d+?,\d*?\.?\d+?,\d*?\.?\d+?(,\*[0-7])?;$")
    #     if not p.match(rect_as_string):
    #         raise ValueError("Wrong rect string format:", rect_as_string)
    #
    #     tmp = rect_as_string.strip("R").strip(";").split(",")
    #
    #     if len(tmp) == 4:
    #         return cls(float(tmp[0]), float(tmp[1]), float(tmp[2]), float(tmp[3]), 0)
    #     elif len(tmp) == 5:
    #         dose = int(tmp[4].strip("*"))
    #         if dose not in range(8):
    #             raise ValueError("Wrong dose specifier:", dose)
    #
    #         return cls(float(tmp[0]), float(tmp[1]), float(tmp[2]), float(tmp[3]), dose)
    #     else:
    #         raise ValueError("Wrong rect parameter list:", tmp)
