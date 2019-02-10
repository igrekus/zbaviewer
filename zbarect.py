import attr


@attr.s
class ZbaRect:
    """
    Represents a ZBA rectangle
    
    attrs:
    x, y: float, float (any)   - rectangle position, microns
    w, h: float, float (amy)   - rectangle width, microns (any)
    d: int             (0-7)   - dose table ID

    from_string: makes RECT object from RECT string
    """
    x = attr.ib(type=float, default=0.0)
    y = attr.ib(type=float, default=0.0)
    w = attr.ib(type=float, default=0.0)
    h = attr.ib(type=float, default=0.0)
    d = attr.ib(type=int, default=0)

    @d.validator
    def check(self, attribute, value):
        if not 0 <= value <= 7:
            raise ValueError('Dose must be in the range [0..7]')

    @classmethod
    def from_string_list(cls, params):
        x, y, w, h, d = map(float, params)
        return cls(x, y, w, h, int(d))

