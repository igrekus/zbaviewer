class ZbaDocHeader(object):
    """
    ZBA document header class:
    <padding <512 bytes 0x20>>
    <ODB:<filename.OL(12 chars)>,  <format TX|BI>, <E>, <AF sizex*sizey>, <M float_scale,
    <GF float_max_stamp>, <KR float_min_stamp>, <IV float_dose_list[x,x,x,x,x,x,x,x]>;@>
    <512 - <size(ODB block) bytes(0x20)> - 1 byte(0x40)>
    """

    def __init__(self, file_name=None, data_format="TX", E="E", af_size=(3200.0, 3200.0,), scale_factor=1,
                 max_stamp=6.2, min_stamp=0.2, doses=(1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,)):
        self.front_padding = ""
        self.filename = file_name
        self.data_format = data_format
        self.E = E
        self.af_size = list(af_size)
        self.scale_factor = scale_factor
        self.max_stamp = max_stamp
        self.min_stamp = min_stamp
        self.doses = list(doses)

    def __str__(self):
        return "ZBA doc header:"\
            "\npadding: " + self.front_padding +\
            "\nfile name: " + self.filename +\
            "\ndata format: " + self.data_format +\
            "\ndata type: " + self.E +\
            "\nAF size: " + str(self.af_size) +\
            "\nscale factor: " + str(self.scale_factor) +\
            "\nmax stamp: " + str(self.max_stamp) +\
            "\nmin stamp: " + str(self.min_stamp) +\
            "\ndoses: " + str(self.doses)

    @classmethod
    def from_string(cls, header_as_string):
        # TODO regex: check header format
        tmplist = header_as_string.strip("ODB:").strip(";@").replace("IV", "").split(",")
        name = tmplist[0]
        frm = tmplist[1]
        e = tmplist[2]
        size = [float(s) for s in tmplist[3].strip("AF").split("*")]
        scale = float(tmplist[4].strip("M"))
        mx = float(tmplist[5].strip("GF"))
        mn = float(tmplist[6].strip("KR"))
        doses = list()
        for s in tmplist[7:]:
            doses.append(float(s)/10)

        return cls(name, frm, e, size, scale, mx, mn, doses)
