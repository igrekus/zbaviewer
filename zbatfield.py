import re
from zbarect import ZbaRect
from zbaufield import ZbaUfield


class ZbaTfield(object):
    """
    ZBA TField class.
    
    properties: 
    default_size: [float, float] - default TField size, microns
    tfield_type: str [TA, TR, TW] - TField type
    size: [float, float] - actual TField size, microns
    pos_list: list[float, float] - TField position list, microns
    ufield_list: list[ZbaUfield] - list of UFields, defined inside current TField
    rect_list: list[ZbaRect] - list of rectangles, defined inside current TField

    from_string: parses UField string and makes UField object.
    """

    default_size = [200.0, 200.0]

    def __init__(self, tf_type=None, size=(200.0, 200.0, ), p_list=None, u_list=None, r_list=None):
        self.tfield_type: str = tf_type
        self.size: list = list(size)
        self.pos_list: list = p_list
        self.ufield_list: list = u_list
        self.rect_list: list = r_list

    def __str__(self):
        return "TField(size:" + str(self.size) + ", type:" + self.tfield_type + ", N pos:" + str(len(self.pos_list)) + ")" + \
            "\npos:" + str(self.pos_list) + \
            "\nN UFields:" + str(len(self.ufield_list)) + \
            "\nN RECTs:" + str(len(self.rect_list))

    def parse_pos_string(self, pos_string=None):
        """
        Internal helper method.
        :param pos_string: str - "<TA|TW|TR><position parameter list>[UField list][RECT list]" 
        :return: 
        """
        # TODO parse string and make a proper generator to use later
        def from_ta_string(string: str):
            # check <TA:float,float;>
            p = re.compile(r"^TA:\d*?\.?\d+?,\d*?\.?\d+?;$")
            if not p.match(string):
                raise ValueError("Wrong TA format.")

            p_list = [[float(s) for s in string.strip("TA:").strip(";").split(",")]]
            return p_list

        def from_tr_string(string: str):

            def pos_generator():
                for j in range(ny):
                    for i in range(nx):
                        yield [x0 + int(dx * i * 10) / 10, y0 + int(dy * j * 10) / 10]

            # check <TR:float,float,float,float,int,int;>
            p = re.compile(r"^TR:\d*?\.?\d+?,\d*?\.?\d+?,\d*?\.?\d+?,\d*?\.?\d+?,\d*?\.?\d+?,\d*?\.?\d+?;$")
            if not p.match(string):
                raise ValueError("Wrong TR format.")

            vals = string.strip("TR:").strip(";").split(",")

            x0 = float(vals[0])
            y0 = float(vals[1])
            dx = float(vals[2])
            dy = float(vals[3])
            nx = int(vals[4])
            ny = int(vals[5])

            p_list = [p for p in pos_generator()]
            return p_list

        def from_tw_string(string: str):

            def pos_generator():
                for i, x in enumerate(string.strip("TW:").strip(";").split(",")):
                    if not i & 1:
                        # x
                        pair = list()
                        pair.append(float(x))
                    else:
                        # y
                        pair.append(float(x))
                        yield pair

            # check <TW:float,float[,float,float];>
            p = re.compile(r"^TW:\d*?\.?\d+?,\d*?\.?\d+?(,\d*?\.?\d+?,\d*?\.?\d+?)*?;$")
            if not p.match(string):
                raise ValueError("Wrong TW format (may be coordinate count?):", string)

            p_list = [p for p in pos_generator()]
            return p_list

        if "TA" in pos_string:
            tf_type = "TA"
            pos_list = from_ta_string(pos_string)

        elif "TR" in pos_string:
            tf_type = "TR"
            pos_list = from_tr_string(pos_string)

        elif "TW" in pos_string:
            tf_type = "TW"
            pos_list = from_tw_string(pos_string)

        else:
            raise ValueError("Wrong pos string format:", pos_string)

        return tf_type, pos_list

    @classmethod
    def from_string(cls, tfield_as_string=None, tf_size=None):
        """
        Makes ZbaTfield instance object from a given sanitized string.
        :param tfield_as_string: str - "@<TA|TA|TA>:<position parameter list>[UField string][RECT string]"
        :param tf_size: [float, float] - TField size
        :return: ZbaUfield instance object
        """
        if tfield_as_string is None or tf_size is None:
            raise ValueError("TF string and tf_size must not be None.")

        # print(tfield_as_string)

        # split TField header
        strlist = tfield_as_string.split(";", 1)

        # make TField pos list
        tf_type, pos_list = cls.parse_pos_string(cls, pos_string=strlist[0] + ";")

        # check data string for Ufield presence
        tmpstr = strlist[1]

        uf_list = list()
        rect_list = list()

        # random UFields + stray RECTs, preceding RECT
        # tmpstr = "R24.6,1.6,1.0,.1;R25.2,1.7,.4,.1;R23.0,.4,2.6,.1;R23.6,.5,2.0,.1;R24.7,.7,.9,.1;R25.3,.8,.3,.1;UW:.0,25.2,.0,24.3,.0,23.4,.0,22.4,.0,21.5,.0,20.6,.0,19.7,.0,18.8,.0,17.9,.0,17.0,.0,16.0,.0,15.1,.0,14.2,.0,13.3,.0,12.4,.0,11.5,.0,10.6,.0,9.6,.0,8.7,.0,7.8,.0,6.9,.0,6.0,.0,5.1,.0,4.2,.0,3.2,.0,2.3,.0,1.4,.0,.5,25.0,4.4,25.0,3.5;R0,0,.6,.1;@UW:.0,25.3,.0,24.4,.0,23.5,.0,22.5,.0,21.6,.0,20.7,.0,19.8,.0,18.9,.0,18.0,.0,17.1,.0,16.1,.0,15.2,.0,14.3,.0,13.4,.0,12.5,.0,11.6,.0,10.7,.0,9.7,.0,8.8,.0,7.9,.0,7.0,.0,6.1,.0,5.2,.0,4.3,.0,3.3,.0,2.4,.0,1.5,.0,.6,24.5,3.4,24.5,2.5;R0,0,1.1,.1;@UW:.0,25.4,.0,24.5,.0,23.6,.0,22.6,.0,21.7,.0,20.8,.0,19.9,.0,19.0,.0,18.1,.0,17.2,.0,16.2,.0,15.3,.0,14.4,.0,13.5,.0,12.6,.0,11.7,.0,10.8,.0,9.8,.0,8.9,.0,8.0,.0,7.1,.0,6.2,.0,5.3,.0,4.4,.0,3.4,.0,2.5,.0,1.6,.0,.7,23.9,3.3;R0,0,1.7,.1;@UW:.0,25.5,.0,24.6,.0,23.7,.0,22.7,.0,21.8,.0,20.9,.0,20.0,.0,19.1,.0,18.2,.0,17.3,.0,16.3,.0,15.4,.0,14.5,.0,13.6,.0,12.7,.0,11.8,.0,10.9,.0,9.9,.0,9.0,.0,8.1,.0,7.2,.0,6.3,.0,5.4,.0,4.5,.0,3.5,.0,2.6,.0,1.7,.0,.8,23.3,4.1,23.3,3.2;R0,0,2.3,.1;@UW:.0,24.7,.0,23.8,.0,22.8,.0,21.9,.0,21.0,.0,20.1,.0,19.2,.0,18.3,.0,17.4,.0,16.4,.0,15.5,.0,14.6,.0,13.7,.0,12.8,.0,11.9,.0,11.0,.0,10.0,.0,9.1,.0,8.2,.0,7.3,.0,6.4,.0,5.5,.0,4.6,.0,3.6,.0,2.7,.0,1.8,.0,.9,22.8,3.1,22.8,2.2;R0,0,2.8,.1;@UW:.5,24.8,1.1,24.9,1.7,25.0,2.2,25.1,2.8,25.2,3.4,25.3,3.9,25.4,4.5,25.5,.5,23.9,1.1,24.0,1.7,24.1,2.2,24.2,2.8,24.3,3.4,24.4,3.9,24.5,4.5,24.6,5.1,24.7,5.6,24.8,6.2,24.9,6.8,25.0,7.3,25.1,7.9,25.2,8.5,25.3,9.0,25.4,9.6,25.5,.5,22.9,1.1,23.0,1.7,23.1,2.2,23.2,2.8,23.3,3.4,23.4,3.9,23.5,4.5,23.6,5.1,23.7,5.6,23.8,6.2,23.9,6.8,24.0,7.3,24.1,7.9,24.2,8.5,24.3,9.0,24.4,9.6,24.5,10.2,24.6,10.7,24.7,11.3,24.8,11.9,24.9,12.4,25.0,13.0,25.1,13.6,25.2,14.1,25.3,14.7,25.4,15.3,25.5,.5,22.0,1.1,22.1,1.7,22.2,2.2,22.3,2.8,22.4,3.4,22.5,3.9,22.6,4.5,22.7,5.1,22.8,5.6,22.9,6.2,23.0,6.8,23.1,7.3,23.2,7.9,23.3,8.5,23.4,9.0,23.5,9.6,23.6,10.2,23.7,10.7,23.8,11.3,23.9,11.9,24.0,12.4,24.1,13.0,24.2,13.6,24.3,14.1,24.4,14.7,24.5,15.3,24.6,15.8,24.7,16.4,24.8,17.0,24.9,17.5,25.0,18.1,25.1,18.7,25.2,19.2,25.3,19.8,25.4,20.4,25.5,.5,21.1,1.1,21.2,1.7,21.3,2.2,21.4,2.8,21.5,3.4,21.6,3.9,21.7,4.5,21.8,5.1,21.9,5.6,22.0,6.2,22.1,6.8,22.2,7.3,22.3,7.9,22.4,8.5,22.5,9.0,22.6,9.6,22.7,10.2,22.8,10.7,22.9,11.3,23.0,11.9,23.1,12.4,23.2,13.0,23.3,13.6,23.4,14.1,23.5,14.7,23.6,15.3,23.7,15.8,23.8,16.4,23.9,17.0,24.0,17.5,24.1,18.1,24.2,18.7,24.3,19.2,24.4,19.8,24.5,20.4,24.6,20.9,24.7,21.5,24.8,22.1,24.9,22.6,25.0,.5,20.2,1.1,20.3,1.7,20.4,2.2,20.5,2.8,20.6,3.4,20.7,3.9,20.8,4.5,20.9,5.1,21.0,5.6,21.1,6.2,21.2,6.8,21.3,7.3,21.4,7.9,21.5,8.5,21.6,9.0,21.7,9.6,21.8,10.2,21.9,10.7,22.0,11.3,22.1,11.9,22.2,12.4,22.3,13.0,22.4,13.6,22.5,14.1,22.6,14.7,22.7,15.3,22.8,15.8,22.9,16.4,23.0,17.0,23.1,17.5,23.2,18.1,23.3,18.7,23.4,19.2,23.5,19.8,23.6,20.4,23.7,20.9,23.8,21.5,23.9,22.1,24.0,22.6,24.1,.5,19.3,1.1,19.4,1.7,19.5,2.2,19.6,2.8,19.7,3.4,19.8,3.9,19.9,4.5,20.0,5.1,20.1,5.6,20.2,6.2,20.3,6.8,20.4,7.3,20.5,7.9,20.6,8.5,20.7,9.0,20.8,9.6,20.9,10.2,21.0,10.7,21.1,11.3,21.2,11.9,21.3,12.4,21.4,13.0,21.5,13.6,21.6,14.1,21.7,14.7,21.8,15.3,21.9,15.8,22.0,16.4,22.1,17.0,22.2,17.5,22.3,18.1,22.4,18.7,22.5,19.2,22.6,19.8,22.7,20.4,22.8,20.9,22.9,21.5,23.0,22.1,23.1,22.6,23.2,.5,18.4,1.1,18.5,1.7,18.6,2.2,18.7,2.8,18.8,3.4,18.9,3.9,19.0,4.5,19.1,5.1,19.2,5.6,19.3,6.2,19.4,6.8,19.5,7.3,19.6,7.9,19.7,8.5,19.8,9.0,19.9,9.6,20.0,10.2,20.1,10.7,20.2,11.3,20.3,11.9,20.4,12.4,20.5,13.0,20.6,13.6,20.7,14.1,20.8,14.7,20.9,15.3,21.0,15.8,21.1,16.4,21.2,17.0,21.3,17.5,21.4,18.1,21.5,18.7,21.6,19.2,21.7,19.8,21.8,20.4,21.9,20.9,22.0,21.5,22.1,22.1,22.2,22.6,22.3,.5,17.5,1.1,17.6;R0,0,2.9,.1;@UW:23.2,25.1,23.2,24.2,23.2,23.3,23.2,22.4,23.2,21.5,23.2,20.5,23.2,19.6,23.2,18.7,23.2,17.8,23.2,16.9,23.2,16.0,23.2,15.1,23.2,14.1,23.2,13.2,23.2,12.3,23.2,11.4,23.2,10.5,23.2,9.6,23.2,8.7,23.2,7.7,23.2,6.8,23.2,5.9,23.2,5.0;R0,0,2.4,.1;@UW:23.8,25.2,23.8,24.3,23.8,23.4,23.8,22.5,23.8,21.6,23.8,20.6,23.8,19.7,23.8,18.8,23.8,17.9,23.8,17.0,23.8,16.1,23.8,15.2,23.8,14.2,23.8,13.3,23.8,12.4,23.8,11.5,23.8,10.6,23.8,9.7,23.8,8.8,23.8,7.8,23.8,6.9,23.8,6.0,23.8,5.1,23.8,4.2;R0,0,1.8,.1;@UW:24.3,25.3,24.3,24.4,24.3,23.5,24.3,22.6,24.3,21.7,24.3,20.7,24.3,19.8,24.3,18.9,24.3,18.0,24.3,17.1,24.3,16.2,24.3,15.3,24.3,14.3,24.3,13.4,24.3,12.5,24.3,11.6,24.3,10.7,24.3,9.8,24.3,8.9,24.3,7.9,24.3,7.0,24.3,6.1,24.3,5.2;R0,0,1.3,.1;@UW:24.9,25.4,24.9,24.5,24.9,23.6,24.9,22.7,24.9,21.8,24.9,20.8,24.9,19.9,24.9,19.0,24.9,18.1,24.9,17.2,24.9,16.3,24.9,15.4,24.9,14.4,24.9,13.5,24.9,12.6,24.9,11.7,24.9,10.8,24.9,9.9,24.9,9.0,24.9,8.0,24.9,7.1,24.9,6.2,24.9,5.3;R0,0,.7,.1;@UW:25.5,25.5,25.5,24.6,25.5,23.7,25.5,22.8,25.5,21.9,25.5,20.9,25.5,20.0,25.5,19.1,25.5,18.2,25.5,17.3,25.5,16.4,25.5,15.5,25.5,14.5,25.5,13.6,25.5,12.7,25.5,11.8,25.5,10.9,25.5,10.0,25.5,9.1,25.5,8.1,25.5,7.2,25.5,6.3,25.5,5.4;R0,0,.1,.1;@UW:1.7,17.7,2.2,17.8,2.8,17.9,3.4,18.0,3.9,18.1,4.5,18.2,5.1,18.3,5.6,18.4,6.2,18.5,6.8,18.6,7.3,18.7,7.9,18.8,8.5,18.9,9.0,19.0,9.6,19.1,10.2,19.2,10.7,19.3,11.3,19.4,11.9,19.5,12.4,19.6,13.0,19.7,13.6,19.8,14.1,19.9,14.7,20.0,15.3,20.1,15.8,20.2,16.4,20.3,17.0,20.4,17.5,20.5,18.1,20.6,18.7,20.7,19.2,20.8,19.8,20.9,20.4,21.0,20.9,21.1,21.5,21.2,22.1,21.3,22.6,21.4,.5,16.5,1.1,16.6,1.7,16.7,2.2,16.8,2.8,16.9,3.4,17.0,3.9,17.1,4.5,17.2,5.1,17.3,5.6,17.4,6.2,17.5,6.8,17.6,7.3,17.7,7.9,17.8,8.5,17.9,9.0,18.0,9.6,18.1,10.2,18.2,10.7,18.3,11.3,18.4,11.9,18.5,12.4,18.6,13.0,18.7,13.6,18.8,14.1,18.9,14.7,19.0,15.3,19.1,15.8,19.2,16.4,19.3,17.0,19.4,17.5,19.5,18.1,19.6,18.7,19.7,19.2,19.8,19.8,19.9,20.4,20.0,20.9,20.1,21.5,20.2,22.1,20.3,22.6,20.4,.5,15.6,1.1,15.7,1.7,15.8,2.2,15.9,2.8,16.0,3.4,16.1,3.9,16.2,4.5,16.3,5.1,16.4,5.6,16.5,6.2,16.6,6.8,16.7,7.3,16.8,7.9,16.9,8.5,17.0,9.0,17.1,9.6,17.2,10.2,17.3,10.7,17.4,11.3,17.5,11.9,17.6,12.4,17.7,13.0,17.8,13.6,17.9,14.1,18.0,14.7,18.1,15.3,18.2,15.8,18.3,16.4,18.4,17.0,18.5,17.5,18.6,18.1,18.7,18.7,18.8,19.2,18.9,19.8,19.0,20.4,19.1,20.9,19.2,21.5,19.3,22.1,19.4,22.6,19.5,.5,14.7,1.1,14.8,1.7,14.9,2.2,15.0,2.8,15.1,3.4,15.2,3.9,15.3,4.5,15.4,5.1,15.5,5.6,15.6,6.2,15.7,6.8,15.8,7.3,15.9,7.9,16.0,8.5,16.1,9.0,16.2,9.6,16.3,10.2,16.4,10.7,16.5,11.3,16.6,11.9,16.7,12.4,16.8,13.0,16.9,13.6,17.0,14.1,17.1,14.7,17.2,15.3,17.3,15.8,17.4,16.4,17.5,17.0,17.6,17.5,17.7,18.1,17.8,18.7,17.9,19.2,18.0,19.8,18.1,20.4,18.2,20.9,18.3,21.5,18.4,22.1,18.5,22.6,18.6,.5,13.8,1.1,13.9,1.7,14.0,2.2,14.1,2.8,14.2,3.4,14.3,3.9,14.4,4.5,14.5,5.1,14.6,5.6,14.7,6.2,14.8,6.8,14.9,7.3,15.0,7.9,15.1,8.5,15.2,9.0,15.3,9.6,15.4,10.2,15.5,10.7,15.6,11.3,15.7,11.9,15.8,12.4,15.9,13.0,16.0,13.6,16.1,14.1,16.2,14.7,16.3,15.3,16.4,15.8,16.5,16.4,16.6,17.0,16.7,17.5,16.8,18.1,16.9,18.7,17.0,19.2,17.1,19.8,17.2,20.4,17.3,20.9,17.4,21.5,17.5,22.1,17.6,22.6,17.7,.5,12.9,1.1,13.0,1.7,13.1,2.2,13.2,2.8,13.3,3.4,13.4,3.9,13.5,4.5,13.6,5.1,13.7,5.6,13.8,6.2,13.9,6.8,14.0,7.3,14.1,7.9,14.2,8.5,14.3,9.0,14.4,9.6,14.5,10.2,14.6,10.7,14.7,11.3,14.8,11.9,14.9,12.4,15.0,13.0,15.1,13.6,15.2,14.1,15.3,14.7,15.4,15.3,15.5,15.8,15.6,16.4,15.7,17.0,15.8,17.5,15.9,18.1,16.0,18.7,16.1,19.2,16.2,19.8,16.3,20.4,16.4,20.9,16.5,21.5,16.6,22.1,16.7,22.6,16.8,.5,12.0,1.1,12.1,1.7,12.2,2.2,12.3,2.8,12.4,3.4,12.5,3.9,12.6,4.5,12.7,5.1,12.8,5.6,12.9,6.2,13.0,6.8,13.1;R0,0,2.9,.1;@UW:7.3,13.2,7.9,13.3,8.5,13.4,9.0,13.5,9.6,13.6,10.2,13.7,10.7,13.8,11.3,13.9,11.9,14.0,12.4,14.1,13.0,14.2,13.6,14.3,14.1,14.4,14.7,14.5,15.3,14.6,15.8,14.7,16.4,14.8,17.0,14.9,17.5,15.0,18.1,15.1,18.7,15.2,19.2,15.3,19.8,15.4,20.4,15.5,20.9,15.6,21.5,15.7,22.1,15.8,22.6,15.9,.5,11.1,1.1,11.2,1.7,11.3,2.2,11.4,2.8,11.5,3.4,11.6,3.9,11.7,4.5,11.8,5.1,11.9,5.6,12.0,6.2,12.1,6.8,12.2,7.3,12.3,7.9,12.4,8.5,12.5,9.0,12.6,9.6,12.7,10.2,12.8,10.7,12.9,11.3,13.0,11.9,13.1,12.4,13.2,13.0,13.3,13.6,13.4,14.1,13.5,14.7,13.6,15.3,13.7,15.8,13.8,16.4,13.9,17.0,14.0,17.5,14.1,18.1,14.2,18.7,14.3,19.2,14.4,19.8,14.5,20.4,14.6,20.9,14.7,21.5,14.8,22.1,14.9,22.6,15.0,.5,10.1,1.1,10.2,1.7,10.3,2.2,10.4,2.8,10.5,3.4,10.6,3.9,10.7,4.5,10.8,5.1,10.9,5.6,11.0,6.2,11.1,6.8,11.2,7.3,11.3,7.9,11.4,8.5,11.5,9.0,11.6,9.6,11.7,10.2,11.8,10.7,11.9,11.3,12.0,11.9,12.1,12.4,12.2,13.0,12.3,13.6,12.4,14.1,12.5,14.7,12.6,15.3,12.7,15.8,12.8,16.4,12.9,17.0,13.0,17.5,13.1,18.1,13.2,18.7,13.3,19.2,13.4,19.8,13.5,20.4,13.6,20.9,13.7,21.5,13.8,22.1,13.9,22.6,14.0,.5,9.2,1.1,9.3,1.7,9.4,2.2,9.5,2.8,9.6,3.4,9.7,3.9,9.8,4.5,9.9,5.1,10.0,5.6,10.1,6.2,10.2,6.8,10.3,7.3,10.4,7.9,10.5,8.5,10.6,9.0,10.7,9.6,10.8,10.2,10.9,10.7,11.0,11.3,11.1,11.9,11.2,12.4,11.3,13.0,11.4,13.6,11.5,14.1,11.6,14.7,11.7,15.3,11.8,15.8,11.9,16.4,12.0,17.0,12.1,17.5,12.2,18.1,12.3,18.7,12.4,19.2,12.5,19.8,12.6,20.4,12.7,20.9,12.8,21.5,12.9,22.1,13.0,22.6,13.1,.5,8.3,1.1,8.4,1.7,8.5,2.2,8.6,2.8,8.7,3.4,8.8,3.9,8.9,4.5,9.0,5.1,9.1,5.6,9.2,6.2,9.3,6.8,9.4,7.3,9.5,7.9,9.6,8.5,9.7,9.0,9.8,9.6,9.9,10.2,10.0,10.7,10.1,11.3,10.2,11.9,10.3,12.4,10.4,13.0,10.5,13.6,10.6,14.1,10.7,14.7,10.8,15.3,10.9,15.8,11.0,16.4,11.1,17.0,11.2,17.5,11.3,18.1,11.4,18.7,11.5,19.2,11.6,19.8,11.7,20.4,11.8,20.9,11.9,21.5,12.0,22.1,12.1,22.6,12.2,.5,7.4,1.1,7.5,1.7,7.6,2.2,7.7,2.8,7.8,3.4,7.9,3.9,8.0,4.5,8.1,5.1,8.2,5.6,8.3,6.2,8.4,6.8,8.5,7.3,8.6,7.9,8.7,8.5,8.8,9.0,8.9,9.6,9.0,10.2,9.1,10.7,9.2,11.3,9.3,11.9,9.4,12.4,9.5,13.0,9.6,13.6,9.7,14.1,9.8,14.7,9.9,15.3,10.0,15.8,10.1,16.4,10.2,17.0,10.3,17.5,10.4,18.1,10.5,18.7,10.6,19.2,10.7,19.8,10.8,20.4,10.9,20.9,11.0,21.5,11.1,22.1,11.2,22.6,11.3,.5,6.5,1.1,6.6,1.7,6.7,2.2,6.8,2.8,6.9,3.4,7.0,3.9,7.1,4.5,7.2,5.1,7.3,5.6,7.4,6.2,7.5,6.8,7.6,7.3,7.7,7.9,7.8,8.5,7.9,9.0,8.0,9.6,8.1,10.2,8.2,10.7,8.3,11.3,8.4,11.9,8.5,12.4,8.6;R0,0,2.9,.1;@UW:13.0,8.7,13.6,8.8,14.1,8.9,14.7,9.0,15.3,9.1,15.8,9.2,16.4,9.3,17.0,9.4,17.5,9.5,18.1,9.6,18.7,9.7,19.2,9.8,19.8,9.9,20.4,10.0,20.9,10.1,21.5,10.2,22.1,10.3,22.6,10.4,.5,5.6,1.1,5.7,1.7,5.8,2.2,5.9,2.8,6.0,3.4,6.1,3.9,6.2,4.5,6.3,5.1,6.4,5.6,6.5,6.2,6.6,6.8,6.7,7.3,6.8,7.9,6.9,8.5,7.0,9.0,7.1,9.6,7.2,10.2,7.3,10.7,7.4,11.3,7.5,11.9,7.6,12.4,7.7,13.0,7.8,13.6,7.9,14.1,8.0,14.7,8.1,15.3,8.2,15.8,8.3,16.4,8.4,17.0,8.5,17.5,8.6,18.1,8.7,18.7,8.8,19.2,8.9,19.8,9.0,20.4,9.1,20.9,9.2,21.5,9.3,22.1,9.4,22.6,9.5,.5,4.7,1.1,4.8,1.7,4.9,2.2,5.0,2.8,5.1,3.4,5.2,3.9,5.3,4.5,5.4,5.1,5.5,5.6,5.6,6.2,5.7,6.8,5.8,7.3,5.9,7.9,6.0,8.5,6.1,9.0,6.2,9.6,6.3,10.2,6.4,10.7,6.5,11.3,6.6,11.9,6.7,12.4,6.8,13.0,6.9,13.6,7.0,14.1,7.1,14.7,7.2,15.3,7.3,15.8,7.4,16.4,7.5,17.0,7.6,17.5,7.7,18.1,7.8,18.7,7.9,19.2,8.0,19.8,8.1,20.4,8.2,20.9,8.3,21.5,8.4,22.1,8.5,22.6,8.6,.5,3.7,1.1,3.8,1.7,3.9,2.2,4.0,2.8,4.1,3.4,4.2,3.9,4.3,4.5,4.4,5.1,4.5,5.6,4.6,6.2,4.7,6.8,4.8,7.3,4.9,7.9,5.0,8.5,5.1,9.0,5.2,9.6,5.3,10.2,5.4,10.7,5.5,11.3,5.6,11.9,5.7,12.4,5.8,13.0,5.9,13.6,6.0,14.1,6.1,14.7,6.2,15.3,6.3,15.8,6.4,16.4,6.5,17.0,6.6,17.5,6.7,18.1,6.8,18.7,6.9,19.2,7.0,19.8,7.1,20.4,7.2,20.9,7.3,21.5,7.4,22.1,7.5,22.6,7.6,.5,2.8,1.1,2.9,1.7,3.0,2.2,3.1,2.8,3.2,3.4,3.3,3.9,3.4,4.5,3.5,5.1,3.6,5.6,3.7,6.2,3.8,6.8,3.9,7.3,4.0,7.9,4.1,8.5,4.2,9.0,4.3,9.6,4.4,10.2,4.5,10.7,4.6,11.3,4.7,11.9,4.8,12.4,4.9,13.0,5.0,13.6,5.1,14.1,5.2,14.7,5.3,15.3,5.4,15.8,5.5,16.4,5.6,17.0,5.7,17.5,5.8,18.1,5.9,18.7,6.0,19.2,6.1,19.8,6.2,20.4,6.3,20.9,6.4,21.5,6.5,22.1,6.6,22.6,6.7,.5,1.9,1.1,2.0,1.7,2.1,2.2,2.2,2.8,2.3,3.4,2.4,3.9,2.5,4.5,2.6,5.1,2.7,5.6,2.8,6.2,2.9,6.8,3.0,7.3,3.1,7.9,3.2,8.5,3.3,9.0,3.4,9.6,3.5,10.2,3.6,10.7,3.7,11.3,3.8,11.9,3.9,12.4,4.0,13.0,4.1,13.6,4.2,14.1,4.3,14.7,4.4,15.3,4.5,15.8,4.6,16.4,4.7,17.0,4.8,17.5,4.9,18.1,5.0,18.7,5.1,19.2,5.2,19.8,5.3,20.4,5.4,20.9,5.5,21.5,5.6,22.1,5.7,22.6,5.8,.5,1.0,1.1,1.1,1.7,1.2,2.2,1.3,2.8,1.4,3.4,1.5,3.9,1.6,4.5,1.7,5.1,1.8,5.6,1.9,6.2,2.0,6.8,2.1,7.3,2.2,7.9,2.3,8.5,2.4,9.0,2.5,9.6,2.6,10.2,2.7,10.7,2.8,11.3,2.9,11.9,3.0,12.4,3.1,13.0,3.2,13.6,3.3,14.1,3.4,14.7,3.5,15.3,3.6,15.8,3.7,16.4,3.8,17.0,3.9,17.5,4.0,18.1,4.1;R0,0,2.9,.1;@UW:18.7,4.2,19.2,4.3,19.8,4.4,20.4,4.5,20.9,4.6,21.5,4.7,22.1,4.8,22.6,4.9,.0,.0,.6,.1,1.1,.2,1.7,.3,2.3,.4,2.8,.5,3.4,.6,4.0,.7,4.5,.8,5.1,.9,5.7,1.0,6.2,1.1,6.8,1.2,7.4,1.3,7.9,1.4,8.5,1.5,9.1,1.6,9.6,1.7,10.2,1.8,10.8,1.9,11.3,2.0,11.9,2.1,12.5,2.2,13.0,2.3,13.6,2.4,14.2,2.5,14.7,2.6,15.3,2.7,15.9,2.8,16.4,2.9,17.0,3.0,17.6,3.1,18.1,3.2,18.7,3.3,19.3,3.4,19.8,3.5,20.4,3.6,21.0,3.7,21.6,3.8,22.1,3.9,22.7,4.0,5.2,.0,5.8,.1,6.3,.2,6.9,.3,7.5,.4,8.0,.5,8.6,.6,9.2,.7,9.7,.8,10.3,.9,10.9,1.0,11.4,1.1,12.0,1.2,12.6,1.3,13.1,1.4,13.7,1.5,14.3,1.6,14.8,1.7,15.4,1.8,16.0,1.9,16.5,2.0,17.1,2.1,17.7,2.2,18.2,2.3,18.8,2.4,19.4,2.5,19.9,2.6,20.5,2.7,21.1,2.8,21.6,2.9,22.2,3.0,10.4,.0,10.9,.1,11.5,.2,12.1,.3,12.6,.4,13.2,.5,13.8,.6,14.3,.7,14.9,.8,15.5,.9,16.0,1.0,16.6,1.1,17.2,1.2,17.7,1.3,18.3,1.4,18.9,1.5,19.4,1.6,20.0,1.7,20.6,1.8,21.1,1.9,21.7,2.0,22.3,2.1,15.5,.0,16.1,.1,16.7,.2,17.3,.3,17.8,.4,18.4,.5,19.0,.6,19.5,.7,20.1,.8,20.7,.9,21.2,1.0,21.8,1.1,22.4,1.2,20.7,.0,21.3,.1,21.9,.2,22.4,.3;R0,0,2.9,.1;@R24.4,4.3,1.2,.1;R23.4,2.3,2.2,.1;R24.0,2.4,1.6,.1;R25.1,2.6,.5,.1;R22.9,1.3,2.7,.1;R23.5,1.4,2.1,.1;UW:24.1,1.5,24.1,.6;R0,0,1.5,.1;@R24.6,1.6,1.0,.1;R25.2,1.7,.4,.1;R23.0,.4,2.6,.1;R23.6,.5,2.0,.1;R24.7,.7,.9,.1;R25.3,.8,.3,.1;"
        # random UFields + stray RECTs
        tmpstr = "UW:.0,25.2,.0,24.3,.0,23.4,.0,22.4,.0,21.5,.0,20.6,.0,19.7,.0,18.8,.0,17.9,.0,17.0,.0,16.0,.0,15.1,.0,14.2,.0,13.3,.0,12.4,.0,11.5,.0,10.6,.0,9.6,.0,8.7,.0,7.8,.0,6.9,.0,6.0,.0,5.1,.0,4.2,.0,3.2,.0,2.3,.0,1.4,.0,.5,25.0,4.4,25.0,3.5;R0,0,.6,.1;@UW:.0,25.3,.0,24.4,.0,23.5,.0,22.5,.0,21.6,.0,20.7,.0,19.8,.0,18.9,.0,18.0,.0,17.1,.0,16.1,.0,15.2,.0,14.3,.0,13.4,.0,12.5,.0,11.6,.0,10.7,.0,9.7,.0,8.8,.0,7.9,.0,7.0,.0,6.1,.0,5.2,.0,4.3,.0,3.3,.0,2.4,.0,1.5,.0,.6,24.5,3.4,24.5,2.5;R0,0,1.1,.1;@UW:.0,25.4,.0,24.5,.0,23.6,.0,22.6,.0,21.7,.0,20.8,.0,19.9,.0,19.0,.0,18.1,.0,17.2,.0,16.2,.0,15.3,.0,14.4,.0,13.5,.0,12.6,.0,11.7,.0,10.8,.0,9.8,.0,8.9,.0,8.0,.0,7.1,.0,6.2,.0,5.3,.0,4.4,.0,3.4,.0,2.5,.0,1.6,.0,.7,23.9,3.3;R0,0,1.7,.1;@UW:.0,25.5,.0,24.6,.0,23.7,.0,22.7,.0,21.8,.0,20.9,.0,20.0,.0,19.1,.0,18.2,.0,17.3,.0,16.3,.0,15.4,.0,14.5,.0,13.6,.0,12.7,.0,11.8,.0,10.9,.0,9.9,.0,9.0,.0,8.1,.0,7.2,.0,6.3,.0,5.4,.0,4.5,.0,3.5,.0,2.6,.0,1.7,.0,.8,23.3,4.1,23.3,3.2;R0,0,2.3,.1;@UW:.0,24.7,.0,23.8,.0,22.8,.0,21.9,.0,21.0,.0,20.1,.0,19.2,.0,18.3,.0,17.4,.0,16.4,.0,15.5,.0,14.6,.0,13.7,.0,12.8,.0,11.9,.0,11.0,.0,10.0,.0,9.1,.0,8.2,.0,7.3,.0,6.4,.0,5.5,.0,4.6,.0,3.6,.0,2.7,.0,1.8,.0,.9,22.8,3.1,22.8,2.2;R0,0,2.8,.1;@UW:.5,24.8,1.1,24.9,1.7,25.0,2.2,25.1,2.8,25.2,3.4,25.3,3.9,25.4,4.5,25.5,.5,23.9,1.1,24.0,1.7,24.1,2.2,24.2,2.8,24.3,3.4,24.4,3.9,24.5,4.5,24.6,5.1,24.7,5.6,24.8,6.2,24.9,6.8,25.0,7.3,25.1,7.9,25.2,8.5,25.3,9.0,25.4,9.6,25.5,.5,22.9,1.1,23.0,1.7,23.1,2.2,23.2,2.8,23.3,3.4,23.4,3.9,23.5,4.5,23.6,5.1,23.7,5.6,23.8,6.2,23.9,6.8,24.0,7.3,24.1,7.9,24.2,8.5,24.3,9.0,24.4,9.6,24.5,10.2,24.6,10.7,24.7,11.3,24.8,11.9,24.9,12.4,25.0,13.0,25.1,13.6,25.2,14.1,25.3,14.7,25.4,15.3,25.5,.5,22.0,1.1,22.1,1.7,22.2,2.2,22.3,2.8,22.4,3.4,22.5,3.9,22.6,4.5,22.7,5.1,22.8,5.6,22.9,6.2,23.0,6.8,23.1,7.3,23.2,7.9,23.3,8.5,23.4,9.0,23.5,9.6,23.6,10.2,23.7,10.7,23.8,11.3,23.9,11.9,24.0,12.4,24.1,13.0,24.2,13.6,24.3,14.1,24.4,14.7,24.5,15.3,24.6,15.8,24.7,16.4,24.8,17.0,24.9,17.5,25.0,18.1,25.1,18.7,25.2,19.2,25.3,19.8,25.4,20.4,25.5,.5,21.1,1.1,21.2,1.7,21.3,2.2,21.4,2.8,21.5,3.4,21.6,3.9,21.7,4.5,21.8,5.1,21.9,5.6,22.0,6.2,22.1,6.8,22.2,7.3,22.3,7.9,22.4,8.5,22.5,9.0,22.6,9.6,22.7,10.2,22.8,10.7,22.9,11.3,23.0,11.9,23.1,12.4,23.2,13.0,23.3,13.6,23.4,14.1,23.5,14.7,23.6,15.3,23.7,15.8,23.8,16.4,23.9,17.0,24.0,17.5,24.1,18.1,24.2,18.7,24.3,19.2,24.4,19.8,24.5,20.4,24.6,20.9,24.7,21.5,24.8,22.1,24.9,22.6,25.0,.5,20.2,1.1,20.3,1.7,20.4,2.2,20.5,2.8,20.6,3.4,20.7,3.9,20.8,4.5,20.9,5.1,21.0,5.6,21.1,6.2,21.2,6.8,21.3,7.3,21.4,7.9,21.5,8.5,21.6,9.0,21.7,9.6,21.8,10.2,21.9,10.7,22.0,11.3,22.1,11.9,22.2,12.4,22.3,13.0,22.4,13.6,22.5,14.1,22.6,14.7,22.7,15.3,22.8,15.8,22.9,16.4,23.0,17.0,23.1,17.5,23.2,18.1,23.3,18.7,23.4,19.2,23.5,19.8,23.6,20.4,23.7,20.9,23.8,21.5,23.9,22.1,24.0,22.6,24.1,.5,19.3,1.1,19.4,1.7,19.5,2.2,19.6,2.8,19.7,3.4,19.8,3.9,19.9,4.5,20.0,5.1,20.1,5.6,20.2,6.2,20.3,6.8,20.4,7.3,20.5,7.9,20.6,8.5,20.7,9.0,20.8,9.6,20.9,10.2,21.0,10.7,21.1,11.3,21.2,11.9,21.3,12.4,21.4,13.0,21.5,13.6,21.6,14.1,21.7,14.7,21.8,15.3,21.9,15.8,22.0,16.4,22.1,17.0,22.2,17.5,22.3,18.1,22.4,18.7,22.5,19.2,22.6,19.8,22.7,20.4,22.8,20.9,22.9,21.5,23.0,22.1,23.1,22.6,23.2,.5,18.4,1.1,18.5,1.7,18.6,2.2,18.7,2.8,18.8,3.4,18.9,3.9,19.0,4.5,19.1,5.1,19.2,5.6,19.3,6.2,19.4,6.8,19.5,7.3,19.6,7.9,19.7,8.5,19.8,9.0,19.9,9.6,20.0,10.2,20.1,10.7,20.2,11.3,20.3,11.9,20.4,12.4,20.5,13.0,20.6,13.6,20.7,14.1,20.8,14.7,20.9,15.3,21.0,15.8,21.1,16.4,21.2,17.0,21.3,17.5,21.4,18.1,21.5,18.7,21.6,19.2,21.7,19.8,21.8,20.4,21.9,20.9,22.0,21.5,22.1,22.1,22.2,22.6,22.3,.5,17.5,1.1,17.6;R0,0,2.9,.1;@UW:23.2,25.1,23.2,24.2,23.2,23.3,23.2,22.4,23.2,21.5,23.2,20.5,23.2,19.6,23.2,18.7,23.2,17.8,23.2,16.9,23.2,16.0,23.2,15.1,23.2,14.1,23.2,13.2,23.2,12.3,23.2,11.4,23.2,10.5,23.2,9.6,23.2,8.7,23.2,7.7,23.2,6.8,23.2,5.9,23.2,5.0;R0,0,2.4,.1;@UW:23.8,25.2,23.8,24.3,23.8,23.4,23.8,22.5,23.8,21.6,23.8,20.6,23.8,19.7,23.8,18.8,23.8,17.9,23.8,17.0,23.8,16.1,23.8,15.2,23.8,14.2,23.8,13.3,23.8,12.4,23.8,11.5,23.8,10.6,23.8,9.7,23.8,8.8,23.8,7.8,23.8,6.9,23.8,6.0,23.8,5.1,23.8,4.2;R0,0,1.8,.1;@UW:24.3,25.3,24.3,24.4,24.3,23.5,24.3,22.6,24.3,21.7,24.3,20.7,24.3,19.8,24.3,18.9,24.3,18.0,24.3,17.1,24.3,16.2,24.3,15.3,24.3,14.3,24.3,13.4,24.3,12.5,24.3,11.6,24.3,10.7,24.3,9.8,24.3,8.9,24.3,7.9,24.3,7.0,24.3,6.1,24.3,5.2;R0,0,1.3,.1;@UW:24.9,25.4,24.9,24.5,24.9,23.6,24.9,22.7,24.9,21.8,24.9,20.8,24.9,19.9,24.9,19.0,24.9,18.1,24.9,17.2,24.9,16.3,24.9,15.4,24.9,14.4,24.9,13.5,24.9,12.6,24.9,11.7,24.9,10.8,24.9,9.9,24.9,9.0,24.9,8.0,24.9,7.1,24.9,6.2,24.9,5.3;R0,0,.7,.1;@UW:25.5,25.5,25.5,24.6,25.5,23.7,25.5,22.8,25.5,21.9,25.5,20.9,25.5,20.0,25.5,19.1,25.5,18.2,25.5,17.3,25.5,16.4,25.5,15.5,25.5,14.5,25.5,13.6,25.5,12.7,25.5,11.8,25.5,10.9,25.5,10.0,25.5,9.1,25.5,8.1,25.5,7.2,25.5,6.3,25.5,5.4;R0,0,.1,.1;@UW:1.7,17.7,2.2,17.8,2.8,17.9,3.4,18.0,3.9,18.1,4.5,18.2,5.1,18.3,5.6,18.4,6.2,18.5,6.8,18.6,7.3,18.7,7.9,18.8,8.5,18.9,9.0,19.0,9.6,19.1,10.2,19.2,10.7,19.3,11.3,19.4,11.9,19.5,12.4,19.6,13.0,19.7,13.6,19.8,14.1,19.9,14.7,20.0,15.3,20.1,15.8,20.2,16.4,20.3,17.0,20.4,17.5,20.5,18.1,20.6,18.7,20.7,19.2,20.8,19.8,20.9,20.4,21.0,20.9,21.1,21.5,21.2,22.1,21.3,22.6,21.4,.5,16.5,1.1,16.6,1.7,16.7,2.2,16.8,2.8,16.9,3.4,17.0,3.9,17.1,4.5,17.2,5.1,17.3,5.6,17.4,6.2,17.5,6.8,17.6,7.3,17.7,7.9,17.8,8.5,17.9,9.0,18.0,9.6,18.1,10.2,18.2,10.7,18.3,11.3,18.4,11.9,18.5,12.4,18.6,13.0,18.7,13.6,18.8,14.1,18.9,14.7,19.0,15.3,19.1,15.8,19.2,16.4,19.3,17.0,19.4,17.5,19.5,18.1,19.6,18.7,19.7,19.2,19.8,19.8,19.9,20.4,20.0,20.9,20.1,21.5,20.2,22.1,20.3,22.6,20.4,.5,15.6,1.1,15.7,1.7,15.8,2.2,15.9,2.8,16.0,3.4,16.1,3.9,16.2,4.5,16.3,5.1,16.4,5.6,16.5,6.2,16.6,6.8,16.7,7.3,16.8,7.9,16.9,8.5,17.0,9.0,17.1,9.6,17.2,10.2,17.3,10.7,17.4,11.3,17.5,11.9,17.6,12.4,17.7,13.0,17.8,13.6,17.9,14.1,18.0,14.7,18.1,15.3,18.2,15.8,18.3,16.4,18.4,17.0,18.5,17.5,18.6,18.1,18.7,18.7,18.8,19.2,18.9,19.8,19.0,20.4,19.1,20.9,19.2,21.5,19.3,22.1,19.4,22.6,19.5,.5,14.7,1.1,14.8,1.7,14.9,2.2,15.0,2.8,15.1,3.4,15.2,3.9,15.3,4.5,15.4,5.1,15.5,5.6,15.6,6.2,15.7,6.8,15.8,7.3,15.9,7.9,16.0,8.5,16.1,9.0,16.2,9.6,16.3,10.2,16.4,10.7,16.5,11.3,16.6,11.9,16.7,12.4,16.8,13.0,16.9,13.6,17.0,14.1,17.1,14.7,17.2,15.3,17.3,15.8,17.4,16.4,17.5,17.0,17.6,17.5,17.7,18.1,17.8,18.7,17.9,19.2,18.0,19.8,18.1,20.4,18.2,20.9,18.3,21.5,18.4,22.1,18.5,22.6,18.6,.5,13.8,1.1,13.9,1.7,14.0,2.2,14.1,2.8,14.2,3.4,14.3,3.9,14.4,4.5,14.5,5.1,14.6,5.6,14.7,6.2,14.8,6.8,14.9,7.3,15.0,7.9,15.1,8.5,15.2,9.0,15.3,9.6,15.4,10.2,15.5,10.7,15.6,11.3,15.7,11.9,15.8,12.4,15.9,13.0,16.0,13.6,16.1,14.1,16.2,14.7,16.3,15.3,16.4,15.8,16.5,16.4,16.6,17.0,16.7,17.5,16.8,18.1,16.9,18.7,17.0,19.2,17.1,19.8,17.2,20.4,17.3,20.9,17.4,21.5,17.5,22.1,17.6,22.6,17.7,.5,12.9,1.1,13.0,1.7,13.1,2.2,13.2,2.8,13.3,3.4,13.4,3.9,13.5,4.5,13.6,5.1,13.7,5.6,13.8,6.2,13.9,6.8,14.0,7.3,14.1,7.9,14.2,8.5,14.3,9.0,14.4,9.6,14.5,10.2,14.6,10.7,14.7,11.3,14.8,11.9,14.9,12.4,15.0,13.0,15.1,13.6,15.2,14.1,15.3,14.7,15.4,15.3,15.5,15.8,15.6,16.4,15.7,17.0,15.8,17.5,15.9,18.1,16.0,18.7,16.1,19.2,16.2,19.8,16.3,20.4,16.4,20.9,16.5,21.5,16.6,22.1,16.7,22.6,16.8,.5,12.0,1.1,12.1,1.7,12.2,2.2,12.3,2.8,12.4,3.4,12.5,3.9,12.6,4.5,12.7,5.1,12.8,5.6,12.9,6.2,13.0,6.8,13.1;R0,0,2.9,.1;@UW:7.3,13.2,7.9,13.3,8.5,13.4,9.0,13.5,9.6,13.6,10.2,13.7,10.7,13.8,11.3,13.9,11.9,14.0,12.4,14.1,13.0,14.2,13.6,14.3,14.1,14.4,14.7,14.5,15.3,14.6,15.8,14.7,16.4,14.8,17.0,14.9,17.5,15.0,18.1,15.1,18.7,15.2,19.2,15.3,19.8,15.4,20.4,15.5,20.9,15.6,21.5,15.7,22.1,15.8,22.6,15.9,.5,11.1,1.1,11.2,1.7,11.3,2.2,11.4,2.8,11.5,3.4,11.6,3.9,11.7,4.5,11.8,5.1,11.9,5.6,12.0,6.2,12.1,6.8,12.2,7.3,12.3,7.9,12.4,8.5,12.5,9.0,12.6,9.6,12.7,10.2,12.8,10.7,12.9,11.3,13.0,11.9,13.1,12.4,13.2,13.0,13.3,13.6,13.4,14.1,13.5,14.7,13.6,15.3,13.7,15.8,13.8,16.4,13.9,17.0,14.0,17.5,14.1,18.1,14.2,18.7,14.3,19.2,14.4,19.8,14.5,20.4,14.6,20.9,14.7,21.5,14.8,22.1,14.9,22.6,15.0,.5,10.1,1.1,10.2,1.7,10.3,2.2,10.4,2.8,10.5,3.4,10.6,3.9,10.7,4.5,10.8,5.1,10.9,5.6,11.0,6.2,11.1,6.8,11.2,7.3,11.3,7.9,11.4,8.5,11.5,9.0,11.6,9.6,11.7,10.2,11.8,10.7,11.9,11.3,12.0,11.9,12.1,12.4,12.2,13.0,12.3,13.6,12.4,14.1,12.5,14.7,12.6,15.3,12.7,15.8,12.8,16.4,12.9,17.0,13.0,17.5,13.1,18.1,13.2,18.7,13.3,19.2,13.4,19.8,13.5,20.4,13.6,20.9,13.7,21.5,13.8,22.1,13.9,22.6,14.0,.5,9.2,1.1,9.3,1.7,9.4,2.2,9.5,2.8,9.6,3.4,9.7,3.9,9.8,4.5,9.9,5.1,10.0,5.6,10.1,6.2,10.2,6.8,10.3,7.3,10.4,7.9,10.5,8.5,10.6,9.0,10.7,9.6,10.8,10.2,10.9,10.7,11.0,11.3,11.1,11.9,11.2,12.4,11.3,13.0,11.4,13.6,11.5,14.1,11.6,14.7,11.7,15.3,11.8,15.8,11.9,16.4,12.0,17.0,12.1,17.5,12.2,18.1,12.3,18.7,12.4,19.2,12.5,19.8,12.6,20.4,12.7,20.9,12.8,21.5,12.9,22.1,13.0,22.6,13.1,.5,8.3,1.1,8.4,1.7,8.5,2.2,8.6,2.8,8.7,3.4,8.8,3.9,8.9,4.5,9.0,5.1,9.1,5.6,9.2,6.2,9.3,6.8,9.4,7.3,9.5,7.9,9.6,8.5,9.7,9.0,9.8,9.6,9.9,10.2,10.0,10.7,10.1,11.3,10.2,11.9,10.3,12.4,10.4,13.0,10.5,13.6,10.6,14.1,10.7,14.7,10.8,15.3,10.9,15.8,11.0,16.4,11.1,17.0,11.2,17.5,11.3,18.1,11.4,18.7,11.5,19.2,11.6,19.8,11.7,20.4,11.8,20.9,11.9,21.5,12.0,22.1,12.1,22.6,12.2,.5,7.4,1.1,7.5,1.7,7.6,2.2,7.7,2.8,7.8,3.4,7.9,3.9,8.0,4.5,8.1,5.1,8.2,5.6,8.3,6.2,8.4,6.8,8.5,7.3,8.6,7.9,8.7,8.5,8.8,9.0,8.9,9.6,9.0,10.2,9.1,10.7,9.2,11.3,9.3,11.9,9.4,12.4,9.5,13.0,9.6,13.6,9.7,14.1,9.8,14.7,9.9,15.3,10.0,15.8,10.1,16.4,10.2,17.0,10.3,17.5,10.4,18.1,10.5,18.7,10.6,19.2,10.7,19.8,10.8,20.4,10.9,20.9,11.0,21.5,11.1,22.1,11.2,22.6,11.3,.5,6.5,1.1,6.6,1.7,6.7,2.2,6.8,2.8,6.9,3.4,7.0,3.9,7.1,4.5,7.2,5.1,7.3,5.6,7.4,6.2,7.5,6.8,7.6,7.3,7.7,7.9,7.8,8.5,7.9,9.0,8.0,9.6,8.1,10.2,8.2,10.7,8.3,11.3,8.4,11.9,8.5,12.4,8.6;R0,0,2.9,.1;@UW:13.0,8.7,13.6,8.8,14.1,8.9,14.7,9.0,15.3,9.1,15.8,9.2,16.4,9.3,17.0,9.4,17.5,9.5,18.1,9.6,18.7,9.7,19.2,9.8,19.8,9.9,20.4,10.0,20.9,10.1,21.5,10.2,22.1,10.3,22.6,10.4,.5,5.6,1.1,5.7,1.7,5.8,2.2,5.9,2.8,6.0,3.4,6.1,3.9,6.2,4.5,6.3,5.1,6.4,5.6,6.5,6.2,6.6,6.8,6.7,7.3,6.8,7.9,6.9,8.5,7.0,9.0,7.1,9.6,7.2,10.2,7.3,10.7,7.4,11.3,7.5,11.9,7.6,12.4,7.7,13.0,7.8,13.6,7.9,14.1,8.0,14.7,8.1,15.3,8.2,15.8,8.3,16.4,8.4,17.0,8.5,17.5,8.6,18.1,8.7,18.7,8.8,19.2,8.9,19.8,9.0,20.4,9.1,20.9,9.2,21.5,9.3,22.1,9.4,22.6,9.5,.5,4.7,1.1,4.8,1.7,4.9,2.2,5.0,2.8,5.1,3.4,5.2,3.9,5.3,4.5,5.4,5.1,5.5,5.6,5.6,6.2,5.7,6.8,5.8,7.3,5.9,7.9,6.0,8.5,6.1,9.0,6.2,9.6,6.3,10.2,6.4,10.7,6.5,11.3,6.6,11.9,6.7,12.4,6.8,13.0,6.9,13.6,7.0,14.1,7.1,14.7,7.2,15.3,7.3,15.8,7.4,16.4,7.5,17.0,7.6,17.5,7.7,18.1,7.8,18.7,7.9,19.2,8.0,19.8,8.1,20.4,8.2,20.9,8.3,21.5,8.4,22.1,8.5,22.6,8.6,.5,3.7,1.1,3.8,1.7,3.9,2.2,4.0,2.8,4.1,3.4,4.2,3.9,4.3,4.5,4.4,5.1,4.5,5.6,4.6,6.2,4.7,6.8,4.8,7.3,4.9,7.9,5.0,8.5,5.1,9.0,5.2,9.6,5.3,10.2,5.4,10.7,5.5,11.3,5.6,11.9,5.7,12.4,5.8,13.0,5.9,13.6,6.0,14.1,6.1,14.7,6.2,15.3,6.3,15.8,6.4,16.4,6.5,17.0,6.6,17.5,6.7,18.1,6.8,18.7,6.9,19.2,7.0,19.8,7.1,20.4,7.2,20.9,7.3,21.5,7.4,22.1,7.5,22.6,7.6,.5,2.8,1.1,2.9,1.7,3.0,2.2,3.1,2.8,3.2,3.4,3.3,3.9,3.4,4.5,3.5,5.1,3.6,5.6,3.7,6.2,3.8,6.8,3.9,7.3,4.0,7.9,4.1,8.5,4.2,9.0,4.3,9.6,4.4,10.2,4.5,10.7,4.6,11.3,4.7,11.9,4.8,12.4,4.9,13.0,5.0,13.6,5.1,14.1,5.2,14.7,5.3,15.3,5.4,15.8,5.5,16.4,5.6,17.0,5.7,17.5,5.8,18.1,5.9,18.7,6.0,19.2,6.1,19.8,6.2,20.4,6.3,20.9,6.4,21.5,6.5,22.1,6.6,22.6,6.7,.5,1.9,1.1,2.0,1.7,2.1,2.2,2.2,2.8,2.3,3.4,2.4,3.9,2.5,4.5,2.6,5.1,2.7,5.6,2.8,6.2,2.9,6.8,3.0,7.3,3.1,7.9,3.2,8.5,3.3,9.0,3.4,9.6,3.5,10.2,3.6,10.7,3.7,11.3,3.8,11.9,3.9,12.4,4.0,13.0,4.1,13.6,4.2,14.1,4.3,14.7,4.4,15.3,4.5,15.8,4.6,16.4,4.7,17.0,4.8,17.5,4.9,18.1,5.0,18.7,5.1,19.2,5.2,19.8,5.3,20.4,5.4,20.9,5.5,21.5,5.6,22.1,5.7,22.6,5.8,.5,1.0,1.1,1.1,1.7,1.2,2.2,1.3,2.8,1.4,3.4,1.5,3.9,1.6,4.5,1.7,5.1,1.8,5.6,1.9,6.2,2.0,6.8,2.1,7.3,2.2,7.9,2.3,8.5,2.4,9.0,2.5,9.6,2.6,10.2,2.7,10.7,2.8,11.3,2.9,11.9,3.0,12.4,3.1,13.0,3.2,13.6,3.3,14.1,3.4,14.7,3.5,15.3,3.6,15.8,3.7,16.4,3.8,17.0,3.9,17.5,4.0,18.1,4.1;R0,0,2.9,.1;@UW:18.7,4.2,19.2,4.3,19.8,4.4,20.4,4.5,20.9,4.6,21.5,4.7,22.1,4.8,22.6,4.9,.0,.0,.6,.1,1.1,.2,1.7,.3,2.3,.4,2.8,.5,3.4,.6,4.0,.7,4.5,.8,5.1,.9,5.7,1.0,6.2,1.1,6.8,1.2,7.4,1.3,7.9,1.4,8.5,1.5,9.1,1.6,9.6,1.7,10.2,1.8,10.8,1.9,11.3,2.0,11.9,2.1,12.5,2.2,13.0,2.3,13.6,2.4,14.2,2.5,14.7,2.6,15.3,2.7,15.9,2.8,16.4,2.9,17.0,3.0,17.6,3.1,18.1,3.2,18.7,3.3,19.3,3.4,19.8,3.5,20.4,3.6,21.0,3.7,21.6,3.8,22.1,3.9,22.7,4.0,5.2,.0,5.8,.1,6.3,.2,6.9,.3,7.5,.4,8.0,.5,8.6,.6,9.2,.7,9.7,.8,10.3,.9,10.9,1.0,11.4,1.1,12.0,1.2,12.6,1.3,13.1,1.4,13.7,1.5,14.3,1.6,14.8,1.7,15.4,1.8,16.0,1.9,16.5,2.0,17.1,2.1,17.7,2.2,18.2,2.3,18.8,2.4,19.4,2.5,19.9,2.6,20.5,2.7,21.1,2.8,21.6,2.9,22.2,3.0,10.4,.0,10.9,.1,11.5,.2,12.1,.3,12.6,.4,13.2,.5,13.8,.6,14.3,.7,14.9,.8,15.5,.9,16.0,1.0,16.6,1.1,17.2,1.2,17.7,1.3,18.3,1.4,18.9,1.5,19.4,1.6,20.0,1.7,20.6,1.8,21.1,1.9,21.7,2.0,22.3,2.1,15.5,.0,16.1,.1,16.7,.2,17.3,.3,17.8,.4,18.4,.5,19.0,.6,19.5,.7,20.1,.8,20.7,.9,21.2,1.0,21.8,1.1,22.4,1.2,20.7,.0,21.3,.1,21.9,.2,22.4,.3;R0,0,2.9,.1;@R24.4,4.3,1.2,.1;R23.4,2.3,2.2,.1;R24.0,2.4,1.6,.1;R25.1,2.6,.5,.1;R22.9,1.3,2.7,.1;R23.5,1.4,2.1,.1;UW:24.1,1.5,24.1,.6;R0,0,1.5,.1;@R24.6,1.6,1.0,.1;R25.2,1.7,.4,.1;R23.0,.4,2.6,.1;R23.6,.5,2.0,.1;R24.7,.7,.9,.1;R25.3,.8,.3,.1;"

        # no UField, stray RECTs only:
        # tmpstr = "R24.6,1.6,1.0,.1;R25.2,1.7,.4,.1;R23.0,.4,2.6,.1;R23.6,.5,2.0,.1;R24.7,.7,.9,.1;R25.3,.8,.3,.1;"

        # several normal UFields, no stray RECTS:
        # tmpstr = "UW:.0,25.2,.0,24.3,.0,23.4,.0,22.4,.0,21.5,.0,20.6,.0,19.7,.0,18.8,.0,17.9,.0,17.0,.0,16.0,.0,15.1,.0,14.2,.0,13.3,.0,12.4,.0,11.5,.0,10.6,.0,9.6,.0,8.7,.0,7.8,.0,6.9,.0,6.0,.0,5.1,.0,4.2,.0,3.2,.0,2.3,.0,1.4,.0,.5,25.0,4.4,25.0,3.5;R0,0,.6,.1;@UW:.0,25.3,.0,24.4,.0,23.5,.0,22.5,.0,21.6,.0,20.7,.0,19.8,.0,18.9,.0,18.0,.0,17.1,.0,16.1,.0,15.2,.0,14.3,.0,13.4,.0,12.5,.0,11.6,.0,10.7,.0,9.7,.0,8.8,.0,7.9,.0,7.0,.0,6.1,.0,5.2,.0,4.3,.0,3.3,.0,2.4,.0,1.5,.0,.6,24.5,3.4,24.5,2.5;R0,0,1.1,.1;@UW:.0,25.4,.0,24.5,.0,23.6,.0,22.6,.0,21.7,.0,20.8,.0,19.9,.0,19.0,.0,18.1,.0,17.2,.0,16.2,.0,15.3,.0,14.4,.0,13.5,.0,12.6,.0,11.7,.0,10.8,.0,9.8,.0,8.9,.0,8.0,.0,7.1,.0,6.2,.0,5.3,.0,4.4,.0,3.4,.0,2.5,.0,1.6,.0,.7,23.9,3.3;R0,0,1.7,.1;@"

        if "UT" not in tmpstr and "UW" not in tmpstr and "UR" not in tmpstr and "UM" not in tmpstr:
            # no UField, make RECTs
            rect_str_list = ["R" + s + ";" for s in tmpstr.strip("R").strip(";").split(";R")]
            rect_list.extend([ZbaRect.from_string(r) for r in rect_str_list])
        else:
            # parse UField string with possible embedded stray RECTs
            if "@R" not in tmpstr:
                # no stray RECTs, parse UField list
                ufstrlist = ["U" + s for s in tmpstr.strip("U").split("U")]

                uf_list.extend([ZbaUfield.from_string(s) for s in ufstrlist])
            else:
                # parse UField with embedded stray RECTs
                if tmpstr[0] == "R":
                    # separate leading stray RECT string
                    pos = tmpstr.index(";U") + 1
                    rect_str = tmpstr[:pos]
                    tmpstr = tmpstr[pos:]

                    rect_str_list = ["R" + s + ";" for s in rect_str.strip("R").strip(";").split(";R")]
                    rect_list.extend([ZbaRect.from_string(r) for r in rect_str_list])

                ufstrlist = ["U" + s for s in tmpstr.split("U")[1:]]

                for u in ufstrlist:
                    strlist = u.split("@")
                    uf_list.append(ZbaUfield.from_string(strlist[0] + "@"))

                    # if exist RECTs after UField
                    if strlist[1]:
                        rect_str_list = ["R" + s + ";" for s in strlist[1].strip("R").strip(";").split(";R")]
                        rect_list.extend([ZbaRect.from_string(r) for r in rect_str_list])

        return cls(tf_type, cls.default_size, pos_list, uf_list, rect_list)

    def print_ufields(self):
        for uf in self.ufield_list:
            print(uf)
