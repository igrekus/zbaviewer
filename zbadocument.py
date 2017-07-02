from zbadocheader import ZbaDocHeader
from zbaafield import ZbaAfield

class ZbaDocument(object):
    """
    ZBA document class:
    """
    header = object
    afield_list = []

    def __init__(self, hdr, af_list):
        self.header = hdr
        self.afield_list = af_list

    @classmethod
    def from_string(cls, doc_as_string):
        # TODO TF size
        tstr = "".join(doc_as_string.split())
        tlist = tstr.split(";@", 1)

        # make header
        hdr = ZbaDocHeader.from_string(tlist[0] + ";@")

        # make AF list
        tstr = tlist[1]
        tlist = ["AF:" + s for s in tstr.split("AF:")[1:]]
        for s in tlist:
            # test for empty AF
            if "TA:" not in s and "TR:" not in s and "TW:" not in s:
                print("Empty AF (no TAF specified), skip:", s)
                continue
            if ";R" not in s:
                print("Empty AF (no RECT specified), skip:", s)
                continue

            # make AF list
            tmpaf = ZbaAfield.from_string(s, af_size=hdr.af_size, tf_size=[200.0, 200.0])
            break

        # return cls(hdr, a_list)

    def dump(self):
        self.header.dump()
        print("N AFields:", len(self.afield_list))

    def dump_afields(self):
        for af in self.afield_list:
            af.dump()
