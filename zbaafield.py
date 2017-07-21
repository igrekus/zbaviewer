from zbatfield import ZbaTfield
import re


class ZbaAfield:
    """
    ZBA AField class.

    properties: 
    default_size: [float, float] - default AField size, microns
    size: [float, float] - actual TField size, microns
    pos_list: list[float, float] - TField position list, microns
    
    from_string: parses UField string and makes UField object.
    """

    default_size = [3200.0, 3200.0]

    def __init__(self, pos=(0, 0,), size=(3200.0, 3200.0,), t_list=None):
        self.size: list = list(size)
        self.pos: list = list(pos)
        self.tfield_list: list = t_list

    def __str__(self) -> str:
        return "AF(pos:" + str(self.pos) + " size:" + str(self.size) + ")" + \
            "\nN TFields:" + str(len(self.tfield_list))


    def pos_list_from_string(self, string):
        # check <AF:float,float;>
        r = re.compile(r"^AF:\d*?\.?\d+?,\d*?\.?\d+?;$")
        if not r.match(string):
            raise ValueError("Wrong AF position format:", string)

        p_list = [[float(x) for x in string.strip("AF:").strip(";").split(",")]]

        return p_list

    @classmethod
    def from_string(cls, afield_as_string="", af_size=None, tf_size=None):
        """
        Makes ZbaAfield instance object from a given sanitized string.
        :param afield_as_string: str - "@<AF>:<position parameter list><TField string>"
        :param af_size: [float, float] - AField size
        :param tf_size: [float, float] - TFiled size
        :return: ZbaUfield instance object
        """

        # split Afield header
        strlist = afield_as_string.split(";", 1)

        # make AF pos list
        pos_list = cls.pos_list_from_string(cls, string=strlist[0] + ";")

        tf_str_list = ["T" + s.replace("UG", "UT") for s in strlist[1].replace("UT", "UG").split("T")[1:]]

        # make TF list
        tf_list = [ZbaTfield.from_string(tfield_as_string=s, tf_size=tf_size) for s in tf_str_list]

        return cls(pos=pos_list, size=cls.default_size, t_list=tf_list)

    def print_tfields(self):
        for tf in self.tfield_list:
            print(tf)
