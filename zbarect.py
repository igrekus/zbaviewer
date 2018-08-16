import re
# from PyQt5.QtWidgets import QGraphicsRectItem


class ZbaRect:
    """
    ZBA rectangle class.
    
    properties:
    pos: [float, float] - rectangle position, microns
    size: [float, float] - rectangle size, microns
    d: int - dose table ID

    from_string: makes RECT object from RECT string
    """

    def __init__(self, x: float=0, y: float=0, w: float=0, h: float=0, d: int=0, parent=None):
        """
        Default constructor, takes:
        :param x: float 
        :param y: float 
        :param w: float 
        :param h: float         
        :param d: int, [0-7]
        """
        print("new zbarect")
        # self.setRect(0, 0, w, h)
        # self.posx: float = x
        # self.posy: float = y
        # self.dose_id: int = d

    # def __str__(self):
    #     return "ZBARect(rect:" + str(self.posx) + ", " + str(self.posy) + ", " + \
    #            str(self.rect().width()) + ", " + str(self.rect().height()) + \
    #            ", dose id:" + str(self.dose_id) + ")"
    #
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
