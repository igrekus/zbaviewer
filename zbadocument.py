import zbadocheader
import zbaafield


class ZbaDocument:
    """
    ZBA document class:
    <padding <512 bytes 0x20>>
    <ODB:<filename.OL(12 chars)>,  <format TX|BI>, <E>, <AF sizex*sizey>, <M float_scale,
    <GF float_max_stamp>, <KR float_min_stamp>, <IV int_dose_list[x,x,x,x,x,x,x,x]>;>
    <512 - <size(ODB block) bytes(0x20)> - 1 byte(0x40)>
    """
    header = object
    afield_list = []

    def __init__(self, hdr, af_list):
        self.header = hdr
        self.afield_list = af_list

    @classmethod
    def from_string(cls, doc_as_string):
        tmp = doc_as_string.replace(" ", "").replace("UT", "UG").strip("$").replace("@", "")
        delim = tmp.index("AF:", 1)
        hdrstr = tmp[:delim]
        bodystr = tmp[delim:]

        hdr = zbadocheader.ZbaDocHeader.from_string(hdrstr)

        a_list = [zbaafield.ZbaAfield.from_string("A"+s) for s in bodystr.split("A")[1:]]

        return cls(hdr, a_list)

    def dump(self):
        self.header.dump()
        print("N AFields:", len(self.afield_list))

    def dump_afields(self):
        for af in self.afield_list:
            af.dump()
