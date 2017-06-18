from enum import Enum


class DocFormat(Enum):
    TXT = 0
    BIN = 1


class ZbaDocHeader(object):
    """
    ZBA document header class:
    <padding <512 bytes 0x20>>
    <ODB:<filename.OL(12 chars)>,  <format TX|BI>, <E>, <AF sizex*sizey>, <M float_scale,
    <GF float_max_stamp>, <KR float_min_stamp>, <IV float_dose_list[x,x,x,x,x,x,x,x]>;>
    <512 - <size(ODB block) bytes(0x20)> - 1 byte(0x40)>
    """
    front_padding = ""
    filename = ""
    format = DocFormat.TXT
    e = "E"
    size = [3200.0, 3200.0]
    scale_factor = 1.0
    max_stamp = 6.0
    min_stamp = 0.2
    doses = []
    back_padding = ""

    def __init__(self, name, f, e, size, scale, mx, mn, doses):
        # for i in range(512):
        #     self.front_padding += " "
        self.filename = name
        self.format = f
        self.e = e
        self.size = size
        self.scale_factor = scale
        self.max_stamp = mx
        self.min_stamp = mn
        self.doses = doses

    @classmethod
    def from_string(cls, header_as_string):
        # tmplist = header_as_string.replace(" ", "").strip("ODB:").strip(";@").split(",")
        tmplist = header_as_string.strip("ODB:").strip(";@").split(",")

        name = tmplist[0]

        if tmplist[1] == "TX":
            frm = DocFormat.TXT
        elif tmplist[1] == "BI":
            frm = DocFormat.BIN
        else:
            raise ValueError("Wrong document format.")

        e = tmplist[2]
        size = [float(s) for s in tmplist[3].strip("AF").split("*")]
        scale = float(tmplist[4].strip("M"))
        mx = float(tmplist[5].strip("GF"))
        mn = float(tmplist[6].strip("KR"))
        doses = []
        doses.append(float(tmplist[7].strip("IV")))
        for s in tmplist[8:]:
            doses.append(float(s))

        return cls(name, frm, e, size, scale, mx, mn, doses)

    def dump(self):
        print(len(self.front_padding))
        print("filename:", self.filename)
        print("format:", self.format)
        print("E(?):", self.e)
        print("AFsize:", self.size)
        print("scale:", self.scale_factor)
        print("max stamp size:", self.max_stamp)
        print("min stamp size:", self.min_stamp)
        print("dose table:", self.doses)
        print(len(self.back_padding))
