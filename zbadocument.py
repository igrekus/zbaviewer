from zbadocheader import ZbaDocHeader
from zbaafield import ZbaAfield


class ZbaDocument(object):
    """
    ZBA AField class.

    properties: 
    header: ZbaDocHeader - ZBA document header object
    afield_list: list[ZbaAfield] - ZBA AField list 

    from_string: parses ZBA document data and makes ZbaDocument object.
    """

    def __init__(self, header=None, a_list=None):
        self.header: ZbaDocHeader = header
        self.afield_list: list = a_list

    def __str__(self) -> str:
        return str(self.header) + \
            "\nN AFields:" + str(len(self.afield_list))

    @classmethod
    def from_string(cls, doc_as_string):
        # TODO TF size (not needed on read)
        strlist = "".join(doc_as_string.split()).split(";@", 1)

        # make header
        hdr = ZbaDocHeader.from_string(strlist[0] + ";@")

        # make AF list
        tmpstr = strlist[1].strip("$")
        strlist = ["AF:" + s for s in tmpstr.split("AF:")[1:]]

        af_list = list()
        for s in strlist:
            # test for empty AFields
            if "TA:" not in s and "TR:" not in s and "TW:" not in s:
                print("Empty AF (no TAF specified), skip:", s)
                continue
            if ";R" not in s:
                print("Empty AF (no RECT specified), skip:", s)
                continue

            # make AF list
            af_list.append(ZbaAfield.from_string(s, af_size=hdr.af_size, tf_size=[200.0, 200.0]))

        return cls(header=hdr, a_list=af_list)

    def print_afields(self):
        for af in self.afield_list:
            print(af)
