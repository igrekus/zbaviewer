import attr


@attr.s
class ZbaTri:
    """
    Represents a ZBA triangle
    # x, y, height, type, dose

    attrs:
    x, y: float, float   - triangle position, microns
    h: float             - triangle cathetus, microns
    t: int (0-7)         - triangle position
    d: int (0-7)         - dose table ID
    """
    x = attr.ib(type=float, default=0.0)
    y = attr.ib(type=float, default=0.0)
    h = attr.ib(type=float, default=0.0)
    t = attr.ib(type=int, default=0)
    d = attr.ib(type=int, default=0)

    @d.validator
    def check(self, attribute, value):
        if not 0 <= value <= 7:
            raise ValueError('Dose must be in the range [0..7]')

    @classmethod
    def from_string_list(cls, params):
        x, y, w, h, d = map(float, params)
        return cls(x, y, w, h, int(d))

